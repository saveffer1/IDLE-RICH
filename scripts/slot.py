import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from settings import data_path

class SlotItem:
    next_id = 0
    def __init__(self, symbol: str, image: pygame.Surface, probability, skill: str="price", payout: dict={3:25, 4:50, 5:200}):
        self.id = SlotItem.next_id
        SlotItem.next_id += 1
        self.symbol = symbol
        self.probability = probability
        self.payout = payout
        if skill not in ["price", "wild", "scatter", "bonus"]:
            raise Exception("Invalid skill type. Can only be 'price', 'wild', or 'scatter'")
        else:
            self.skill = skill

class SlotSystem:
    def __init__(self, min_bet, paylines: list=[]):
        self.min_bet = min_bet
        self.max_bet = 15 * min_bet
        
        self.banana = SlotItem("🍌", pygame.image.load(os.path.join(data_path, 'assets/slot/item/banana.png')), 15, "price", {3:25, 4:50, 5:200})
        self.grape = SlotItem("🍇", pygame.image.load(os.path.join(data_path, 'assets/slot/item/grape.png')), 15, "price", {3:25, 4:50, 5:200})
        self.cherry = SlotItem("🍒", pygame.image.load(os.path.join(data_path, 'assets/slot/item/cherry.png')), 20, "price", {3:15, 4:45, 5:150})
        self.lemon = SlotItem("🍋", pygame.image.load(os.path.join(data_path, 'assets/slot/item/lemon.png')), 20, "price", {3:15, 4:45, 5:150})
        self.bigprize = SlotItem("💰", pygame.image.load(os.path.join(data_path, 'assets/slot/item/bigprize.png')), 5, "price", {3:150, 4:250, 5:500})
        self.scatter = SlotItem("🎲", pygame.image.load(os.path.join(data_path, 'assets/slot/item/freespin.png')), 10, "scatter", {3:25, 4:50, 5:200})
        self.bonusgame = SlotItem("🃏", pygame.image.load(os.path.join(data_path, 'assets/slot/item/game.png')), 5, "bonus", {3:150, 4:250, 5:500})
        self.jackpot = SlotItem("👑", pygame.image.load(os.path.join(data_path, 'assets/slot/item/jackpot.png')), 2, "price", {3:250, 4:500, 5:2000})
        self.wild = SlotItem("🍀", pygame.image.load(os.path.join(data_path, 'assets/slot/item/wildcard.png')), 8, "wild", {3:15, 4:45, 5:150})
        
        self.normal_reel = [
            self.banana, self.grape, self.cherry, 
            self.lemon, self.bigprize, self.scatter,
            self.bonusgame, self.jackpot, self.wild
        ]
        
        self.no_wild_reel = [
            self.banana, self.grape, self.cherry, 
            self.lemon, self.bigprize, self.jackpot, 
            self.bonusgame, self.scatter
        ]

        self.paylines = [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2],
            
            [2, 2, 1, 2, 2],
            [0, 0, 1, 0, 0],
            
            [1, 2, 2, 2, 1],
            [1, 0, 0, 0, 1],
            
            [2, 1, 0, 1, 2],
            [0, 1, 2, 1, 0]
        ]
    
    def calculate_rtp(self, item_id, duplicate_count, bet:int=None):
        if bet == None:
            bet = self.min_bet
        rtp = 0
        payout = self.normal_reel[item_id].payout[duplicate_count]
        rtp = payout * (bet // len(self.normal_reel))
        # print("id:", item_id, " : ", self.normal_reel[item_id].symbol, "pay count: ", duplicate_count)
        # print("payout", payout)
        # print("rtp", rtp)

        return rtp
    
    def check_for_wins(self, reels, bet=None):
        wins = []
        wild_symbol_id = self.wild.id
        specialobj = {"wild": set(), "bonus": set(), "scatter": set()}
        payout = 0

        for index, winline in enumerate(self.paylines):
            set_of_symbols = set()
            duplicate_between = {}
            for col, row in enumerate(winline):
                current = reels[row][col]
                prev = reels[winline[col - 1]][col - 1] if col != 0 else None

                if current.skill != "price":
                    specialobj[current.skill].add((row, col))

                if current.id not in set_of_symbols and current.id != wild_symbol_id:
                    set_of_symbols.add(current.id)
                    duplicate_between[current.id] = 1
                if col != 0 and prev.id is not None:
                    if current.id in set_of_symbols:
                        if current.id == prev.id:
                            duplicate_between[current.id] += 1
                        elif prev.id == wild_symbol_id:
                            duplicate_between[current.id] += 1
                            if col > 1:  # when reel > 1 check wild right to left
                                if (winline[col - 2], col - 2) in specialobj["wild"]:
                                    duplicate_between[current.id] += 1
                                if (winline[col - 3], col - 3) in specialobj["wild"]:
                                    duplicate_between[current.id] += 1
                    # check wild if current = wild
                    if current.id == wild_symbol_id:
                        if prev.id != wild_symbol_id:
                            duplicate_between[prev.id] += 1
                        else:
                            if reels[winline[col - 2]][col - 2].id != wild_symbol_id:
                                duplicate_between[reels[winline[col - 2]][col - 2].id] += 1
                            else:
                                duplicate_between[reels[winline[col - 3]][col - 3].id] += 1
            # check duplicate of max value and calculate rtp
            max_key, max_value = max(duplicate_between.items(), key=lambda x: x[1])
            if len(set_of_symbols) <= 1:
                wins.append(winline)
                payout += self.calculate_rtp(max_key, max_value, bet)
            else:
                max_duplicate = max(duplicate_between.values())
                if max_duplicate >= 3:
                    # print("winline: ", index + 1, duplicate_between)
                    wins.append(winline)
                    duplicate = [k for k, v in duplicate_between.items() if v == max_value]
                    if len(duplicate) == 0:
                        # print("no duplicate")
                        payout += self.calculate_rtp(max_key, max_value, bet)
                    else:
                        # print("duplicate", duplicate)
                        for key in duplicate:
                            payout += self.calculate_rtp(key, duplicate_between[key], bet)

        return wins, payout, specialobj
    
    def print_slot_machine(self, randreels, id_format=False):
        symbol_length = 2 if id_format else 5
        symbol_format = "{}" if id_format else " {} "

        horizontal_line = "-" * (symbol_length * 5 + 11)
        
        print(horizontal_line)
        
        for row in randreels:
            symbols = [symbol_format.format(reel.id if id_format else reel.symbol) for reel in row]
            row_line = "| {} |".format(" | ".join(symbols))
            print(row_line)
            
        print(horizontal_line)
    
    def spin(self, bet):
        if bet < self.min_bet or bet > self.max_bet:
            raise Exception(f"Invalid bet amount. Bet must be between {self.min_bet} and {self.max_bet}")
        
        randreels = []
        for i in range(3):
            reel1 = random.choices(self.no_wild_reel, weights=[item.probability for item in self.no_wild_reel])[0]
            reel2 = random.choices(self.normal_reel, weights=[item.probability for item in self.normal_reel])[0]
            reel3 = random.choices(self.normal_reel, weights=[item.probability for item in self.normal_reel])[0]
            reel4 = random.choices(self.normal_reel, weights=[item.probability for item in self.normal_reel])[0]
            reel5 = random.choices(self.no_wild_reel, weights=[item.probability for item in self.no_wild_reel])[0]
            
            randreels.append([reel1, reel2, reel3, reel4, reel5])

        # for test case
        # randreels = [
        #     [self.banana, self.banana, self.wild, self.banana, self.cherry],
        #     [self.banana, self.wild, self.wild, self.wild, self.bonusgame],
        #     [self.jackpot, self.bigprize, self.wild, self.scatter, self.grape]
        # ]
        
        self.print_slot_machine(randreels, id_format=False)
        
        wins = self.check_for_wins(randreels, bet)
        print("Winlines: ", wins[0])
        print("Prize: ", wins[1])
        print(f"Special: bonus-level({len(wins[2]['bonus'])}) freespin({len(wins[2]['scatter'])})")
        
        return wins

if __name__ == "__main__":
    import time
    start = time.time()
    slot = SlotSystem(100)
    slot.spin(100)
    end = time.time()
    print("Time elapsed: ", end - start)
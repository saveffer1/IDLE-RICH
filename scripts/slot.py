import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from settings import data_path
        
class SlotItem:
    def __init__(self, id, symbol: str, image: pygame.Surface, probability, skill: str="price", payout: dict={3:25, 4:50, 5:200}):
        self.id = id
        self.symbol = symbol
        self.probability = probability
        self.payout = payout
        if skill not in ["price", "wild", "scatter", "bonus"]:
            raise Exception("Invalid skill type. Can only be 'price', 'wild', 'scatter', or bonus")
        else:
            self.skill = skill
        self.image = image
            
class SlotSystem:
    def __init__(self, min_bet):
        self.min_bet = min_bet
        self.max_bet = 15 * min_bet
        self.wild = None
        self.reels = [
            SlotItem(0, "🍌", pygame.image.load(os.path.join(data_path, 'assets/slot/item/banana.png')), 15, "price", {3:25, 4:50, 5:200}),
            SlotItem(1, "🍇", pygame.image.load(os.path.join(data_path, 'assets/slot/item/grape.png')), 15, "price", {3:25, 4:50, 5:200}),
            SlotItem(2, "🍒", pygame.image.load(os.path.join(data_path, 'assets/slot/item/cherry.png')), 20, "price", {3:15, 4:45, 5:150}),
            SlotItem(3, "🍋", pygame.image.load(os.path.join(data_path, 'assets/slot/item/lemon.png')), 20, "price", {3:15, 4:45, 5:150}),
            SlotItem(4, "💰", pygame.image.load(os.path.join(data_path, 'assets/slot/item/bigprize.png')), 5, "price", {3:150, 4:250, 5:500}),
            SlotItem(5, "🎲", pygame.image.load(os.path.join(data_path, 'assets/slot/item/freespin.png')), 10, "scatter", {3:25, 4:50, 5:200}),
            SlotItem(6, "🃏", pygame.image.load(os.path.join(data_path, 'assets/slot/item/game.png')), 5, "bonus", {3:150, 4:250, 5:500}),
            SlotItem(7, "👑", pygame.image.load(os.path.join(data_path, 'assets/slot/item/jackpot.png')), 2, "price", {3:250, 4:500, 5:2000}),
            SlotItem(8, "🍀", pygame.image.load(os.path.join(data_path, 'assets/slot/item/wildcard.png')), 8, "wild", {3:15, 4:45, 5:150})
        ]
        self.paylines = [
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(2, 0), (2, 1), (1, 2), (2, 3), (2, 4)],
            [(0, 0), (0, 1), (1, 2), (0, 3), (0, 4)],
            [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
            [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],
            [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
            [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)]
        ]
        
        self.win_result = []
        
    def change_bet(self, min_bet):
        self.min_bet = min_bet
        self.max_bet = 15 * min_bet
    
    def __create_random_reels(self):
        randreels = []
        for i in range(3):
            reel1 = random.choices(self.reels[:-1], weights=[item.probability for item in self.reels[:-1]])[0]
            reel2 = random.choices(self.reels, weights=[item.probability for item in self.reels])[0]
            reel3 = random.choices(self.reels, weights=[item.probability for item in self.reels])[0]
            reel4 = random.choices(self.reels, weights=[item.probability for item in self.reels])[0]
            reel5 = random.choices(self.reels[:-1], weights=[item.probability for item in self.reels[:-1]])[0]
                
            randreels.append([reel1, reel2, reel3, reel4, reel5])
        return randreels
        
    def __calculate_rtp(self, symbol_id, duplicate_count, bet=None):
        if bet == None:
            bet = self.min_bet
        rtp = 0
        payout = self.reels[symbol_id].payout[duplicate_count]
        rtp = payout * (bet // len(self.reels))
        # print("id:", symbol_id, " : ", self.normal_reel[symbol_id].symbol, "pay count: ", duplicate_count)
        # print("payout", payout)
        # print("rtp", rtp)
        return rtp
        
    def __get_paylines(self, reels, bet=None):
        wins = []
        wild_symbol_id = self.reels[-1].id
        specialobj = {"wild": set(), "bonus": set(), "scatter": set()}
        payout = 0
        
        for payline in self.paylines:
            set_of_symbols = set()
            duplicate_between = {}
            for i in range(5):
                row, col = payline[i]
                current = reels[row][col]
                prev = reels[payline[i-1][0]][payline[i-1][1]]
                if current.skill != "price":
                    specialobj[current.skill].add((row, col))
                if current.id == wild_symbol_id:
                    for j in range(i, -1, -1):
                        add = 1
                        row, col = payline[j]
                        prev = reels[row][col]
                        if prev.id != wild_symbol_id:
                            duplicate_between[prev.id] += add
                            break
                        else:
                            add += 1
                else:
                    if current.id not in set_of_symbols:
                        set_of_symbols.add(current.id)
                        duplicate_between[current.id] = 1
                    elif current.id == prev.id:
                        duplicate_between[current.id] += 1
                    elif current.id != prev.id and prev.id == wild_symbol_id:
                        for j in range(i, -1, -1):
                            add = 1
                            row, col = payline[j]
                            prev = reels[row][col]
                            if prev.id != wild_symbol_id:
                                duplicate_between[prev.id] += add
                                break
                            else:
                                add += 1
            # check duplicate of max value and calculate rtp
            max_key, max_value = max(duplicate_between.items(), key=lambda x: x[1])
            max_duplicate = max(duplicate_between.values())
            if max_duplicate >= 3:
                wins.append(payline)
                duplicate = [k for k, v in duplicate_between.items() if v == max_value]
                if len(duplicate) == 0:
                    payout += self.__calculate_rtp(max_key, max_value, bet)
                else:
                    for key in duplicate:
                        payout += self.__calculate_rtp(key, duplicate_between[key], bet)
        freespin_count = len(specialobj["scatter"])
        bounus_level = len(specialobj["bonus"])
        if bounus_level - 2 >= 3:
            bounus_level -= 2
        else:
            bounus_level = 0
        
        return wins, payout, bounus_level, freespin_count
            
    @staticmethod
    def print_slot_symbol(randreels, id_format=False):
        symbol_length = 2 if id_format else 5
        symbol_format = "{}" if id_format else " {} "

        horizontal_line = "-" * (symbol_length * 5 + 11)
            
        print(horizontal_line)
            
        for row in randreels:
            symbols = [symbol_format.format(reel.id if id_format else reel.symbol) for reel in row]
            row_line = "| {} |".format(" | ".join(symbols))
            print(row_line)
                
        print(horizontal_line)
        
    def spin(self, randreels=None, bet=None):
        if bet is None:
            bet = self.min_bet
            
        if bet < self.min_bet or bet > self.max_bet:
            raise Exception(f"Invalid bet amount. Bet must be between {self.min_bet} and {self.max_bet}")
        
        if not randreels:
            randreels = self.__create_random_reels()
        else:
            reel = [[], [], []]
            for i in range(5):
                reel[0].append(self.reels[randreels[0][i]])
                reel[1].append(self.reels[randreels[1][i]])
                reel[2].append(self.reels[randreels[2][i]])
            
            randreels = reel
        
        self.print_slot_symbol(randreels, id_format=False)
        
        wins = self.__get_paylines(randreels, bet)
        
        print("Winlines: ", wins[0])
        print("Prize: ", wins[1])
        print(f"Special: bonus-level({wins[2]}) freespin({wins[2]})")
        
        return wins
    

if __name__ == "__main__":
    x =SlotSystem(100)
    x.spin()


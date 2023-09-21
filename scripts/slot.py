import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

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
        
        #0
        self.banana = SlotItem("🍌", pygame.image.load('assets/slot/item/banana.png'), 20, "price", {3:25, 4:50, 5:200})
        #1
        self.grape = SlotItem("🍇", pygame.image.load('assets/slot/item/grape.png'), 20, "price", {3:25, 4:50, 5:200})
        #2
        self.cherry = SlotItem("🍒", pygame.image.load('assets/slot/item/cherry.png'), 15, "price", {3:15, 4:45, 5:150})
        #3
        self.lemon = SlotItem("🍋", pygame.image.load('assets/slot/item/lemon.png'), 15, "price", {3:15, 4:45, 5:150})
        #4
        self.bigprize = SlotItem("💰", pygame.image.load('assets/slot/item/bigprize.png'), 5, "price", {3:150, 4:250, 5:500})
        #5
        self.scatter = SlotItem("🎲", pygame.image.load('assets/slot/item/freespin.png'), 10, "scatter", {3:25, 4:50, 5:200})
        #6
        self.bonusgame = SlotItem("🃏", pygame.image.load('assets/slot/item/game.png'), 5, "bonus", {3:150, 4:250, 5:500})
        #7
        self.jackpot = SlotItem("👑", pygame.image.load('assets/slot/item/jackpot.png'), 2, "price", {3:250, 4:500, 5:2000})
        #8
        self.wild = SlotItem("🍀", pygame.image.load('assets/slot/item/wildcard.png'), 8, "wild", {3:15, 4:45, 5:150})
        
        self.normal_reel = [
            self.banana, self.grape, self.cherry, 
            self.lemon, self.bigprize, self.jackpot, 
            self.bonusgame, self.scatter, self.wild
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
    
        self.reset_reel()
        self.reels = [
            self.first_reel, 
            self.second_reel, 
            self.third_reel, 
            self.fourth_reel, 
            self.fifth_reel
        ]

    def reset_reel(self):
        self.first_reel = self.no_wild_reel.copy()
        self.second_reel = self.normal_reel.copy()
        self.third_reel = self.normal_reel.copy()
        self.fourth_reel = self.normal_reel.copy()
        self.fifth_reel = self.no_wild_reel.copy()
    
    def calculate_rtp(self, wins, reels):
        #FIXME: calculate rtp
        total_payout = 0
        winline = wins[0]
        for win in wins:
            symbol_id = reels[win[0][0]][win[0][1]]
            if symbol_id in SlotItem.payout:
                total_payout += SlotItem.payout[symbol_id]

        total_bet = len(self.paylines)
        rtp = (total_payout / total_bet) * 100

        return rtp
    
    def check_for_wins(self, reels):
        wins = []
        wild_symbol_id = self.wild.id
        specialobj = {
            "wild": [],
            "bonus": [],
            "scatter": []
        }
        
        for reel in range(5):
            itemrow0 = reels[0][reel]
            itemrow1 = reels[1][reel]
            itemrow2 = reels[2][reel]
            
            if itemrow0.skill not in "price":
                specialobj[itemrow0.skill].append((0, reel))
            if itemrow1.skill not in "price":
                specialobj[itemrow1.skill].append((1, reel))
            if itemrow2.skill not in "price":
                specialobj[itemrow2.skill].append((2, reel))

        for index, winline in enumerate(self.paylines):
            set_of_symbols = set()
            duplicate_between = dict()
            for col, row in enumerate(winline):
                current = reels[row][col]
                prev = reels[winline[col - 1]][col - 1] if col != 0 else None
                
                if current.id not in set_of_symbols and current.id != wild_symbol_id:
                    set_of_symbols.add(current.id)
                    duplicate_between[current.id] = 1
                elif col != 0 and prev.id != None:
                    if current.id in set_of_symbols:
                        if current.id == prev.id:
                            duplicate_between[current.id] += 1
                        if prev.id == wild_symbol_id:
                            duplicate_between[current.id] += 1
                    elif current.id == wild_symbol_id:
                        if prev.id != wild_symbol_id:
                            duplicate_between[prev.id] += 1
                        else:
                            if reels[winline[col - 2]][col - 2].id != wild_symbol_id:
                                duplicate_between[reels[winline[col - 2]][col - 2].id] += 1
                            else:
                                duplicate_between[reels[winline[col - 3]][col - 3].id] += 1
                            
            if len(set_of_symbols) <= 1:
                wins.append(winline)
            else:
                for k, v in duplicate_between.items():
                    if v >= 3:
                        wins.append(winline)
                        break
            print("winline", index+1, duplicate_between)
            
        return wins, specialobj
                    
    def print_slot_machine(self, randreels, id_format=False):
        symlenght = 21 if id_format else 26
        print("-" * symlenght)
        for row in range(3):
            for col in range(5):
                if id_format:
                    symbol = randreels[row][col].id
                else:
                    symbol = randreels[row][col].symbol
                if [row, col] in self.paylines:
                    print(f"*{symbol}*", end=" | ")
                else:
                    if col == 0:
                        print("|", end=" ")
                    print(symbol, end=" | ")
            print("\n" + "-" * symlenght)
    
    def spin(self, bet):
        if bet < self.min_bet or bet > self.max_bet:
            raise Exception(f"Invalid bet amount. Bet must be between {self.min_bet} and {self.max_bet}")
        
        randreels = [[], [],[]]
        for reel in self.reels:
            col0 = random.choices(reel, weights=[item.probability for item in reel])[0]
            col1 = random.choices(reel, weights=[item.probability for item in reel])[0]
            col2 = random.choices(reel, weights=[item.probability for item in reel])[0]
            
            randreels[0].append(col0)
            randreels[1].append(col1)
            randreels[2].append(col2)

        # self.print_slot_machine(randreels)
        self.print_slot_machine(randreels, id_format=True)
        wins = self.check_for_wins(randreels)
        prize = 0#self.calculate_rtp(wins, randreels)
        
        print(wins[0])

if __name__ == "__main__":
    slot = SlotSystem(100)
    slot.spin(100)
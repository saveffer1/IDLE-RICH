import os
import pygame
import random
import slotitems
from player import Player
        
class SlotSymbol(pygame.sprite.Sprite):
    def __init__(self, item_id, symbol, image, pos, idx):
        super().__init__()

        self.item_id = item_id
        self.symbol = symbol
        self.pos = pos
        self.idx = idx
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.x_val = self.rect.left

class SlotReel:
    def __init__(self, pos, reels):
        self.symbol_list = pygame.sprite.Group()
        self.reels = reels
        self.reel_is_spinning = False
        self.vreel_pos = pos
        self.pos_adj = 160
        
        self.draw_virtual_reels(self.vreel_pos)

    def draw_virtual_reels(self, pos):
        for idx, item in enumerate(self.reels):
            self.symbol_list.add(SlotSymbol(item.id, item.symbol, item.image, pos, idx))
            x, y = pos
            y += self.pos_adj
            # if idx == 0:
            #     y = self.pos_adj
            pos = [x, y]
            
    def animate(self, delta_time):
        weights = [item.probability for item in slotitems.items]
        randsym = None
                        
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            if self.delay_time <= 0:
                for i, symbol in enumerate(self.symbol_list):
                    symbol.rect.bottom += 80

                    if symbol.rect.top == (self.pos_adj * 4):
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()

                        randsym = random.choices(slotitems.items, weights=weights)
                        randsym = randsym[0]
   
                        self.symbol_list.add(SlotSymbol(randsym.id, randsym.symbol, randsym.image, ((symbol.x_val), self.pos_adj), symbol_idx))
        
    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True
    
    def reel_spin_result(self):
        spin_symbols = []
        for i in range(3):
            spin_symbols.append(slotitems.items[self.symbol_list.sprites()[i].item_id])
        return spin_symbols[::-1]
    
class SlotMachine:
    def __init__(self, minbet:int=100):
        self.slot_items = slotitems.items
        self.paytables = [
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
        
        self.player = Player("Player")
        self.player_bet = 0
        self.player_balance = self.player.balance
        self.player_free_spin = self.player.auto_spin
        self.min_bet = minbet
        self.max_bet = minbet ** 2
        
        self.surface = pygame.display.get_surface()
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.pos_adj = 160
        self.reel_index = 0
        self.reel_list = {}
        
        self.spawn_reels()
    
    def spawn_reels(self):
        weights = [item.probability for item in self.slot_items]
        rand_reels = [random.choices(self.slot_items, weights=weights, k=3) for _ in range(5)]

        if not self.reel_list:
            x_topleft, y_topleft = 250, self.pos_adj
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (self.pos_adj), self.pos_adj
            
            self.reel_list[self.reel_index] = SlotReel((x_topleft, y_topleft), rand_reels[self.reel_index]) # Need to create reel class
            self.reel_index += 1
    
    def cooldown(self):
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True
        
    def check_wins(self, reels):
        result = [[tile[0].symbol for tile in reels], [tile[1].symbol for tile in reels], [tile[2].symbol for tile in reels]]
        
        paylines = [
            [0, 1, 2],
            [1, 2, 3],
            [2, 3, 4],
            [0, 1, 2, 3],
            [1, 2, 3, 4],
        ]
        
        wild_id = "🍀"
        win_amount = 0
        
        for index, table in enumerate(self.paytables):
            win_symbols = [False] * 5
            mapped_table_reel = [result[row][col] for row, col in table]
            
            for payline in paylines:
                symbols_in_payline = [mapped_table_reel[i] for i in payline]
                wild_indices = [i for i in range(len(payline)) if symbols_in_payline[i] == wild_id]
                
                if wild_indices:
                    first_non_wild_index = [i for i in range(len(payline)) if symbols_in_payline[i] != wild_id][0]

                    for wild_index in wild_indices:
                        symbols_in_payline[wild_index] = symbols_in_payline[first_non_wild_index]

                if all(symbol == symbols_in_payline[0] for symbol in symbols_in_payline):
                    for i in payline:
                        win_symbols[i] = True
            
            print()
            print(f"pay table {index}")
            for i in range(5):
                if win_symbols[i]:
                    win_amount += self.payout(mapped_table_reel[i])
                    print(mapped_table_reel[i], self.payout(mapped_table_reel[i]), win_amount)

        win_amount = win_amount * (self.player_bet * 0.1)
        
        return int(win_amount)
    
    def get_result(self):
        reels = [self.reel_list[reel].reel_spin_result() for reel in self.reel_list]
            
        symbols = [symbol.symbol for reel in reels for symbol in reel]
    
        bonus_count = symbols.count('🃏')
        free_spin_count = symbols.count('🎲')
                
        if bonus_count > 2:
            bonus_count -= 2
        else:
            bonus_count = 0

        return reels, bonus_count, free_spin_count
    
    def payout(self, symbol):
        payouts = {item.symbol: item.payout for item in self.slot_items}
        return payouts.get(symbol, 0)
    
    def print_reels(self, reels, id_format=False):
        os.system('cls')
        symbol_length = 2 if id_format else 4
        horizontal_line = "-" * (symbol_length * 5 + 11)
        
        print(horizontal_line)
        for i in range(3):
            if not id_format:
                print(f'| {reels[0][i].symbol}  | {reels[1][i].symbol}  | {reels[2][i].symbol}  | {reels[3][i].symbol}  | {reels[4][i].symbol}  |')
            else:
                print(f'| {reels[0][i].id} | {reels[1][i].id} | {reels[2][i].id} | {reels[3][i].id} | {reels[4][i].id} |')
        print(horizontal_line)
    
    def spin(self, bet, pull_lever=False):
        keys = pygame.key.get_pressed()

        # Checks for space key, ability to toggle spin, and balance to cover bet size
        # if keys[pygame.K_SPACE] and self.can_toggle:
        if self.can_toggle and pull_lever:
            
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False
            
            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False
        
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.play(bet)
    
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)
            
    def update(self, delta_time, bet, pull_lever=False):
        self.cooldown()
        self.spin(bet, pull_lever)
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.surface)

    def play(self, bet_amount):      
        if bet_amount < self.min_bet or bet_amount > self.max_bet:
            raise Exception(f"Invalid bet amount. Bet must be between {self.min_bet} and {self.max_bet}")
        if self.player_balance - bet_amount < 0:
            print("Not enough balance")
            return

        self.player_bet = bet_amount
        
        if self.player_free_spin - (self.player_bet * 0.01) >= 0:
            self.player_free_spin -= int((self.player_bet * 0.01))
        else:
            self.player_balance -= bet_amount
        
        result, bonus_count, free_spin_count = self.get_result()
        payout = self.check_wins(result)

        self.print_reels(result)
        print(f"Special: bonus-level({bonus_count}) freespin({free_spin_count})")
        
        self.player_free_spin += free_spin_count
        
        if payout > 0:
            print(f"You won {payout} coins!")
            self.player_balance += (payout + self.player_bet)
        else:
            print(f"No win this time.")

        print(f"Balance: {self.player_balance} coins\n")

if __name__ == "__main__":
    exec(open("scripts/main.py").read())
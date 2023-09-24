import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from settings import data_path

class Reel:
    def __init__(self, pos, reels):
        self.symbol_list = pygame.sprite.Group()
        self.reels = reels
        random.shuffle(self.reels)
        self.reels = self.reels[:9] # Only matters when there are more than 5 symbols

        self.reel_is_spinning = False

        # Sounds
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)

        for idx, item in enumerate(self.reels):
            self.symbol_list.add(SlotSymbol(item.symbol, item.image, pos, idx))
            pos = list(pos)
            pos[1] += (144 + 10)
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            # Stagger reel spin start animation
            if self.delay_time <= 0:

                # Iterate through all 5 symbols in reel; truncate; add new random symbol on top of stack
                for i, symbol in enumerate(self.symbol_list):
                    symbol.rect.bottom += 100

                    # Correct spacing is dependent on the above addition eventually hitting 1200
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Spawn random symbol in place of the above
                        randsym = random.choice(self.reels)
                        self.symbol_list.add(SlotSymbol(randsym.symbol, randsym.image, ((symbol.x_val), -300), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        # Get and return text representation of symbols in a given reel
        spin_symbols = []
        for i in [0, 1, 2]:
            spin_symbols.append(self.symbol_list.sprites()[i].symbol)
        return spin_symbols

class SlotSymbol(pygame.sprite.Sprite):
    def __init__(self, symbol, image, pos, idx):
        super().__init__()

        self.symbol = symbol
        self.pos = pos
        self.idx = idx
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.x_val = self.rect.left

        # Used for win animations
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # Slightly increases size of winning symbols
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        
        # Fades out non-winning symbols
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)

class SlotMachine:
    def __init__(self, min_bet):
        self.surface = pygame.display.get_surface()
        self.system = SlotSystem(min_bet)
        
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False
        
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        
        self.spawn_reels()
    
    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            result = self.get_result()
            print(result)
    
    def input(self):
        keys = pygame.key.get_pressed()

        # Checks for space key, ability to toggle spin, and balance to cover bet size
        if keys[pygame.K_SPACE] and self.can_toggle:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 250, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (144 + 10), y_topleft
            
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft), self.system.reels) # Need to create reel class
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False
            
            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False
    
    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    # You need to provide sounds and load them in the Machine init function for this to work!
    def play_win_sound(self):
        pass

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.surface)
            self.reel_list[reel].symbol_list.update()
        
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
        
    def spin(self, bet=None):
        if bet < self.min_bet or bet > self.max_bet:
            raise Exception(f"Invalid bet amount. Bet must be between {self.min_bet} and {self.max_bet}")
        
        randreels = self.__create_random_reels()
        self.print_slot_symbol(randreels, id_format=False)
        
        wins = self.__get_paylines(randreels, bet)
        
        print("Winlines: ", wins[0])
        print("Prize: ", wins[1])
        print(f"Special: bonus-level({wins[2]}) freespin({wins[2]})")
        
        
        reel0 = [randreels[0][0], randreels[1][0], randreels[2][0]]
        reel1 = [randreels[0][1], randreels[1][1], randreels[2][1]]
        reel2 = [randreels[0][2], randreels[1][2], randreels[2][2]]
        reel3 = [randreels[0][3], randreels[1][3], randreels[2][3]]
        reel4 = [randreels[0][4], randreels[1][4], randreels[2][4]]
        
        reel = [reel0, reel, reel2, reel3, reel4]
                
        return reel, wins

if __name__ == "__main__":
    import time
    start = time.time()
    slot = SlotSystem(100)
    slot.spin(100)
    end = time.time()
    print("Time elapsed: ", end - start)
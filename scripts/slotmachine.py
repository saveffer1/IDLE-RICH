import pygame
import random
from slot import SlotSystem
from settings import reel_adj

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

        self.reels = self.reels[:5]

        self.reel_is_spinning = False

        # Sounds
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)

        for idx, item in enumerate(self.reels):
            self.symbol_list.add(SlotSymbol(item.id, item.symbol, item.image, pos, idx))
            x, y = pos
            y += reel_adj
            pos = [x, y]
        
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
                    symbol.rect.bottom += reel_adj

                    # Correct spacing is dependent on the above addition eventually hitting
                    if symbol.rect.top == reel_adj * 4:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Spawn random symbol in place of the above
                        randsym = random.choice(self.reels)
                        self.symbol_list.add(SlotSymbol(randsym.id, randsym.symbol, randsym.image, ((symbol.x_val), -reel_adj), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        # Get and return text representation of symbols in a given reel
        # spin_symbols = []
        # for i in [1, 2, 3]:
        #     spin_symbols.append(self.symbol_list.sprites()[i].symbol)
        #     print(spin_symbols[i-1], end=' ')
        # print()
        
        spin_symbols = []
        
        spin_symbols.append(self.symbol_list.sprites()[3].item_id)
        spin_symbols.append(self.symbol_list.sprites()[2].item_id)
        spin_symbols.append(self.symbol_list.sprites()[1].item_id)
        
        return spin_symbols
    
        
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
        
        # self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = [[], [], []]
        
        self.spawn_reels()
    
    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 250, -reel_adj
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (reel_adj), -reel_adj
            
            self.reel_list[self.reel_index] = SlotReel((x_topleft, y_topleft), self.system.reels) # Need to create reel class
            self.reel_index += 1
            
    def cooldown(self):
        # Only lets player spin if all reels are NOT spinning
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

    def spin(self, bet):
        keys = pygame.key.get_pressed()

        # Checks for space key, ability to toggle spin, and balance to cover bet size
        if keys[pygame.K_SPACE] and self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False
            
            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False
        
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()
            print(self.spin_result)
            self.system.spin(self.spin_result, bet=bet)
    
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)
    
    def get_result(self):
        sym = [[], [], []]
        for reel in self.reel_list:
            sym[0].append(self.reel_list[reel].reel_spin_result()[0])
            sym[1].append(self.reel_list[reel].reel_spin_result()[1])
            sym[2].append(self.reel_list[reel].reel_spin_result()[2])

        return sym

    # You need to provide sounds and load them in the Machine init function for this to work!
    def play_win_sound(self):
        pass

    def update(self, delta_time):
        self.cooldown()
        self.spin(100)
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.surface)

if __name__ == "__main__":
    exec(open("scripts/main.py").read())
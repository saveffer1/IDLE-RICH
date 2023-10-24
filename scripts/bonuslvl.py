import pygame
from pygame.locals import *
from pygame import mixer
import sys
import math
import random
import time
from settings import *
from gamestate import GameState
from pgui import *
from bonusitem import *
from system import *
from datakit import LimitedQueue
from translator import tl, lang, translator

class Bonus1(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.deck1 = [(pygame.image.load(os.path.join(data_path, f"assets/bonus/lv1/{i}_spade.png")), (i*100)) for i in range(1, 6)]
        self.deck2 = [(pygame.image.load(os.path.join(data_path, f"assets/bonus/lv1/{i}_spade.png")), (i*100)) for i in range(6, 11)]
        self.deck = LimitedQueue(max_size=4)
        self.cards = []
        
        self.shuffle()
        
        self.reward = 0
        self.slot_machine = self.game.slot_machine
        
        self.btn_claim = TextButton(tl("claim_reward"), x=525, y=450)
        self.lbl_reward = Label(f'{tl("bonus_reward")} {self.reward}', font_size=50, x=540, y=350)
        
    def shuffle(self):
        deck1 = self.deck1.copy()
        deck2 = self.deck2.copy()
        random.shuffle(deck1)
        random.shuffle(deck2)
        
        while not deck1 == [] and not deck2 == []:
            if not self.deck1 == []:
                self.deck.enqueue(deck1.pop(0))

            if not deck2 == []:
                self.deck.enqueue(deck2.pop(-1))
        
        self.cards = [Card(self.deck[i][0], 400 + int(i*120), 150, self.deck[i][1]) for i in range(len(self.deck))]
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for card in self.cards:
                    if card.rect.collidepoint(event.pos):
                        if not card.is_flipped:
                            GUI.clicked_sound(SOUND_FLIPCARD, addition_vol=0.5)
                            card.flip()
                        else:
                            GUI.clicked_sound(SOUND_CANTCLICK, addition_vol=0.2)
                            
                        if self.reward == 0:
                            self.reward = card.index
                            self.slot_machine.player_balance += self.reward
                            
                if self.btn_claim.clicked():
                    self.reward = 0
                    self.shuffle()
                    for card in self.cards:
                        card.image = card.card_back
                        card.is_flipped = False
                    self.game.change_state("game_play")
                
    def update(self):
        if self.reward != 0:
            self.lbl_reward.text = f'{tl("bonus_reward")} {self.reward}'
            self.btn_claim.set_hover()
            
        for card in self.cards:
            card.update()
    
    def render(self):
        self.surface.fill("#000000")
        self.surface.blit(pygame.transform.scale(BG, (self.surf_width, self.surf_height)), (0, 0))
        
        if self.reward != 0:
            self.lbl_reward.draw()
            self.btn_claim.draw()
        
        for card in self.cards:
            card.draw()
                
        pygame.display.update()
        self.clock.tick(self.fps)

class Bonus2(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.chest_lst = DCList()
        chest_types = ["low", "medium", "high"]

        self.reward = 0
        
        for i in range(1, 7):
            chest_type = chest_types[(i - 1) % len(chest_types)]
            self.chest_lst.append(Chest(chest_type, 300 + int(i * 100), 150, i))
        
        self.random_pos()

        self.slot_machine = self.game.slot_machine
        self.btn_claim = TextButton(tl("claim_reward"), x=525, y=450)
        self.lbl_reward = Label(f'{tl("bonus_reward")} {self.reward}', font_size=50, x=540, y=350)
        
    def random_pos(self):
        loop = random.randint(1, 10)
        
        cur = self.chest_lst.head
        for i in range(loop + 1):
            cur = cur.next
        
        cur.prev.data.rect.topleft = (200, 100)
        cur.data.rect.topleft = (500, 100)
        cur.next.data.rect.topleft = (800, 100)
        
        self.chest = [cur.data, cur.prev.data, cur.next.data]
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for chest in self.chest:
                    if chest.rect.collidepoint(event.pos):
                        if not chest.is_opened:
                            GUI.clicked_sound(SOUND_OPENCHEST, addition_vol=0.5)
                            chest.open()
                        else:
                            GUI.clicked_sound(SOUND_CANTCLICK, addition_vol=0.2)
                        if self.reward == 0:
                            self.reward = chest.reward
                            self.slot_machine.player_balance += self.reward
                
                if self.btn_claim.clicked():
                    self.reward = 0
                    self.random_pos()
                    for chest in self.chest:
                        chest.image = chest.chest_closed
                        chest.is_opened = False
                    self.game.change_state("game_play")
    
    def update(self):
        if self.reward != 0:
            self.lbl_reward.text = f'{tl("bonus_reward")} {self.reward}'
            self.btn_claim.set_hover()
            
        for chest in self.chest:
            chest.update()
    
    def render(self):
        self.surface.fill("#000000")
        self.surface.blit(pygame.transform.scale(BG, (self.surf_width, self.surf_height)), (0, 0))
        
        if self.reward != 0:
            self.lbl_reward.draw()
            self.btn_claim.draw()
        
        for chest in self.chest:
            chest.draw()
                
        pygame.display.update()
        self.clock.tick(self.fps)

class Bonus3(GameState):
    def __init__(self, game):
        super().__init__(game)

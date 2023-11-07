from typing import Any
import pygame
import time
import os
import random
from settings import data_path

card_back = pygame.image.load(os.path.join(data_path, "assets/bonus/lv1/card_back.png"))
chest_closed = pygame.image.load(os.path.join(data_path, "assets/bonus/lv2/chest_back.png"))
chest_opened = {
    "low": pygame.image.load(os.path.join(data_path, "assets/bonus/lv2/chest1.png")),
    "medium": pygame.image.load(os.path.join(data_path, "assets/bonus/lv2/chest2.png")),
    "high": pygame.image.load(os.path.join(data_path, "assets/bonus/lv2/chest3.png"))
}

class Card(pygame.sprite.Sprite):
    def __init__(self, image, x, y, index):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.card_back = card_back
        self.card_front = image
        self.image = self.card_back
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.index = index
        self.is_flipped = False
        
    def flip(self):
        if not self.is_flipped:
            self.image = self.card_front
    
    def draw(self):
        self.surface.blit(self.image, self.rect.topleft)

class Chest(pygame.sprite.Sprite):
    def __init__(self, type, x, y, index):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.chest_closed = pygame.transform.scale(chest_closed, (300, 300))
        self.chest_opened = pygame.transform.scale(chest_opened[type], (300, 300))
        self.image = self.chest_closed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.money = {
            "low": 500,
            "medium": 1000,
            "high": 2000
        }
        
        self.reward = self.money[type]
        self.type = type
        self.is_opened = False
    
    def open(self):
        if not self.is_opened:
            self.is_opened = True
            self.image = self.chest_opened

    def draw(self):
        self.surface.blit(self.image, self.rect.topleft)
        
class Brick(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, color, speed):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))
    
    def move(self):
        self.x += self.speed
        if self.x > self.surface.get_width():
            self.speed *= -1
        if self.x + self.w < 1:
            self.speed *= -1
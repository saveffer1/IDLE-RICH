import pygame, os
from settings import data_path

class SlotItem:
    def __init__(self, id, symbol: str, image: pygame.Surface, probability, skill: str="price", payout: int=50):
        self.id = id
        self.symbol = symbol
        self.probability = probability
        self.payout = payout
        if skill not in ["price", "wild", "scatter", "bonus"]:
            raise Exception("Invalid skill type. Can only be 'price', 'wild', 'scatter', or bonus")
        else:
            self.skill = skill
        self.image = image

items = [
    SlotItem(0, "🍌", pygame.image.load(os.path.join(data_path, 'assets/slot/item/banana.png')), 15, "price", 2),
    SlotItem(1, "🍇", pygame.image.load(os.path.join(data_path, 'assets/slot/item/grape.png')), 15, "price", 2),
    SlotItem(2, "🍒", pygame.image.load(os.path.join(data_path, 'assets/slot/item/cherry.png')), 20, "price", 4),
    SlotItem(3, "🍋", pygame.image.load(os.path.join(data_path, 'assets/slot/item/lemon.png')), 20, "price", 4),
    SlotItem(4, "💰", pygame.image.load(os.path.join(data_path, 'assets/slot/item/bigprize.png')), 5, "price", 15),
    SlotItem(5, "🎲", pygame.image.load(os.path.join(data_path, 'assets/slot/item/freespin.png')), 10, "scatter", 5),
    SlotItem(6, "🃏", pygame.image.load(os.path.join(data_path, 'assets/slot/item/game.png')), 5, "bonus", 5),
    SlotItem(7, "👑", pygame.image.load(os.path.join(data_path, 'assets/slot/item/jackpot.png')), 2, "price", 25),
    SlotItem(8, "🍀", pygame.image.load(os.path.join(data_path, 'assets/slot/item/wildcard.png')), 8, "wild", 0)
]
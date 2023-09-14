from pygame import mixer
from configparser import ConfigParser
import pygame
import os
from datakit import *

# main font
FONT = os.path.join('assets', "fonts", "DM Academy.ttf")
FONT_ICON = os.path.join('assets', "fonts", "MaterialIcons-Regular.ttf")

# load config file
config = ConfigParser()
config.read(os.path.join('config', 'config.ini'))

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# load save file
# SAVEPATH = os.path.join('data', 'savefile.sav')
SAVEPATH = os.path.join('config', 'save.json')

# load sfx file
mixer.init()
SOUND_UISELECT = mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'ui-selected.mp3'))
SOUND_BTNCLICK = mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'btn-clicked.wav'))
SOUND_COLLECT = mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'collected.wav'))
SOUND_CANTCLICK = mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'ui-cantclick.mp3'))
SOUND_START = mixer.Sound(os.path.join('assets', 'audio', 'sfx', 'start.mp3'))

# load sound with doubly circular linked list
msc_ingame = MusicList()
msc_ingame.append(SoundNode(os.path.join('assets', 'audio', 'music', 'Idle Rich 1.mp3')))
msc_ingame.append(SoundNode(os.path.join('assets', 'audio', 'music', 'Idle Rich 2.mp3')))
msc_ingame.append(SoundNode(os.path.join('assets', 'audio', 'music', 'Idle Rich 3.mp3')))
msc_ingame.append(SoundNode(os.path.join('assets', 'audio', 'music', 'Idle Rich 4.mp3')))

msc_menu = MusicList()
msc_menu.append(SoundNode(os.path.join('assets', 'audio', 'music', 'menu 1.mp3')))
msc_menu.append(SoundNode(os.path.join('assets', 'audio', 'music', 'menu 2.mp3')))
msc_menu.append(SoundNode(os.path.join('assets', 'audio', 'music', 'menu 3.mp3')))

# load GUI assets
text_button_hashed = {
    "button":{
        "active":pygame.image.load('assets/gui/btn_empty_active.png'),
        "inactive":pygame.image.load('assets/gui/btn_empty.png')
    },
    "ciclebtn":{
        "active":pygame.image.load('assets/gui/circle_btn_active.png'),
        "inactive":pygame.image.load('assets/gui/circle_btn.png')
    },
}

button_hashed = {
    "close":{
        "active":pygame.image.load('assets/gui/close_active.png'),
        "inactive":pygame.image.load('assets/gui/close.png')
    },
    "arrow_left":{
        "active":pygame.image.load('assets/gui/arrow_back_active.png'),
        "inactive":pygame.image.load('assets/gui/arrow_back.png')
    },
    "arrow_right":{
        "active":pygame.image.load('assets/gui/arrow_forward_active.png'),
        "inactive":pygame.image.load('assets/gui/arrow_forward.png')
    },
    "delsave":{
        "active":pygame.image.load('assets/gui/delsave_active.png'),
        "inactive":pygame.image.load('assets/gui/delsave.png')
    }
}

range_slider_hashed = { 
    "btn": pygame.image.load('assets/gui/rg_btn.png'), 
    "bar": pygame.image.load('assets/gui/rg_bar.png') 
}

toggle_hashed = {
    "on":pygame.image.load('assets/gui/rg_btn.png'),
    "rect":pygame.image.load('assets/gui/tg_rect.png')
}


# Slot Machine assets
slot_img = {
    "banana": pygame.image.load('assets/slot/item/banana.png'),
    "bigprize": pygame.image.load('assets/slot/item/bigprize.png'),
    "cherry": pygame.image.load('assets/slot/item/cherry.png'),
    "freespin": pygame.image.load('assets/slot/item/freespin.png'),
    "game": pygame.image.load('assets/slot/item/game.png'),
    "jackpot": pygame.image.load('assets/slot/item/jackpot.png'),
    "lemon": pygame.image.load('assets/slot/item/lemon.png'),
    "wildcard": pygame.image.load('assets/slot/item/wildcard.png')
}

if __name__ == "__main__":
    raise RuntimeError("This module is not meant to run on its own!")
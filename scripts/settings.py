from pygame import mixer
from configparser import ConfigParser
import pygame
import os
from datakit import *
import json

script_directory = os.path.dirname(__file__)
data_path = os.path.join(script_directory, "..")

# main font
FONT = os.path.join(data_path,data_path,"assets", "fonts", "DM Academy.ttf")
FONT_ICON = os.path.join(data_path,data_path,'assets', "fonts", "MaterialIcons-Regular.ttf")

# load config file
config = ConfigParser()
config.read(os.path.join(data_path,'config/config.ini'))

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# load save file
SAVEPATH = os.path.join(data_path,'config/savefile.sav')
# SAVEPATH = os.path.join(data_path'config/save.json')

# load sfx file
mixer.init()
SOUND_UISELECT = mixer.Sound(os.path.join(data_path,'assets/audio/sfx/ui-selected.mp3'))
SOUND_BTNCLICK = mixer.Sound(os.path.join(data_path,'assets/audio/sfx/btn-clicked.wav'))
SOUND_COLLECT = mixer.Sound(os.path.join(data_path,'assets/audio/sfx/collected.wav'))
SOUND_CANTCLICK = mixer.Sound(os.path.join(data_path,'assets/audio/sfx/ui-cantclick.mp3'))
SOUND_START = mixer.Sound(os.path.join(data_path,'assets/audio/sfx/start.mp3'))
SOUND_BUY = mixer.Sound(os.path.join(data_path,'assets/audio/sfx/buy.wav'))

# load sound with doubly circular linked list
msc_ingame = MusicList()
msc_ingame.append(SoundNode(os.path.join(data_path,'assets/audio/music/Idle Rich 1.mp3')))
msc_ingame.append(SoundNode(os.path.join(data_path,'assets/audio/music/Idle Rich 2.mp3')))
msc_ingame.append(SoundNode(os.path.join(data_path,'assets/audio/music/Idle Rich 3.mp3')))
msc_ingame.append(SoundNode(os.path.join(data_path,'assets/audio/music/Idle Rich 4.mp3')))

msc_menu = MusicList()
msc_menu.append(SoundNode(os.path.join(data_path,'assets/audio/music/menu 1.mp3')))
msc_menu.append(SoundNode(os.path.join(data_path,'assets/audio/music/menu 2.mp3')))
msc_menu.append(SoundNode(os.path.join(data_path,'assets/audio/music/menu 3.mp3')))

# load GUI assets
text_button_hashed = {
    "button":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/btn_empty_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/btn_empty.png'))
    },
    "buy_button":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/btn_buycoins_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/btn_buycoins.png'))
    },
    "ciclebtn":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/circle_btn_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/circle_btn.png'))
    },
}

button_hashed = {
    "close":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/close_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/close.png'))
    },
    "arrow_left":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/arrow_back_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/arrow_back.png'))
    },
    "arrow_right":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/arrow_forward_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/arrow_forward.png'))
    },
    "delsave":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/delsave_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/delsave.png'))
    },
    "buy":{
        "active":pygame.image.load(os.path.join(data_path,'assets/gui/buy_credit_active.png')),
        "inactive":pygame.image.load(os.path.join(data_path,'assets/gui/buy_credit.png'))
    }
}

range_slider_hashed = { 
    "btn": pygame.image.load(os.path.join(data_path,'assets/gui/rg_btn.png')), 
    "bar": pygame.image.load(os.path.join(data_path,'assets/gui/rg_bar.png')) 
}

toggle_hashed = {
    "on":pygame.image.load(os.path.join(data_path,'assets/gui/rg_btn.png')),
    "rect":pygame.image.load(os.path.join(data_path,'assets/gui/tg_rect.png'))
}

BG_ALPHA = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
BG_ALPHA.fill((0,0,0,128))

BG = pygame.image.load(os.path.join(data_path,'assets/BG/screen.png'))

WINDOW = pygame.image.load(os.path.join(data_path, "assets/BG/window.png"))

current_language = config.get("LANGUAGE", "CURRENT_LANGUAGE")
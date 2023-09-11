import pygame
from pygame.locals import *
import sys
import os
import pickle
import threading
from settings import *
import time

class Options:
    @staticmethod
    def save_config():
        with open(os.path.join('config', 'config.ini'), 'w') as configfile:
            config.write(configfile)
            configfile.close()
            
    @staticmethod
    def toggle_fullscreen(state: bool):
        res_code = state
        config.set('GRAPHIC', 'SCREEN_CODE', str(res_code))
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if config.getboolean("GRAPHIC", "SCREEN_CODE") else 0)
        print('[DEBUG] set fullscreen to ', state)
        Options.save_config()
        
    @staticmethod
    def set_sfx_volume(value):
        value = int(value)
        config.set('AUDIO', 'SFX_VOLUME', str(value))
        print('[DEBUG] set sfx volume to ', value)
        Options.save_config()
        
    @staticmethod
    def set_music_volume(value):
        value = int(value)
        config.set('AUDIO', 'MUSIC_VOLUME', str(value))
        print('[DEBUG] set music volume to ', value)
        Options.save_config()
    
    @staticmethod
    def save_ingame_music(obj_index: int, obj: pygame.mixer.Sound):
        config.set('AUDIO', 'MUSIC_INGAME', str(obj_index))
        print('[DEBUG] set ingame music to ', msc_ingame.path(obj_index))
        Options.save_config()
    
    @staticmethod
    def save_menu_music(obj_index: int, obj: pygame.mixer.Sound):
        config.set('AUDIO', 'MUSIC_MENU', str(obj_index))
        print('[DEBUG] set menu music to ', msc_ingame.path(obj_index))
        Options.save_config()
    
    @staticmethod
    def handle_pygame_event(event):
        if event.type == QUIT:
            Options.save_config()
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    raise Exception('This is not a standalone file, please run main.py instead')
    
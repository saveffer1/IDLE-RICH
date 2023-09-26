import pygame
from pygame.locals import *
import sys
import os
import pickle
import threading
from settings import *
import time
from decimal import Decimal

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

class SaveData:
    def __init__(self):
        # check SAVE_PATH file exist
        if not os.path.exists(SAVEPATH):
            self.reset_data()
        
        self.data = self.load_data()
        self.player_coins = self.data["coins"]
    
    def load_data(self):
        with open(SAVEPATH, 'rb') as savefile:
            data = pickle.load(savefile)
            savefile.close()
            return data
    
    def save_data(self, data):
        with open(SAVEPATH, 'wb') as savefile:
            pickle.dump(data, savefile)
            savefile.close()
    
    def reset_data(self):
        data = {
            "coins": Decimal(0),
        }
        self.save_data(data)

if __name__ == "__main__":
    raise Exception('This is not a standalone file, please run main.py instead')
    
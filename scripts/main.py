import pygame, ctypes
from pygame import mixer
from settings import *
from state import *
from system import Options
from translator import tl
import threading
from bonuslvl import *
# ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if config.getboolean("GRAPHIC", "FULL_SCREEN") else 0)
        self.title = pygame.display.set_caption(tl("title"))
        self.icon = pygame.image.load(os.path.join("assets", "logo", "LOGO.png"))
        self.menu_music = msc_menu[config.getint("AUDIO", "MUSIC_MENU")]
        self.game_music = msc_ingame[config.getint("AUDIO", "MUSIC_INGAME")]
        self.game_music.set_volume(config.getint("AUDIO", "MUSIC_VOLUME") / 100)
        self.menu_music.set_volume(config.getint("AUDIO", "MUSIC_VOLUME") / 100)
        
        self.save_game = SaveData()
        self.save_data = self.save_game.data
        self.player = Player(self.save_data["name"], self.save_data["balance"], self.save_data["auto_spin"], self.save_data["current_bet"])
        self.slot_machine = SlotMachine(minbet=100, player=self.player)
        
        pygame.display.set_icon(self.icon)

        self.states = {
            "loading": LoadingStage(self),
        }
        
        self.current_state = "loading"
        self.prev_state = None
        
        self.loading_complete = threading.Event()
        self.loading_complete.set()
        
        state_th = threading.Thread(target=self.__first_load)
        state_th.daemon = True
        state_th.start()
        # transaction_th.join()
        
        self.states["loading"].load()
        
        self.menu_music.play(-1)
        self.game_music.stop()
    
    def __first_load(self):
        self.states = {
            "loading": LoadingStage(self),
            "main_menu": MainMenu(self),
            "option_menu": OptionMenu(self),
            "credit_menu": CreditMenu(self),
            "lobby_menu": Lobby(self),
            "game_play": GamePlay(self),
            "bonus1": Bonus1(self),
            "bonus2": Bonus2(self),
            "bonus3": Bonus3(self),
        }
        
        self.loading_complete.clear()
        self.change_state("main_menu")
        
    def change_state(self, new_state):
        if new_state in self.states:
            self.prev_state = self.current_state
            self.current_state = new_state
            
    def run(self):
        while True:
            events = pygame.event.get()
            
            # Handle events and update/render the current state
            for event in events:
                self.states[self.current_state].handle_events(event)
                if event.type == QUIT:
                    Options.save_config()
                    pygame.quit()
                    sys.exit()            
            
            self.states[self.current_state].update()
            self.menu_music.set_volume(config.getint("AUDIO", "MUSIC_VOLUME") / 100)
            self.game_music.set_volume((config.getint("AUDIO", "MUSIC_VOLUME") / 100))
            self.states[self.current_state].render()
            
            self.player = self.slot_machine.player
            self.save_data["name"] = self.player.name
            self.save_data["balance"] = self.slot_machine.player_balance
            self.save_data["auto_spin"] = self.slot_machine.player_free_spin
            self.save_data["current_bet"] = self.slot_machine.player_bet
            
            self.save_game.save_data(self.save_data)
            
if __name__ == "__main__":
    game = Game()
    game.run()
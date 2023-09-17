import pygame
from pygame.locals import *
from pygame import mixer
import sys
import math
import random
import time
from settings import *
from pgui import *
from system import *

class GameState:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.display.get_surface()
        self.display_info = pygame.display.Info()
        self.surf_width = self.display_info.current_w
        self.surf_height = self.display_info.current_h
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def handle_events(self, events):
        pass

    def update(self):
        self.display_info = pygame.display.Info()
        self.surf_width = self.display_info.current_w
        self.surf_height = self.display_info.current_h
    
    def render(self):
        pass
    
    def play_sound(self, sound:str, type:str):
        try:
            mixer.music.load(sound)
            if type.lower() == "music":
                mixer.music.set_volume(config.getint("AUDIO", "MUSIC_VOLUME") * 0.01)
            elif type.lower() == "sfx":
                mixer.music.set_volume(config.getint("AUDIO", "SFX_VOLUME") * 0.01)
            else:
                raise ValueError("Invalid sound type only 'music' or 'sfx'")
        except:
            raise FileNotFoundError("Sound file not found or invalid file type")
        mixer.music.play()    

class LoadingStage(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.loading_font = pygame.font.Font(FONT, 70)
        self.loading_animation = ""
        
    def load(self):
        while self.game.loading_complete.is_set():
            self.loading_animation += "."
            if len(self.loading_animation) > 3:
                self.loading_animation = ""
            
            self.surface.fill((0,0,0))
            textsurf = self.loading_font.render(f"{tl('loading')}{self.loading_animation}", True, (255, 255, 255))
            textrect = textsurf.get_rect(center=self.game.screen.get_rect().center)
            self.surface.blit(textsurf, textrect)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            self.clock.tick(self.fps)
            
            pygame.time.delay(500)

class MainMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        # Assets
        self.background = pygame.image.load(os.path.join("assets", "LOGO", "BG2.png"))
        
        # GUI
        self.btn_play = TextButton(text=tl("btn_play"), x=870, y=200)
        self.btn_option = TextButton(text=tl("btn_option"), x= 870, y=300)
        self.btn_credit = TextButton(text=tl("btn_credit"), x=870, y=400)
        self.btn_quit = TextButton(text=tl("btn_quit"), x=870, y=500)
        
        # Packed GUI
        self.all_btn = (self.btn_play, self.btn_option, self.btn_credit, self.btn_quit)
        
    def handle_events(self, events):
        for event in events:
            Options.handle_pygame_event(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.btn_quit.clicked():
                        pygame.quit()
                        sys.exit()
                    if self.btn_play.clicked():
                        GUI.clicked_sound(SOUND_START, addition_vol=0.3)
                        self.game.menu_music.stop()
                        self.game.game_music.play(-1)
                        self.game.change_state("game_play")
                    if self.btn_option.clicked():
                        GUI.clicked_sound(SOUND_BTNCLICK)
                        self.game.menu_music.stop()
                        self.game.menu_music.play(-1)
                        self.game.change_state("option_menu")
                    if self.btn_credit.clicked():
                        GUI.clicked_sound(SOUND_BTNCLICK)
                        self.game.menu_music.stop()
                        self.game.menu_music.play(-1)
                        self.game.change_state("credit_menu")       
    
    def update(self):
        for btn in self.all_btn:
            if isinstance(btn, TextButton):
                btn.set_elevate()
            btn.set_hover()
            btn.collide_sound(SOUND_UISELECT)

    def render(self):
        self.surface.fill((0,0,0))
        self.surface.blit(pygame.transform.scale(self.background, (self.surf_width, self.surf_height)), (0, 0))

        for btn in self.all_btn:
            btn.draw()

        pygame.display.update()
        self.clock.tick(self.fps)

class PauseMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            Options.handle_pygame_event(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game.change_state("game_play")
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_clicked = True
                    # if self.btn_resume.clicked():
                    #     self.game.game_music.play(-1)
                    #     self.game.change_state("game_play")
                    # if self.btn_option.clicked():
                    #     self.game.menu_music.play(-1)
                    #     self.game.change_state("option_menu")
                    # if self.btn_main_menu.clicked():
                    #     self.game.menu_music.play(-1)
                    #     self.game.change_state("main_menu")

    def update(self):
        self.mouse_clicked = False
        
        self.game.menu_music.stop()
        
        for btn in self.all_btn:
            btn.collide_sound(SOUND_UISELECT)
            btn.set_hover()
            btn.set_elevate()

    def render(self):
        self.surface.fill((0, 0, 0))
        
        self.menutext.draw()
        
        for btn in self.all_btn:
            btn.draw()
        
        pygame.display.update()
        self.clock.tick(self.fps)

class OptionMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Assets
        self.test_music = msc_ingame[0]
        self.background = pygame.image.load(os.path.join("assets", "BG", "screen.png"))
        self.option_rect = pygame.image.load(os.path.join("assets", "BG", "window.png"))
        
        # GUI
        self.option_label = Label(tl("lbl_options"), font_size=60, x=550, y=60)
        self.music_label = Label(tl("lbl_music"), font_size=40, x=350, y=160)
        self.sfx_label = Label(tl("lbl_sfx"), font_size=40, x=350, y=240)
        self.menumsc_label = Label(tl("lbl_menumsc"), font_size=40, x=350, y=300)
        self.gamemsc_label = Label(tl("lbl_gamemsc"), font_size=40, x=350, y=360)
        self.fullscr_label = Label(tl("lbl_fullscr"), font_size=40, x=350, y=450)
        self.clrsav_label = Label(tl("lbl_clearsav"), font_size=40, x=350, y=520)
        self.toggle_fullscreen = ToggleButton(x=725, y=450, callback=Options.toggle_fullscreen)
        
        self.music_slider = RangeSlider(start_value=config.getint("AUDIO", "MUSIC_VOLUME"), x=600, y=200, range_width=300, callback=Options.set_music_volume)
        self.sfx_slider = RangeSlider(start_value=config.getint("AUDIO", "SFX_VOLUME"), x=600, y=280, range_width=300, callback=Options.set_sfx_volume)
        self.sfx_slider.play_sound_after_drag = True
        
        self.menumsc_select = Selector(msc_menu, start_index=config.getint("AUDIO", "MUSIC_MENU"), x=650, y=320, callback=self.setmusic_menu)
        self.gamemsc_select = Selector(msc_ingame, start_index=config.getint("AUDIO", "MUSIC_INGAME"), x=650, y=380, callback=self.setmusic_ingame)
        
        self.btn_clrsav = IMGButton(type="delsave", x=725, y=520)
        self.btn_back = IMGButton(type="close", x=920, y=50)
        
        self.all_lbl = (self.option_label, self.music_label, self.sfx_label, self.menumsc_label, self.gamemsc_label, self.fullscr_label, self.clrsav_label)
        self.all_btn = (self.btn_back, self.btn_clrsav)
        
        # GAME
        self.stop_sound_event = threading.Event()
        
    def handle_events(self, events):
        for event in events:
            Options.handle_pygame_event(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game.menu_music.stop()
                    self.game.menu_music.play(-1)
                    self.game.change_state("main_menu") 
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.btn_back.clicked():
                        self.stop_sound_event.set()
                        self.test_music.stop()
                        self.stop_sound_event.clear()
                        GUI.clicked_sound(SOUND_BTNCLICK)
                        if self.game.prev_state == "main_menu":
                            self.game.menu_music.stop()
                            self.game.menu_music.play(-1)
                        self.game.change_state(self.game.prev_state)
            
            self.sfx_slider.handle_event(event)
            self.music_slider.handle_event(event)
            self.toggle_fullscreen.handle_event(event)
            self.menumsc_select.handle_event(event)
            self.gamemsc_select.handle_event(event)

    def update(self):
        for btn in self.all_btn:
            if isinstance(btn, TextButton):
                btn.set_elevate()
            btn.set_hover()
            btn.collide_sound(SOUND_UISELECT)
        
        self.sfx_slider.update()
        self.music_slider.update()
    
    def render(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(pygame.transform.scale(self.background, (self.surf_width, self.surf_height)), (0, 0))
        self.surface.blit(pygame.transform.scale(self.option_rect, (self.surf_width//2, 600)), (320,70))
        
        for component in self.all_lbl + self.all_btn:
            component.draw()
        
        self.sfx_slider.draw()
        self.music_slider.draw()
        self.toggle_fullscreen.draw()
        self.menumsc_select.draw()
        self.gamemsc_select.draw()
        
        pygame.display.update()
        self.clock.tick(self.fps)

    def play_sound_thread(self, musicobj: int, duration_seconds: int):
        if self.stop_sound_event.is_set():
            self.test_music.stop()
            self.stop_sound_event.clear()
        self.test_music = musicobj
        self.test_music.play(-1)

        pygame.time.wait(duration_seconds * 1000)

        self.test_music.stop()
        self.game.menu_music.play(-1)
    
    def setmusic_menu(self, obj_index: int):
        self.stop_sound_event.set()
        self.game.menu_music.stop()
        self.test_music.stop()

        duration_seconds = 5
        sound_thread = threading.Thread(target=self.play_sound_thread, args=(msc_menu[obj_index], duration_seconds))
        sound_thread.start()
        Options.save_menu_music(obj_index, msc_menu)
        self.game.menu_music = msc_menu[config.getint('AUDIO', 'MUSIC_MENU')]
    
    def setmusic_ingame(self, obj_index: int):
        self.stop_sound_event.set()
        self.game.menu_music.stop()
        self.test_music.stop()

        duration_seconds = 5
        sound_thread = threading.Thread(target=self.play_sound_thread, args=(msc_ingame[obj_index], duration_seconds))
        sound_thread.start()
        Options.save_ingame_music(obj_index, msc_ingame)

class CreditMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        # Assets
        self.background = pygame.image.load(os.path.join("assets", "BG", "screen.png"))
        self.credit_music = pygame.mixer.Sound(os.path.join("assets", "audio", "music", "credit.mp3"))
        
        self.btn_back = IMGButton(type="close", x=25, y=25)
        
        self.centerx = self.surface.get_rect().centerx
        self.centery = self.surface.get_rect().centery
        self.deltaY = self.centery + 50
        
        self.credit_text = tl("credit")
    
    def handle_events(self, events):
        for event in events:
            Options.handle_pygame_event(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.credit_music.stop()
                    self.game.menu_music.play(-1)
                    self.deltaY = self.centery + 50
                    self.game.change_state(self.game.prev_state)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_clicked = True
                    if self.btn_back.clicked():
                        self.credit_music.stop()
                        self.game.menu_music.play(-1)
                        self.deltaY = self.centery + 50
                        self.game.change_state(self.game.prev_state)
            
    def update(self):
        self.btn_back.set_hover()
        
        self.credit_music.set_volume((config.getint('AUDIO', 'MUSIC_VOLUME') / 100))
        self.game.menu_music.stop()
        self.credit_music.play(-1)

    def render(self):
        self.surface.fill((0,0,0))
        self.surface.blit(pygame.transform.scale(self.background, (self.surf_width, self.surf_height)), (0, 0))
        
        self.btn_back.draw()
        
        self.deltaY -= 1
            
        index = 0
        msg_list=[]
        pos_list=[]
        
        if self.deltaY < -720:
            self.deltaY = self.centery + 50
        
        font = pygame.font.Font(FONT, 45)
        
        for line in self.credit_text.split('\n'):
            msg=font.render(line, True, "#FFFFFF")
            msg_list.append(msg)
            pos= msg.get_rect(center=(self.centerx, self.centery + self.deltaY + 30 * index))
            pos_list.append(pos)
            index = index + 1
        
        for i in range(len(msg_list)):
            self.surface.blit(msg_list[i], pos_list[i])
        
        pygame.display.update()
        self.clock.tick(self.fps)

class GamePlay(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.game_state = "idle" # now has idle, slot
    
    def handle_idle_state(self, event):
        pass
    
    def handle_slot_state(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_clicked = True
        
    def handle_events(self, events):
        for event in events:
            Options.handle_pygame_event(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game.game_music.stop()
                    self.game_data.update_save()
                    self.game.change_state("pause_menu")
            if self.game_state == "idle":
                self.handle_idle_state(event)
            elif self.game_state == "slot":
                self.handle_slot_state(event)

    def update_idle_state(self):
        pass
    
    def update_slot_state(self):
        pass


    def update(self):
        self.game.menu_music.stop()
        
        if self.game_state == "idle":
            self.update_idle_state()
        elif self.game_state == "slot":
            self.update_slot_state()

    def render_idle_state(self):
        self.surface.fill((217,189,165))
        
    def render_slot_state(self):
        pass
    
    def render(self):
        if self.game_state == "idle":
            self.render_idle_state()
        elif self.game_state == "slot":
            self.render_slot_state()
        
        pygame.display.update()
        self.clock.tick(self.fps)
        
if __name__ == "__main__":
    # raise Exception('This is not a standalone file, please run main.py instead')
    exec(open("scripts/main.py").read())
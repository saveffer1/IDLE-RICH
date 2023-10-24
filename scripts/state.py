import pygame
from pygame.locals import *
from pygame import mixer
import sys
import math
import random
import time
from settings import *
from gamestate import GameState
from bonuslvl import *
from pgui import *
from system import *
from slotmachine import *
from translator import tl, lang, translator

class LoadingStage(GameState):
    """
    A class representing the loading stage of the game.
    
    Attributes:
    -----------
    game : Game
        The instance of the Game class.
    loading_font : pygame.font.Font
        The font used for the loading text.
    loading_animation : str
        The animation displayed during loading.
    """
    
    def __init__(self, game):
        super().__init__(game)
        
        self.loading_font = pygame.font.Font(FONT, 70)
        self.loading_animation = ""
        
    def load(self):
        """
        Loads the game while displaying a loading animation.
        """
        load_count = 0
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
            
            load_count += 1
            pygame.time.delay(500)
            if load_count >= 120:
                raise TimeoutError("Error loading timout")

class MainMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        # Assets
        self.background = pygame.image.load(os.path.join(data_path, "assets", "LOGO", "BG2.png"))
        
        # GUI
        self.btn_play = TextButton(text=tl("btn_play"), x=870, y=200)
        self.btn_option = TextButton(text=tl("btn_option"), x= 870, y=300)
        self.btn_credit = TextButton(text=tl("btn_credit"), x=870, y=400)
        self.btn_quit = TextButton(text=tl("btn_quit"), x=870, y=500)
        
        # Packed GUI
        self.all_btn = (self.btn_play, self.btn_option, self.btn_credit, self.btn_quit)
        
    def handle_events(self, event):
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
                    self.game.change_state("lobby_menu")
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
        self.btn_play.update(tl("btn_play"))
        self.btn_option.update(tl("btn_option"))
        self.btn_credit.update(tl("btn_credit"))
        self.btn_quit.update(tl("btn_quit"))

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
        
        self.alpha_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.alpha_background.fill((0, 0, 0, 128))
        
        self.btn_resume = TextButton(text=tl("btn_resume"), x=self.surf_width//2 - 212//2, y=200)
        self.btn_option = TextButton(text=tl("btn_option"), x=self.surf_width//2 - 212//2, y=300)
        self.btn_main_menu = TextButton(text=tl("btn_main_menu"), x=self.surf_width//2 - 212//2, y=400)
        
        self.pause_state = False
        
        self.all_btn = (self.btn_resume, self.btn_option, self.btn_main_menu)
    
    def show(self):
        self.pause_state = True
    
    def hide(self):
        self.pause_state = False
    
    def is_open(self):
        return self.pause_state
        
    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.hide()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.btn_resume.clicked():
                    self.game.game_music.play(-1)
                    self.hide()
                if self.btn_option.clicked():
                    self.game.menu_music.play(-1)
                    self.game.change_state("option_menu")
                if self.btn_main_menu.clicked():
                    self.hide()
                    self.game.change_state("main_menu")

    def update(self):
        if self.pause_state:
            self.game.menu_music.stop()
            
            for btn in self.all_btn:
                if isinstance(btn, TextButton):
                    btn.set_elevate()
                btn.set_hover()
                btn.collide_sound(SOUND_UISELECT)
            
            self.btn_resume.update(tl("btn_resume"))
            self.btn_option.update(tl("btn_option"))
            self.btn_main_menu.update(tl("btn_main_menu"))

    def render(self):
        if self.pause_state:
            # self.surface.blit(self.alpha_background, (0, 0))
            self.surface.fill("#000000")
            for btn in self.all_btn:
                btn.draw()

class OptionMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Assets
        self.test_music = msc_ingame[0]

        self.option_rect = WINDOW
        
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
        
        self.menumsc_select = Selector(msc_menu, start_index=config.getint("AUDIO", "MUSIC_MENU"), x=650, y=320, callback=self.__setmusic_menu)
        self.gamemsc_select = Selector(msc_ingame, start_index=config.getint("AUDIO", "MUSIC_INGAME"), x=650, y=380, callback=self.__setmusic_ingame)
        self.lang_select = Selector(lang, start_index=lang.find(config.get("LANGUAGE", "CURRENT_LANGUAGE")), x=1000, y=600, callback=lambda x : translator.set_language(lang[x]))
        self.lang_select.left_arrow_rect = pygame.Rect(1060, 610, 50, self.lang_select.rect.h)
        self.lang_select.right_arrow_rect = pygame.Rect(1120, 610, 50, self.lang_select.rect.h)
        
        
        self.btn_clrsav = IMGButton(type="delsave", x=725, y=520)
        self.btn_back = IMGButton(type="close", x=920, y=50)
        
        self.panel_clrsav = YesNoPopup(tl("clearsav_question"), width=500, height=500, x=400, y=200)
        
        self.all_lbl = (self.option_label, self.music_label, self.sfx_label, self.menumsc_label, self.gamemsc_label, self.fullscr_label, self.clrsav_label)
        self.all_btn = (self.btn_back, self.btn_clrsav)
        
        # GAME
        self.stop_sound_event = threading.Event()
        
    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.game.menu_music.stop()
                self.game.menu_music.play(-1)
                self.game.change_state("main_menu") 
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not self.panel_clrsav.is_open():
                if self.btn_back.clicked():
                    self.stop_sound_event.set()
                    self.test_music.stop()
                    self.stop_sound_event.clear()
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    if self.game.prev_state == "main_menu":
                        self.game.menu_music.stop()
                        self.game.menu_music.play(-1)
                    self.game.change_state(self.game.prev_state)
                if self.btn_clrsav.clicked():
                    self.panel_clrsav.show()

        self.sfx_slider.handle_events(event)
        self.music_slider.handle_events(event)
        self.toggle_fullscreen.handle_events(event)
        self.menumsc_select.handle_events(event)
        self.gamemsc_select.handle_events(event)
        self.lang_select.handle_events(event)
        confirm = self.panel_clrsav.handle_events(event)
        if self.panel_clrsav.is_open() and confirm is not None:
            if not confirm:
                self.panel_clrsav.hide()
            else:
                GUI.clicked_sound(SOUND_START, addition_vol=0.3)
                self.game.save_game.reset_data()
                self.game.save_game.load_data()
                self.panel_clrsav.hide()

    def update(self):
        if self.panel_clrsav.is_open():
            self.panel_clrsav.update()
        else:
            for btn in self.all_btn:
                if isinstance(btn, TextButton):
                    btn.set_elevate()
                btn.set_hover()
                btn.collide_sound(SOUND_UISELECT)
        
            self.sfx_slider.update()
            self.music_slider.update()
            
            self.option_label.update(tl("lbl_options"))
            self.music_label.update(tl("lbl_music"))
            self.sfx_label.update(tl("lbl_sfx"))
            self.menumsc_label.update(tl("lbl_menumsc"))
            self.gamemsc_label.update(tl("lbl_gamemsc"))
            self.fullscr_label.update(tl("lbl_fullscr"))
            self.clrsav_label.update(tl("lbl_clearsav"))
            self.panel_clrsav.update(tl("clearsav_question"))
    
    def render(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(pygame.transform.scale(BG, (self.surf_width, self.surf_height)), (0, 0))
        self.surface.blit(pygame.transform.scale(self.option_rect, (self.surf_width//2, 600)), (320,70))
        
        for component in self.all_lbl + self.all_btn:
            component.draw()
        
        self.sfx_slider.draw()
        self.music_slider.draw()
        self.toggle_fullscreen.draw()
        self.menumsc_select.draw()
        self.gamemsc_select.draw()
        self.lang_select.draw()
        
        if self.panel_clrsav.is_open():
            self.panel_clrsav.draw()
        
        pygame.display.update()
        self.clock.tick(self.fps)

    def __play_sound_thread(self, musicobj: int, duration_seconds: int):
        if self.stop_sound_event.is_set():
            self.test_music.stop()
            self.stop_sound_event.clear()
        self.test_music = musicobj
        self.test_music.play(-1)

        pygame.time.wait(duration_seconds * 1000)

        self.test_music.stop()
        self.game.menu_music.play(-1)
    
    def __setmusic_menu(self, obj_index: int):
        self.stop_sound_event.set()
        self.game.menu_music.stop()
        self.test_music.stop()

        duration_seconds = 5
        sound_thread = threading.Thread(target=self.__play_sound_thread, args=(msc_menu[obj_index], duration_seconds))
        sound_thread.start()
        Options.save_menu_music(obj_index, msc_menu)
        self.game.menu_music = msc_menu[config.getint('AUDIO', 'MUSIC_MENU')]
    
    def __setmusic_ingame(self, obj_index: int):
        self.stop_sound_event.set()
        self.game.menu_music.stop()
        self.test_music.stop()

        duration_seconds = 5
        sound_thread = threading.Thread(target=self.__play_sound_thread, args=(msc_ingame[obj_index], duration_seconds))
        sound_thread.start()
        Options.save_ingame_music(obj_index, msc_ingame)

class CreditMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        # Assets
        self.credit_music = pygame.mixer.Sound(os.path.join(data_path, "assets", "audio", "music", "credit.mp3"))
        
        self.btn_back = IMGButton(type="close", x=25, y=25)
        
        self.centerx = self.surface.get_rect().centerx
        self.centery = self.surface.get_rect().centery
        self.deltaY = self.centery + 50
        
        self.credit_text = tl("credit")
    
    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.credit_music.stop()
                self.game.menu_music.play(-1)
                self.deltaY = self.centery + 50
                self.game.change_state(self.game.prev_state)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.btn_back.clicked():
                    self.credit_music.stop()
                    self.game.menu_music.play(-1)
                    self.deltaY = self.centery + 50
                    self.game.change_state(self.game.prev_state)
            
    def update(self):
        self.credit_text = tl("credit")
        self.btn_back.set_hover()
        
        self.credit_music.set_volume((config.getint('AUDIO', 'MUSIC_VOLUME') / 100))
        self.game.menu_music.stop()
        self.credit_music.play(-1)

    def render(self):
        self.surface.fill((0,0,0))
        self.surface.blit(pygame.transform.scale(BG, (self.surf_width, self.surf_height)), (0, 0))
        
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

class Lobby(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.play_image = pygame.image.load(os.path.join(data_path, "assets/gui/lobby-play.png"))
        self.navbar = pygame.image.load(os.path.join(data_path, "assets/gui/lobby-nav.png"))
        self.btn_buy = IMGButton(type="buy", x=750, y=5)
        self.btn_pause = TextButton(text="\ue5d2", font=FONT_ICON, x=1225, y=5)
        self.btn_pause.resize(50, 50)
        self.btn_playslot = TextButton(text=tl("btn_playslot"), x=self.surf_width//2 - 212//2, y=500)
        
        self.all_btn = [self.btn_buy, self.btn_playslot]
        
        self.slot_machine = self.game.slot_machine
        self.lbl_player_balance = Label(text=str(self.slot_machine.player_balance), font_size=35, x=80, y=-4)
    
        # panel section
        self.buy_panel = Buy_Popup(width=500, height=500, x=400, y=200)
        self.pause_panel = PauseMenu(self.game)
    
    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.game.game_music.stop()
                self.game.menu_music.play(-1)
                self.game.change_state("main_menu")
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not self.buy_panel.is_open() and not self.pause_panel.is_open():
                if self.btn_buy.clicked():
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    self.game.game_music.stop()
                    self.buy_panel.show()
                if self.btn_pause.clicked():
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    self.game.game_music.stop()
                    self.game.menu_music.play(-1)
                    self.pause_panel.show()
                if self.btn_playslot.clicked():
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    self.game.game_music.stop()
                    self.game.menu_music.stop()
                    self.game.change_state("game_play")
            
        if self.buy_panel.is_open() and not self.pause_panel.is_open():
            amount = self.buy_panel.handle_events(event)
            if amount != None:
                    self.add_money(amount)
        elif self.pause_panel.is_open() and not self.buy_panel.is_open():
            self.pause_panel.handle_events(event)

    def add_money(self, amount):
        self.slot_machine.player_balance += amount
    
    def update(self):
        self.lbl_player_balance.update(str(self.slot_machine.player_balance))
        
        if not self.buy_panel.is_open() and not self.pause_panel.is_open():
            self.btn_pause.set_hover()
            self.btn_pause.collide_sound(SOUND_UISELECT)
            for btn in self.all_btn:
                if isinstance(btn, TextButton):
                    btn.set_elevate()
                btn.set_hover()
                btn.collide_sound(SOUND_UISELECT)
        
        if self.buy_panel.is_open() and not self.pause_panel.is_open():
            self.buy_panel.update()
            
        elif self.pause_panel.is_open() and not self.buy_panel.is_open():
            self.pause_panel.update()
        
        self.btn_playslot.update(tl("btn_playslot"))
    
    def render(self):
        self.surface.fill("#000000")
        self.surface.blit(pygame.transform.scale(BG, (self.surf_width, self.surf_height)), (0, 0))
        self.surface.blit(self.navbar, (0, 0))
        self.surface.blit(self.play_image, (self.surf_width//2 - self.play_image.get_width()//2, self.surf_height//2 - self.play_image.get_height()//2))
        
        self.lbl_player_balance.draw()
        
        self.btn_pause.draw()
        for btn in self.all_btn:
            btn.draw()
        
        if self.buy_panel.is_open() and not self.pause_panel.is_open():
            self.buy_panel.draw()
        
        elif self.pause_panel.is_open() and not self.buy_panel.is_open():
            self.pause_panel.render()
        
        pygame.display.update()
        self.clock.tick(self.fps)

class GamePlay(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.alpha_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.alpha_background.fill((0, 0, 0, 128))
        
        self.frame = pygame.image.load(os.path.join(data_path, "assets/BG/back.png"))
        
        self.image_home = pygame.image.load(os.path.join(data_path, "assets/gui/home_btn.png"))
        self.btn_home = pygame.Rect(50, 90, self.image_home.get_width(), self.image_home.get_height())
        
        self.image_info = pygame.image.load(os.path.join(data_path, "assets/gui/info_btn.png"))
        self.btn_info = pygame.Rect(1150, 90, self.image_info.get_width(), self.image_info.get_height())
        
        self.image_paylines = pygame.image.load(os.path.join(data_path, "assets/gui/paylines.png"))
        # self.paylines = pygame.Rect(0, 0, )
        self.btn_paylines_close = IMGButton(type="close", x=self.image_paylines.get_width() - 200, y=80)
        self.paylines_show = False
        
        self.slot_machine = self.game.slot_machine
        self.lever = SlotLever(x=SCREEN_WIDTH//2 + 500, y=SCREEN_HEIGHT//2 - 40)
        self.lever_state = False
        self.lbl_player_balance = Label(text=str(self.slot_machine.player_balance), font_size=35, x=80, y=-4)
        self.lbl_player_free_spin = Label(text=str(self.slot_machine.player_free_spin), font_size=35, x=770, y=-4)
        
        self.bet = self.slot_machine.player_bet
        self.btn_addbet = TextButton(text="+", font_size=50, x=50, y=300)
        self.btn_addbet.resize(50, 50)
        self.btn_subbet = TextButton(text="-", font_size=50, x=50, y=420)
        self.btn_subbet.resize(50, 50)
        self.lbl_bet = Label(text=str(self.bet), font_size=35, x=40, y=350)
        
        self.start_time = pygame.time.get_ticks()
        self.delta_time = 0
        
        self.light_effect = [pygame.image.load(f'assets/lightrays/File {i}.png') for i in range(1, 21)]
        self.bonuswin_image = pygame.image.load(os.path.join(data_path, "assets/bonus/bonusgame.png"))
        
    def handle_events(self, event):
        if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game.game_music.stop()
                    self.game.game_music.play(-1)
                    self.game.change_state("lobby_menu")
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not self.paylines_show:
                if self.btn_home.collidepoint(event.pos):
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    self.game.game_music.stop()
                    self.game.game_music.play(-1)
                    self.game.change_state("lobby_menu")
                    
                if self.btn_info.collidepoint(event.pos):
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    self.paylines_show = True
                    
                if self.btn_addbet.clicked():
                    if self.bet <= self.slot_machine.max_bet:
                        GUI.clicked_sound(SOUND_BTNCLICK)
                        self.bet += 100
                    else:
                        self.bet = self.slot_machine.max_bet
                        GUI.clicked_sound(SOUND_CANTCLICK)    
                    
                if self.btn_subbet.clicked():
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    if self.bet > self.slot_machine.min_bet:
                        self.bet -= self.slot_machine.min_bet
                    else:
                        GUI.clicked_sound(SOUND_CANTCLICK)  
                        self.bet = self.slot_machine.min_bet
                    
            elif event.button == 1 and self.paylines_show:
                if self.btn_paylines_close.clicked():
                    GUI.clicked_sound(SOUND_BTNCLICK)
                    self.paylines_show = False

        self.lever.handle_events(event, self.slot_machine.player_balance - self.bet >= 0)
    
    def update(self):
        self.lbl_player_balance.update(str(self.slot_machine.player_balance))
        self.lbl_player_free_spin.update(str(self.slot_machine.player_free_spin))
        self.lbl_bet.update(str(self.bet))
        self.btn_addbet.set_hover()
        self.btn_subbet.set_hover()
        
        self.slot_machine.player_bet = self.bet
        print(self.slot_machine.player_bet)
        
        if self.paylines_show:
            self.btn_paylines_close.set_hover()
            self.btn_paylines_close.collide_sound(SOUND_UISELECT)
        
        self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.start_time = pygame.time.get_ticks()
    
    def render(self):
        self.surface.fill("#000000")
        self.surface.blit(pygame.transform.scale(BG, (self.surf_width, self.surf_height)), (0, 0))
            
        self.slot_machine.update(self.delta_time, self.bet, pull_lever=self.lever.clicked())
        
        if self.slot_machine.cur_bonus_level > 0:
            for frame in self.light_effect:
                self.surface.blit(frame, (0, 0))
                self.surface.blit(self.bonuswin_image, (400, 200))
                
                pygame.display.update()
                self.clock.tick(self.fps)
                
            if self.slot_machine.cur_bonus_level == 1:
                self.game.change_state("bonus1")
            elif self.slot_machine.cur_bonus_level == 2:
                self.game.change_state("bonus2")
            
            self.slot_machine.cur_bonus_level = 0
            
        self.surface.blit(self.frame, (0, 0))
        self.surface.blit(self.image_home, self.btn_home)
        self.surface.blit(self.image_info, self.btn_info)
        
        self.btn_addbet.draw()
        self.btn_subbet.draw()
        self.lbl_bet.draw()
            
        self.lever.draw()
            
        self.lbl_player_balance.draw()
        self.lbl_player_free_spin.draw()
            
        if self.paylines_show:
            self.surface.blit(self.alpha_background, (0, 0))
            self.surface.blit(self.image_paylines, (0, 0))
            self.btn_paylines_close.draw()

        pygame.display.update()
        self.clock.tick(self.fps)
        
if __name__ == "__main__":
    # raise Exception('This is not a standalone file, please run main.py instead')
    exec(open("scripts/main.py").read())
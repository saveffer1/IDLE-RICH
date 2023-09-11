import pygame
from pygame.locals import *
from pygame import mixer
from settings import *
from datakit import MusicList

class GUI:
    def __init__(self, width=250, height=50, x=0, y=0) -> None:
        self.surface = pygame.display.get_surface()
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        
    def draw(self):
        pass
    
    def is_collided(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def clicked(self):
        mouse_press = pygame.mouse.get_pressed()[0]
        return self.is_collided() and mouse_press

    @staticmethod
    def clicked_sound(sound: mixer.Sound, addition_vol: float=0.0):
        vol = config.getint("AUDIO", "SFX_VOLUME") / 100
        sound.set_volume(vol + addition_vol)
        sound.play()

class Label(GUI):
    def __init__(self, text, font_size:int=30, x=0, y=0) -> None:
        super().__init__(x=x, y=y)
        
        self.text = text
        self.font = pygame.font.Font(FONT, font_size)
        self.text_color = "#FFFFFF"
        self.outline_color = "#FF9600"
        self.outline = True
    
    def draw(self):
        textobj = self.font.render(self.text, True, self.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (self.x, self.y)
        if self.outline:
            outline_surf = self.font.render(self.text, True, self.outline_color)
            outline_w, outline_h = outline_surf.get_size()
            self.text_surf = pygame.Surface((outline_w, outline_h), pygame.SRCALPHA)
            self.text_surf.blit(outline_surf, (1, 1))
            self.text_surf.blit(textobj, (0, 0))
            
            self.surface.blit(self.text_surf, textrect)
        else:
            self.surface.blit(textobj, textrect)

class IMGButton(GUI):
    def __init__(self, type:str="close", x=0, y=0) -> None:
        super().__init__(x=x, y=y)
        mixer.init()
        
        self.imgrect = button_hashed[type]["active"].get_rect()
        self.rect = self.rect = pygame.Rect(x, y, self.imgrect.width, self.imgrect.height)
        
        self.active_image = button_hashed[type]["active"]
        self.inactive_image = button_hashed[type]["inactive"]
        self.image = self.inactive_image
        
        self.is_hovered = False
        self.collide_sound_played = False
    
    def draw(self):
        self.surface.blit(self.image, self.rect)
    
    def collide_sound(self, sound: mixer.Sound):
        if self.is_collided() and self.collide_sound_played == False:
            vol = config.getint("AUDIO", "SFX_VOLUME") / 100
            sound.set_volume(vol)
            sound.play()
            self.collide_sound_played = True
        elif not self.is_collided() and self.collide_sound_played == True:
            self.collide_sound_played = False
                
    def set_hover(self):
        if self.is_collided():
            self.image = self.active_image
        elif not self.is_collided():
            self.image = self.inactive_image 

class TextButton(IMGButton):
    def __init__(self, text, font_size:int=50, type: str="button", x=0, y=0) -> None:
        super().__init__(x=x, y=y)
        
        self.imgrect = text_button_hashed[type]["active"].get_rect()
        self.rect = self.rect = pygame.Rect(x, y, self.imgrect.width, self.imgrect.height)
        
        self.active_image = text_button_hashed[type]["active"]
        self.inactive_image = text_button_hashed[type]["inactive"]
        self.image = self.inactive_image
    
        self.top_rect = self.rect.copy()
        self.bottom_rect = self.rect.copy()
        self.bottom_color = "#354B5E"
        
        self.adjust_texty = 10
        self.text = text
        self.text_color = "#FFFFFF"
        self.outline_color = "#FF9600"
        self.font_size = font_size
        self.font = pygame.font.Font(FONT, font_size)
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.is_hovered = False
        self.collide_sound_played = False
        self.elevation = 0
        self.dynamic_elevation = 0
    
    def draw(self):
        outline_surf = self.font.render(self.text, True, self.outline_color)
        outline_w, outline_h = outline_surf.get_size()
        
        self.top_rect.y = self.rect.y - self.dynamic_elevation
        self.text_rect.center = (self.top_rect.centerx, self.top_rect.centery - self.adjust_texty)
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        pygame.draw.rect(self.surface, self.bottom_color, self.bottom_rect, border_radius=12)
        
        self.surface.blit(self.image, self.top_rect)
        
        # Create a text_surf with an outline
        self.text_surf = pygame.Surface((outline_w, outline_h), pygame.SRCALPHA)
        self.text_surf.blit(outline_surf, (1, 1))  # Offset by (1, 1) for the outline effect
        self.text_surf.blit(self.font.render(self.text, True, self.text_color), (0, 0))
        
        # Now, blit the text_surf onto the button's surface
        self.surface.blit(self.text_surf, self.text_rect)

    def set_elevate(self, elevation: int = 5):
        self.elevation = elevation
        if self.clicked():
            self.dynamic_elevation = 0
        else:
            self.dynamic_elevation = self.elevation

class RangeSlider(GUI):
    def __init__(self, min_value: int=0, max_value: int=100,
                 start_value:int=None, x: int=10, y: int=10, 
                 range_width: int=700, range_height: int=20,
                 show_min_max: bool=False, callback: callable=None
        ) -> None:
        
        super().__init__(x=x, y=y)
        
        self.callback = callback
        
        self.dragging = False
        self.play_sound_after_drag = False
        
        self.min_value = min_value
        self.max_value = max_value
        
        self.range_width = range_width
        self.range_height = range_height
        
        self.gauge_image = pygame.transform.scale(range_slider_hashed["bar"], (300, 32))
        self.button_image = pygame.transform.scale(range_slider_hashed["btn"], (40, 40))
        
        self.button_size = 40

        self.font = pygame.font.Font(FONT, 40)
        
        self.show_min_max = show_min_max
        self.text_color = "#FFFFFF"

        if start_value is not None:
            self.value = start_value
            self.thumb_position = self.x + int((start_value - min_value) / (max_value - min_value) * range_width)
        else:
            self.value = min_value
            self.thumb_position = x
        

    def draw(self):
        # Draw the green fill rectangle
        fill_width = self.thumb_position - self.x
        pygame.draw.rect(self.surface, (0, 255, 0), (self.x+5, self.y - (self.range_height // 2 - 5), fill_width, self.range_height))

        # Draw the custom slider image
        self.surface.blit(self.gauge_image, (self.x, self.y - self.range_height // 2))
        self.surface.blit(self.button_image, (self.thumb_position - self.button_image.get_width() // 2, self.y - (self.button_image.get_height() // 2 - 5)))

        if self.show_min_max:
            min_label = self.font.render(str(self.min_value), True, self.text_color)
            max_label = self.font.render(str(self.max_value), True, self.text_color)
            min_label_width = min_label.get_width()
            max_label_width = max_label.get_width()
            self.surface.blit(min_label, (self.x - min_label_width // 2, self.y + 20))
            self.surface.blit(max_label, (self.x + self.range_width - max_label_width // 2, self.y + 20))
        
        if self.dragging:
            value_label = self.font.render(str(self.value), True, self.text_color)
            value_label_width = value_label.get_width()
            value_label_height = value_label.get_height()

            label_y = self.y - self.range_height // 2 - value_label_height - 5
            self.surface.blit(value_label, (self.thumb_position - value_label_width // 2, label_y))
    
    def update(self):
        if self.dragging:
            self.thumb_position = min(max(pygame.mouse.get_pos()[0], self.x), self.x + self.range_width)
            self.value = int((self.thumb_position - self.x) / self.range_width * (self.max_value - self.min_value) + self.min_value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.thumb_position - self.button_size // 2 <= mouse_x <= self.thumb_position + self.button_size // 2 and self.y - self.button_size // 2 <= mouse_y <= self.y + self.button_size // 2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            if self.callback:
                self.callback(self.value)
            if self.play_sound_after_drag:
                GUI.clicked_sound(SOUND_UISELECT)

class ToggleButton(GUI):
    def __init__(self, x, y, start_state: bool=False, callback: callable=None) -> None:
        super().__init__(x=x, y=y)
        
        self.is_on = start_state
        self.callback = callback
        
        self.state = start_state
        self.frame_img = pygame.transform.scale(toggle_hashed["rect"], (64, 64))
        self.on_img = pygame.transform.scale(toggle_hashed["on"], (45, 45))

        self.rect_frame = self.frame_img.get_rect(topleft=(x, y))
        
    def draw(self):
        self.surface.blit(self.frame_img, self.rect_frame)
        if self.is_on:
            self.surface.blit(self.on_img, (self.rect_frame.x + 10, self.rect_frame.y + 10))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                if self.callback:
                    self.callback(self.is_on)

class Selector(GUI):
    def __init__(self, tracks: iter, start_index: int=0, 
                 width=220, height=50, x=0, y=0, callback: callable=None
        ) -> None:
        
        super().__init__(width, height, x, y)
        
        self.callback = callback
        
        self.tracks = tracks
        self.current_index = start_index
        
        self.uifont = pygame.font.Font(FONT_ICON, 40)
        self.font = pygame.font.Font(FONT, 40)
        
        self.text_color = "#FFFFFF"
        
        self.left_arrow_rect = pygame.Rect(x - 50, y, 50, height)
        self.right_arrow_rect = pygame.Rect(x + width, y, 50, height)
    
    def draw(self):
        current_track_name = self.tracks.name(self.current_index)
        track_text = self.font.render(current_track_name, True, self.text_color)
        text_rect = track_text.get_rect(center=self.rect.center)
        self.surface.blit(track_text, text_rect)

        left_arrow = self.uifont.render("\ue5e0", True, self.text_color)
        left_arrow_rect = left_arrow.get_rect(center=self.left_arrow_rect.center)
        self.surface.blit(left_arrow, left_arrow_rect)

        right_arrow = self.uifont.render("\ue5e1", True, self.text_color)
        right_arrow_rect = right_arrow.get_rect(center=self.right_arrow_rect.center)
        self.surface.blit(right_arrow, right_arrow_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.left_arrow_rect.collidepoint(event.pos):
                self.current_index = (self.current_index - 1) % len(self.tracks)
            elif self.right_arrow_rect.collidepoint(event.pos):
                self.current_index = (self.current_index + 1) % len(self.tracks)
            if self.callback and self.left_arrow_rect.collidepoint(event.pos) or self.right_arrow_rect.collidepoint(event.pos):
                self.callback(self.current_index)

class YesNoPopup(GUI):
    def __init__(self, width=250, height=50, x=0, y=0) -> None:
        super().__init__(width, height, x, y)
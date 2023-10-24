import pygame
from pygame.locals import *
from pygame import mixer
from settings import config

class GameState:
    """
    Base class for all game states
    
    Attributes:
    -----------
    game : Game
        The game object that this state belongs to
    surface : pygame.Surface
        The surface object of the game window
    display_info : pygame.DisplayInfo
        The display information object of the game window
    surf_width : int
        The width of the game window
    surf_height : int
        The height of the game window
    clock : pygame.time.Clock
        The clock object used to control the game's frame rate
    fps : int
        The target frame rate of the game
    """
    def __init__(self, game):
        self.game = game
        self.surface = pygame.display.get_surface()
        self.display_info = pygame.display.Info()
        self.surf_width = self.display_info.current_w
        self.surf_height = self.display_info.current_h
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def handle_events(self, events):
        """
        Handles events for the GameState object
        
        Parameters:
        -----------
        events : list
            A list of pygame events to be handled
        """
        pass

    def update(self):
        """
        Updates the GameState object
        """
        self.display_info = pygame.display.Info()
        self.surf_width = self.display_info.current_w
        self.surf_height = self.display_info.current_h
    
    def render(self):
        """
        Renders the GameState object
        """
        pass
    
    def play_sound(self, sound:str, type:str):
        """
        Plays a sound effect or music
        
        Parameters:
        -----------
        sound : str
            The path to the sound file to be played
        type : str
            The type of sound to be played, either 'music' or 'sfx'
        """
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
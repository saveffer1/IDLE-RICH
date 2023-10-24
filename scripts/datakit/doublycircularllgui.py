from pygame import mixer
from .doublycircularll import DCList, Node

class SoundNode(Node):
    def __init__(self, data=None) -> None:
        super().__init__(data)
        try:
            self.music = mixer.Sound(data)
        except:
            raise ValueError("Data must be a valid path to a sound file")
        
        self.music_path = data  

class MusicList(DCList):
    def __getitem__(self, index: int):
        if index < -1 or index >= self.length:
            raise IndexError("DCList index out of bounds")
        
        if index == -1:
            return self.tail.music
        elif index == 0:
            return self.head.music
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            return current.music
    
    def path(self, index: int):
        if index < -1 or index >= self.length:
            raise IndexError("DCList index out of bounds")
        
        if index == -1:
            return self.tail.data
        elif index == 0:
            return self.head.data
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            return current.data
    
    def name(self, index: int):
        return self.path(index).split('/')[-1].split('.')[0]

class LanguageList(DCList):
    def name(self, index:int):
        return self.__getitem__(index)
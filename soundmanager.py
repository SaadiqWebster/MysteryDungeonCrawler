import pygame, os

class SoundManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sounds = self.load_sounds(self.file_path)
        self.music_volume = 50 # between 0 and 100
        self.sfx_volume = 50 # between 0 and 100
     
    def load_sounds(self, file_path):
        sounds = {}
        files = os.listdir(file_path)
        for f in files:
            sounds[f] = pygame.mixer.Sound(file_path+f)
        return sounds
    
    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume/100)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume

    def play_music(self, music, fade_in=0):
        pygame.mixer.music.load(self.file_path+music)
        pygame.mixer.music.set_volume(self.music_volume/100)
        pygame.mixer.music.play(-1, 0, fade_in)

    def play_sfx(self, sound):
        self.sounds[sound].set_volume(self.sfx_volume/100)
        self.sounds[sound].play()

    def pause_music(self):
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        pygame.mixer.music.unpause()

    def stop_music(self, fade_out=0):
        pygame.mixer.music.fadeout(fade_out)


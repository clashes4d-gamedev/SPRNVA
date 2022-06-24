from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
pygame.mixer.init()


class Audio:
    """Wrapper around pygame.mixer"""
    def __init__(self, audio: str, volume=1) -> None:
        pygame.mixer.init()
        self.audio = audio
        self.sound = pygame.mixer.music.load(self.audio)
        self.set_volume(volume)

    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
    
    def restart(self):
        pygame.mixer.music.rewind()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def get_playback_time(self):
        return pygame.mixer.music.get_pos()

    def get_length(self):
        sound = pygame.mixer.Sound(self.audio)
        return sound.get_length()
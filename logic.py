import pygame
class WatchValue:
    def __init__(self, value: any):
        self.value = value

    def check_change(self, value: any):
        if self.value != value:
            return False
        else:
            return True

class DeltaTime:
    def __init__(self):
        self.get_ticksLastFrame = 0
    def count(self):
        t = pygame.time.get_ticks()
        deltatime = (t - self.get_ticksLastFrame) / 1000.0
        self.get_ticksLastFrame = t
        return deltatime
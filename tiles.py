from os import path, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from .vector import Vector2D

class Tile:
    def __init__(self, win: pygame.Surface, pos: Vector2D, size: Vector2D, img='', type='0'):
        self.win = win
        self.collider = pygame.Rect(pos.x, pos.y, size.x, size.y)
        self.type = type
        self.img = img if img != '' and path.isfile(img) else path.join(path.split(__file__)[0], path.join('res', 'missing_texture.png'))
        self.loaded_img = pygame.image.load(self.img).convert_alpha()

    def draw(self):
        self.win.blit(self.loaded_img, (self.collider.x, self.collider.y))
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import os
from .vector import Vector2D

#TODO fix tiles scrolling by or not blitting in the right spot
class Spritesheet:
    def __init__(self, filepath: str, cols: int, rows: int) -> None:
        self.current_spritesheet = pygame.image.load(filepath) if filepath != '' and os.path.isfile(filepath) else None
        self.cols = cols
        self.rows = rows
        self.total = self.rows * self.cols

        if self.current_spritesheet is not None:
            self.spritesheet_rect = self.current_spritesheet.get_rect()
            self.tile_width = self.spritesheet_rect.width / self.cols
            self.tile_height = self.spritesheet_rect.height / self.rows
            self.tile_center = Vector2D(self.tile_width/2, self.tile_height/2)
            self.tiles = list([(index % self.cols * self.tile_width, index / self.cols * self.tile_height, self.tile_width, self.tile_height) for index in range(self.total)])
        else:
            raise FileNotFoundError(f'No file named {filepath}')

    def draw(self, win, x: int, y: int, tile_index: int):
        win.blit(self.current_spritesheet, (x, y), self.tiles[tile_index])

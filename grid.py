from os import path
from .vector import Vector2D
import pygame

supp_img_formats = ['PNG', 'JPG', 'BMP']


class IsoImageLoadError(Exception):
    def __init__(self):
        pass

class Tile:
    def __init__(self, x: int, y: int, width: int, height: int, color=(255, 0, 0), img='', color_key=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.img = pygame.image.load(self._import_img(img)).convert_alpha() if img != '' else pygame.image.load(path.join(path.split(__file__)[0], path.join('res', 'missing_texture.png'))).convert_alpha()
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)

    def _import_img(self, img: str):
        if img[-3:].upper() in supp_img_formats and path.isfile(img):
            return img
        else:
            raise IsoImageLoadError()

    def draw(self, win: pygame.Surface):
        if self.img is not None or type(self.img) == str():
            win.blit(self.img, (self.collider.x, self.collider.y))
        else:
            pygame.draw.rect(win, self.color, self.collider)


class IsoGrid:
    def __init__(self, x: int, y: int, rows: int, cols: int, tile_size: tuple, img=''):
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.tile_width = tile_size[0]
        self.tile_height = tile_size[1]

        self.i_hat = Vector2D(1 * (self.tile_width/2),
                              0.5 * (self.tile_height / 2))

        self.j_hat = Vector2D(-1 * (self.tile_width/2),
                              0.5 * (self.tile_height / 2))

        self.img = self._import_img(img) if img != '' else None
        self.tiles = []
        self._generate_grid()

    def _import_img(self, img: str):
        if img[-3:].upper() in supp_img_formats and path.isfile(img):
            return img
        else:
            raise IsoImageLoadError()

    def _generate_grid(self):
        x, y = 0, 0
        for row in range(self.rows):
            x = 0
            y_row = []
            for col in range(self.cols):
                x_coords, y_coords = self.ISO_toXY(x, y)
                curr_tile = Tile(x_coords + self.x, y_coords + self.y, self.tile_width, self.tile_height, img=self.img if self.img is not None else '')
                y_row.append(curr_tile)
                x += 1
            self.tiles.append(y_row)
            y += 1

    def ISO_toXY(self, x, y):
        coords = Vector2D(x * self.i_hat.x + y * self.j_hat.x,
                          x * self.i_hat.y + y * self.j_hat.y)
        return coords.x - (self.tile_width/2), int(coords.y)

    def XY_toISO(self, Sx, Sy):
        Sx = Sx - self.x
        Sy = Sy - self.y
        det = (1 / (self.i_hat.x * self.j_hat.y - self.j_hat.x * self.i_hat.y))

        a = det * self.j_hat.y
        b = det * -self.j_hat.x
        c = det * -self.i_hat.y
        d = det * self.i_hat.x

        return int((Sx * a) + (Sy * b)), int((Sx * c) + (Sy * d))

    def get_tiles(self):
        return self.tiles

    def draw(self, win: pygame.Surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(win)

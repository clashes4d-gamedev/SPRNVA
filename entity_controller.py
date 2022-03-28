import pygame
from .vector import Vector

class Player:
    def __init__(self, win, pos: Vector, size: Vector, img='', color=(255, 0, 0)):
        self.win = win
        self.x = pos.x
        self.y = pos.y
        self.width = size.x
        self.height = size.y
        self.color = color
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface((self.collider.width, self.collider.height))
        self.img = pygame.image.load(img).convert_alpha() if img != '' else img

    def draw(self):
        if self.img == '':
            self.surf.fill(self.color)
        else:
            self.surf.blit(self.img, (0, 0))
        self.win.blit(self.surf, (self.collider.x, self.collider.y))

    def check_collisions(self, tiles):
        collisions = []
        for tile in tiles:
            if self.collider.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move(self, tiles, vel, x=False, y=False, minus_y=False, minus_x=False, boundaries=True):
        if vel >= 0:
            if boundaries:
                if x is not False and (self.collider.x + self.collider.width) <= self.win.get_width():
                    self.collider.x += vel.x
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.right = tile.left

                elif y is not False and (self.collider.y + self.collider.height) <= self.win.get_height():
                    self.collider.y += vel.y
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.bottom = tile.top

                elif minus_x is not False and self.collider.x >= 0:
                    self.collider.x -= vel.x
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.left = tile.right

                elif minus_y is not False and self.collider.y >= 0:
                    self.collider.y -= vel.y
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.top = tile.bottom

                else:
                    return
            else:
                if x is not False:
                    self.collider.x += vel.x
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.right = tile.left

                elif y is not False:
                    self.collider.y += vel.y
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.bottom = tile.top

                elif minus_x is not False:
                    self.collider.x -= vel.x
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.left = tile.right

                elif minus_y is not False:
                    self.collider.y -= vel.y
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.top = tile.bottom

                else:
                    return
        else:
            return

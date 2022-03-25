import pygame

class Crate:
    def __init__(self, win, x, y, width, height, img='', color=(64, 6, 64)):
        self.win = win
        self.x = x
        self.y = y
        self.img = img
        self.width = width
        self.height = height
        self.color = color
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.collider.width, self.collider.height))
        self.context_options = ['Open', 'Destroy', 'Pick Up']

        if self.img == '':
            self.surface.fill(self.color)
        else:
            self.img = pygame.image.load(img)
            self.img.convert()
            self.surface.blit(self.img, (0, 0))

    def check_collision(self, rect):
        if pygame.Rect.colliderect(self.collider, rect):
            return True
        else:
            return False

    def draw(self):
        self.win.blit(self.surface, (self.collider.x, self.collider.y))
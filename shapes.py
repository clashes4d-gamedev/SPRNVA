import pygame
from pygame import gfxdraw
from .vector import Vector

class Draw:
    def __init__(self, win: pygame.Surface):
        self.win = win

    def pixel(self, pos: Vector, color: tuple):
        gfxdraw.pixel(self.win, int(pos.x), int(pos.y), color)

    def draw_aacircle(self, pos: Vector, color, radius):
        """Draws an antialiased circle on a Pygame Surface."""
        pygame.draw.circle(self.win, color, (pos.x, pos.y), radius)
        gfxdraw.aacircle(self.win, int(pos.x), int(pos.y), radius, color)

    def draw_aaNgon(self, color, points):
        """Draws an antialiased Polygon on a Pygame Surface"""
        pygame.draw.polygon(self.win, color, points)
        gfxdraw.aapolygon(self.win, points, color)

    def draw_gradient_circle(self, pos: Vector, color: tuple, radius: int, steps: int, getting_darker=False, getting_brighter=False):
        """Draws a circular gradient."""
        r, g, b = color

        if steps >= radius:
            steps = radius

        for i in range(steps):
            if not getting_darker and not getting_brighter:
                pass
            elif getting_darker and getting_brighter:
                pass
            else:
                if getting_darker == True:
                    if r != 0:
                        r -= 1
                    else:
                        r = 0

                    if g != 0:
                        g -= 1
                    else:
                        g = 0

                    if b != 0:
                        b -= 1
                    else:
                        b = 0

                elif getting_brighter == True:
                    if r != 255:
                        r += 1
                    else:
                        r = 255

                    if g != 255:
                        g += 1
                    else:
                        g = 255

                    if b != 255:
                        b += 1
                    else:
                        b = 255

            color = (r, g, b)
            curr_radius = int(radius - i)
            self.draw_aacircle(pos, color, curr_radius)
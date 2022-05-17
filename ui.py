import pygame
import math
import keyboard
from .vector import Vector
from .logic import *
from pygame.locals import *

class TextRenderer:
    def __init__(self, win, x, y, text, font, size, color):
        pygame.font.init()
        txt = pygame.font.SysFont(font, size)
        txt_surf = txt.render(text, False, color)
        text_dim = txt.size(text)
        win.blit(txt_surf, (x - text_dim[0]/2, y - text_dim[1]/2))
        self.size = (txt_surf.get_width(), txt_surf.get_height())

#TODO Rewrite and Optimize this
class Button:
    def __init__(self, win, x, y, width, height, mouse, mouse_btns, btn, img_path='', btn_color=(255,255,255), btn_txt_color=(0,0,0), btn_txt_size=10, btn_font='Arial', btn_text='BTN'):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mouse = mouse
        self.mouse_btns = mouse_btns
        self.btn = btn
        self.img_path = img_path
        self.btn_color = btn_color
        self.btn_txt_color = btn_txt_color
        self.btn_txt_size = btn_txt_size
        self.btn_font = btn_font
        self.btn_text = btn_text
        self.button_collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_surf = pygame.Surface((self.button_collider.width, self.button_collider.height))

    def draw(self):
        if self.img_path != '':
            button_img = pygame.image.load(str(self.img_path), '.png').convert()
            button_img.set_colorkey((0,0,0))
            button_img = pygame.transform.scale(button_img, (self.button_surf.get_width(), self.button_surf.get_height()))
            self.button_surf.blit(button_img, (0,0))
        else:
            self.button_surf.fill(self.btn_color)
            TextRenderer(self.button_surf, self.button_surf.get_width()/2, self.button_surf.get_height()/2, self.btn_text, self.btn_font, self.btn_txt_size, self.btn_txt_color)
        self.win.blit(self.button_surf, (self.button_collider.x, self.button_collider.y))

        if pygame.Rect.collidepoint(self.button_collider, self.mouse[0], self.mouse[1]):
            if self.mouse_btns[self.btn]:
                return True
            else:
                return False
        else:
            return False


class SubMenu:
    def __init__(self, win, x: int, y: int, width: int, options: list, color: tuple, button_height=20) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.options = options
        self.color = color
        self.button_height = button_height
        self.collider = pygame.Rect(self.x, self.y, self.width, self.button_height*len(self.options))

    def get_dist_from_cursor(self, cursor):
        return math.sqrt(cursor[0]**2 + cursor[1]**2) - math.sqrt(self.y**2 + self.x**2)

    def draw(self, mouse):
        mouse_btns = pygame.mouse.get_pressed()
        if len(self.options) != 0:
            index = 0
            button_dir = dict()
            for option in self.options:
                active_button = self.button(self.win, self.x, self.y + (index * self.button_height), self.width, self.button_height,
                                            mouse, mouse_btns, 0, btn_color=(64, 64, 64), btn_txt_color=(255,255,255), btn_text=option, btn_txt_size=15)
                if active_button == True:
                    button_dir[index] = True
                else:
                    button_dir[index] = False
                index += 1
            return button_dir
        else:
            pass

class InputBox:
    def __init__(self, win: pygame.Surface, pos: Vector, size: Vector, border_thickness=3):
        self.win = win
        self.pos = pos
        self.size = size
        #self.collider = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.border = 1
        self.border_thickness = border_thickness
        self.focused = False
        self.value = ''
        self.surf = pygame.Surface((self.size.x, self.size.y))
        self.collider = self.surf.get_rect(topleft=(self.pos.x, self.pos.y))

    def update(self, m_btn: tuple, mouse=(0,0)):
        if mouse == (0, 0):
            mouse = pygame.mouse.get_pos()
        else:
            pass

        if self.collider.collidepoint(mouse[0], mouse[1]):
            if pygame.mouse.get_pressed() == m_btn:
                self.border = self.border_thickness
                self.focused = True
        else:
            if True in pygame.mouse.get_pressed():
                self.focused = False

    def get_input(self, events):
        """Call this before the event loop."""
        if self.focused:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE:
                        self.value += event.unicode

                    elif event.key == pygame.K_BACKSPACE and self.value != '':
                        self.value = self.value[:-1]

                    elif event.key == pygame.K_RETURN:
                        self.focused = False
        else:
            pass

    def draw(self, text_color=(255, 255, 255), color=(64, 64, 64), border_color=(20, 95, 255), border_radius=5):
        pygame.draw.rect(self.surf, color, (0, 0, self.collider.width, self.collider.height), border_radius=border_radius)
        if self.focused:
            pygame.draw.rect(self.surf, border_color, (0, 0, self.collider.width, self.collider.height), width=self.border, border_radius=border_radius)

        TextRenderer(self.surf, self.collider.width/2, self.collider.height/2, self.value, 'Arial', self.collider.height - 5, text_color)
        self.win.blit(self.surf, (self.collider.x, self.collider.y))

    def get_value(self):
        return self.value

class Card:
    def __init__(self, win, x, y, width, height, bg_color, rounded_corners=False, title_image=''):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.card_surf = pygame.Surface((self.collider.width, self.collider.height), pygame.SRCALPHA)
        self.bg_color = bg_color
        self.rounded_corners = rounded_corners
        self.border_radius = 10

        self.title_image = title_image
        self.got_title_img = False

        if self.title_image != '' and CheckPath(self.title_image).existance() and CheckPath(self.title_image).isfile():
            self.title_image = pygame.image.load(self.title_image).convert_alpha()
            self.title_image = pygame.transform.scale(self.title_image, (self.collider.width, self.collider.height/3))
            self.got_title_img = True

        self.font = 'Arial'
        self.text_color = (255, 255, 255)
        self.content_font_size = 10
        self.title_font_size = 20
        self.title = 'Title'
        self.content = ['This is some ordinary',
                        'card content to',              # This is like a really stupid way to do word wrapping but it works for now
                        'test if the card',
                        'supports word-wraoping.']
        self.content_surf = pygame.Surface((self.collider.width, self.collider.height * 2/3), pygame.SRCALPHA)
        self.content_surf_color = self.bg_color

    def draw(self):
        if self.rounded_corners:
            pygame.draw.rect(self.card_surf, self.bg_color, (0, 0, self.collider.width, self.collider.height), border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.card_surf, self.bg_color, (0, 0, self.collider.width, self.collider.height))

        if self.got_title_img:
            self.card_surf.blit(self.title_image, (0, 0), special_flags=pygame.BLEND_ADD)

        # Begin Drawing the content
        # Displaying the title
        TextRenderer(self.content_surf, self.content_surf.get_width()/2, self.content_surf.get_height() * 1/4, self.title, self.font, self.title_font_size, self.text_color)

        # Displaying the actual text is a bit more difficult because i have to implement word-wrapping somehow
        x, y = 0, self.content_surf.get_height() * 2 / 4
        for line in self.content:
            TextRenderer(self.content_surf, self.content_surf.get_width() / 2, y, line, self.font, self.content_font_size, self.text_color)
            y += 10

        self.card_surf.blit(self.content_surf, (0, self.collider.height/3), special_flags=pygame.BLEND_ALPHA_SDL2)
        self.win.blit(self.card_surf, (self.collider.x, self.collider.y))


def add_vignette(win: pygame.Surface, offset: int, color: tuple, alpha: int):
    """Draws a Vignette around the given coordinates.
       Returns a pygame Surface with the Vignette."""
    vignetten_surf = pygame.Surface((win.get_width(), win.get_height()))
    vignetten_surf.set_colorkey((255, 255, 255))
    vignetten_surf.set_alpha(alpha)
    vignetten_surf.fill(color)
    vignetten_rect = vignetten_surf.get_rect()
    vignetten_rect = pygame.Rect(vignetten_rect.x - (offset*8), vignetten_rect.y + offset*.03125, vignetten_rect.width + (offset*16), vignetten_rect.height - offset*.0625)
    pygame.draw.ellipse(vignetten_surf, (255, 255, 255), vignetten_rect)
    return vignetten_surf

SUPPORTED_UI_TYPES = [TextRenderer, Button, SubMenu, InputBox]

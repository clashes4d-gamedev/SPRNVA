import pygame
import math
import keyboard
from sys import exit
from os import path
from .vector import Vector
from .logic import *
from pygame.locals import *

class Window:
    def __init__(self, size: tuple, caption='THIS WINDOW WAS MADE WITH SPRNVA.', vsync=True, fps=60, resizable=False, fullscreen=False) -> None:
        self.size = size
        self.caption = caption
        self.fps = fps
        self.fullscreen = fullscreen
        self.resizable = resizable
        self.vsync = vsync
        self.clock = pygame.time.Clock()
        self.get_ticksLastFrame = 0

    def create(self) -> pygame.Surface:
        if self.resizable:
            if self.vsync:
                display = pygame.display.set_mode(self.size, pygame.RESIZABLE, vsync=1)
                pygame.display.set_caption(self.caption)
            else:
                display = pygame.display.set_mode(self.size, pygame.RESIZABLE)
                pygame.display.set_caption(self.caption)

        elif self.fullscreen:
            if self.vsync:
                display = pygame.display.set_mode(self.size, pygame.FULLSCREEN, vsync=1)
                pygame.display.set_caption(self.caption)
            else:
                display = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
                pygame.display.set_caption(self.caption)
        else:
            if self.vsync:
                display = pygame.display.set_mode(self.size, vsync=1)
                pygame.display.set_caption(self.caption)
            else:
                display = pygame.display.set_mode(self.size)
                pygame.display.set_caption(self.caption)
        return display

    def update(self, events, rects=None, cap_framerate=True) -> None:
        """If rects is set this function will only update parts of the screen."""
        if events is not None:
            for event in events:
                if event.type == pygame.QUIT:
                    print('exit')
                    pygame.quit()
                    exit()

                if event.type == pygame.VIDEORESIZE:
                    self.size = (event.w, event.h)
        
        else:
            raise ValueError('events must be given and should be a list of current pygame events.')
        
        if rects is not None:
            if type(rects) == list():
                pygame.display.update(rects)
            elif type(rects) == pygame.Rect:
                pygame.display.update(rects)
            elif type(rects) == None:
                pass
            else:
                raise TypeError('rects argument must be of type pygame.Rect or list containing multiple pygame.Rect objects.')
        else:
            pygame.display.flip()

        if cap_framerate:
            self.clock.tick(self.fps)

    def get_fps(self, integer=False) -> float:
        if integer:
            return int(self.clock.get_fps())
        else:
            return self.clock.get_fps()

    def get_dt(self) -> float:
        t = pygame.time.get_ticks()
        deltatime = (t - self.get_ticksLastFrame) / 1000.0
        self.get_ticksLastFrame = t
        return deltatime + 1

class TextRenderer:
    def __init__(self, win, x, y, text, font, size, color, font_file=False):
        pygame.font.init()
        if font_file is False:
            txt = pygame.font.SysFont(font, size)
            txt_surf = txt.render(text, False, color)
            text_dim = txt.size(text)
            win.blit(txt_surf, (x - text_dim[0]/2, y - text_dim[1]/2))
            self.size = (txt_surf.get_width(), txt_surf.get_height())
        else:
            txt = pygame.font.Font(font, size)
            txt_surf = txt.render(text, False, color)
            text_dim = txt.size(text)
            win.blit(txt_surf, (x - text_dim[0]/2, y - text_dim[1]/2))
            self.size = (txt_surf.get_width(), txt_surf.get_height())


class Button:
    def __init__(self, win, x, y, width, height, color, img='', font_color=(255, 255, 255),
                 font='Arial', font_size=10, text='Text', use_sys_font=True, mb_pressed=(True, False, False),
                 rounded_corners=False, border_radius=10, high_precision_mode=False):
        """Initilizes a Button. (if img!='' or rounded_corners=True it is recommended to use high precision mode for collision detection.)"""
        self.win = win
        self.collider = pygame.Rect(x, y, width, height)
        self.color = color

        if img != '' and CheckPath().existance() and CheckPath().isfile():
            self.img = pygame.image.load(img).convert()
            self.img = pygame.transform.scale(self.img, (self.collider.width, self.collider.height))
        else:
            self.img = ''

        self.font_color = font_color
        self.font = font
        self.font_size = font_size
        self.use_sys_font = use_sys_font
        self.text = text
        self.rounded_corners = rounded_corners
        self.border_radius = border_radius
        self.high_precision = high_precision_mode
        self.state = False
        self.hover_state = False
        self.mb_pressed = mb_pressed

    def draw(self):
        """Draws the Button on a Surface."""
        button_surf = pygame.Surface((self.collider.width, self.collider.height))

        if self.img == '':
            if self.rounded_corners:
                pygame.draw.rect(button_surf, self.color, pygame.Rect(0, 0, self.collider.width, self.collider.height), border_radius=self.border_radius)
            else:
                pygame.draw.rect(button_surf, self.color, pygame.Rect(0, 0, self.collider.width, self.collider.height))
        else:
            button_surf.blit(self.img, (0, 0))

        if self.use_sys_font:
            TextRenderer(button_surf, self.collider.width//2, self.collider.height//2, self.text, self.font, self.font_size, self.font_color)
        else:
            TextRenderer(button_surf, self.collider.width//2, self.collider.height//2, self.text, self.font, self.font_size, self.font_color, font_file=True)

        self.win.blit(button_surf, (self.collider.x, self.collider.y))

        if self.high_precision:
            mouse = pygame.mouse.get_pos()
            ms_collider = pygame.Surface((1,1))
            ms_collider.set_alpha(0)
            ox = (self.win.get_width()/2) - self.collider.center[0]
            oy = (self.win.get_height()/2) - self.collider.center[1]

            button_mask = pygame.mask.from_surface(button_surf)
            cs_mask = pygame.mask.from_surface(ms_collider)
            cs_mask.fill()

            offset = (mouse[0] - self.collider.x, mouse[1] - self.collider.y)
            result = button_mask.overlap(cs_mask, offset)

            if result:
                self.hover_state = True
                if pygame.mouse.get_pressed() == self.mb_pressed:
                    self.state = True
                else:
                    self.state = False
            else:
                self.hover_state = False
                self.state = False

        else:
            mouse = pygame.mouse.get_pos()
            if self.collider.collidepoint(mouse[0], mouse[1]):
                self.hover_state = True
                if pygame.mouse.get_pressed() == self.mb_pressed:
                    self.state = True
                else:
                    self.state = False
            else:
                self.hover_state = False
                self.state = False

    def get_state(self, hover=False):
        """Returns the state of the Button either Clicked(True) or Not Clicked(False). \nIf hover is True this returns the hoverstate."""
        if hover:
            return self.hover_state
        else:
            return self.state

class SubMenu:
    # TODO rewrite this to fit to the new button class
    def __init__(self, win, x: int, y: int, width: int, options: list, color: tuple, button_height=20) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.options = options
        self.color = color
        self.button_height = button_height
        self.collider = pygame.Rect(self.x, self.y, self.width, self.button_height*len(self.options))

    def get_hover(self):
        mouse = pygame.mouse.get_pos()
        if self.collider.collidepoint(mouse[0], mouse[1]):
            return True
        else:
            return False

    def get_dist_from_cursor(self, cursor):
        return math.sqrt(cursor[0]**2 + cursor[1]**2) - math.sqrt(self.y**2 + self.x**2)

    def draw(self):
        mouse_btns = pygame.mouse.get_pressed()
        if len(self.options) != 0:
            index = 0
            button_dir = dict()
            for option in self.options:
                active_button = Button(self.win, self.x, self.y, self.width, self.button_height, self.color, text=str(option))
                active_button.draw()
                if active_button == True:
                    button_dir[index] = True
                else:
                    button_dir[index] = False
                index += 1
            return button_dir
        else:
            pass

class InputBox:
    def __init__(self, win: pygame.Surface, pos: Vector, size: Vector, border_thickness=3, placeholder_text='', placeholder_color=(84, 84, 84)):
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
        self.placeholder_text = placeholder_text
        self.placeholder_color = placeholder_color

    def update(self, m_btn: tuple, mouse=(0, 0)):
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
        else:
            if self.value == '':
                TextRenderer(self.surf, self.collider.width/2, self.collider.height/2, self.placeholder_text, 'Arial', self.collider.height - 5, self.placeholder_color)

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


def add_vignette(win: pygame.Surface, x, y, offset: int, color: tuple, alpha: int) -> pygame.Surface:
    """Draws a Vignette around the given coordinates.
       Returns a pygame Surface with the Vignette."""
    # TODO Rewrite this
    vignetten_surf = pygame.Surface((win.get_width(), win.get_height()))
    vignetten_surf.set_colorkey((255, 255, 255))
    vignetten_surf.set_alpha(alpha)
    vignetten_surf.fill(color)
    vignetten_rect = vignetten_surf.get_rect()
    vignetten_rect = pygame.Rect(vignetten_rect.x - (offset*8), vignetten_rect.y + offset*.03125, vignetten_rect.width + (offset*16), vignetten_rect.height - offset*.0625)
    pygame.draw.ellipse(vignetten_surf, (255, 255, 255), vignetten_rect)
    win.blit(vignetten_surf, (x, y))
    #return vignetten_surf

SUPPORTED_UI_TYPES = [TextRenderer, Button, SubMenu, InputBox, Card]

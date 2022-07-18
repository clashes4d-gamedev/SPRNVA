from os import path, environ, getcwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
import cv2
import json
from typing import Optional
from sys import exit
from .vector import Vector2D
from .logic import *
from scipy.interpolate import interp1d


class Window:
    def __init__(self, size: tuple, caption='THIS WINDOW WAS MADE WITH SPRNVA.', vsync=True, fps=60, resizable=False, fullscreen=False, icon_path='', splash_vid=True) -> None:
        self.size = size
        self.caption = caption
        self.fps = fps
        self.fullscreen = fullscreen
        self.resizable = resizable
        self.vsync = vsync
        self.splash_vid = splash_vid
        self.icon_path = icon_path if icon_path != '' and path.isfile(icon_path) else path.join(path.split(__file__)[0], path.join('res', 'missing_texture.png'))
        self.clock = pygame.time.Clock()
        self.get_ticksLastFrame = 0
        self.win = self.create()

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

        icon = pygame.image.load(self.icon_path).convert_alpha()
        pygame.display.set_icon(icon)
        return display

    def update(self, events, rects=None, cap_framerate=True) -> None:
        """If rects is set this function will only update parts of the screen."""
        if self.splash_vid:
            wdir = path.join(path.split(__file__)[0], 'res')
            video = cv2.VideoCapture(path.join(wdir, 'SPRNVA_SPLASH.mp4'))
            success, video_image = video.read()
            while success:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                success, video_image = video.read()

                if success:
                    video_surf = pygame.image.frombuffer(
                        video_image.tobytes(), video_image.shape[1::-1], "BGR")
                    video_surf = pygame.transform.scale(video_surf, self.size)
                    self.win.blit(video_surf, (0, 0))

                pygame.display.flip()
            self.splash_vid = False

        if events is not None:
            for event in events:
                if event.type == pygame.QUIT:
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
            elif type(rects) is None:
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

    def get_size(self) -> Vector2D:
        return Vector2D(self.size[0], self.size[1])

    def get_dt(self) -> float:
        t = pygame.time.get_ticks()
        deltatime = (t - self.get_ticksLastFrame) / 1000.0
        self.get_ticksLastFrame = t
        return deltatime + 1

    def get_keys(self):
        return pygame.key.get_pressed()

    def get_mouse(self):
        mouse = pygame.mouse.get_pos()
        return Vector2D(mouse[0], mouse[1])

    def get_events(self):
        return pygame.event.get()

    def get_missing_texture_path(self):
        return path.join(path.split(__file__)[0], path.join('res', 'missing_texture.png'))

class TextRenderer:
    def __init__(self, win: pygame.Surface, x: float, y: float, text: str, font: str, size: int, color: tuple, font_file=False, centered=True):
        self.win = win
        self.x = x
        self.y = y
        self.centered = centered
        self.text = text
        self.font = font
        self.text_size = size
        self.color = color
        self.font_file = font_file
        pygame.font.init()

    def draw(self):
        if self.font_file is False:
            self.txt = pygame.font.SysFont(self.font, self.text_size)
            self.txt_surf = self.txt.render(self.text, False, self.color)
            self.text_dim = self.txt.size(self.text)
            if self.centered:
                self.win.blit(self.txt_surf, (self.x - self.text_dim[0]/2, self.y - self.text_dim[1]/2))
                self.size = (self.txt_surf.get_width(), self.txt_surf.get_height())
            else:
                self.win.blit(self.txt_surf, (self.x, self.y))
                self.size = (self.txt_surf.get_width(), self.txt_surf.get_height())
        else:
            self.txt = pygame.font.Font(self.font, self.text_size)
            self.txt_surf = self.txt.render(self.text, False, self.color)
            self.text_dim = self.txt.size(self.text)
            if self.centered:
                self.win.blit(self.txt_surf, (self.x - self.text_dim[0] / 2, self.y - self.text_dim[1] / 2))
                self.size = (self.txt_surf.get_width(), self.txt_surf.get_height())
            else:
                self.win.blit(self.txt_surf, (self.x, self.y))
                self.size = (self.txt_surf.get_width(), self.txt_surf.get_height())


class Button:
    def __init__(self, win, x, y, width, height, color, img='', font_color=(255, 255, 255),
                 font='Arial', font_size=10, text='Text', use_sys_font=True, mb_pressed=(True, False, False),
                 rounded_corners=False, border_radius=10, high_precision_mode=False):
        """Initilizes a Button. (if img!='' or rounded_corners=True it is recommended to use high precision mode for collision detection.)"""
        self.win = win
        self.collider = pygame.Rect(x, y, width, height)
        self.color = color

        if img != '' and CheckPath(img).existance() and CheckPath(img).isfile():
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
        # TODO known issues: mac specific: -mouse hover counts sometimes as mouse click
        button_surf = pygame.Surface((self.collider.width, self.collider.height))

        if self.img == '':
            if self.rounded_corners:
                pygame.draw.rect(button_surf, self.color, pygame.Rect(0, 0, self.collider.width, self.collider.height), border_radius=self.border_radius)
            else:
                pygame.draw.rect(button_surf, self.color, pygame.Rect(0, 0, self.collider.width, self.collider.height))
        else:
            button_surf.blit(self.img, (0, 0))

        if self.use_sys_font:
            TextRenderer(button_surf, self.collider.width//2, self.collider.height//2, self.text, self.font, self.font_size, self.font_color).draw()
        else:
            TextRenderer(button_surf, self.collider.width//2, self.collider.height//2, self.text, self.font, self.font_size, self.font_color, font_file=True).draw()

        self.win.blit(button_surf, (self.collider.x, self.collider.y))

        if self.high_precision:
            mouse = pygame.mouse.get_pos()
            ms_collider = pygame.Surface((1, 1))
            ms_collider.set_alpha(0)

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
    def __init__(self, win: pygame.Surface, pos: Vector2D, size: Vector2D, border_thickness=3, placeholder_text='', placeholder_color=(84, 84, 84),
                 text_color=(255, 255, 255), color=(64, 64, 64), border_color=(20, 95, 255), border_radius=5):
        self.win = win
        self.pos = pos
        self.size = size
        self.border = 1
        self.border_thickness = border_thickness
        self.focused = False
        self.value = ''
        self.surf = pygame.Surface((self.size.x, self.size.y), flags=pygame.SRCALPHA)
        self.surf.convert_alpha()
        self.collider = self.surf.get_rect(topleft=(self.pos.x, self.pos.y))
        self.placeholder_text = placeholder_text
        self.placeholder_color = placeholder_color
        self.text_color = text_color
        self.color = color
        self.border_color = border_color
        self.border_radius = border_radius

    def update(self, events, mouse=(0, 0)):
        if mouse == (0, 0):
            mouse = pygame.mouse.get_pos()
        else:
            pass

        if self.collider.collidepoint(mouse[0], mouse[1]):
            if pygame.mouse.get_pressed() == (True, False, False):
                self.border = self.border_thickness
                self.focused = True
        else:
            if True in pygame.mouse.get_pressed():
                self.focused = False

        self.get_input(events)

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

    def draw(self):
        pygame.draw.rect(self.surf, self.color, (0, 0, self.collider.width, self.collider.height), border_radius=self.border_radius)
        if self.focused:
            pygame.draw.rect(self.surf, self.border_color, (0, 0, self.collider.width, self.collider.height), width=self.border, border_radius=self.border_radius)
        else:
            if self.value == '':
                TextRenderer(self.surf, self.collider.width/2, self.collider.height/2, self.placeholder_text, 'Arial', self.collider.height - 5, self.placeholder_color).draw()

        TextRenderer(self.surf, self.collider.width/2, self.collider.height/2, self.value, 'Arial', self.collider.height - 5, self.text_color).draw()
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

class Slider:
    def __init__(self, win: pygame.Surface, pos: Vector2D, size: Vector2D, min_val: float, max_val: float, mid_color=(64, 64, 64), bar_color=(128, 128, 128), offset=Vector2D(0, 0)):
        self.win = win
        self.pos = pos
        self.size = size
        self.min_val = min_val
        self.max_val = max_val
        self.mid_color = mid_color
        self.bar_color = bar_color
        self.mid_val = 0.5 * max_val
        _mid_sl_bl_pos = self.pos.interpolate(self.size, 0.5)
        self.mid_sl_bar = pygame.Rect(_mid_sl_bl_pos.x, _mid_sl_bl_pos.y, 10, self.size.y)
        self.slider_rect = pygame.Rect(self.pos.x, (self.pos.y) - self.size.y/8, self.size.x, self.size.y/4)  # TODO Fix the positioning

    def _map_range(self):
        mapper = interp1d([self.pos.x, self.pos.x + self.size.x], [self.min_val, self.max_val], fill_value='extrapolate')
        mapped_value = mapper(self.mid_sl_bar.x)

        return mapped_value

    def update(self):
        mouse = pygame.mouse.get_pos()

        if self.mid_sl_bar.collidepoint(mouse[0], mouse[1]) and pygame.mouse.get_pressed() == (True, False, False):
            self.mid_sl_bar.x = mouse[0] - self.mid_sl_bar.width / 2

            if self.mid_sl_bar.x <= self.pos.x + self.size.x:
                pass
            else:
                self.mid_sl_bar.x = self.pos.x + self.size.x

            if self.mid_sl_bar.x >= self.pos.x:
                pass
            else:
                self.mid_sl_bar.x = self.pos.x

        elif self.slider_rect.collidepoint(mouse.x, mouse.y) and pygame.mouse.get_pressed() == (True, False, False):
            self.mid_sl_bar.x = mouse.x - self.mid_sl_bar.width / 2

        self.mid_val = self._map_range()

    def get_val(self):
        return self.mid_val

    def draw(self):
        TextRenderer(self.win, self.slider_rect.x, (self.slider_rect.y) - 20, str(self.min_val), 'Arial', 10, (255, 255, 255)).draw()
        TextRenderer(self.win, (self.slider_rect.x + self.size.x) , (self.slider_rect.y) - 20, str(self.max_val), 'Arial', 10, (255, 255, 255)).draw()
        TextRenderer(self.win, self.mid_sl_bar.x , (self.mid_sl_bar.y) - 20, str(self.mid_val), 'Arial', 10, (255, 255, 255)).draw()

        pygame.draw.rect(self.win, self.bar_color, pygame.Rect(self.slider_rect.x, self.slider_rect.y, self.slider_rect.width, self.slider_rect.height))
        pygame.draw.rect(self.win, self.mid_color, pygame.Rect(self.mid_sl_bar.x, self.mid_sl_bar.y, self.mid_sl_bar.width, self.mid_sl_bar.height))

class CheckBox:
    def __init__(self, win: pygame.Surface, pos: Vector2D, size: Vector2D, color=(255, 255, 255), toggled=False):
        self.win = win
        self.pos = pos
        self.size = size
        self.color = color
        self.toggeled = toggled
        self.checkbox_rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def update(self, events):
        mouse = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.checkbox_rect.collidepoint(mouse[0], mouse[1]):

                    if event.button == 1:
                        if self.toggeled:
                            self.toggeled = False
                        else:
                            self.toggeled = True

    def draw(self):
        pygame.draw.rect(self.win, self.color, self.checkbox_rect, border_radius=int((self.size.x + self.size.y)/16))
        if self.toggeled:
            pygame.draw.ellipse(self.win, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), self.checkbox_rect)

    def get_val(self):
        return self.toggeled

class JsonUiFile:
    """Takes in a Json file in which all ui element are defined, then Parses it and updates/renders them.
    NOTE: All x, y values are not dependent on screen size e.g. in your json file x=0.2 = 20% of screen width.(NOT FOR WIDTH/HEIGHT THO.)"""
    def __init__(self, json_file: str, json_dict: Optional[dict] = None):
        if json_dict is not None:
            if json_dict != {}:
                self.json_data = json_dict
            else:
                raise FileNotFoundError(f'Cant parse ui elements from empty dict: {json_dict}')
        else:
            if json_file != '' and path.isfile(json_file) and json_file.endswith('.json'):
                with open(json_file) as json_data:
                    self.json_data = json.load(json_data)
            else:
                raise FileNotFoundError(f'File either doesn\'t exists or is not a json file: {json_file}')


        self.ui_elems = {}
        self.supported_ui_elems = ['BUTTON', 'TEXTBOX', 'CHECKBOX', 'TEXT', 'SLIDER']

    def load(self, win: pygame.Surface):
        """Loads all elements into Memory."""
        win_size = win.get_size()
        for ui_elem in self.json_data.items():
            ui_elem_data = ui_elem[1]
            if ui_elem_data['TYPE'] in self. supported_ui_elems:
                if ui_elem_data['TYPE'] == self.supported_ui_elems[0]:  # Button                                                                                                      # TODO Replace this with an actual image
                    btn_tex = ui_elem_data['BACKGROUND'] if ui_elem_data['BACKGROUND'] != '' and path.isfile(ui_elem_data['BACKGROUND']) else '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/SPRNVA/res/missing_texture.png'
                    self.ui_elems[ui_elem[0]] = Button(win, win_size[0] * ui_elem_data['x'], win_size[1] * ui_elem_data['y'], ui_elem_data['WIDTH'], ui_elem_data['HEIGHT'], (0, 0, 0), img=btn_tex,
                                                       text=ui_elem_data['TEXT'], font=ui_elem_data['FONT'], font_size=ui_elem_data['FONTSIZE'], high_precision_mode=True)

                if ui_elem_data['TYPE'] == self.supported_ui_elems[1]:  # Textbox
                    self.ui_elems[ui_elem[0]] = InputBox(win, Vector2D(win_size[0] * ui_elem_data['x'], win_size[1] * ui_elem_data['y']), Vector2D(ui_elem_data['WIDTH'], ui_elem_data['HEIGHT']),
                                                                placeholder_text=ui_elem_data['PLACEHOLDER_TEXT'], color=(ui_elem_data['BGCOLOR'][0], ui_elem_data['BGCOLOR'][1], ui_elem_data['BGCOLOR'][2]),
                                                                text_color=(ui_elem_data['TEXTCOLOR'][0], ui_elem_data['TEXTCOLOR'][1], ui_elem_data['TEXTCOLOR'][2]), border_radius=ui_elem_data['BORDERRADIUS'])

                if ui_elem_data['TYPE'] == self.supported_ui_elems[2]:  # Checkbox
                    self.ui_elems[ui_elem[0]] = CheckBox(win, Vector2D(win_size[0] * ui_elem_data['x'], win_size[1] * ui_elem_data['y']),
                                                                Vector2D(ui_elem_data['WIDTH'], ui_elem_data['HEIGHT']),
                                                                color=(ui_elem_data['COLOR'][0], ui_elem_data['COLOR'][1], ui_elem_data['COLOR'][2]),
                                                                toggled=ui_elem_data['INITVALUE'])

                if ui_elem_data['TYPE'] == self.supported_ui_elems[3]:  # Text
                    av_font = pygame.font.get_fonts()
                    if ui_elem_data['FONT'].lower() in av_font:
                        self.ui_elems[ui_elem[0]] = TextRenderer(win, win_size[0] * ui_elem_data['x'], win_size[1] * ui_elem_data['y'], ui_elem_data['TEXT'], ui_elem_data['FONT'], ui_elem_data['SIZE'], ui_elem_data['COLOR'])
                    else:
                        self.ui_elems[ui_elem[0]] = TextRenderer(win, win_size[0] * ui_elem_data['x'], win_size[1] * ui_elem_data['y'], ui_elem_data['TEXT'], ui_elem_data['FONT'], ui_elem_data['SIZE'], ui_elem_data['COLOR'], font_file=True)

                if ui_elem_data['TYPE'] == self.supported_ui_elems[4]:  # Slider
                    self.ui_elems[ui_elem[0]] = Slider(win, Vector2D(win_size[0] * ui_elem_data['x'], win_size[1] * ui_elem_data['y']),
                                                              Vector2D(ui_elem_data['WIDTH'], ui_elem_data['HEIGHT']), ui_elem_data['MINVAL'],
                                                              ui_elem_data['MAXVAL'], ui_elem_data['BARCOLOR'], ui_elem_data['COLOR'])

    def update_elems(self, events: list):
        """Updates all elements."""
        for ui_elem in self.ui_elems.items():
            try:
                ui_elem[1].update()
            except Exception:  # TODO find out which exception type is raised
                try:
                    ui_elem[1].update(events)
                except Exception:
                    pass

    def draw_elems(self):
        """Draws all Elements."""
        for ui_elem in self.ui_elems.items():
            ui_elem[1].draw()

    def get_elem_by_key(self, key: str):
        """Returns ui object."""
        return self.ui_elems[key]

SUPPORTED_UI_TYPES = [TextRenderer, Button, SubMenu, InputBox, Card, Slider]

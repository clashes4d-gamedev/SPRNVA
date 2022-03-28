import pygame
import math

class TextRenderer:
    def __init__(self, win, x, y, text, font, size, color):
        pygame.font.init()
        txt = pygame.font.SysFont(font, size)
        txt_surf = txt.render(text, False, color)
        text_dim = txt.size(text)
        win.blit(txt_surf, (x - text_dim[0]/2, y - text_dim[1]/2))

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
            TextRenderer(self.button_surf, self.button_surf.get_width()/2, self.button_surf.get_height()/2, self.btn_font, self.btn_txt_size, self.btn_txt_color, self.btn_text)
        self.win.blit(self.button_surf, (self.button_collider.x, self.button_collider.y))
        pygame.draw.rect(self.win, (128,128,128), (self.x, self.y, self.width, self.height), width=1)

        if pygame.Rect.collidepoint(self.button_collider, self.mouse[0], self.mouse[1]):
            if self.mouse_btns[self.btn]:
                return True
            else:
                return False
        else:
            return False


class SubMenu:
    def __init__(self, win, x:int, y:int, width:int, options:list, color:tuple, button_height=20) -> None:
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

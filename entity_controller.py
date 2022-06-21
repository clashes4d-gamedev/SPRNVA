import pygame
from .vector import Vector2D, VectorOperations

class Player:
    def __init__(self, win, pos: Vector2D, size: Vector2D, img='', color=(255, 0, 0),
                 health=100, shield=50, shield_regen_counter=1, health_regen_counter=1, resistance=0.25):
        self.win = win
        self.x = pos.x
        self.y = pos.y
        self.width = size.x
        self.height = size.y
        self.color = color

        self.health = health
        self._base_health = self.health
        self.health_regen_counter = health_regen_counter
        self._base_health_regen_counter = self.health_regen_counter

        self.resistance = resistance
        self._base_resistance = self.resistance

        self.shield = shield
        self.shield_regen_counter = shield_regen_counter
        self._base_shield_regen_counter = self.shield_regen_counter
        self._base_shield = self.shield

        self.finished_health_regen = False
        self.finished_shield_regen = False

        self.total_health = self._base_health + self._base_shield
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surf = pygame.Surface((self.collider.width, self.collider.height))
        self.img = pygame.image.load(img).convert_alpha() if img != '' else img

    def draw_player_health(self, x, y, width, height, health_color=(171, 21, 21), vertical=False, border=False, border_radius=0, vignette=False):
        health = self.health/100
        h_vig_offset = 100
        if border_radius:
            if vertical:
                pygame.draw.rect(self.win, health_color, pygame.Rect(x, y - (height * health)/2, width, height * health), border_radius=border_radius)
                if border:
                    pygame.draw.rect(self.win, health_color, pygame.Rect(x, y - height/2, width, height), width=1, border_radius=border_radius)
            else:
                pygame.draw.rect(self.win, health_color, pygame.Rect(x - (width * health)/2, y, width * health, height), border_radius=border_radius)
                if border:
                    pygame.draw.rect(self.win, health_color, pygame.Rect(x - width/2, y, width, height), width=1, border_radius=border_radius)
                # if vignette:
                #     if self.health <= self.health/2:
                #         h_vig_offset = 50
                #         print('adding vignette')
                #         #win: pygame.Surface, offset: int, color: tuple, alpha: int
                #         add_vignette(self.win, 0, 0, h_vig_offset, health_color, 50)
                #     else:
                #         if h_vig_offset <= 100:
                #             h_vig_offset += 0.005
                #             add_vignette(self.win, 0, 0, h_vig_offset, health_color, 50)
                    
        else:
            if vertical:
                pygame.draw.rect(self.win, health_color, pygame.Rect(x, y - (height * health)/2, width, height * health))
                if border:
                    pygame.draw.rect(self.win, health_color, pygame.Rect(x, y - height/2, width, height), width=1)
            else:
                pygame.draw.rect(self.win, health_color, pygame.Rect(x - (width * health)/2, y, width * health, height))
                if border:
                    pygame.draw.rect(self.win, health_color, pygame.Rect(x - width/2, y, width, height), width=1)

    def draw_player_shield(self, x, y, width, height, shield_color=(76, 76, 176), vertical=False, border=False, border_radius=0):
        shield = self.shield/100
        if border_radius:
            if vertical:
                pygame.draw.rect(self.win, shield_color, pygame.Rect(x, y - (height * shield)/2, width, height * shield), border_radius=border_radius)
                if border:
                    pygame.draw.rect(self.win, shield_color, pygame.Rect(x, y - height/2, width, height), width=1, border_radius=border_radius)
            else:
                pygame.draw.rect(self.win, shield_color, pygame.Rect(x - (width * shield)/2, y, width * shield, height), border_radius=border_radius)
                if border:
                    pygame.draw.rect(self.win, shield_color, pygame.Rect(x - width/2, y, width, height), width=1, border_radius=border_radius)
        else:
            if vertical:
                pygame.draw.rect(self.win, shield_color, pygame.Rect(x, y - (height * shield)/2, width, height * shield))
                if border:
                    pygame.draw.rect(self.win, shield_color, pygame.Rect(x, y - height/2, width, height), width=1)
            else:
                pygame.draw.rect(self.win, shield_color, pygame.Rect(x - (width * shield)/2, y, width * shield, height))
                if border:
                    pygame.draw.rect(self.win, shield_color, pygame.Rect(x - width/2, y, width, height), width=1)


    def add_damage(self, damage: float):
        # TODO Make a seperate funtion to check if the player can take damage on shields or health and then call this
        if self.shield != 0:  # Shields absord damage without any resistances (cough...cough...space ninja wizard game...cough...cough)
            self.shield_regen_counter = 0
            if self.shield >= 0:
                self.shield -= damage
            else:
                self.shield = 0
        else:
            damage = damage - (damage * self.resistance)
            self.health_regen_counter = 0
            if self.health >= 0:
                self.health -= damage
            else:
                self.health = 0
        return self.health

    def regenerate_health(self, regen_rate=0.0025):
        if self.health <= self._base_health and self.health_regen_counter >= self._base_health_regen_counter:
            reg_step = self._base_health * regen_rate
            self.finished_health_regen = False
            self.health += reg_step
        else:
            self.health_regen_counter += regen_rate
            self.finished_health_regen = False

        if round(self.health) == self._base_health:
            self.finished_health_regen = True
        return self.health

    def regenerate_shield(self, regen_rate=0.0025):
        if self.finished_health_regen and self.shield_regen_counter >= self._base_shield_regen_counter:
            if self.shield <= self._base_shield:
                reg_step = self._base_shield * regen_rate
                self.finished_shield_regen = False
                self.shield += reg_step
            else:
                self.finished_shield_regen = True
        else:
            self.shield_regen_counter += regen_rate
        return self.shield

    def draw_player(self):
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

    def move(self, tiles, vel:Vector2D, dt:float, x=False, y=False, minus_y=False, minus_x=False, boundaries=True):
        if vel >= 0:
            if boundaries:
                if x is not False and (self.collider.x + self.collider.width) <= self.win.get_width():
                    self.collider.x += vel.x * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.right = tile.left

                elif y is not False and (self.collider.y + self.collider.height) <= self.win.get_height():
                    self.collider.y += vel.y * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.bottom = tile.top

                elif minus_x is not False and self.collider.x >= 0:
                    self.collider.x -= vel.x * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.left = tile.right

                elif minus_y is not False and self.collider.y >= 0:
                    self.collider.y -= vel.y * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.top = tile.bottom

                else:
                    return
            else:
                if x is not False:
                    self.collider.x += vel.x * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.right = tile.left

                elif y is not False:
                    self.collider.y += vel.y * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.bottom = tile.top

                elif minus_x is not False:
                    self.collider.x -= vel.x * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.left = tile.right

                elif minus_y is not False:
                    self.collider.y -= vel.y * dt
                    collisions = self.check_collisions(tiles)
                    for tile in collisions:
                        self.collider.top = tile.bottom

                else:
                    return
        else:
            return

class Enemy:
    def __init__(self, win, pos: Vector2D, size: Vector2D, img='', color=(255, 0, 0)):
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

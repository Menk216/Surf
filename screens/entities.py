import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, image_surface, start_x=WIDTH//2, start_y=-200, target_y=None,
                 size=(140,140), drop_speed=8):
        super().__init__()

        self.base_img = pygame.transform.smoothscale(image_surface, size)
        self.image = self.base_img
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.mask = pygame.mask.from_surface(self.image)

        self.target_y = target_y if target_y is not None else int(HEIGHT * 0.62)
        self.drop_speed = drop_speed
        self.active = False
        self.angle_timer = 0

        self.score = 0
        self.coins_collected = 0

        self.invincible = False
        self.speed_multiplier = 1.0
        self.magnet_active = False
        self.score_multiplier = 1.0
        self.magnet_radius = 150

    def update(self, dt, mouse_pos):
        if not self.active:

            if self.rect.centery < self.target_y:
                self.rect.centery += self.drop_speed
            else:
                self.active = True
        else:
            mx, my = mouse_pos

            move_speed = 0.12 * self.speed_multiplier
            self.rect.centerx += (mx - self.rect.centerx) * move_speed

            halfw = self.rect.width // 2
            self.rect.centerx = max(halfw, min(WIDTH - halfw, self.rect.centerx))

            self.angle_timer += dt
            angle = math.sin(self.angle_timer * 0.005) * 8
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.base_img, angle)
            self.rect = self.image.get_rect(center=old_center)
            self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y=-220, size=(100,100), speed=6):
        super().__init__()
        self.base_img = pygame.transform.smoothscale(image_surface, size)
        self.image = self.base_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

    def update(self, dt, scroll_speed=0):
        self.rect.y += int(self.speed + scroll_speed)
        if self.rect.top > HEIGHT + 50:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y=-100, size=(64,64), speed=6):
        super().__init__()
        self.base_img = pygame.transform.smoothscale(image_surface, size)
        self.image = self.base_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

    def update(self, dt, scroll_speed=0):
        self.rect.y += int(self.speed + scroll_speed)
        if self.rect.top > HEIGHT + 20:
            self.kill()

class Treasure(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y=-180, size=(100,100), speed=5):
        super().__init__()
        self.base_img = pygame.transform.smoothscale(image_surface, size)
        self.image = self.base_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

    def update(self, dt, scroll_speed=0):
        self.rect.y += int(self.speed + scroll_speed)
        if self.rect.top > HEIGHT + 50:
            self.kill()

class Tree(pygame.sprite.Sprite):
    def __init__(self, image_surface, x, y=-200, size=(100,100), speed=6):
        super().__init__()
        self.base_img = pygame.transform.smoothscale(image_surface, size)
        self.image = self.base_img
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.called_monster = False

    def update(self, dt, scroll_speed=0):
        self.rect.y += int(self.speed + scroll_speed)
        if self.rect.top > HEIGHT + 50:
            self.kill()

class Monster(pygame.sprite.Sprite):
    def __init__(self, image_surface, player_sprite, spawn_x=None, spawn_y=-250,
                 size=(240,240), speed=5):
        super().__init__()
        self.base_img = pygame.transform.smoothscale(image_surface, size)
        self.image = self.base_img
        px = player_sprite.rect.centerx if spawn_x is None else spawn_x
        self.rect = self.image.get_rect(midbottom=(px, spawn_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.player = player_sprite
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt, scroll_speed=0):
        self.rect.y += int(self.speed + scroll_speed)

        if self.player.rect.centerx < self.rect.centerx:
            self.rect.x -= min(6, (self.rect.centerx - self.player.rect.centerx) // 8 + 1)
        elif self.player.rect.centerx > self.rect.centerx:
            self.rect.x += min(6, (self.player.rect.centerx - self.rect.centerx) // 8 + 1)

        if pygame.time.get_ticks() - self.spawn_time > 60_000:
            self.kill()

        if self.rect.top > HEIGHT + 200:
            self.kill()

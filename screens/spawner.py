from settings import *
import pygame
import random
from screens.entities import Obstacle, Coin, Treasure, Tree, Monster
from utils import resource_path

class Spawner:
    def __init__(self, game, groups, images, speeds=None, spawn_delay_ms=2000, rates=None):
    
        self.game = game
        self.groups = groups
        self.images = images

        self.base_scroll_speed = 0
        self.obstacle_speed = (speeds.get('obstacle') if speeds else 8)
        self.coin_speed = (speeds.get('coin') if speeds else 8)
        self.tree_speed = (speeds.get('tree') if speeds else 8)
        self.treasure_speed = (speeds.get('treasure') if speeds else 7)
        self.monster_speed = (speeds.get('monster') if speeds else 8)

        w = WIDTH
        self.obstacle_patterns = [
            [w//2],
            [w//4, w//2, w*3//4],
            [150, w-150],
            [w//3, w*2//3],
            [w//6, w//2, w*5//6]
        ]

        default_rates = {
            'obstacle_group': 0.6,
            'single_obstacle': 1.2,
            'coin': 4.0,
            'tree': 1.0,
        }

        self.rates = rates if rates else default_rates

        self.start_time = pygame.time.get_ticks()
        self.spawn_delay = spawn_delay_ms

        self.last_treasure_time = pygame.time.get_ticks()
        self.treasure_interval = 120_000

    def _safe_add(self, sprite, group_key, max_attempts=5, jitter_x=60):
        for _ in range(max_attempts):
            collide_obs = pygame.sprite.spritecollideany(sprite, self.groups.get('obstacles', []))
            collide_trees = pygame.sprite.spritecollideany(sprite, self.groups.get('trees', []))
            if not collide_obs and not collide_trees:
                self.groups[group_key].add(sprite)
                return True

            sprite.rect.centerx = max(60, min(WIDTH-60,
                                  sprite.rect.centerx + random.randint(-jitter_x, jitter_x)))
        return False

    def spawn_obstacle_group(self):
        pattern = random.choice(self.obstacle_patterns)

        if len(pattern) <= 2:
            max_obs = len(pattern)
        else:
            max_obs = random.randint(2, min(3, len(pattern)))

        chosen_positions = random.sample(pattern, max_obs)

        if len(chosen_positions) > 1 and random.random() < 0.7:
            safe_x = random.choice(chosen_positions)
            chosen_positions.remove(safe_x)

        for x in chosen_positions:
            img = random.choice(self.images.get('obstacles', []))
            y = -random.randint(400, 700)
            obs = Obstacle(img, x, y=y, size=(220, 220), speed=self.obstacle_speed)

            too_close = any(abs(o.rect.centerx - x) < 180 for o in self.groups['obstacles'])
            if too_close:
                continue

            self._safe_add(obs, 'obstacles')

    def spawn_single_obstacle(self):
        x = random.randint(100, WIDTH-100)
        img = random.choice(self.images.get('obstacles', []))
        y = -random.randint(300, 600)
        obs = Obstacle(img, x, y=y, size=(200,200), speed=self.obstacle_speed)
        self._safe_add(obs, 'obstacles')

    def spawn_coin(self):
        x = random.randint(80, WIDTH-80)
        img = self.images.get('coin')
        if img:
            y = -random.randint(220, 450)
            coin = Coin(img, x, y=y, size=(64,64), speed=self.coin_speed)
            self._safe_add(coin, 'coins')

    def spawn_tree(self):
        x = random.randint(100, WIDTH-100)
        img = random.choice(self.images.get('trees', []))
        y = -random.randint(350, 600)
        t = Tree(img, x, y=y, size=(200,220), speed=self.tree_speed)
        self._safe_add(t, 'trees')

    def spawn_treasure_if_needed(self):
        now = pygame.time.get_ticks()
        if now - self.last_treasure_time > self.treasure_interval:
            x = random.randint(120, WIDTH-120)
            img = self.images.get('treasure')
            if img:
                tr = Treasure(img, x, y=-400, size=(140,140), speed=self.treasure_speed)
                self.groups['treasures'].add(tr)
            self.last_treasure_time = now

    def spawn_monster_from_tree(self, tree_sprite, player_sprite):

        spawn_x = player_sprite.rect.centerx + random.randint(-80, 80)
        img = self.images.get('monster')
        if img:
            m = Monster(img, player_sprite, spawn_x=spawn_x, spawn_y=-220,
                        size=(260,260), speed=self.monster_speed)
            self.groups['monsters'].add(m)

    def maybe_spawn_every_frame(self, dt):
        if pygame.time.get_ticks() - self.start_time < self.spawn_delay:
            self.spawn_treasure_if_needed()
            return

        sec = dt / 1000.0
        if random.random() < self.rates['obstacle_group'] * sec:
            self.spawn_obstacle_group()
        if random.random() < self.rates['single_obstacle'] * sec:
            self.spawn_single_obstacle()
        if random.random() < self.rates['coin'] * sec:
            self.spawn_coin()
        if random.random() < self.rates['tree'] * sec:
            self.spawn_tree()

        self.spawn_treasure_if_needed()

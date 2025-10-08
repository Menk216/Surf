from settings import *
import pygame
import random
from screens.entities import Obstacle, Coin, Treasure, Tree, Monster

class Spawner:
    def __init__(self, game, groups, images, speeds=None, spawn_delay_ms=2000, rates=None):  # Giảm delay từ 3000 xuống 2000
    

        """
        Spawner (bộ sinh vật thể trong game)

        game: tham chiếu tới game chính (có thể lấy player, thông tin state, ...)
        groups: dict chứa các sprite groups {'obstacles','coins','treasures','trees','monsters'}
        images: dict chứa ảnh đã load {'obstacles':list, 'coin', 'treasure', 'trees':list, 'monster'}
        speeds: dict tuỳ chỉnh tốc độ rơi của từng loại
        spawn_delay_ms: delay (ms) lúc bắt đầu game để tránh spawn sớm khi player đang rơi xuống
        rates: dict tuỳ chỉnh tỉ lệ spawn mỗi giây (spawn probability per second)
        """
        self.game = game
        self.groups = groups
        self.images = images

        # tốc độ rơi (nếu không truyền thì lấy mặc định)
        self.base_scroll_speed = 0
        self.obstacle_speed = (speeds.get('obstacle') if speeds else 8)  # Tăng từ 6 lên 8
        self.coin_speed = (speeds.get('coin') if speeds else 8)  # Tăng từ 6 lên 8
        self.tree_speed = (speeds.get('tree') if speeds else 8)  # Tăng từ 6 lên 8
        self.treasure_speed = (speeds.get('treasure') if speeds else 7)  # Tăng từ 5 lên 7
        self.monster_speed = (speeds.get('monster') if speeds else 8)  # Tăng từ 6 lên 8

        # các pattern x cố định cho obstacles (để spawn theo hàng/cột)
        w = WIDTH
        self.obstacle_patterns = [
            [w//2],
            [w//4, w//2, w*3//4],
            [150, w-150],
            [w//3, w*2//3],
            [w//6, w//2, w*5//6]
        ]

        # tỉ lệ spawn mặc định (per second, thay vì per frame → không phụ thuộc FPS)
        default_rates = {
            'obstacle_group': 0.8,   # Tăng từ 0.48 lên 0.8
            'single_obstacle': 2.0,   # Tăng từ 1.2 lên 2.0
            'coin': 4.0,              # Tăng từ 2.7 lên 4.0
            'tree': 1.0,              # Tăng từ 0.6 lên 1.0
        }
        self.rates = rates if rates else default_rates

        # thời gian bắt đầu game (để tính delay spawn ban đầu)
        self.start_time = pygame.time.get_ticks()
        self.spawn_delay = spawn_delay_ms

        # timer cho rương báu (xuất hiện mỗi 2 phút)
        self.last_treasure_time = pygame.time.get_ticks()
        self.treasure_interval = 120_000  # 2 phút (ms)

    # ---------- hàm phụ ----------
    def _safe_add(self, sprite, group_key, max_attempts=5, jitter_x=60):
        """
        Thêm sprite vào group nhưng kiểm tra tránh chồng chéo quá mức.
        - Nếu spawn bị overlap với obstacle/tree khác thì thử xê dịch ngang vài lần
        - Nếu thử nhiều lần vẫn đè nhau thì bỏ qua
        """
        for _ in range(max_attempts):
            collide_obs = pygame.sprite.spritecollideany(sprite, self.groups.get('obstacles', []))
            collide_trees = pygame.sprite.spritecollideany(sprite, self.groups.get('trees', []))
            if not collide_obs and not collide_trees:
                self.groups[group_key].add(sprite)
                return True
            # dịch sprite sang trái/phải rồi thử lại
            sprite.rect.centerx = max(60, min(WIDTH-60,
                                  sprite.rect.centerx + random.randint(-jitter_x, jitter_x)))
        return False  # bỏ qua nếu vẫn bị chồng

    # ---------- hàm spawn từng loại ----------
    def spawn_obstacle_group(self):
        pattern = random.choice(self.obstacle_patterns)
        for x in pattern:
            img = random.choice(self.images.get('obstacles', []))
            y = -random.randint(400, 700)  # spawn cao hơn màn hình → rớt từ từ xuống
            obs = Obstacle(img, x, y=y, size=(220,220), speed=self.obstacle_speed)
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
        # spawn quái gần player để nó đuổi theo
        spawn_x = player_sprite.rect.centerx + random.randint(-80, 80)
        img = self.images.get('monster')
        if img:
            m = Monster(img, player_sprite, spawn_x=spawn_x, spawn_y=-220,
                        size=(260,260), speed=self.monster_speed)
            self.groups['monsters'].add(m)

    # ---------- gọi mỗi frame ----------
    def maybe_spawn_every_frame(self, dt):
        """
        dt: mili-giây từ frame trước tới frame hiện tại
        - spawn theo tỉ lệ mỗi giây (dựa vào dt)
        - chặn spawn trong vài giây đầu để tránh player chết ngay khi vừa rơi xuống
        """
        # block spawn ban đầu (tránh chết tức thì)
        if pygame.time.get_ticks() - self.start_time < self.spawn_delay:
            self.spawn_treasure_if_needed()
            return

        sec = dt / 1000.0  # đổi dt sang giây
        if random.random() < self.rates['obstacle_group'] * sec:
            self.spawn_obstacle_group()
        if random.random() < self.rates['single_obstacle'] * sec:
            self.spawn_single_obstacle()
        if random.random() < self.rates['coin'] * sec:
            self.spawn_coin()
        if random.random() < self.rates['tree'] * sec:
            self.spawn_tree()

        # treasure dựa theo timer, không dựa random
        self.spawn_treasure_if_needed()

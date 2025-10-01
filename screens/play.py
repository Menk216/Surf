# play_screen.py
import pygame
import math
from settings import *
from screens.entities import Player
from screens.spawner import Spawner

class PlayScreen:
    def __init__(self, game):
        """
        Màn chơi chính (PlayScreen)
        game: object chứa ít nhất
          - screen, clock
          - images: obstacle_imgs, coin_img, treasure_img, tree_imgs, monster_img, player_img
        """
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        # Background
        self.background = pygame.image.load("resources/assets/backgrounds/test.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.wave_offset = 0     # hiệu ứng sóng ngang
        self.scroll_y = 0        # hiệu ứng cuộn dọc

        # Nút back (chỉ hiện trong countdown)
        self.back_button = pygame.Rect(30, 30, 60, 60)
        self.back_icon = pygame.image.load("resources/assets/icon/return_icon.png").convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (32, 32))

        # Countdown trước khi chơi
        self.countdown = 3
        self.countdown_timer = 0

        # Sprite groups
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        groups = {
            'obstacles': self.obstacles,
            'coins': self.coins,
            'treasures': self.treasures,
            'trees': self.trees,
            'monsters': self.monsters
        }

        # Ảnh vật thể (lấy từ game hoặc None)
        images = {
            'obstacles': getattr(game, 'obstacle_imgs', []),
            'coin': getattr(game, 'coin_img', None),
            'treasure': getattr(game, 'treasure_img', None),
            'trees': getattr(game, 'tree_imgs', []),
            'monster': getattr(game, 'monster_img', None)
        }

        # Player
        player_img = getattr(game, 'player_img', "resources/assets/characters/player.png")
        self.player = Player(player_img,
                             start_x=WIDTH//2, start_y=-200,
                             target_y=int(HEIGHT*0.62),
                             size=(150,150), drop_speed=9)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        # Spawner
        self.spawner = Spawner(game, groups, images)

        # Gameplay
        self.running = False
        self.score = 0

    # ---------------- Vẽ nền ----------------
    def draw_background(self):
        """Vẽ nền với hiệu ứng sóng ngang + cuộn dọc"""
        wave_surface = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            shift = int(10 * math.sin(y/30 + self.wave_offset*0.02))
            line = self.background.subsurface((0, y, WIDTH, 1))
            wave_surface.blit(line, (shift, y))
            if shift > 0:
                wave_surface.blit(line, (shift-WIDTH, y))
            elif shift < 0:
                wave_surface.blit(line, (shift+WIDTH, y))

        sy = self.scroll_y % HEIGHT
        self.screen.blit(wave_surface, (0, sy-HEIGHT))
        self.screen.blit(wave_surface, (0, sy))

    def draw_back_button(self):
        """Vẽ nút quay lại (trong countdown)"""
        if self.countdown > 0:
            btn_surf = pygame.Surface(self.back_button.size, pygame.SRCALPHA)
            pygame.draw.rect(btn_surf, (0,0,0,120), btn_surf.get_rect(), border_radius=15)
            btn_surf.blit(self.back_icon,
                          (self.back_button.width//2 - self.back_icon.get_width()//2,
                           self.back_button.height//2 - self.back_icon.get_height()//2))
            self.screen.blit(btn_surf, self.back_button.topleft)

    def draw_countdown(self):
        """Vẽ đồng hồ đếm ngược"""
        if self.countdown > 0:
            pulse = 1.0 + 0.12 * math.sin(pygame.time.get_ticks() * 0.01)
            size = int(200 * pulse)
            font = pygame.font.SysFont("Arial", size, bold=True)
            text = font.render(str(self.countdown), True, (255,80,40))
            shadow = font.render(str(self.countdown), True, (0,0,0))
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(shadow, (rect.x+6, rect.y+6))
            self.screen.blit(text, rect)

    def draw_score(self):
        """Vẽ điểm số"""
        f = pygame.font.SysFont("Arial", 30, bold=True)
        txt = f.render(f"Score: {self.score}  Coins: {self.player.coins_collected}", True, (255,255,255))
        self.screen.blit(txt, (WIDTH-240, 20))

    # ---------------- Va chạm ----------------
    def handle_collisions(self):
        """Xử lý va chạm & luật chơi"""
        # Ăn coin
        coins_hit = pygame.sprite.spritecollide(
            self.player, self.coins, dokill=True, collided=pygame.sprite.collide_mask
        )
        if coins_hit:
            self.player.coins_collected += len(coins_hit)
            self.score += 5 * len(coins_hit)

        # Ăn treasure
        treasures_hit = pygame.sprite.spritecollide(
            self.player, self.treasures, dokill=True, collided=pygame.sprite.collide_mask
        )
        if treasures_hit:
            self.score += 50 * len(treasures_hit)

        # Đụng obstacle = thua
        if pygame.sprite.spritecollideany(
            self.player, self.obstacles, collided=pygame.sprite.collide_mask
        ):
            self.game.state = "game_over"
            return True

        # Đụng tree = spawn monster
        trees_hit = pygame.sprite.spritecollide(
            self.player, self.trees, dokill=False, collided=pygame.sprite.collide_mask
        )
        for t in trees_hit:
            if not getattr(t, 'called_monster', False):
                t.called_monster = True
                self.spawner.spawn_monster_from_tree(t, self.player)

        # Nếu có monster và player đang va vào tree = thua
        if len(self.monsters) > 0 and len(trees_hit) > 0:
            self.game.state = "game_over"
            return True

        # Monster đụng obstacle = chết
        pygame.sprite.groupcollide(
            self.monsters, self.obstacles, True, False, collided=pygame.sprite.collide_mask
        )

        return False


    # ---------------- Loop chính ----------------
    def run(self):
        self.running = True
        while self.running and self.game.running:
            dt = self.clock.tick(FPS)
            self.wave_offset += 2
            self.scroll_y += 1

            # Countdown
            if self.countdown > 0:
                self.countdown_timer += dt
                if self.countdown_timer >= 1000:
                    self.countdown -= 1
                    self.countdown_timer = 0

            # Event
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    self.game.running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.game.state = "start"
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN and self.countdown > 0:
                    if self.back_button.collidepoint(e.pos):
                        self.game.state = "start"
                        self.running = False

            # Vẽ nền
            self.draw_background()

            # Update / spawn
            if self.countdown <= 0:
                self.spawner.maybe_spawn_every_frame(dt)
                self.obstacles.update(dt, 0)
                self.coins.update(dt, 0)
                self.treasures.update(dt, 0)
                self.trees.update(dt, 0)
                self.monsters.update(dt, 0)
            else:
                # countdown thì update nhẹ thôi
                self.obstacles.update(dt, 0)
                self.coins.update(dt, 0)
                self.treasures.update(dt, 0)
                self.trees.update(dt, 0)
                self.monsters.update(dt, 0)

            # Update player (luôn hoạt động để hiệu ứng rơi xuống xuất hiện)
            mouse_pos = pygame.mouse.get_pos()
            self.player.update(dt, mouse_pos)

            # Vẽ sprites
            self.obstacles.draw(self.screen)
            self.trees.draw(self.screen)
            self.coins.draw(self.screen)
            self.treasures.draw(self.screen)
            self.monsters.draw(self.screen)
            self.player_group.draw(self.screen)

            # HUD
            self.draw_back_button()
            self.draw_countdown()
            self.draw_score()

            # Va chạm (sau khi countdown xong)
            if self.countdown <= 0:
                if self.handle_collisions():
                    self.running = False

            pygame.display.flip()

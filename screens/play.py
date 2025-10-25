import pygame
import math
from settings import *
from screens.entities import Player
from screens.spawner import Spawner
from theme_manager import ThemeManager
from ui_manager import UIManager
from utils import resource_path

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

        self.theme_manager = ThemeManager()
        self.ui_manager = UIManager(self.theme_manager)
        
        self.background = pygame.image.load(resource_path("resources/assets/backgrounds/test.jpg")).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.wave_offset = 0
        self.scroll_y = 0

        self.back_button = pygame.Rect(30, 30, 60, 60)
        self.back_icon = pygame.image.load(resource_path("resources/assets/icon/return_icon.png")).convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (32, 32))

        self.countdown = 3
        self.countdown_timer = 0

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

        images = {
            'obstacles': getattr(game, 'obstacle_imgs', []),
            'coin': getattr(game, 'coin_img', None),
            'treasure': getattr(game, 'treasure_img', None),
            'trees': getattr(game, 'tree_imgs', []),
            'monster': getattr(game, 'monster_img', None)
        }

        player_img = getattr(game, 'player_img', resource_path("resources/assets/characters/player.png"))
        self.player = Player(player_img,
                             start_x=WIDTH//2, start_y=-200,
                             target_y=int(HEIGHT*0.62),
                             size=(150,150), drop_speed=20)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.spawner = Spawner(game, groups, images)
        
        self.running = False
        self.score = 0

        self.invincible_timer = 0
        self.invincible_blink_timer = 0
        
        try:
            pygame.mixer.music.load(resource_path("resources/assets/sound/sound.mp3"))

            import settings as settings_module
            pygame.mixer.music.set_volume(settings_module.CURRENT_VOLUME)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Cannot load PlayScreen music: {e}")

    def draw_background(self):
        """Vẽ nền với hiệu ứng sóng ngang + cuộn dọc và theme"""
        theme = self.theme_manager.get_current_theme()
        
        background_surface = pygame.Surface((WIDTH, HEIGHT))
        background_surface.fill(theme['background_color'])
        
        if self.background:

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, int(255 * theme['ambient_light'])))
            
            wave_surface = pygame.Surface((WIDTH, HEIGHT))
            for y in range(0, HEIGHT, 4):
                shift = int(6 * math.sin(y/50 + self.wave_offset*0.01) * theme['wave_intensity'])
                line = self.background.subsurface((0, y, WIDTH, 4))
                wave_surface.blit(line, (shift, y))
                if shift > 0:
                    wave_surface.blit(line, (shift-WIDTH, y))
                elif shift < 0:
                    wave_surface.blit(line, (shift+WIDTH, y))
            
            wave_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            background_surface.blit(wave_surface, (0, 0))
        
        water_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 4):
            alpha = int(80 * (1 - y / HEIGHT))
            water_color = (*theme['water_color'][:3], alpha)
            pygame.draw.line(water_overlay, water_color, (0, y), (WIDTH, y))
        
        background_surface.blit(water_overlay, (0, 0))
        
        if theme['name'] == "Đêm":
            dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 100))
            background_surface.blit(dark_overlay, (0, 0))
        
        sy = self.scroll_y % HEIGHT
        self.screen.blit(background_surface, (0, sy-HEIGHT))
        self.screen.blit(background_surface, (0, sy))

    def draw_countdown(self):
        """Vẽ đồng hồ đếm ngược với theme"""
        if self.countdown > 0:
            theme = self.theme_manager.get_current_theme()
            pulse = 1.0 + 0.12 * math.sin(pygame.time.get_ticks() * 0.01)
            size = int(200 * pulse)
            font = pygame.font.Font(None, size)
            text = font.render(str(self.countdown), True, theme['accent_color'])
            shadow = font.render(str(self.countdown), True, theme['shadow_color'])
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            glow_surface = pygame.Surface((rect.width + 40, rect.height + 40), pygame.SRCALPHA)
            for i in range(20):
                alpha = int(50 * (1 - i / 20))
                glow_color = (*theme['accent_color'][:3], alpha)
                glow_rect = pygame.Rect(i, i, rect.width + 40 - i*2, rect.height + 40 - i*2)
                pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=size//4)
            
            self.screen.blit(glow_surface, (rect.x - 20, rect.y - 20))
            self.screen.blit(shadow, (rect.x+6, rect.y+6))
            self.screen.blit(text, rect)

    def draw_score(self):
        """Vẽ điểm số với UI mới"""
        self.ui_manager.draw_score_panel(self.screen, self.score)
        self.ui_manager.draw_coin_panel(self.screen, self.player.coins_collected)
        self.ui_manager.draw_theme_indicator(self.screen)

    def handle_collisions(self):
        """Xử lý va chạm & luật chơi"""
        
        coins_hit = pygame.sprite.spritecollide(
            self.player, self.coins, dokill=True, collided=pygame.sprite.collide_mask
        )
        if coins_hit:
            self.player.coins_collected += len(coins_hit)
            self.score += int(5 * len(coins_hit) * self.player.score_multiplier)

            for coin in coins_hit:
                self.ui_manager.add_coin_collect_effect(coin.rect.centerx, coin.rect.centery)
        
        if self.invincible_timer > 0 or self.player.invincible:

            trees_hit = pygame.sprite.spritecollide(
                self.player, self.trees, dokill=False, collided=pygame.sprite.collide_mask
            )
            for t in trees_hit:
                if not getattr(t, 'called_monster', False):
                    t.called_monster = True
                    self.spawner.spawn_monster_from_tree(t, self.player)
            return False
        
        if pygame.sprite.spritecollideany(
            self.player, self.obstacles, collided=pygame.sprite.collide_mask
        ):
            self.game.state = "game_over"
            return True
        
        trees_hit = pygame.sprite.spritecollide(
            self.player, self.trees, dokill=False, collided=pygame.sprite.collide_mask
        )
        for t in trees_hit:
            if not getattr(t, 'called_monster', False):
                t.called_monster = True
                self.spawner.spawn_monster_from_tree(t, self.player)
        
        if pygame.sprite.spritecollideany(
            self.player, self.monsters, collided=pygame.sprite.collide_mask
        ):
            self.game.state = "game_over"
            return True
        
        return False

    def run(self):
        self.running = True
        while self.running and self.game.running:
            dt = self.clock.tick(FPS)
            self.wave_offset += 5  
            self.scroll_y += 4  
            
            self.theme_manager.update(dt)
            self.ui_manager.update(dt)

            if self.countdown > 0:
                self.countdown_timer += dt
                if self.countdown_timer >= 1000:
                    self.countdown -= 1
                    self.countdown_timer = 0

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.running = False
                    self.game.running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    self.game.state = "start"
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.countdown > 0 and self.back_button.collidepoint(e.pos):
                        pygame.mixer.music.stop()
                        self.game.state = "start"
                        self.running = False
                    else:

                        ui_action = self.ui_manager.handle_click(e.pos)

            self.draw_background()

            if self.countdown <= 0:
                self.spawner.maybe_spawn_every_frame(dt)
                self.obstacles.update(dt, 0)
                self.coins.update(dt, 0)
                self.treasures.update(dt, 0)
                self.trees.update(dt, 0)
                self.monsters.update(dt, 0)
            else:

                self.obstacles.update(dt, 0)
                self.coins.update(dt, 0)
                self.treasures.update(dt, 0)
                self.trees.update(dt, 0)
                self.monsters.update(dt, 0)

            mouse_pos = pygame.mouse.get_pos()
            self.player.update(dt, mouse_pos)

            self.obstacles.draw(self.screen)
            self.trees.draw(self.screen)
            self.coins.draw(self.screen)
            self.treasures.draw(self.screen)
            self.monsters.draw(self.screen)
            
            if self.invincible_timer > 0:
                self.invincible_timer -= dt
                self.invincible_blink_timer += dt
                
                if int(self.invincible_blink_timer / 150) % 2 == 0:
                    self.player.image.set_alpha(80)
                else:
                    self.player.image.set_alpha(255)
            else:
                self.player.image.set_alpha(255)

            self.player_group.draw(self.screen)

            self.draw_countdown()
            self.draw_score()
            
            self.theme_manager.draw_transition_effects(self.screen)

            self.ui_manager.draw_coin_collect_effects(self.screen)
            
            mouse_pos = pygame.mouse.get_pos()
            self.ui_manager.draw_control_buttons(self.screen, mouse_pos)

            if self.countdown <= 0:
                if self.handle_collisions():
                    from screens.gameover import GameOverScreen
                    gameover_screen = GameOverScreen(self.game, self)
                    gameover_screen.run()
                    self.running = False

            pygame.display.flip()

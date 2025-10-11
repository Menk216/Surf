# play_screen.py
import pygame
import math
from settings import *
from screens.entities import Player
from screens.spawner import Spawner
from theme_manager import ThemeManager
from ui_manager import UIManager
from power_up_manager import PowerUpManager

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

        # Theme và UI Manager
        self.theme_manager = ThemeManager()
        self.ui_manager = UIManager(self.theme_manager)
        
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
        self.power_ups = pygame.sprite.Group()

        groups = {
            'obstacles': self.obstacles,
            'coins': self.coins,
            'treasures': self.treasures,
            'trees': self.trees,
            'monsters': self.monsters,
            'power_ups': self.power_ups
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
                             size=(150,150), drop_speed=20)  # Tăng từ 12 lên 15
        self.player_group = pygame.sprite.GroupSingle(self.player)

        # Spawner
        self.spawner = Spawner(game, groups, images)
        
        # Power-up Manager
        self.power_up_manager = PowerUpManager(game, groups, images)

        # Gameplay
        self.running = False
        self.score = 0
        # Timer bất tử
        self.invincible_timer = 0  # Timer bất tử (ms)
        self.invincible_blink_timer = 0  # Timer cho hiệu ứng nhấp nháy
        
        # Khởi tạo và phát nhạc nền cho PlayScreen
        try:
            pygame.mixer.music.load("resources/assets/sound/sound.mp3")
            pygame.mixer.music.set_volume(0.7)  # Âm lượng 70%
            pygame.mixer.music.play(-1)  # Lặp vô hạn
            print("PlayScreen music started!")
        except pygame.error as e:
            print(f"Cannot load PlayScreen music: {e}")


    # ---------------- Vẽ nền ----------------
    def draw_background(self):
        """Vẽ nền với hiệu ứng sóng ngang + cuộn dọc và theme"""
        theme = self.theme_manager.get_current_theme()
        
        # Tạo surface với màu nền theme
        background_surface = pygame.Surface((WIDTH, HEIGHT))
        background_surface.fill(theme['background_color'])
        
        # Vẽ background image với độ trong suốt theo theme
        if self.background:
            # Áp dụng ambient light từ theme
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, int(255 * theme['ambient_light'])))
            
            wave_surface = pygame.Surface((WIDTH, HEIGHT))
            for y in range(0, HEIGHT, 4):  # Vẽ mỗi 4 pixel để tăng tốc hơn
                shift = int(6 * math.sin(y/50 + self.wave_offset*0.01) * theme['wave_intensity'])  # Giảm độ mạnh hơn
                line = self.background.subsurface((0, y, WIDTH, 4))  # Lấy 4 pixel cùng lúc
                wave_surface.blit(line, (shift, y))
                if shift > 0:
                    wave_surface.blit(line, (shift-WIDTH, y))
                elif shift < 0:
                    wave_surface.blit(line, (shift+WIDTH, y))
            
            # Áp dụng overlay để điều chỉnh độ sáng
            wave_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            background_surface.blit(wave_surface, (0, 0))
        
        # Vẽ hiệu ứng nước với màu theme (tối ưu hóa)
        water_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 4):  # Vẽ mỗi 4 pixel để tăng tốc hơn
            alpha = int(80 * (1 - y / HEIGHT))  # Tăng alpha để nước đậm hơn
            water_color = (*theme['water_color'][:3], alpha)
            pygame.draw.line(water_overlay, water_color, (0, y), (WIDTH, y))
        
        background_surface.blit(water_overlay, (0, 0))
        
        # Thêm overlay tối cho theme đêm
        if theme['name'] == "Đêm":
            dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 100))  # Overlay đen với alpha 100
            background_surface.blit(dark_overlay, (0, 0))
        
        # Cuộn dọc
        sy = self.scroll_y % HEIGHT
        self.screen.blit(background_surface, (0, sy-HEIGHT))
        self.screen.blit(background_surface, (0, sy))

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
        """Vẽ đồng hồ đếm ngược với theme"""
        if self.countdown > 0:
            theme = self.theme_manager.get_current_theme()
            pulse = 1.0 + 0.12 * math.sin(pygame.time.get_ticks() * 0.01)
            size = int(200 * pulse)
            font = pygame.font.SysFont("Arial", size, bold=True)
            text = font.render(str(self.countdown), True, theme['accent_color'])
            shadow = font.render(str(self.countdown), True, theme['shadow_color'])
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            # Hiệu ứng glow
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

    # ---------------- Va chạm ----------------
    def handle_collisions(self):
        """Xử lý va chạm & luật chơi"""
        
        # Ăn coin
        coins_hit = pygame.sprite.spritecollide(
            self.player, self.coins, dokill=True, collided=pygame.sprite.collide_mask
        )
        if coins_hit:
            self.player.coins_collected += len(coins_hit)
            self.score += int(5 * len(coins_hit) * self.player.score_multiplier)
            # Thêm hiệu ứng thu thập coin
            for coin in coins_hit:
                self.ui_manager.add_coin_collect_effect(coin.rect.centerx, coin.rect.centery)
        
        # Ăn power-up
        power_ups_hit = pygame.sprite.spritecollide(
            self.player, self.power_ups, dokill=True, collided=pygame.sprite.collide_mask
        )
        if power_ups_hit:
            for power_up in power_ups_hit:
                self.power_up_manager.activate_power_up(power_up.power_up_type, self.player)
        
        # Nếu đang bất tử, bỏ qua va chạm với obstacle và monster
        if self.invincible_timer > 0 or self.player.invincible:
            # Vẫn xử lý tree spawn monster
            trees_hit = pygame.sprite.spritecollide(
                self.player, self.trees, dokill=False, collided=pygame.sprite.collide_mask
            )
            for t in trees_hit:
                if not getattr(t, 'called_monster', False):
                    t.called_monster = True
                    self.spawner.spawn_monster_from_tree(t, self.player)
            return False
        
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
        
        # Player đụng trực tiếp monster = thua
        if pygame.sprite.spritecollideany(
            self.player, self.monsters, collided=pygame.sprite.collide_mask
        ):
            self.game.state = "game_over"
            return True
        
        return False



    # ---------------- Loop chính ----------------
    def run(self):
        self.running = True
        while self.running and self.game.running:
            dt = self.clock.tick(FPS)
            self.wave_offset += 5  
            self.scroll_y += 4  
            
            # Cập nhật theme và UI
            self.theme_manager.update(dt)
            self.ui_manager.update(dt)

            # Countdown
            if self.countdown > 0:
                self.countdown_timer += dt
                if self.countdown_timer >= 1000:
                    self.countdown -= 1
                    self.countdown_timer = 0

            # Event
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.mixer.music.stop()  # Dừng nhạc khi thoát
                    self.running = False
                    self.game.running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()  # Dừng nhạc khi quay lại menu
                    self.game.state = "start"
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.countdown > 0 and self.back_button.collidepoint(e.pos):
                        pygame.mixer.music.stop()  # Dừng nhạc khi quay lại menu
                        self.game.state = "start"
                        self.running = False
                    else:
                        # Xử lý click UI
                        ui_action = self.ui_manager.handle_click(e.pos)
                        if ui_action == "pause":
                            # TODO: Implement pause functionality
                            pass
                        elif ui_action == "settings":
                            # TODO: Implement settings functionality
                            pass

            # Vẽ nền
            self.draw_background()

            # Update / spawn
            if self.countdown <= 0:
                self.spawner.maybe_spawn_every_frame(dt)
                self.power_up_manager.update(dt, self.player)
                self.obstacles.update(dt, 0)
                self.coins.update(dt, 0)
                self.treasures.update(dt, 0)
                self.trees.update(dt, 0)
                self.monsters.update(dt, 0)
                self.power_ups.update(dt, 0)
            else:
                # countdown thì update nhẹ thôi
                self.obstacles.update(dt, 0)
                self.coins.update(dt, 0)
                self.treasures.update(dt, 0)
                self.trees.update(dt, 0)
                self.monsters.update(dt, 0)
                self.power_ups.update(dt, 0)

            # Update player (luôn hoạt động để hiệu ứng rơi xuống xuất hiện)
            mouse_pos = pygame.mouse.get_pos()
            self.player.update(dt, mouse_pos)

            # Vẽ sprites
            self.obstacles.draw(self.screen)
            self.trees.draw(self.screen)
            self.coins.draw(self.screen)
            self.treasures.draw(self.screen)
            self.monsters.draw(self.screen)
            
            # Vẽ power-ups với hiệu ứng glow
            for power_up in self.power_ups:
                power_up.draw_glow_effect(self.screen)
            self.power_ups.draw(self.screen)
            # Update invincible timer và hiệu ứng nhấp nháy
            if self.invincible_timer > 0:
                self.invincible_timer -= dt
                self.invincible_blink_timer += dt
                
                # Nhấp nháy: mỗi 150ms đổi alpha
                if int(self.invincible_blink_timer / 150) % 2 == 0:
                    self.player.image.set_alpha(80)
                else:
                    self.player.image.set_alpha(255)
            else:
                self.player.image.set_alpha(255)

            self.player_group.draw(self.screen)

            # HUD
            self.draw_back_button()
            self.draw_countdown()
            self.draw_score()
            
            # Vẽ hiệu ứng theme
            self.theme_manager.draw_transition_effects(self.screen)
            # self.theme_manager.draw_night_effects(self.screen)
            
            # Vẽ hiệu ứng UI
            self.ui_manager.draw_coin_collect_effects(self.screen)
            
            # Vẽ power-up status
            self.ui_manager.draw_power_up_status(self.screen, self.power_up_manager)
            
            # Vẽ nút điều khiển
            mouse_pos = pygame.mouse.get_pos()
            self.ui_manager.draw_control_buttons(self.screen, mouse_pos)

            # Va chạm (sau khi countdown xong)
            if self.countdown <= 0:
                if self.handle_collisions():
                    from screens.gameover import GameOverScreen
                    gameover_screen = GameOverScreen(self.game, self)  # Truyền self (PlayScreen)
                    gameover_screen.run()
                    self.running = False


            pygame.display.flip()

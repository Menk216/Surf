import pygame
import math
from settings import *

class PlayScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        # Background gốc
        self.background = pygame.image.load("resources/assets/backgrounds/test.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Nút back
        self.back_button = pygame.Rect(30, 30, 60, 60)
        self.back_icon = pygame.image.load("resources/assets/icon/return_icon.png").convert_alpha()
        self.back_icon = pygame.transform.smoothscale(self.back_icon, (32, 32))

        # Hiệu ứng sóng
        self.wave_offset = 0

        # Countdown
        self.countdown = 3
        self.countdown_timer = 0
        self.font_big = pygame.font.SysFont("Arial", 120, bold=True)

        # Nhân vật
        self.character_img = pygame.image.load("resources/assets/characters/player.png").convert_alpha()
        self.character_img = pygame.transform.smoothscale(self.character_img, (450, 300))  # cho to hơn
        self.character_pos = [WIDTH // 2, -150]  # bắt đầu từ trên màn hình
        self.character_active = False
        self.scroll_y = 0  # để tạo hiệu ứng màn hình di chuyển

    def draw_background_wave(self):
        """Tạo hiệu ứng gợn sóng cho background"""
        wave_surface = pygame.Surface((WIDTH, HEIGHT))

        for y in range(HEIGHT):
            shift = int(10 * math.sin(y / 30 + self.wave_offset * 0.02))
            line = self.background.subsurface((0, y, WIDTH, 1))
            wave_surface.blit(line, (shift, y))
            if shift > 0:
                wave_surface.blit(line, (shift - WIDTH, y))
            elif shift < 0:
                wave_surface.blit(line, (shift + WIDTH, y))

        # Dời background theo scroll_y
        self.screen.blit(wave_surface, (0, self.scroll_y % HEIGHT - HEIGHT))
        self.screen.blit(wave_surface, (0, self.scroll_y % HEIGHT))

    def draw_back_button(self):
        """Custom nút back"""
        if self.countdown > 0:  # chỉ hiện trong lúc countdown
            button_surface = pygame.Surface(self.back_button.size, pygame.SRCALPHA)
            pygame.draw.rect(button_surface, (0, 0, 0, 100), button_surface.get_rect(), border_radius=15)
            button_surface.blit(
                self.back_icon,
                (
                    self.back_button.width // 2 - self.back_icon.get_width() // 2,
                    self.back_button.height // 2 - self.back_icon.get_height() // 2
                )
            )
            self.screen.blit(button_surface, self.back_button.topleft)

    def draw_countdown(self):
        if self.countdown > 0:
            text = self.font_big.render(str(self.countdown), True, (255, 50, 50))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)

    def draw_character(self):
        if self.character_active:
            # Animation nghiêng trái phải (wave effect)
            angle = math.sin(pygame.time.get_ticks() * 0.005) * 10
            rotated_img = pygame.transform.rotate(self.character_img, angle)
            rect = rotated_img.get_rect(center=self.character_pos)
            self.screen.blit(rotated_img, rect)

    def run(self):
        running = True
        while running and self.game.running:
            dt = self.clock.tick(FPS)
            self.wave_offset += 2

            # Update countdown
            if self.countdown > 0:
                self.countdown_timer += dt
                if self.countdown_timer >= 1000:  # mỗi giây giảm 1
                    self.countdown -= 1
                    self.countdown_timer = 0
                if self.countdown == 0:
                    self.character_active = True

            # Vẽ background
            self.draw_background_wave()

            # Vẽ nút back hoặc countdown
            self.draw_back_button()
            self.draw_countdown()

            # Nhân vật trượt xuống ban đầu
            if self.character_active:
                if self.character_pos[1] < HEIGHT // 2 + 100:  # cho nó trượt xuống tới gần giữa
                    self.character_pos[1] += 5

                # Nhân vật theo chuột
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.character_pos[0] += (mouse_x - self.character_pos[0]) * 0.1
                self.character_pos[1] += (mouse_y - self.character_pos[1]) * 0.05

                # Background di chuyển khi nhân vật di chuyển
                self.scroll_y += 2

                self.draw_character()

            # Xử lý event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.state = "start"
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos) and self.countdown > 0:
                        self.game.state = "start"
                        running = False

            pygame.display.flip()

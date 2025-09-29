import pygame
import random
import math
from settings import *


def draw_gradient_rect(surface, rect, color1, color2, border_radius=0):
    x, y, w, h = rect
    gradient_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(h):
        r = color1[0] + (color2[0] - color1[0]) * i // h
        g = color1[1] + (color2[1] - color1[1]) * i // h
        b = color1[2] + (color2[2] - color1[2]) * i // h
        pygame.draw.line(gradient_surface, (r, g, b), (0, i), (w, i))
    
    rounded_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(rounded_surface, (255, 255, 255), (0, 0, w, h), border_radius=border_radius)
    gradient_surface.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(gradient_surface, (x, y))


class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT + random.randint(0, 300)
        self.size = random.randint(5, 35)
        self.speed = random.uniform(0.5, 3.0)
        self.alpha = random.randint(120, 200)
        self.wobble = random.uniform(0, math.pi * 2)
        self.wobble_speed = random.uniform(0.01, 0.08)
        self.pop_time = random.randint(400, 1000)
        self.age = 0
        
    def update(self):
        self.y -= self.speed
        self.wobble += self.wobble_speed
        self.x += math.sin(self.wobble) * 1.5
        self.age += 1
        
        # Bọt nhỏ dần khi gần "nổ"
        if self.age > self.pop_time * 0.8:
            self.alpha = max(50, self.alpha - 3)
        
        # Reset bọt khi ra khỏi màn hình hoặc "nổ"
        if self.y < -50 or self.age > self.pop_time:
            self.y = HEIGHT + random.randint(0, 300)
            self.x = random.randint(0, WIDTH)
            self.size = random.randint(5, 35)
            self.speed = random.uniform(0.5, 3.0)
            self.alpha = random.randint(120, 200)
            self.age = 0
            self.pop_time = random.randint(400, 1000)
    
    def draw(self, surface):
        # Bọt chính với màu rõ nét hơn
        bubble_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        center = (self.size, self.size)
        
        # Vẽ bóng mờ phía sau
        shadow_color = (100, 180, 255, self.alpha // 4)
        pygame.draw.circle(bubble_surface, shadow_color, (center[0] + 2, center[1] + 2), self.size)
        
        # Gradient từ trong ra ngoài với màu rõ hơn
        for r in range(self.size, 0, -2):
            ratio = r / self.size
            alpha = int(self.alpha * (0.8 - ratio * 0.6))
            
            # Màu xanh biển rõ nét
            r_val = int(150 + ratio * 80)
            g_val = int(220 + ratio * 35)
            b_val = 255
            
            color = (r_val, g_val, b_val, alpha)
            pygame.draw.circle(bubble_surface, color, center, r)
        
        # Viền bọt rõ nét
        pygame.draw.circle(bubble_surface, (255, 255, 255, self.alpha // 2), center, self.size, 2)
        
        # Điểm sáng lớn hơn và rõ hơn
        highlight_pos = (self.size - self.size//3, self.size - self.size//3)
        highlight_size = max(2, self.size//3)
        pygame.draw.circle(bubble_surface, (255, 255, 255, self.alpha), highlight_pos, highlight_size)
        
        # Điểm sáng nhỏ thứ 2
        small_highlight = (self.size + self.size//4, self.size - self.size//2)
        small_size = max(1, self.size//6)
        pygame.draw.circle(bubble_surface, (255, 255, 255, self.alpha // 2), small_highlight, small_size)
        
        surface.blit(bubble_surface, (self.x - self.size, self.y - self.size))


class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        # Background
        self.background = pygame.image.load("resources/assets/backgrounds/bg_startgame2.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Font chữ
        self.title_font = pygame.font.Font("resources/assets/fonts/ClimateCrisis-Regular-VariableFont_YEAR.ttf", 120)
        self.button_font = pygame.font.SysFont("Segoe UI", 48, bold=True)

        # Text tiêu đề
        self.title_text = self.title_font.render("Fantascy Suffer", True, (125, 147, 255))

        # Nút start
        self.button_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 100)
        self.button_text = self.button_font.render("Start", True, (255, 255, 255))
        
        # Hiệu ứng - tăng số lượng bọt
        self.bubbles = [Bubble() for _ in range(120)]
        self.wave_offset = 0
        self.button_pulse = 0
        self.title_float = 0
        
    def draw_waves(self):
        wave_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(3):
            wave_y = HEIGHT - 100 + i * 30
            points = []
            for x in range(0, WIDTH + 20, 20):
                y = wave_y + math.sin((x + self.wave_offset + i * 50) * 0.01) * 15
                points.append((x, y))
            
            if len(points) > 2:
                points.append((WIDTH, HEIGHT))
                points.append((0, HEIGHT))
                pygame.draw.polygon(wave_surface, (100, 150, 255, 30 - i * 10), points)
        
        self.screen.blit(wave_surface, (0, 0))

    def run(self):
        running = True
        while running and self.game.running:
            dt = self.clock.tick(FPS)
            self.wave_offset += 2
            self.button_pulse += 0.1
            self.title_float += 0.05
            
            self.screen.blit(self.background, (0, 0))
            
            # Vẽ gợn sóng
            self.draw_waves()
            
            # Vẽ bọt biển
            for bubble in self.bubbles:
                bubble.update()
                bubble.draw(self.screen)
            
            # Vẽ tiêu đề với hiệu ứng float
            title_y = HEIGHT // 4 + math.sin(self.title_float) * 5
            self.screen.blit(self.title_text, (WIDTH // 2 - self.title_text.get_width() // 2, title_y))
            
            # Nút Start luôn có hiệu ứng đẹp
            mouse_pos = pygame.mouse.get_pos()
            pulse_size = math.sin(self.button_pulse) * 8
            glow_size = math.sin(self.button_pulse * 0.7) * 15
            
            # Hiệu ứng ánh sáng xung quanh nút
            glow_rect = self.button_rect.inflate(20 + glow_size, 10 + glow_size//2)
            draw_gradient_rect(self.screen, glow_rect,
                             (60, 120, 200, 30), (100, 160, 240, 50), border_radius=40)
            
            # Nút chính với hiệu ứng pulse
            main_rect = self.button_rect.inflate(pulse_size, pulse_size//2)
            draw_gradient_rect(self.screen, main_rect,
                             (120, 220, 255), (200, 140, 255), border_radius=35)
            
            # Viền sáng động
            border_alpha = int(100 + math.sin(self.button_pulse * 1.5) * 50)
            pygame.draw.rect(self.screen, (255, 255, 255, border_alpha), main_rect, 3, border_radius=35)
            
            # Hiệu ứng lấp lánh
            for i in range(5):
                sparkle_x = self.button_rect.centerx + random.randint(-150, 150)
                sparkle_y = self.button_rect.centery + random.randint(-30, 30)
                sparkle_alpha = random.randint(50, 150)
                pygame.draw.circle(self.screen, (255, 255, 255, sparkle_alpha), 
                                 (sparkle_x, sparkle_y), random.randint(1, 3))

            # Vẽ chữ trên nút
            self.screen.blit(self.button_text,
                           (self.button_rect.centerx - self.button_text.get_width() // 2,
                            self.button_rect.centery - self.button_text.get_height() // 2))

            # Sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                        self.game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(mouse_pos):
                        self.game.state = "play"
                        running = False

            pygame.display.flip()

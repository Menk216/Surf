import pygame
import random
import math
from settings import *
from utils import resource_path

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
        
        if self.age > self.pop_time * 0.8:
            self.alpha = max(50, self.alpha - 3)
        
        if self.y < -50 or self.age > self.pop_time:
            self.y = HEIGHT + random.randint(0, 300)
            self.x = random.randint(0, WIDTH)
            self.size = random.randint(5, 35)
            self.speed = random.uniform(0.5, 3.0)
            self.alpha = random.randint(120, 200)
            self.age = 0
            self.pop_time = random.randint(400, 1000)
    
    def draw(self, surface):

        bubble_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        center = (self.size, self.size)
        
        shadow_color = (100, 180, 255, self.alpha // 4)
        pygame.draw.circle(bubble_surface, shadow_color, (center[0] + 2, center[1] + 2), self.size)
        
        for r in range(self.size, 0, -2):
            ratio = r / self.size
            alpha = int(self.alpha * (0.8 - ratio * 0.6))
            
            r_val = int(150 + ratio * 80)
            g_val = int(220 + ratio * 35)
            b_val = 255
            
            color = (r_val, g_val, b_val, alpha)
            pygame.draw.circle(bubble_surface, color, center, r)
        
        pygame.draw.circle(bubble_surface, (255, 255, 255, self.alpha // 2), center, self.size, 2)
        
        highlight_pos = (self.size - self.size//3, self.size - self.size//3)
        highlight_size = max(2, self.size//3)
        pygame.draw.circle(bubble_surface, (255, 255, 255, self.alpha), highlight_pos, highlight_size)
        
        small_highlight = (self.size + self.size//4, self.size - self.size//2)
        small_size = max(1, self.size//6)
        pygame.draw.circle(bubble_surface, (255, 255, 255, self.alpha // 2), small_highlight, small_size)
        
        surface.blit(bubble_surface, (self.x - self.size, self.y - self.size))

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        self.background = pygame.image.load(resource_path("resources/assets/backgrounds/bg_startgame2.jpg"))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.title_font = pygame.font.Font(resource_path("resources/assets/fonts/ClimateCrisis-Regular-VariableFont_YEAR.ttf"), 120)
        self.button_font = pygame.font.Font(None, 48)

        self.title_text = self.title_font.render("Fantascy Suffer", True, (125, 147, 255))

        self.button_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 100)
        self.button_text = self.button_font.render("Start", True, (255, 255, 255))

        self.settings_button = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 130, 400, 80)
        self.settings_text = self.button_font.render("Settings", True, (255, 255, 255))

        self.quit_button = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 240, 400, 80)
        self.quit_text = self.button_font.render("Quit", True, (255, 255, 255))

        self.bubbles = [Bubble() for _ in range(120)]
        self.wave_offset = 0
        self.button_pulse = 0
        self.title_float = 0
        
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(resource_path("resources/assets/sound/sound.mp3"))
            import settings as settings_module
            pygame.mixer.music.set_volume(settings_module.CURRENT_VOLUME)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Không thể tải nhạc nền: {e}")
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
            
            self.draw_waves()
            
            for bubble in self.bubbles:
                bubble.update()
                bubble.draw(self.screen)
            
            title_y = HEIGHT // 4 + math.sin(self.title_float) * 5
            self.screen.blit(self.title_text, (WIDTH // 2 - self.title_text.get_width() // 2, title_y))
            
            mouse_pos = pygame.mouse.get_pos()
            pulse_size = math.sin(self.button_pulse) * 8
            glow_size = math.sin(self.button_pulse * 0.7) * 15
            
            glow_rect = self.button_rect.inflate(20 + glow_size, 10 + glow_size//2)
            draw_gradient_rect(self.screen, glow_rect,
                             (60, 120, 200, 30), (100, 160, 240, 50), border_radius=40)
            
            main_rect = self.button_rect.inflate(pulse_size, pulse_size//2)
            draw_gradient_rect(self.screen, main_rect,
                             (120, 220, 255), (200, 140, 255), border_radius=35)
            
            border_alpha = int(100 + math.sin(self.button_pulse * 1.5) * 50)
            pygame.draw.rect(self.screen, (255, 255, 255, border_alpha), main_rect, 3, border_radius=35)
            
            for i in range(5):
                sparkle_x = self.button_rect.centerx + random.randint(-150, 150)
                sparkle_y = self.button_rect.centery + random.randint(-30, 30)
                sparkle_alpha = random.randint(50, 150)
                pygame.draw.circle(self.screen, (255, 255, 255, sparkle_alpha), 
                                 (sparkle_x, sparkle_y), random.randint(1, 3))

            self.screen.blit(self.button_text,
                           (self.button_rect.centerx - self.button_text.get_width() // 2,
                            self.button_rect.centery - self.button_text.get_height() // 2))

            settings_pulse = math.sin(self.button_pulse * 0.8) * 6
            settings_glow = math.sin(self.button_pulse * 0.5) * 12

            settings_glow_rect = self.settings_button.inflate(15 + settings_glow, 8 + settings_glow//2)
            draw_gradient_rect(self.screen, settings_glow_rect,
                            (60, 120, 200, 25), (100, 160, 240, 45), border_radius=35)

            settings_main_rect = self.settings_button.inflate(settings_pulse, settings_pulse//2)
            draw_gradient_rect(self.screen, settings_main_rect,
                            (100, 180, 240), (180, 120, 240), border_radius=30)

            settings_border_alpha = int(80 + math.sin(self.button_pulse * 1.2) * 40)
            pygame.draw.rect(self.screen, (255, 255, 255, settings_border_alpha), 
                            settings_main_rect, 3, border_radius=30)

            self.screen.blit(self.settings_text,
                            (self.settings_button.centerx - self.settings_text.get_width() // 2,
                            self.settings_button.centery - self.settings_text.get_height() // 2))

            quit_pulse = math.sin(self.button_pulse * 0.6) * 5
            quit_glow = math.sin(self.button_pulse * 0.4) * 10

            quit_glow_rect = self.quit_button.inflate(12 + quit_glow, 6 + quit_glow//2)
            draw_gradient_rect(self.screen, quit_glow_rect,
                            (80, 50, 50, 20), (120, 70, 70, 40), border_radius=32)

            quit_main_rect = self.quit_button.inflate(quit_pulse, quit_pulse//2)
            draw_gradient_rect(self.screen, quit_main_rect,
                            (220, 80, 80), (180, 50, 50), border_radius=28)

            quit_border_alpha = int(70 + math.sin(self.button_pulse) * 35)
            pygame.draw.rect(self.screen, (255, 150, 150, quit_border_alpha), 
                            quit_main_rect, 3, border_radius=28)

            self.screen.blit(self.quit_text,
                            (self.quit_button.centerx - self.quit_text.get_width() // 2,
                            self.quit_button.centery - self.quit_text.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    running = False
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        pygame.mixer.music.stop()
                        running = False
                        self.game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        self.game.state = "play"
                        running = False
                    elif self.settings_button.collidepoint(mouse_pos):
                        self.game.state = "settings"
                        running = False
                    elif self.quit_button.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        self.game.running = False
                        running = False

            pygame.display.flip()

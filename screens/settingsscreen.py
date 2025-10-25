import pygame
import random
import math
from settings import *
from utils import resource_path

def draw_gradient_rect(surface, rect, color1, color2, border_radius=0):
    """Vẽ gradient cho button"""
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
    """Class hiệu ứng bọt biển giống màn hình start"""
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

class SettingsScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        
        self.background = pygame.image.load(resource_path("resources/assets/backgrounds/bg_startgame2.jpg"))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        self.title_font = pygame.font.Font(resource_path("resources/assets/fonts/ClimateCrisis-Regular-VariableFont_YEAR.ttf"), 100)
        self.label_font = pygame.font.Font(None, 52)
        self.button_font = pygame.font.Font(None, 40)
        
        self.title_text = self.title_font.render("Settings", True, (125, 147, 255))
        
        self.bubbles = [Bubble() for _ in range(100)]
        self.wave_offset = 0
        self.title_float = 0
        
        import settings as settings_module
        self.volume = settings_module.CURRENT_VOLUME
        self.difficulty = settings_module.CURRENT_DIFFICULTY
        
        self.volume_slider_x = WIDTH // 2 - 250
        self.volume_slider_y = HEIGHT // 2 - 80
        self.volume_slider_width = 500
        self.volume_slider_height = 20
        
        self.volume_slider_rect = pygame.Rect(
            self.volume_slider_x, 
            self.volume_slider_y,
            self.volume_slider_width, 
            self.volume_slider_height
        )
        
        slider_handle_x = self.volume_slider_x + int(self.volume * self.volume_slider_width)
        self.volume_handle = pygame.Rect(slider_handle_x - 15, self.volume_slider_y - 10, 30, 40)
        self.dragging_volume = False
        
        button_y = HEIGHT // 2 + 60
        button_spacing = 180
        center_x = WIDTH // 2
        
        self.easy_button = pygame.Rect(center_x - button_spacing - 60, button_y, 120, 60)
        self.medium_button = pygame.Rect(center_x - 60, button_y, 120, 60)
        self.hard_button = pygame.Rect(center_x + button_spacing - 60, button_y, 120, 60)
        
        self.back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 70)
        
        self.button_pulse = 0
    
    def draw_waves(self):
        """Vẽ hiệu ứng sóng biển"""
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
    
    def draw_slider(self):
        """Vẽ thanh trượt âm lượng"""

        volume_label = self.label_font.render("Volume", True, (255, 255, 255))
        self.screen.blit(volume_label, (self.volume_slider_x, self.volume_slider_y - 60))
        
        pygame.draw.rect(self.screen, (80, 100, 150), self.volume_slider_rect, border_radius=10)
        
        filled_width = int(self.volume * self.volume_slider_width)
        filled_rect = pygame.Rect(
            self.volume_slider_x,
            self.volume_slider_y,
            filled_width,
            self.volume_slider_height
        )
        pygame.draw.rect(self.screen, (120, 220, 255), filled_rect, border_radius=10)
        
        pygame.draw.circle(self.screen, (200, 140, 255), self.volume_handle.center, 20)
        pygame.draw.circle(self.screen, (255, 255, 255), self.volume_handle.center, 20, 3)
        
        volume_percent = self.label_font.render(f"{int(self.volume * 100)}%", True, (255, 255, 255))
        self.screen.blit(volume_percent, (self.volume_slider_x + self.volume_slider_width + 30, self.volume_slider_y - 15))
    
    def draw_difficulty_buttons(self):
        """Vẽ các nút chọn độ khó"""
        mouse_pos = pygame.mouse.get_pos()
        
        difficulty_label = self.label_font.render("Difficulty", True, (255, 255, 255))
        label_x = WIDTH // 2 - difficulty_label.get_width() // 2
        self.screen.blit(difficulty_label, (label_x, self.easy_button.y - 60))
        
        buttons = [
            (self.easy_button, "Easy", "easy"),
            (self.medium_button, "Medium", "medium"),
            (self.hard_button, "Hard", "hard")
        ]
        
        for button_rect, text, diff_value in buttons:
            is_selected = (self.difficulty == diff_value)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            if is_selected:
                color1 = (200, 140, 255)
                color2 = (120, 220, 255)
                border_color = (255, 255, 255)
                text_color = (255, 255, 255)
            elif is_hovered:
                color1 = (100, 180, 240)
                color2 = (150, 120, 240)
                border_color = (200, 200, 200)
                text_color = (255, 255, 255)
            else:
                color1 = (80, 120, 180)
                color2 = (100, 140, 200)
                border_color = (150, 150, 150)
                text_color = (200, 200, 200)
            
            if is_selected:
                glow_rect = button_rect.inflate(10, 10)
                draw_gradient_rect(self.screen, glow_rect, (60, 120, 200, 30), (100, 160, 240, 50), border_radius=20)
            
            draw_gradient_rect(self.screen, button_rect, color1, color2, border_radius=15)
            pygame.draw.rect(self.screen, border_color, button_rect, 3, border_radius=15)
            
            button_text = self.button_font.render(text, True, text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
    
    def draw_back_button(self):
        """Vẽ nút Back"""
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.back_button.collidepoint(mouse_pos)
        
        pulse_size = math.sin(self.button_pulse) * 5 if is_hovered else 0
        
        if is_hovered:
            glow_rect = self.back_button.inflate(15, 10)
            draw_gradient_rect(self.screen, glow_rect, (60, 120, 200, 30), (100, 160, 240, 50), border_radius=25)
        
        main_rect = self.back_button.inflate(pulse_size, pulse_size//2)
        draw_gradient_rect(self.screen, main_rect, (120, 220, 255), (200, 140, 255), border_radius=20)
        
        border_alpha = int(100 + math.sin(self.button_pulse * 1.5) * 50) if is_hovered else 150
        pygame.draw.rect(self.screen, (255, 255, 255, border_alpha), main_rect, 3, border_radius=20)
        
        button_text = self.button_font.render("Back", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=self.back_button.center)
        self.screen.blit(button_text, text_rect)
    
    def handle_volume_drag(self, mouse_pos):
        """Xử lý kéo thanh âm lượng"""
        if self.volume_slider_x <= mouse_pos[0] <= self.volume_slider_x + self.volume_slider_width:
            self.volume = (mouse_pos[0] - self.volume_slider_x) / self.volume_slider_width
            self.volume = max(0.0, min(1.0, self.volume))
            
            slider_handle_x = self.volume_slider_x + int(self.volume * self.volume_slider_width)
            self.volume_handle.centerx = slider_handle_x
            
            pygame.mixer.music.set_volume(self.volume)
    
    def save_settings(self):
        """Lưu cài đặt vào module settings"""
        import settings as settings_module
        settings_module.CURRENT_VOLUME = self.volume
        settings_module.CURRENT_DIFFICULTY = self.difficulty
        
        pygame.mixer.music.set_volume(self.volume)
    
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
            
            title_y = 80 + math.sin(self.title_float) * 5
            self.screen.blit(self.title_text, (WIDTH // 2 - self.title_text.get_width() // 2, title_y))
            
            self.draw_slider()
            self.draw_difficulty_buttons()
            self.draw_back_button()
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_settings()
                    running = False
                    self.game.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.save_settings()
                        self.game.state = "start"
                        running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if self.volume_handle.collidepoint(mouse_pos):
                        self.dragging_volume = True
                    
                    elif self.volume_slider_rect.collidepoint(mouse_pos):
                        self.handle_volume_drag(mouse_pos)
                        self.dragging_volume = True
                    
                    elif self.easy_button.collidepoint(mouse_pos):
                        self.difficulty = "easy"
                    elif self.medium_button.collidepoint(mouse_pos):
                        self.difficulty = "medium"
                    elif self.hard_button.collidepoint(mouse_pos):
                        self.difficulty = "hard"
                    
                    elif self.back_button.collidepoint(mouse_pos):
                        self.save_settings()
                        self.game.state = "start"
                        running = False
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging_volume = False
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_volume:
                        self.handle_volume_drag(mouse_pos)
            
            pygame.display.flip()

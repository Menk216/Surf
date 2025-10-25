import pygame
import math
import random
from utils import resource_path

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.theme_timer = 0
        self.theme_duration = 30000
        self.transition_timer = 0
        self.transition_duration = 2000
        self.is_transitioning = False
        
        self.themes = {
            "light": {
                "name": "Ngày",
                "background_color": (135, 206, 250),
                "water_color": (64, 164, 223),
                "ui_color": (255, 255, 255),
                "text_color": (0, 0, 0),
                "accent_color": (255, 215, 0),
                "shadow_color": (0, 0, 0, 50),
                "glow_color": (255, 255, 255, 100),
                "particle_color": (255, 255, 255),
                "ambient_light": 1.0,
                "wave_intensity": 1.0,
                "background_image": resource_path("resources/assets/backgrounds/test.jpg")            
                },
            "dark": {
                "name": "Đêm",
                "background_color": (2, 2, 15),
                "water_color": (0, 0, 30),
                "ui_color": (10, 10, 10),
                "text_color": (255, 255, 255),
                "accent_color": (150, 200, 255),
                "shadow_color": (0, 0, 0, 200),
                "glow_color": (100, 150, 255, 150),
                "particle_color": (100, 150, 255),
                "ambient_light": 0.1,
                "wave_intensity": 0.3,
                "background_image": resource_path("resources/assets/backgrounds/test.jpg")            
                }
        }

        self.transition_particles = []
    
    def get_current_theme(self):
        return self.themes[self.current_theme]
    
    def update(self, dt):
        """Cập nhật thời gian và trạng thái chuyển theme"""
        self.theme_timer += dt
        
        if self.theme_timer >= self.theme_duration:
            self.start_transition()
            self.theme_timer = 0
        
        if self.is_transitioning:
            self.transition_timer += dt
            self.update_transition_effects()
            if self.transition_timer >= self.transition_duration:
                self.complete_transition()
    
    def start_transition(self):
        """Bắt đầu hiệu ứng chuyển"""
        if not self.is_transitioning:
            self.is_transitioning = True
            self.transition_timer = 0
            self.create_transition_particles()
    
    def create_transition_particles(self):
        """Hạt chuyển đổi"""
        self.transition_particles = []
        for _ in range(10):
            particle = {
                'x': random.randint(0, 1920),
                'y': random.randint(0, 1080),
                'size': random.randint(2, 4),
                'speed': random.uniform(1, 1.5),
                'alpha': random.randint(80, 150),
                'color': random.choice([
                    (255, 255, 255),
                    (255, 215, 0),
                    (100, 100, 255)
                ])
            }
            self.transition_particles.append(particle)
    
    def update_transition_effects(self):
        """Cập nhật hiệu ứng hạt"""
        for p in self.transition_particles:
            p['y'] -= p['speed']
            p['alpha'] -= 2
            if p['alpha'] <= 0:
                p['alpha'] = 255
                p['y'] = 1080
                p['x'] = random.randint(0, 1920)
    
    def complete_transition(self):
        """Kết thúc hiệu ứng chuyển"""
        self.is_transitioning = False
        self.transition_timer = 0
        
        self.current_theme = "dark" if self.current_theme == "light" else "light"
    
    def draw_transition_effects(self, screen):
        """Vẽ hiệu ứng chuyển"""
        if not self.is_transitioning:
            return
        
        for p in self.transition_particles:
            color = (*p['color'], p['alpha'])
            pygame.draw.circle(screen, color,
                             (int(p['x']), int(p['y'])),
                             p['size'])
        
        fade_alpha = int(100 * (self.transition_timer / self.transition_duration))
        fade_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, fade_alpha))
        screen.blit(fade_surface, (0, 0))
    
    def get_theme_progress(self):
        """Tiến độ theme"""
        return self.theme_timer / self.theme_duration
    
    def get_transition_progress(self):
        """Tiến độ chuyển"""
        return 0 if not self.is_transitioning else self.transition_timer / self.transition_duration

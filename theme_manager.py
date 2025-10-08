# theme_manager.py
import pygame
import math
import random

class ThemeManager:
    def __init__(self):
        # Theme hiện tại
        self.current_theme = "light"  # "light" hoặc "dark"
        self.theme_timer = 0
        self.theme_duration = 30000  # 30 giây (ms)
        self.transition_timer = 0
        self.transition_duration = 2000  # 2 giây chuyển đổi
        self.is_transitioning = False
        
        # Định nghĩa các theme
        self.themes = {
            "light": {
                "name": "Ngày",
                "background_color": (135, 206, 250),  # Sky blue
                "water_color": (64, 164, 223),        # Deep sky blue
                "ui_color": (255, 255, 255),         # White
                "text_color": (0, 0, 0),             # Black
                "accent_color": (255, 215, 0),       # Gold
                "shadow_color": (0, 0, 0, 50),      # Black with alpha
                "glow_color": (255, 255, 255, 100),  # White glow
                "particle_color": (255, 255, 255),   # White particles
                "ambient_light": 1.0,
                "wave_intensity": 1.0,
                "background_image": "resources/assets/backgrounds/test.jpg"
            },
            "dark": {
                "name": "Đêm",
                "background_color": (2, 2, 15),     # Very dark blue
                "water_color": (0, 0, 30),          # Very dark blue water
                "ui_color": (10, 10, 10),          # Very dark gray
                "text_color": (255, 255, 255),       # Bright white text
                "accent_color": (150, 200, 255),     # Bright blue accent
                "shadow_color": (0, 0, 0, 200),     # Black with more alpha
                "glow_color": (100, 150, 255, 150), # Blue glow
                "particle_color": (100, 150, 255),   # Blue particles
                "ambient_light": 0.1,               # Very dark
                "wave_intensity": 0.3,               # Less wave effect
                "background_image": "resources/assets/backgrounds/test.jpg"
            }
        }
        
        # Hiệu ứng chuyển đổi
        self.transition_particles = []
        self.star_particles = []
        self.moon_phase = 0
        
    def get_current_theme(self):
        """Lấy theme hiện tại"""
        return self.themes[self.current_theme]
    
    def update(self, dt):
        """Cập nhật theme timer và hiệu ứng"""
        self.theme_timer += dt
        
        # Kiểm tra chuyển đổi theme
        if self.theme_timer >= self.theme_duration:
            self.start_transition()
            self.theme_timer = 0
        
        # Cập nhật hiệu ứng chuyển đổi
        if self.is_transitioning:
            self.transition_timer += dt
            self.update_transition_effects()
            
            if self.transition_timer >= self.transition_duration:
                self.complete_transition()
        
        # Cập nhật hiệu ứng đặc biệt cho theme đêm
        if self.current_theme == "dark":
            self.update_night_effects()
    
    def start_transition(self):
        """Bắt đầu chuyển đổi theme"""
        if not self.is_transitioning:
            self.is_transitioning = True
            self.transition_timer = 0
            self.create_transition_particles()
    
    def create_transition_particles(self):
        """Tạo hiệu ứng hạt chuyển đổi (tối ưu hóa)"""
        self.transition_particles = []
        for _ in range(10):  # Giảm từ 20 xuống 10
            particle = {
                'x': random.randint(0, 1920),
                'y': random.randint(0, 1080),
                'size': random.randint(2, 4),  # Giảm kích thước
                'speed': random.uniform(1, 1.5),  # Giảm tốc độ
                'alpha': random.randint(80, 150),  # Giảm alpha
                'color': random.choice([(255, 255, 255), (255, 215, 0), (100, 100, 255)])
            }
            self.transition_particles.append(particle)
    
    def update_transition_effects(self):
        """Cập nhật hiệu ứng chuyển đổi"""
        for particle in self.transition_particles:
            particle['y'] -= particle['speed']
            particle['alpha'] -= 2
            if particle['alpha'] <= 0:
                particle['alpha'] = 255
                particle['y'] = 1080
                particle['x'] = random.randint(0, 1920)
    
    def complete_transition(self):
        """Hoàn thành chuyển đổi theme"""
        self.is_transitioning = False
        self.transition_timer = 0
        
        # Chuyển đổi theme
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        
        # Tạo hiệu ứng sao cho theme đêm
        if self.current_theme == "dark":
            self.create_star_field()
    
    def create_star_field(self):
        """Tạo trường sao cho theme đêm (tối ưu hóa)"""
        self.star_particles = []
        for _ in range(25):  # Giảm từ 50 xuống 25
            star = {
                'x': random.randint(0, 1920),
                'y': random.randint(0, 200),  # Giảm vùng hiển thị
                'size': random.randint(1, 2),  # Giảm kích thước
                'twinkle': random.uniform(0, 2 * math.pi),
                'twinkle_speed': random.uniform(0.005, 0.03),  # Giảm tốc độ
                'brightness': random.randint(100, 180)  # Giảm độ sáng
            }
            self.star_particles.append(star)
    
    def update_night_effects(self):
        """Cập nhật hiệu ứng đêm"""
        for star in self.star_particles:
            star['twinkle'] += star['twinkle_speed']
            star['brightness'] = int(150 + 105 * math.sin(star['twinkle']))
    
    def draw_transition_effects(self, screen):
        """Vẽ hiệu ứng chuyển đổi"""
        if self.is_transitioning:
            # Vẽ hạt chuyển đổi
            for particle in self.transition_particles:
                color = (*particle['color'], particle['alpha'])
                pygame.draw.circle(screen, color, 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
            
            # Hiệu ứng fade với màu tối hơn
            fade_alpha = int(100 * (self.transition_timer / self.transition_duration))
            fade_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, fade_alpha))
            screen.blit(fade_surface, (0, 0))
    
    def draw_night_effects(self, screen):
        """Vẽ hiệu ứng đêm"""
        if self.current_theme == "dark":
            # Vẽ sao
            for star in self.star_particles:
                color = (255, 255, 255, star['brightness'])
                pygame.draw.circle(screen, color, 
                                 (int(star['x']), int(star['y'])), 
                                 star['size'])
            
            # Vẽ mặt trăng
            moon_x = 1600
            moon_y = 100
            moon_radius = 40
            
            # Mặt trăng với phase
            self.moon_phase += 0.01
            phase_offset = int(20 * math.sin(self.moon_phase))
            
            # Vẽ mặt trăng
            pygame.draw.circle(screen, (255, 255, 200), 
                             (moon_x, moon_y), moon_radius)
            
            # Vẽ phase của mặt trăng
            phase_rect = pygame.Rect(moon_x - moon_radius + phase_offset, 
                                    moon_y - moon_radius, 
                                    moon_radius * 2 - abs(phase_offset), 
                                    moon_radius * 2)
            pygame.draw.rect(screen, self.get_current_theme()['background_color'], phase_rect)
    
    def get_theme_progress(self):
        """Lấy tiến độ theme hiện tại (0-1)"""
        return self.theme_timer / self.theme_duration
    
    def get_transition_progress(self):
        """Lấy tiến độ chuyển đổi (0-1)"""
        if not self.is_transitioning:
            return 0
        return self.transition_timer / self.transition_duration

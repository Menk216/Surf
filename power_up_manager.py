# power_up_manager.py
import pygame
import random
import math
from settings import *

class PowerUpManager:
    def __init__(self, game, groups, images):
        self.game = game
        self.groups = groups
        self.images = images
        
        # Power-up types
        self.power_up_types = {
            'shield': {
                'name': 'Khiên Bảo Vệ',
                'duration': 10000,  # 10 giây
                'color': (0, 255, 255),
                'spawn_rate': 0.1,  # 10% chance per second
                'icon': '🛡'
            },
            'speed_boost': {
                'name': 'Tăng Tốc',
                'duration': 8000,   # 8 giây
                'color': (255, 255, 0),
                'spawn_rate': 0.15,
                'icon': '⚡'
            },
            'magnet': {
                'name': 'Nam Châm',
                'duration': 12000,  # 12 giây
                'color': (255, 0, 255),
                'spawn_rate': 0.08,
                'icon': '🧲'
            },
            'double_score': {
                'name': 'Điểm Kép',
                'duration': 15000,  # 15 giây
                'color': (255, 165, 0),
                'spawn_rate': 0.05,
                'icon': '⭐'
            }
        }
        
        # Active power-ups
        self.active_power_ups = {}
        self.power_up_timers = {}
        
        # Spawn timer
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 20000  # 20 giây
        
    def update(self, dt, player):
        """Cập nhật power-ups"""
        current_time = pygame.time.get_ticks()
        
        # Spawn power-ups
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_random_power_up()
            self.last_spawn_time = current_time
        
        # Update active power-ups
        for power_up_type in list(self.active_power_ups.keys()):
            self.power_up_timers[power_up_type] -= dt
            if self.power_up_timers[power_up_type] <= 0:
                self.deactivate_power_up(power_up_type, player)
        
        # Apply power-up effects
        self.apply_power_up_effects(player)
    
    def spawn_random_power_up(self):
        """Spawn một power-up ngẫu nhiên"""
        power_up_type = random.choice(list(self.power_up_types.keys()))
        x = random.randint(100, WIDTH - 100)
        y = -100
        
        power_up = PowerUp(
            power_up_type,
            self.power_up_types[power_up_type],
            x, y,
            size=(80, 80),
            speed=4
        )
        
        self.groups['power_ups'].add(power_up)
    
    def activate_power_up(self, power_up_type, player):
        """Kích hoạt power-up"""
        if power_up_type in self.active_power_ups:
            # Reset timer nếu đã có
            self.power_up_timers[power_up_type] = self.power_up_types[power_up_type]['duration']
        else:
            # Thêm power-up mới
            self.active_power_ups[power_up_type] = True
            self.power_up_timers[power_up_type] = self.power_up_types[power_up_type]['duration']
    
    def deactivate_power_up(self, power_up_type, player):
        """Hủy kích hoạt power-up"""
        if power_up_type in self.active_power_ups:
            del self.active_power_ups[power_up_type]
            del self.power_up_timers[power_up_type]
    
    def apply_power_up_effects(self, player):
        """Áp dụng hiệu ứng power-up"""
        # Shield effect
        if 'shield' in self.active_power_ups:
            player.invincible = True
        else:
            player.invincible = False
        
        # Speed boost effect
        if 'speed_boost' in self.active_power_ups:
            player.speed_multiplier = 1.5
        else:
            player.speed_multiplier = 1.0
        
        # Magnet effect
        if 'magnet' in self.active_power_ups:
            player.magnet_active = True
        else:
            player.magnet_active = False
        
        # Double score effect
        if 'double_score' in self.active_power_ups:
            player.score_multiplier = 2.0
        else:
            player.score_multiplier = 1.0
    
    def get_active_power_ups(self):
        """Lấy danh sách power-ups đang hoạt động"""
        return self.active_power_ups.copy()
    
    def get_power_up_timer(self, power_up_type):
        """Lấy thời gian còn lại của power-up"""
        return self.power_up_timers.get(power_up_type, 0)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, power_up_data, x, y, size=(80, 80), speed=4):
        super().__init__()
        self.power_up_type = power_up_type
        self.power_up_data = power_up_data
        
        # Tạo surface cho power-up
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        
        # Animation
        self.rotation = 0
        self.pulse_timer = 0
        self.glow_timer = 0
        
        # Vẽ power-up
        self.draw_power_up()
    
    def draw_power_up(self):
        """Vẽ power-up với hiệu ứng"""
        size = self.image.get_width()
        center = size // 2
        
        # Background circle với gradient
        for i in range(size // 2):
            alpha = int(200 * (1 - i / (size // 2)))
            color = (*self.power_up_data['color'], alpha)
            pygame.draw.circle(self.image, color, (center, center), size // 2 - i)
        
        # Border
        pygame.draw.circle(self.image, (255, 255, 255), (center, center), size // 2, 3)
        
        # Icon
        font = pygame.font.SysFont("Arial", size // 2, bold=True)
        icon_text = font.render(self.power_up_data['icon'], True, (255, 255, 255))
        icon_rect = icon_text.get_rect(center=(center, center))
        self.image.blit(icon_text, icon_rect)
    
    def update(self, dt, scroll_speed=0):
        """Cập nhật power-up"""
        self.rect.y += int(self.speed + scroll_speed)
        
        # Animation
        self.rotation += dt * 0.1
        self.pulse_timer += dt * 0.005
        self.glow_timer += dt * 0.003
        
        # Xoay
        old_center = self.rect.center
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = rotated_image.get_rect(center=old_center)
        self.mask = pygame.mask.from_surface(rotated_image)
        
        # Pulse effect
        pulse_scale = 1.0 + 0.1 * math.sin(self.pulse_timer)
        original_size = self.image.get_width()
        scaled_size = int(original_size * pulse_scale)
        if scaled_size != original_size:
            self.image = pygame.transform.scale(self.image, (scaled_size, scaled_size))
            self.rect = self.image.get_rect(center=old_center)
        
        # Xóa khi ra khỏi màn hình
        if self.rect.top > HEIGHT + 50:
            self.kill()
    
    def draw_glow_effect(self, surface):
        """Vẽ hiệu ứng glow"""
        glow_size = int(20 * (1 + 0.5 * math.sin(self.glow_timer)))
        glow_surface = pygame.Surface((self.rect.width + glow_size * 2, 
                                     self.rect.height + glow_size * 2), pygame.SRCALPHA)
        
        for i in range(glow_size):
            alpha = int(50 * (1 - i / glow_size))
            glow_color = (*self.power_up_data['color'], alpha)
            pygame.draw.circle(glow_surface, glow_color, 
                             (glow_surface.get_width() // 2, glow_surface.get_height() // 2),
                             self.rect.width // 2 + i)
        
        surface.blit(glow_surface, (self.rect.x - glow_size, self.rect.y - glow_size))

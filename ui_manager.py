import pygame
import math
import random
from utils import resource_path

class UIManager:
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager

        self.score_font = pygame.font.Font(None, 48)
        self.coin_font = pygame.font.Font(None, 44)
        self.button_font = pygame.font.Font(None, 32)

        self.score_panel_rect = pygame.Rect(1600, 20, 320, 100)
        self.coin_panel_rect = pygame.Rect(1600, 130, 320, 80)
        
        self.score_pulse = 0
        self.coin_sparkle_timer = 0
        self.button_hover_timer = 0

        self.score_glow_timer = 0
        self.coin_collect_effects = []
        
    def update(self, dt):
        """Cập nhật animations và effects (tối ưu hóa)"""
        self.score_pulse += dt * 0.001
        self.coin_sparkle_timer += dt * 0.002
        self.button_hover_timer += dt * 0.0005
        self.score_glow_timer += dt * 0.001
   
        for effect in self.coin_collect_effects[:]:
            effect['timer'] += dt
            effect['y'] -= effect['speed']
            effect['alpha'] -= effect['fade_speed']
            
            if effect['alpha'] <= 0:
                self.coin_collect_effects.remove(effect)
    
    def add_coin_collect_effect(self, x, y):
        """Thêm hiệu ứng khi thu thập coin"""
        effect = {
            'x': x,
            'y': y,
            'timer': 0,
            'speed': 2,
            'alpha': 255,
            'fade_speed': 3,
            'size': 8
        }
        self.coin_collect_effects.append(effect)
    
    def draw_gradient_panel(self, surface, rect, color1, color2, border_radius=15):
        """Vẽ panel với gradient"""
        x, y, w, h = rect
        gradient_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        
        for i in range(h):
            ratio = i / h
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color2[2] + (color2[2] - color2[2]) * ratio)
            a = color1[3] if len(color1) > 3 else 255
            
            pygame.draw.line(gradient_surface, (r, g, b, a), (0, i), (w, i))
        
        mask_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255), (0, 0, w, h), border_radius=border_radius)
        gradient_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        surface.blit(gradient_surface, (x, y))
    
    def draw_glow_effect(self, surface, rect, color, intensity=50):
        """Vẽ hiệu ứng glow (tối ưu hóa)"""
        glow_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        
        for i in range(3):
            alpha = int(intensity * (1 - i / 3))
            glow_color = (*color[:3], alpha)
            glow_rect = pygame.Rect(i*3, i*3, rect.width + 10 - i*6, rect.height + 10 - i*6)
            pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=15)
        
        surface.blit(glow_surface, (rect.x - 5, rect.y - 5))
    
    def draw_score_panel(self, surface, score):
        """Vẽ panel điểm số với thiết kế mới đẹp hơn"""
        theme = self.theme_manager.get_current_theme()
        pulse_size = int(2 * math.sin(self.score_pulse))
        panel_rect = self.score_panel_rect.inflate(pulse_size, pulse_size)
  
        glow_color = theme['glow_color']
        self.draw_glow_effect(surface, panel_rect, glow_color, 50)
    
        panel_color1 = (*theme['ui_color'][:3], 180)
        panel_color2 = (*theme['accent_color'][:3], 120)
        self.draw_gradient_panel(surface, panel_rect, panel_color1, panel_color2)
        
        border_color = theme['accent_color']
        pygame.draw.rect(surface, border_color, panel_rect, 4, border_radius=20)
       
        inner_rect = panel_rect.inflate(-8, -8)
        pygame.draw.rect(surface, (*theme['accent_color'][:3], 100), inner_rect, 2, border_radius=16)
        
        star_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 20, 60, 60)
        self.draw_enhanced_star_icon(surface, star_rect, (255, 255, 0))
       
        try:
            score_text = self.score_font.render(f"{score:,}", True, (0, 255, 0))
            shadow_text = self.score_font.render(f"{score:,}", True, (0, 100, 0))
            outline_text = self.score_font.render(f"{score:,}", True, (0, 0, 0))
        except:
            score_text = pygame.font.Font(None, 48).render(f"{score:,}", True, (0, 255, 0))
            shadow_text = pygame.font.Font(None, 48).render(f"{score:,}", True, (0, 100, 0))
            outline_text = pygame.font.Font(None, 48).render(f"{score:,}", True, (0, 0, 0))
   
        score_rect = score_text.get_rect()
        score_x = panel_rect.x + 90 + (panel_rect.width - 90 - score_rect.width) // 2
        score_y = panel_rect.y + 18
   
        surface.blit(outline_text, (score_x - 2, score_y))
        surface.blit(outline_text, (score_x + 2, score_y))
        surface.blit(outline_text, (score_x, score_y - 2))
        surface.blit(outline_text, (score_x, score_y + 2))
        surface.blit(shadow_text, (score_x + 3, score_y + 3))
        surface.blit(score_text, (score_x, score_y))
        label_text = self.button_font.render("", True, (0, 255, 0))
        label_outline = self.button_font.render("", True, (0, 0, 0))

        label_rect = label_text.get_rect()
        label_x = panel_rect.x + 90 + (panel_rect.width - 90 - label_rect.width) // 2
        label_y = panel_rect.y + 58
  
        surface.blit(label_outline, (label_x - 2, label_y))
        surface.blit(label_outline, (label_x + 2, label_y))
        surface.blit(label_outline, (label_x, label_y - 2))
        surface.blit(label_outline, (label_x, label_y + 2))
        
        surface.blit(label_text, (label_x, label_y))
        
    def draw_enhanced_star_icon(self, surface, rect, color):
        """Vẽ icon ngôi sao nâng cao với hiệu ứng"""
        center_x = rect.centerx
        center_y = rect.centery
        radius = rect.width // 2
   
        twinkle = int(3 * math.sin(self.score_pulse * 2))
        radius += twinkle
        
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.4
            x = center_x + r * math.cos(angle - math.pi / 2)
            y = center_y + r * math.sin(angle - math.pi / 2)
            points.append((x, y))
        
        shadow_points = [(p[0] + 2, p[1] + 2) for p in points]
        pygame.draw.polygon(surface, (0, 0, 0, 100), shadow_points)
        
        pygame.draw.polygon(surface, color, points)
        
        inner_points = [(p[0] * 0.7 + center_x * 0.3, p[1] * 0.7 + center_y * 0.3) for p in points]
        pygame.draw.polygon(surface, (*color[:3], 150), inner_points)
    
    def draw_coin_panel(self, surface, coins):
        """Vẽ panel coin với thiết kế mới"""
        theme = self.theme_manager.get_current_theme()
        
        panel_color1 = (*theme['ui_color'][:3], 180)
        panel_color2 = (*theme['accent_color'][:3], 120)
        self.draw_gradient_panel(surface, self.coin_panel_rect, panel_color1, panel_color2)
        
        border_color = theme['accent_color']
        pygame.draw.rect(surface, border_color, self.coin_panel_rect, 4, border_radius=20)
        
        inner_rect = self.coin_panel_rect.inflate(-8, -8)
        pygame.draw.rect(surface, (*theme['accent_color'][:3], 100), inner_rect, 2, border_radius=16)
        
        coin_rect = pygame.Rect(self.coin_panel_rect.x + 20, self.coin_panel_rect.y + 15, 50, 50)
        self.draw_enhanced_coin_icon(surface, coin_rect, (255, 255, 0))
        
        try:
            coin_text = self.coin_font.render(f"{coins:,}", True, (0, 255, 0))
            shadow_text = self.coin_font.render(f"{coins:,}", True, (0, 100, 0))
        except:

            coin_text = pygame.font.Font(None, 44).render(f"{coins:,}", True, (0, 255, 0))
            shadow_text = pygame.font.Font(None, 44).render(f"{coins:,}", True, (0, 100, 0))
        
        coin_rect = coin_text.get_rect()
        coin_x = self.coin_panel_rect.x + 85 + (self.coin_panel_rect.width - 85 - coin_rect.width) // 2
        coin_y = self.coin_panel_rect.y + 17
        
        surface.blit(shadow_text, (coin_x + 3, coin_y + 3))
        surface.blit(coin_text, (coin_x, coin_y))
        
        label_text = self.button_font.render("", True, (0, 255, 0))
        
        label_rect = label_text.get_rect()
        label_x = self.coin_panel_rect.x + 85 + (self.coin_panel_rect.width - 85 - label_rect.width) // 2
        label_y = self.coin_panel_rect.y + 45
        
        surface.blit(label_text, (label_x, label_y))
        
    def draw_star_icon(self, surface, rect, color):
        """Vẽ icon ngôi sao"""
        center_x = rect.centerx
        center_y = rect.centery
        radius = rect.width // 2
        
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.4
            x = center_x + r * math.cos(angle - math.pi / 2)
            y = center_y + r * math.sin(angle - math.pi / 2)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
    
    def draw_enhanced_coin_icon(self, surface, rect, color):
        """Vẽ icon coin nâng cao với hiệu ứng"""
        center_x = rect.centerx
        center_y = rect.centery
        radius = rect.width // 2
        
        pygame.draw.circle(surface, (0, 0, 0, 100), (center_x + 2, center_y + 2), radius)
        
        pygame.draw.circle(surface, color, (center_x, center_y), radius)
        
        pygame.draw.circle(surface, (200, 200, 0), (center_x, center_y), radius, 3)
        
        try:
            font = pygame.font.Font(None, radius)
        except:
            font = pygame.font.Font(None, radius)
        
        dollar_text = font.render("$", True, (255, 255, 255))
        text_rect = dollar_text.get_rect(center=(center_x, center_y))
        surface.blit(dollar_text, text_rect)
        
    def draw_control_buttons(self, surface, mouse_pos):
        """Vẽ các nút điều khiển"""
        theme = self.theme_manager.get_current_theme()
        
    def draw_button(self, surface, rect, icon, hovered, theme):
        """Vẽ nút với hiệu ứng"""

        if hovered:
            glow_color = theme['glow_color']
            self.draw_glow_effect(surface, rect, glow_color, 40)
        
        panel_color1 = (*theme['ui_color'][:3], 200)
        panel_color2 = (*theme['accent_color'][:3], 150)
        self.draw_gradient_panel(surface, rect, panel_color1, panel_color2)
        
        border_color = theme['accent_color']
        border_width = 4 if hovered else 2
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=15)
        
        font = pygame.font.Font(None, 24)
        icon_text = font.render(icon, True, theme['text_color'])
        icon_rect = icon_text.get_rect(center=rect.center)
        surface.blit(icon_text, icon_rect)
    
    def draw_coin_collect_effects(self, surface):
        """Vẽ hiệu ứng thu thập coin"""
        theme = self.theme_manager.get_current_theme()
        
        for effect in self.coin_collect_effects:
            color = (*theme['accent_color'][:3], effect['alpha'])
            pygame.draw.circle(surface, color, 
                             (int(effect['x']), int(effect['y'])), 
                             effect['size'])
            
            for i in range(3):
                sparkle_x = effect['x'] + random.randint(-20, 20)
                sparkle_y = effect['y'] + random.randint(-20, 20)
                sparkle_alpha = int(effect['alpha'] * 0.7)
                pygame.draw.circle(surface, (*theme['accent_color'][:3], sparkle_alpha), 
                                 (int(sparkle_x), int(sparkle_y)), 2)
    
    def draw_theme_indicator(self, surface):
        """Vẽ chỉ báo theme hiện tại"""
        theme = self.theme_manager.get_current_theme()
        progress = self.theme_manager.get_theme_progress()
        
        indicator_rect = pygame.Rect(30, 30, 200, 40)
        
        pygame.draw.rect(surface, (*theme['ui_color'][:3], 150), indicator_rect, border_radius=20)
        pygame.draw.rect(surface, theme['accent_color'], indicator_rect, 2, border_radius=20)
        
        progress_width = int(196 * progress)
        progress_rect = pygame.Rect(32, 32, progress_width, 36)
        pygame.draw.rect(surface, theme['accent_color'], progress_rect, border_radius=18)
        
        try:
            theme_text = self.button_font.render(f"{theme['name']}", True, theme['text_color'])
        except:

            theme_text = pygame.font.Font(None, 32).render(f"{theme['name']}", True, theme['text_color'])
        text_rect = theme_text.get_rect(center=indicator_rect.center)
        surface.blit(theme_text, text_rect)
        
        if theme['name'] == "Ngày":
            icon = "☀"
        else:
            icon = "🌙"
        
        try:
            icon_font = pygame.font.Font(None, 24)
        except:
            icon_font = pygame.font.Font(None, 20)
        
        icon_text = icon_font.render(icon, True, theme['text_color'])
        surface.blit(icon_text, (indicator_rect.x + 10, indicator_rect.y + 10))
    
    def handle_click(self, mouse_pos):
        """Xử lý click chuột"""
        return None

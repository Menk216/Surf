
import pygame
import math
from settings import *

class PlayScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        
        # Background
        self.background = pygame.image.load("resources/assets/backgrounds/bg_game.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        # Font for UI
        self.font = pygame.font.SysFont("Arial", 36)
        self.title_text = self.font.render("Game Screen", True, (255, 255, 255))
        
        # Back button
        self.back_button = pygame.Rect(50, 50, 120, 50)
        self.back_text = pygame.font.SysFont("Arial", 24).render("Back", True, (255, 255, 255))
        
        # Wave animation
        self.wave_offset = 0
    
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
            
            # Draw background
            self.screen.blit(self.background, (0, 0))
            
            # Draw waves
            self.draw_waves()
            
            # Draw title
            self.screen.blit(self.title_text, 
                           (WIDTH // 2 - self.title_text.get_width() // 2, HEIGHT // 2))
            
            # Draw back button
            pygame.draw.rect(self.screen, (100, 100, 100), self.back_button)
            pygame.draw.rect(self.screen, (255, 255, 255), self.back_button, 2)
            self.screen.blit(self.back_text,
                           (self.back_button.centerx - self.back_text.get_width() // 2,
                            self.back_button.centery - self.back_text.get_height() // 2))
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.state = "start"
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.back_button.collidepoint(mouse_pos):
                        self.game.state = "start"
                        running = False
            
            pygame.display.flip()


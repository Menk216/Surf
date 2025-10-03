import pygame
from settings import *

class GameOverScreen:
    def __init__(self, game, play_screen):
        """
        game: tham chiếu game chính
        play_screen: tham chiếu đến PlayScreen hiện tại để có thể continue
        """
        self.game = game
        self.play_screen = play_screen

    def run(self):
        running = True
        
        # Tạo snapshot của màn chơi hiện tại
        gameplay_snapshot = self.game.screen.copy()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        from screens.play import PlayScreen
                        play_screen = PlayScreen(self.game)
                        self.game.state = "play"
                        play_screen.run()
                        running = False
                        
                    elif event.key == pygame.K_c:  # Continue (bất tử 3s)
                        self.play_screen.invincible_timer = 3000  # 3000ms = 3s
                        self.play_screen.invincible_blink_timer = 0
                        self.game.state = "play"
                        self.play_screen.run()
                        running = False
                        
                    elif event.key == pygame.K_q:  # Quit
                        self.game.running = False
                        running = False
            
            # Vẽ màn chơi phía sau (snapshot)
            self.game.screen.blit(gameplay_snapshot, (0, 0))
            
            # Tạo overlay bán trong suốt
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Alpha 150 (0-255)
            self.game.screen.blit(overlay, (0, 0))
            
            # Vẽ text GAME OVER
            font_big = pygame.font.SysFont("Arial", 100, bold=True)
            text_gameover = font_big.render("GAME OVER", True, (255, 50, 50))
            shadow_gameover = font_big.render("GAME OVER", True, (0, 0, 0))
            
            go_rect = text_gameover.get_rect(center=(WIDTH//2, HEIGHT//3))
            self.game.screen.blit(shadow_gameover, (go_rect.x + 4, go_rect.y + 4))
            self.game.screen.blit(text_gameover, go_rect)
            
            # Vẽ các nút
            font_small = pygame.font.SysFont("Arial", 45, bold=True)
            
            restart_text = font_small.render("Press R to Restart", True, (255, 255, 255))
            continue_text = font_small.render("Press C to Continue", True, (100, 255, 100))
            quit_text = font_small.render("Press Q to Quit", True, (255, 100, 100))
            
            y_start = HEIGHT // 2
            spacing = 70
            
            self.game.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, y_start))
            self.game.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, y_start + spacing))
            self.game.screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, y_start + spacing * 2))
            
            pygame.display.flip()
            self.game.clock.tick(FPS)

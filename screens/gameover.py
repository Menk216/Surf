import pygame
from settings import *

class GameOverScreen:
    def __init__(self, game):
        self.game = game

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        self.game.state = "play"
                        running = False
                    elif event.key == pygame.K_q:  # Quit
                        self.game.running = False
                        running = False

            self.game.screen.fill((0, 0, 0))
            font_big = pygame.font.SysFont(None, 100)
            text_gameover = font_big.render("GAME OVER", True, (255, 0, 0))
            self.game.screen.blit(text_gameover, (WIDTH//2 - text_gameover.get_width()//2, HEIGHT//3))

            font_small = pygame.font.SysFont(None, 50)
            restart_text = font_small.render("Press R to Restart", True, (255, 255, 255))
            quit_text = font_small.render("Press Q to Quit", True, (255, 255, 255))
            self.game.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
            self.game.screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 60))

            pygame.display.flip()
            self.game.clock.tick(FPS)

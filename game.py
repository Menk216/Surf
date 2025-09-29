import pygame
from settings import *
from screens.start import StartScreen
# from screens.play import PlayScreen  # sau này thêm

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"

    def run(self):
        while self.running:
            if self.state == "start":
                StartScreen(self).run()
            elif self.state == "play":
                # TODO: gọi PlayScreen(self).run()
                self.running = False

        pygame.quit()

import pygame
from settings import *
from screens.start import StartScreen
from screens.play import PlayScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"

        # ==== TẢI TÀI NGUYÊN Ở ĐÂY ====
        # Người chơi
        self.player_img = pygame.image.load("resources/assets/characters/player.png").convert_alpha()
        self.player_img = pygame.transform.smoothscale(self.player_img, (120, 120))

        # Vật cản
        self.obstacle_imgs = [
            pygame.image.load("resources/assets/backgrounds/1.png").convert_alpha(),
            pygame.image.load("resources/assets/backgrounds/2.png").convert_alpha(),
            pygame.image.load("resources/assets/backgrounds/3.png").convert_alpha(),
            pygame.image.load("resources/assets/backgrounds/4.png").convert_alpha(),
            pygame.image.load("resources/assets/backgrounds/12.png").convert_alpha(),
            pygame.image.load("resources/assets/backgrounds/13.png").convert_alpha(),
        ]
        self.obstacle_imgs = [pygame.transform.smoothscale(img, (150, 150)) for img in self.obstacle_imgs]

        # Đồng xu
        self.coin_img = pygame.image.load("resources/assets/backgrounds/11.png").convert_alpha()
        self.coin_img = pygame.transform.smoothscale(self.coin_img, (50, 50))

        # Rương báu
        self.treasure_img = pygame.image.load("resources/assets/backgrounds/5.png").convert_alpha()
        self.treasure_img = pygame.transform.smoothscale(self.treasure_img, (100, 100))

        # Cây
        self.tree_imgs = [
            pygame.image.load("resources/assets/backgrounds/7.png").convert_alpha(),
            pygame.image.load("resources/assets/backgrounds/8.png").convert_alpha(),
        ]
        self.tree_imgs = [pygame.transform.smoothscale(img, (200, 200)) for img in self.tree_imgs]

        # Quái vật
        self.monster_img = pygame.image.load("resources/assets/backgrounds/9.png").convert_alpha()
        self.monster_img = pygame.transform.smoothscale(self.monster_img, (200, 200))

        # Âm thanh
        # self.coin_sound = pygame.mixer.Sound("res/sound/coin.wav")
        # self.treasure_sound = pygame.mixer.Sound("res/sound/treasure.wav")
        # self.hit_sound = pygame.mixer.Sound("res/sound/hit.wav")

    def run(self):
        while self.running:
            if self.state == "start":
                StartScreen(self).run()
            elif self.state == "play":
                PlayScreen(self).run()

        pygame.quit()

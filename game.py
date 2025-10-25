import pygame
from settings import *
from screens.start import StartScreen
from screens.play import PlayScreen
from screens.gameover import GameOverScreen
from screens.settingsscreen import SettingsScreen
from utils import resource_path

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"
        
        self.player_img = pygame.image.load(resource_path("resources/assets/characters/player.png")).convert_alpha()
        self.player_img = pygame.transform.smoothscale(self.player_img, (120, 120))
        
        self.obstacle_imgs = [
            pygame.image.load(resource_path("resources/assets/backgrounds/1.png")).convert_alpha(),
            pygame.image.load(resource_path("resources/assets/backgrounds/2.png")).convert_alpha(),
            pygame.image.load(resource_path("resources/assets/backgrounds/3.png")).convert_alpha(),
            pygame.image.load(resource_path("resources/assets/backgrounds/4.png")).convert_alpha(),
            pygame.image.load(resource_path("resources/assets/backgrounds/12.png")).convert_alpha(),
            pygame.image.load(resource_path("resources/assets/backgrounds/13.png")).convert_alpha(),
        ]

        self.obstacle_imgs = [pygame.transform.smoothscale(img, (150, 150)) for img in self.obstacle_imgs]
        
        self.coin_img = pygame.image.load(resource_path("resources/assets/backgrounds/11.png")).convert_alpha()
        self.coin_img = pygame.transform.smoothscale(self.coin_img, (50, 50))
        
        self.treasure_img = pygame.image.load(resource_path("resources/assets/backgrounds/5.png")).convert_alpha()
        self.treasure_img = pygame.transform.smoothscale(self.treasure_img, (100, 100))
        
        self.tree_imgs = [
            pygame.image.load(resource_path("resources/assets/backgrounds/7.png")).convert_alpha(),
            pygame.image.load(resource_path("resources/assets/backgrounds/8.png")).convert_alpha(),
        ]
        self.tree_imgs = [pygame.transform.smoothscale(img, (200, 200)) for img in self.tree_imgs]
        
        self.monster_img = pygame.image.load(resource_path("resources/assets/backgrounds/9.png")).convert_alpha()
        self.monster_img = pygame.transform.smoothscale(self.monster_img, (200, 200))
    
    def run(self):
        start_screen = StartScreen(self)
        settings_screen = SettingsScreen(self)
        
        while self.running:
            if self.state == "start":
                start_screen.run()
            elif self.state == "settings":
                settings_screen.run()
            elif self.state == "play":

                import settings as settings_module
                difficulty_config = DIFFICULTY_CONFIGS[settings_module.CURRENT_DIFFICULTY]
                
                play_screen = PlayScreen(self)
                
                play_screen.spawner.obstacle_speed = difficulty_config["obstacle_speed"]
                play_screen.spawner.coin_speed = difficulty_config["coin_speed"]
                play_screen.spawner.tree_speed = difficulty_config["tree_speed"]
                play_screen.spawner.treasure_speed = difficulty_config["treasure_speed"]
                play_screen.spawner.monster_speed = difficulty_config["monster_speed"]
                play_screen.spawner.rates = difficulty_config["spawn_rates"]
                
                play_screen.run()
        
        pygame.quit()

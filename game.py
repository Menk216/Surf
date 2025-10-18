import pygame
from settings import *
from screens.start import StartScreen
from screens.play import PlayScreen
from screens.gameover import GameOverScreen
from screens.settingsscreen import SettingsScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"
        
        # ==== TẢI TÀI NGUYÊN ====
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
    
    def run(self):
        start_screen = StartScreen(self)
        settings_screen = SettingsScreen(self)
        
        while self.running:
            if self.state == "start":
                start_screen.run()
            elif self.state == "settings":
                settings_screen.run()
            elif self.state == "play":
                # Lấy cấu hình độ khó hiện tại
                import settings as settings_module
                difficulty_config = DIFFICULTY_CONFIGS[settings_module.CURRENT_DIFFICULTY]
                
                # Khởi tạo PlayScreen với độ khó được cấu hình
                play_screen = PlayScreen(self)
                
                # CẬP NHẬT SPAWNER VỚI ĐỘ KHÓ MỚI
                play_screen.spawner.obstacle_speed = difficulty_config["obstacle_speed"]
                play_screen.spawner.coin_speed = difficulty_config["coin_speed"]
                play_screen.spawner.tree_speed = difficulty_config["tree_speed"]
                play_screen.spawner.treasure_speed = difficulty_config["treasure_speed"]
                play_screen.spawner.monster_speed = difficulty_config["monster_speed"]
                play_screen.spawner.rates = difficulty_config["spawn_rates"]
                
                print(f"Starting game with difficulty: {settings_module.CURRENT_DIFFICULTY}")
                print(f"Obstacle speed: {difficulty_config['obstacle_speed']}")
                print(f"Spawn rates: {difficulty_config['spawn_rates']}")
                
                play_screen.run()
            elif self.state == "game_over":
                from screens.gameover import GameOverScreen
                gameover_screen = GameOverScreen(self, None)
                gameover_screen.run()
        
        pygame.quit()


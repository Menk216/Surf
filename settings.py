WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Fantascy Suffer"

# Cài đặt mặc định
DEFAULT_VOLUME = 0.5  # 50%
DEFAULT_DIFFICULTY = "medium"  # easy, medium, hard

# Cài đặt hiện tại
CURRENT_VOLUME = DEFAULT_VOLUME
CURRENT_DIFFICULTY = DEFAULT_DIFFICULTY

# Cấu hình độ khó
DIFFICULTY_CONFIGS = {
    "easy": {
        "obstacle_speed": 6,
        "coin_speed": 6,
        "tree_speed": 6,
        "treasure_speed": 5,
        "monster_speed": 6,
        "spawn_rates": {
            "obstacle_group": 0.4,
            "single_obstacle": 0.8,
            "coin": 5.0,
            "tree": 0.7
        }
    },
    "medium": {
        "obstacle_speed": 8,
        "coin_speed": 8,
        "tree_speed": 8,
        "treasure_speed": 7,
        "monster_speed": 8,
        "spawn_rates": {
            "obstacle_group": 0.6,
            "single_obstacle": 1.2,
            "coin": 4.0,
            "tree": 1.0
        }
    },
    "hard": {
        "obstacle_speed": 11,
        "coin_speed": 11,
        "tree_speed": 11,
        "treasure_speed": 10,
        "monster_speed": 11,
        "spawn_rates": {
            "obstacle_group": 0.9,
            "single_obstacle": 1.8,
            "coin": 3.5,
            "tree": 1.4
        }
    }
}

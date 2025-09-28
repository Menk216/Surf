import pygame
import sys

# Hàm vẽ hình chữ nhật gradient có bo góc
def draw_gradient_rect(surface, rect, color1, color2, border_radius=0):
    x, y, w, h = rect
    # Vẽ gradient dọc
    gradient_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(h):
        r = color1[0] + (color2[0] - color1[0]) * i // h
        g = color1[1] + (color2[1] - color1[1]) * i // h
        b = color1[2] + (color2[2] - color1[2]) * i // h
        pygame.draw.line(gradient_surface, (r, g, b), (0, i), (w, i))
    # Bo góc
    rounded_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(rounded_surface, (255, 255, 255), (0, 0, w, h), border_radius=border_radius)
    gradient_surface.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(gradient_surface, (x, y))


# Khởi tạo pygame
pygame.init()

# Full màn hình
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Fantascy Suffer")

# Load ảnh nền và scale full màn
background = pygame.image.load("resources/assets/backgrounds/bg_startgame.jpg")  
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Font chữ (tăng kích thước title)
title_font = pygame.font.Font("resources/assets/fonts/ClimateCrisis-Regular-VariableFont_YEAR.ttf", 120)
button_font = pygame.font.SysFont("Segoe UI", 48, bold=True)

# Text tiêu đề
title_text = title_font.render("Whispering Horizon", True, (255, 255, 255))

# Nút bắt đầu chơi
button_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2, 400, 100)
button_text = button_font.render("Start", True, (255, 255, 255))

# Vòng lặp game
running = True
while running:
    screen.blit(background, (0, 0))  # vẽ background

    # Vẽ tiêu đề
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))

    # Kiểm tra hover
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        draw_gradient_rect(screen, button_rect, (100, 200, 255), (180, 120, 255), border_radius=30)
    else:
        draw_gradient_rect(screen, button_rect, (80, 160, 220), (150, 100, 220), border_radius=30)

    # Vẽ chữ trên nút
    screen.blit(button_text, (button_rect.centerx - button_text.get_width()//2,
                              button_rect.centery - button_text.get_height()//2))

    # Sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Sau này gán sự kiện click
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if button_rect.collidepoint(mouse_pos):
        #         print("Start game")

        # Thoát game bằng phím ESC hoặc Q
        if event.type == pygame.KEYDOWN:
            # Thoát game bằng ESC hoặc Q
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()
sys.exit()

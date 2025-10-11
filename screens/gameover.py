import pygame
from settings import *

def draw_gradient_rect(surface, rect, color1, color2):
    """Draw a vertical gradient rectangle."""
    x, y, w, h = rect
    gradient = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(gradient, (r, g, b), (0, i), (w, i))
    surface.blit(gradient, (x, y))

class GameOverScreen:
    def __init__(self, game, play_screen):
        self.game = game
        self.play_screen = play_screen
        self.continue_count = getattr(play_screen, "continue_count", 0)
        self.buttons = {}
        self.create_buttons()

        # Popup notification
        self.popup_text = None
        self.popup_timer = 0
        self.popup_duration = 1500  # ms
        self.popup_alpha = 255

    def create_buttons(self):
        font = pygame.font.Font(None, 48)
        btn_w, btn_h = 320, 85
        spacing = 30
        start_y = HEIGHT * 0.55

        btn_names = ["Restart", "Continue", "Quit"]
        color_pairs = [
            ((255, 255, 255), (220, 220, 220)),
            ((100, 255, 100), (40, 180, 40)),
            ((255, 100, 100), (180, 40, 40))
        ]

        for i, (name, colors) in enumerate(zip(btn_names, color_pairs)):
            rect = pygame.Rect(WIDTH//2 - btn_w//2, start_y + i*(btn_h + spacing), btn_w, btn_h)
            self.buttons[name] = {
                "rect": rect,
                "colors": colors,
                "text": font.render(name, True, (0, 0, 0))
            }

    def draw_button(self, screen, name, hover=False, disabled=False):
        button = self.buttons[name]
        rect = button["rect"]
        c1, c2 = button["colors"]

        if hover and not disabled:
            c1 = tuple(min(255, x + 30) for x in c1)
            c2 = tuple(min(255, x + 30) for x in c2)

        draw_gradient_rect(screen, rect, c1, c2)
        pygame.draw.rect(screen, (0, 0, 0), rect, 4, border_radius=18)

        if disabled:
            dark = pygame.Surface(rect.size, pygame.SRCALPHA)
            dark.fill((0, 0, 0, 120))
            screen.blit(dark, rect.topleft)

        text = button["text"]
        screen.blit(text, text.get_rect(center=rect.center))

    def draw_popup(self, screen, dt):
        """Display popup notification (fade out)."""
        if self.popup_text:
            self.popup_timer += dt
            if self.popup_timer > self.popup_duration:
                self.popup_text = None
                self.popup_timer = 0
                self.popup_alpha = 255
                return

            # Fade out near the end
            if self.popup_timer > self.popup_duration * 0.7:
                self.popup_alpha = int(255 * (1 - (self.popup_timer - self.popup_duration * 0.7) / (self.popup_duration * 0.3)))

            font = pygame.font.Font(None, 46)
            text_surf = font.render(self.popup_text, True, (255, 255, 255))
            text_surf.set_alpha(self.popup_alpha)
            bg = pygame.Surface((text_surf.get_width() + 40, text_surf.get_height() + 20), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            screen.blit(bg, (WIDTH//2 - bg.get_width()//2, HEIGHT//2 - bg.get_height()//2))
            screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, HEIGHT//2 - text_surf.get_height()//2))

    def run(self):
        running = True
        gameplay_snapshot = self.game.screen.copy()
        clock = pygame.time.Clock()

        while running:
            dt = clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.handle_restart()
                        running = False
                    elif event.key == pygame.K_c:
                        if self.handle_continue():
                            running = False
                    elif event.key == pygame.K_q:
                        self.handle_quit()
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            # Dimmed background
            self.game.screen.blit(gameplay_snapshot, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.game.screen.blit(overlay, (0, 0))

            # Title
            font_big = pygame.font.Font(None, 110)
            text = font_big.render("GAME OVER", True, (255, 50, 50))
            shadow = font_big.render("GAME OVER", True, (0, 0, 0))
            rect = text.get_rect(center=(WIDTH//2, HEIGHT * 0.3))
            self.game.screen.blit(shadow, (rect.x + 5, rect.y + 5))
            self.game.screen.blit(text, rect)

            # Buttons
            for name, button in self.buttons.items():
                rect = button["rect"]
                hover = rect.collidepoint(mouse_pos)
                disabled = (name == "Continue" and self.continue_count >= 2)
                self.draw_button(self.game.screen, name, hover, disabled)

                if hover and mouse_click and not disabled:
                    if name == "Restart":
                        self.handle_restart()
                        running = False
                    elif name == "Continue":
                        if self.handle_continue():
                            running = False
                    elif name == "Quit":
                        self.handle_quit()
                        running = False
                elif hover and mouse_click and disabled:
                    self.show_popup("No continues remaining!")

            # Draw popup
            self.draw_popup(self.game.screen, dt)

            pygame.display.flip()

    # === Button actions ===
    def handle_restart(self):
        from screens.play import PlayScreen
        play_screen = PlayScreen(self.game)
        self.game.state = "play"
        play_screen.run()

    def handle_continue(self):
        if self.continue_count >= 2:
            self.show_popup("No continues remaining!")
            return False

        self.continue_count += 1
        remaining = 2 - self.continue_count
        self.show_popup(f"You have {remaining} continue(s) left.")

        self.play_screen.continue_count = self.continue_count
        self.play_screen.invincible_timer = 3000
        self.play_screen.invincible_blink_timer = 0
        self.game.state = "play"
        self.play_screen.run()
        return True

    def handle_quit(self):
        self.game.running = False

    def show_popup(self, message):
        """Display popup text."""
        self.popup_text = message
        self.popup_timer = 0
        self.popup_alpha = 255
        self.popup_duration = 1500  # ms

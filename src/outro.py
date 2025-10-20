import pygame
import sys

pygame.init()

# --- Екран ---
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# --- Кольори ---
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
OVERLAY = (0, 0, 0, 180)
BUTTON_COLOR = (50, 50, 0)
BUTTON_HOVER_COLOR = (30, 30, 0)
BUTTON_BORDER = (255, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 0)

# --- Шрифти ---
font = pygame.font.SysFont("Franklin Gothic Medium", 120, True)
button_font = pygame.font.SysFont("Arial", 28, True)

def draw_button(text, rect, alpha, hover):
    """Малює кнопку з рамкою та текстом"""
    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    color = (BUTTON_HOVER_COLOR if hover else BUTTON_COLOR) + (alpha,)
    border = BUTTON_BORDER + (alpha,)

    pygame.draw.rect(button_surface, color, (0, 0, rect.width, rect.height), border_radius=10)
    pygame.draw.rect(button_surface, border, (0, 0, rect.width, rect.height), 4, border_radius=10)

    text_render = button_font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_render.get_rect(center=(rect.width//2, rect.height//2))
    button_surface.blit(text_render, text_rect)

    screen.blit(button_surface, rect.topleft)

def game_over_screen():
    text_surface = font.render("GAME OVER", True, YELLOW)
    outline = pygame.Surface((text_surface.get_width()+4, text_surface.get_height()+4), pygame.SRCALPHA)
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            outline.blit(font.render("GAME OVER", True, (0, 0, 0)), (dx+2, dy+2))
    outline.blit(text_surface, (2, 2))

    y = -text_surface.get_height()
    target_y = HEIGHT // 2 - text_surface.get_height() // 2
    velocity = 20
    bounces = 0
    max_bounces = 3
    damping = 0.5

    # --- Кнопки ---
    button_size = (260, 80)
    restart_rect = pygame.Rect(WIDTH//2 - button_size[0]//2, target_y + text_surface.get_height() + 150, *button_size)
    quit_rect = pygame.Rect(WIDTH//2 - button_size[0]//2, restart_rect.bottom + 40, *button_size)

    button_alpha = 0
    button_fade_speed = 5
    overlay_alpha = 0
    overlay_max = 180
    restart_clicked = False

    while True:
        screen.fill(BLACK)

        # --- Поступове затемнення ---
        if overlay_alpha < overlay_max:
            overlay_alpha += 3
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        screen.blit(overlay, (0, 0))

        # --- Анімація GAME OVER ---
        y += velocity
        if y >= target_y:
            y = target_y
            velocity = -velocity * damping
            bounces += 1
            if bounces > max_bounces:
                velocity = 0
                y = target_y
        else:
            velocity += 1

        screen.blit(outline, (WIDTH//2 - outline.get_width()//2, int(y)))

        # --- Кнопки після зупинки ---
        if velocity == 0 and overlay_alpha >= overlay_max:
            if button_alpha < 255:
                button_alpha += button_fade_speed

            mx, my = pygame.mouse.get_pos()
            hover_restart = restart_rect.collidepoint(mx, my)
            hover_quit = quit_rect.collidepoint(mx, my)

            draw_button("RESTART", restart_rect, button_alpha, hover_restart)
            draw_button("QUIT", quit_rect, button_alpha, hover_quit)

        pygame.display.flip()
        clock.tick(75)

        # --- Події ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and velocity == 0 and overlay_alpha >= overlay_max:
                if restart_rect.collidepoint(event.pos):
                    return True
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def main():
    running = True
    while running:
        screen.fill((20, 20, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(75)

if __name__ == "__main__":
    while True:
        game_over_screen()
        main()

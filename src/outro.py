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
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
D_WHITE = (100, 100, 100)
OVERLAY = (0, 0, 0, 180)
BUTTON_COLOR = (50, 50, 0)
BUTTON_HOVER_COLOR = (30, 30, 0)  # темніший при наведенні
BUTTON_BORDER = (255, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 0)

# --- Шрифти ---
font = pygame.font.SysFont("Franklin Gothic Medium", 120, True)
button_font = pygame.font.SysFont("Arial", 28, True)


def game_over_screen():
    text_surface = font.render("GAME OVER", True, YELLOW)
    outline = pygame.Surface(
        (text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA
    )
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            outline.blit(font.render("GAME OVER", True, (0, 0, 0)), (dx + 2, dy + 2))
    outline.blit(text_surface, (2, 2))

    y = -text_surface.get_height()
    target_y = HEIGHT // 2 - text_surface.get_height() // 2
    velocity = 20
    bounces = 0
    max_bounces = 3
    damping = 0.5

    button_radius = 80
    button_center = [WIDTH // 2, target_y + text_surface.get_height() + 150]
    button_alpha = 0
    button_fade_speed = 5
    button_surface = pygame.Surface(
        (button_radius * 2, button_radius * 2), pygame.SRCALPHA
    )
    button_bounce = 0
    button_velocity = 0
    button_target_y = button_center[1]

    restart_clicked = False

    while not restart_clicked:
        screen.fill(BLACK)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
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
        screen.blit(outline, (WIDTH // 2 - outline.get_width() // 2, int(y)))

        # --- Кнопка ---
        if velocity == 0:
            if button_alpha < 255:
                button_alpha += button_fade_speed

            if button_bounce < 4:
                button_velocity += 1
                button_center[1] += button_velocity
                if button_center[1] >= button_target_y:
                    button_center[1] = button_target_y
                    button_velocity = -button_velocity * 0.5
                    button_bounce += 1

            # Перевірка наведення миші
            mx, my = pygame.mouse.get_pos()
            dx = mx - button_center[0]
            dy = my - button_center[1]
            if dx * dx + dy * dy <= button_radius * button_radius:
                color = BUTTON_HOVER_COLOR + (button_alpha,)
            else:
                color = BUTTON_COLOR + (button_alpha,)

            button_surface.fill((0, 0, 0, 0))
            pygame.draw.circle(
                button_surface, color, (button_radius, button_radius), button_radius
            )
            pygame.draw.circle(
                button_surface,
                BUTTON_BORDER + (button_alpha,),
                (button_radius, button_radius),
                button_radius,
                4,
            )
            text_btn = button_font.render("RESTART", True, BUTTON_TEXT_COLOR)
            text_rect = text_btn.get_rect(center=(button_radius, button_radius))
            button_surface.blit(text_btn, text_rect)
            screen.blit(
                button_surface,
                (button_center[0] - button_radius, button_center[1] - button_radius),
            )

        pygame.display.flip()
        clock.tick(75)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and velocity == 0:
                mx, my = event.pos
                dx = mx - button_center[0]
                dy = my - button_center[1]
                if dx * dx + dy * dy <= button_radius * button_radius:
                    restart_clicked = True

    return True


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

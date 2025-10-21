import pygame
import sys
import random
import math

pygame.init()

# --- Екран ---
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# --- Кольори ---
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CONFETTI_COLORS = [
    (255, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (0, 255, 0),
    (255, 100, 255),
    (255, 165, 0),
]

# --- Шрифти ---
title_font = pygame.font.SysFont("Franklin Gothic Medium", 100, True)
button_font = pygame.font.SysFont("Arial", 28, True)

# --- Кнопки ---
BUTTON_COLOR = (50, 50, 0)
BUTTON_HOVER_COLOR = (30, 30, 0)
BUTTON_BORDER = (255, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 0)


def draw_button(text, rect, alpha, hover):
    """Малює кнопку"""
    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    color = (BUTTON_HOVER_COLOR if hover else BUTTON_COLOR) + (alpha,)
    border = BUTTON_BORDER + (alpha,)
    pygame.draw.rect(
        button_surface, color, (0, 0, rect.width, rect.height), border_radius=10
    )
    pygame.draw.rect(
        button_surface, border, (0, 0, rect.width, rect.height), 4, border_radius=10
    )
    text_render = button_font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_render.get_rect(center=(rect.width // 2, rect.height // 2))
    button_surface.blit(text_render, text_rect)
    screen.blit(button_surface, rect.topleft)


class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-400, -10)
        self.size = random.randint(6, 14)
        self.color = random.choice(CONFETTI_COLORS)
        self.speed = random.uniform(2, 5)
        self.angle = random.uniform(0, math.pi * 2)
        self.spin_speed = random.uniform(-0.15, 0.15)
        self.shape = random.choice(["circle", "square", "triangle"])
        self.opacity = 255

    def update(self):
        self.y += self.speed
        self.angle += self.spin_speed
        if self.y > HEIGHT:
            self.y = random.randint(-400, -10)
            self.x = random.randint(0, WIDTH)
        self.opacity = max(0, self.opacity - 0.2)

    def draw(self, surface):
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        color = (*self.color, int(self.opacity))

        if self.shape == "circle":
            pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        elif self.shape == "square":
            rotated = pygame.transform.rotate(
                pygame.Surface((self.size, self.size), pygame.SRCALPHA),
                math.degrees(self.angle),
            )
            rotated.fill(color)
            surf.blit(
                rotated,
                (
                    self.size - rotated.get_width() // 2,
                    self.size - rotated.get_height() // 2,
                ),
            )
        else:  # triangle
            points = [
                (
                    self.size + math.cos(self.angle) * self.size,
                    self.size + math.sin(self.angle) * self.size,
                ),
                (
                    self.size + math.cos(self.angle + 2.1) * self.size,
                    self.size + math.sin(self.angle + 2.1) * self.size,
                ),
                (
                    self.size + math.cos(self.angle + 4.2) * self.size,
                    self.size + math.sin(self.angle + 4.2) * self.size,
                ),
            ]
            pygame.draw.polygon(surf, color, points)

        surface.blit(surf, (self.x, self.y))


def tutorial_complete_screen():
    text_surface = title_font.render("LEVEL COMPLETE", True, YELLOW)
    outline = pygame.Surface(
        (text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA
    )
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            outline.blit(
                title_font.render("LEVEL COMPLETE", True, (0, 0, 0)), (dx + 2, dy + 2)
            )
    outline.blit(text_surface, (2, 2))

    # --- Анімація тексту ---
    scale = 0.05
    target_scale = 1.0
    speed = 0.03
    impact_done = False
    bounce_speed = 0.03
    overlay_alpha = 0
    overlay_max = 180
    button_alpha = 0
    button_fade_speed = 5

    # --- Кнопки ---
    button_size = (320, 80)
    level_rect = pygame.Rect(
        WIDTH // 2 - button_size[0] // 2, HEIGHT // 2 + 150, *button_size
    )
    quit_rect = pygame.Rect(
        WIDTH // 2 - button_size[0] // 2, level_rect.bottom + 40, *button_size
    )

    # --- Конфеті ---
    confetti_list = [Confetti() for _ in range(120)]
    show_confetti = False

    while True:
        screen.fill(BLACK)

        # --- Затемнення ---
        if overlay_alpha < overlay_max:
            overlay_alpha += 3
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        screen.blit(overlay, (0, 0))

        # --- Конфеті позаду тексту ---
        if show_confetti:
            for c in confetti_list:
                c.update()
                c.draw(screen)

        # --- Анімація тексту ---
        if not impact_done:
            scale += speed
            if scale >= target_scale:
                scale = target_scale
                impact_done = True
                speed = -bounce_speed
        else:
            scale += speed
            if scale < 1.0:
                speed = 0
                scale = 1.0
                show_confetti = True  # запускаємо конфеті

        scaled_surface = pygame.transform.smoothscale(
            outline,
            (int(outline.get_width() * scale), int(outline.get_height() * scale)),
        )
        rect = scaled_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(scaled_surface, rect)

        # --- Кнопки ---
        if impact_done and speed == 0:
            if button_alpha < 255:
                button_alpha += button_fade_speed
            mx, my = pygame.mouse.get_pos()
            hover_level = level_rect.collidepoint(mx, my)
            hover_quit = quit_rect.collidepoint(mx, my)
            draw_button("CONTINUE", level_rect, button_alpha, hover_level)
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
            elif event.type == pygame.MOUSEBUTTONDOWN and impact_done and speed == 0:
                if level_rect.collidepoint(event.pos):
                    print("Mission is starting...")
                    return True
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    tutorial_complete_screen()

import pygame

BG_COLOR = (30, 30, 30)
BAR_BG = (60, 60, 60)
BAR_FILL = (0, 200, 100)
BAR_FILL2 = (200, 0, 0)
# Progress data
progress = 0.0  # from 0.0 to 1.0


def draw_progress_bar(
    surface: pygame.Surface, x: int, y: int, width: int, height: int, progress: float
):
    # Draw background
    _ = pygame.draw.rect(surface, BAR_BG, (x, y, width, height), border_radius=5)
    # Draw filled part
    if progress > 0.15:
        inner_width = int(width * max(0, min(1, progress)))  # clamp 0-1
        _ = pygame.draw.rect(
            surface, BAR_FILL, (x, y, inner_width, height), border_radius=5
        )
    else:
        _ = pygame.draw.circle(
            surface,
            BAR_FILL,
            (x + height / 2 + progress * 25, y + height / 2),
            height / 2,
        )
    # Optional border
    _ = pygame.draw.rect(
        surface, (255, 255, 255), (x, y, width, height), 2, border_radius=5
    )


def draw_progress_bar_2(
    surface: pygame.Surface, x: int, y: int, width: int, height: int, progress: float
):
    # Draw background
    _ = pygame.draw.rect(surface, BAR_BG, (x, y, width, height), border_radius=5)
    # Draw filled part
    if progress > 0.15:
        inner_width = int(width * max(0, min(1, progress)))  # clamp 0-1
        _ = pygame.draw.rect(
            surface, BAR_FILL2, (x, y, inner_width, height), border_radius=5
        )
    else:
        _ = pygame.draw.circle(
            surface,
            BAR_FILL2,
            (x + height / 2 + progress * 25, y + height / 2),
            height / 2,
        )
    # Optional border
    _ = pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 1, border_radius=5)

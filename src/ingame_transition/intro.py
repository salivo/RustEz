import pygame
import sys
import random
import time

# --- Shared globals ---
screen: pygame.Surface | None = None
width: int = 0
height: int = 0


def init_intro(display: pygame.Surface, w: int, h: int):
    """Initialize intro with the screen and resolution from the main game."""
    global screen, width, height
    screen = display
    width = w
    height = h


# --- Colors ---
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
D_WHITE = (100, 100, 100)

# --- Fonts ---
pygame.font.init()
font_text = pygame.font.SysFont("Arial", 32, True)
font_button = pygame.font.SysFont("Arial", 36, True)
end_font = pygame.font.SysFont("Arial", 60)
logo_font = pygame.font.SysFont("Franklin Gothic Medium", 144, True, False)

# --- Text and Stars ---
intro_text = [
    "On the planet EREVOS-9, a deadly virus has transformed",
    "native ants into towering monsters — THE GRAXIDS.",
    "The human outpost is under siege. Some AEGIS TURRETS",
    "still fire, but most are crippled.",
    "You are Commander RYN SOLAS, armed with the NULLSTAR RIFLE",
    "this is a pulse weapon made for close combat.",
    "Move between turrets, fight off the GRAXIDS,",
    "and repair the damaged DEFENSES.",
    "Repel the swarm. Repair the turrets. Protect humanity. The hunt begins...",
]

text_surfaces: list[pygame.Surface] = [
    font_text.render(line, True, YELLOW).convert_alpha() for line in intro_text
]

clock = pygame.time.Clock()
star_list = [
    (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.2, 1))
    for _ in range(400)
]


def draw_stars(speed: float, warp: bool):
    for i, (x, y, z) in enumerate(star_list):
        if warp:
            z -= speed * 0.05
        else:
            z -= 0.002

        if z <= 0.05:
            z = 1
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)

        sx = int(width / 2 + x / z * width / 2)
        sy = int(height / 2 + y / z * height / 2)
        size = int((1 - z) * (10 if warp else 3))
        brightness = min(255, int(180 + (1 - z) * 180))
        color = (brightness, brightness, 255)
        pygame.draw.circle(screen, color, (sx, sy), max(size, 1))
        star_list[i] = (x, y, z)


def show_logo():
    logo_text = "RUSTEZ"
    logo_surf = logo_font.render(logo_text, True, YELLOW).convert_alpha()
    logo_alpha = 0
    logo_time = 0
    showing = True

    while showing:
        screen.fill(BLACK)
        if logo_alpha < 255:
            logo_alpha += 3
        logo_surf.set_alpha(logo_alpha)
        screen.blit(
            logo_surf,
            (
                width // 2 - logo_surf.get_width() // 2,
                height // 2 - logo_surf.get_height() // 2,
            ),
        )
        pygame.display.flip()
        clock.tick(75)
        logo_time += 1
        if logo_time > 250:
            showing = False

    while logo_alpha > 0:
        screen.fill(BLACK)
        logo_alpha -= 5
        if logo_alpha < 0:
            logo_alpha = 0
        logo_surf.set_alpha(logo_alpha)
        screen.blit(
            logo_surf,
            (
                width // 2 - logo_surf.get_width() // 2,
                height // 2 - logo_surf.get_height() // 2,
            ),
        )
        pygame.display.flip()
        clock.tick(75)


def intro_screen():
    alpha = 0
    fade_out = False
    fade_alpha = 255
    warp_start = False
    warp_speed = 0
    MAX_WARP_SPEED = 4
    warp_acceleration = 0.05
    warp_time = 0
    post_warp_fade = False
    fade_black_alpha = 0
    button_phase = 0.0

    # --- Button ---
    button_rect = pygame.Rect(0, 0, 200, 50)
    button_rect.bottomright = (width - 50, height - 50)

    # --- Music ---
    pygame.mixer.music.load("assets/intro_music.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    warp_sound = pygame.mixer.Sound("assets/warp_sound.mp3")
    warp_channel = pygame.mixer.Channel(1)
    warp_channel.set_volume(0.0)

    text_total_height = len(text_surfaces) * 50
    base_y = height // 2 - text_total_height // 2

    warp_duration = 1.1
    warp_playing = False
    running = True

    while running:
        screen.fill(BLACK)

        if warp_start:
            draw_stars(speed=warp_speed, warp=True)
            if warp_speed < MAX_WARP_SPEED:
                warp_speed += warp_acceleration
        else:
            draw_stars(1, False)

        if not fade_out:
            alpha = min(alpha + 2, 255)
        else:
            fade_alpha -= 20
            pygame.mixer.music.set_volume(
                max(0, pygame.mixer.music.get_volume() - 0.02)
            )

            if fade_alpha <= 0 and not warp_start:
                warp_start = True
                warp_speed = 0.5
                warp_time = time.time()
                warp_playing = True
                warp_channel.play(warp_sound, loops=-1)

        if warp_playing and warp_channel.get_busy():
            elapsed = time.time() - warp_time
            progress = elapsed / warp_duration
            warp_channel.set_volume(min(1.0, progress))

        for idx, surf in enumerate(text_surfaces):
            surf.set_alpha(alpha if not fade_out else max(fade_alpha, 0))
            x = width // 2 - surf.get_width() // 2
            y = base_y + idx * 50
            screen.blit(surf, (x, y))

        button_phase = (button_phase + 0.01) % 1
        t = abs(0.5 - button_phase) * 2
        color_val = int(100 + 155 * t)
        button_color = (color_val, color_val, color_val)
        button_text = font_button.render("Continue", True, button_color)
        button_text.set_alpha(255 if not fade_out else max(fade_alpha, 0))
        screen.blit(button_text, button_rect.topleft)

        if warp_start and time.time() - warp_time > warp_duration:
            post_warp_fade = True

        if post_warp_fade:
            fade_black_alpha = min(fade_black_alpha + 5, 255)
            black_surface = pygame.Surface((width, height))
            black_surface.fill(BLACK)
            black_surface.set_alpha(fade_black_alpha)
            screen.blit(black_surface, (0, 0))
            warp_channel.set_volume(max(0.0, warp_channel.get_volume() - 0.03))
            if warp_channel.get_volume() <= 0.05:
                warp_channel.stop()

        pygame.display.flip()
        clock.tick(75)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not fade_out:
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and button_rect.collidepoint(event.pos)
                ) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    fade_out = True

        if post_warp_fade and fade_black_alpha >= 255:
            pygame.mixer.music.stop()
            warp_channel.stop()
            running = False


# --- Only run if directly executed ---
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("RustEz")
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h

    show_logo()
    intro_screen()

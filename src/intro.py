import pygame
import sys
import random
import time

pygame.init()

# --- Налаштування екрану ---
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bug Hunt: Intro")

# --- Кольори ---
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# --- Шрифти ---
font_text = pygame.font.SysFont('Arial', 32, True)
font_button = pygame.font.SysFont('Arial', 36, True)
end_font = pygame.font.SysFont('Arial', 60)
logo_font = pygame.font.SysFont('Franklin Gothic Medium', 144, True, False)  # логотип

# --- Текст логотипу ---
logo_text = "RUSTEZ"
logo_surf = logo_font.render(logo_text, True, YELLOW).convert_alpha()
logo_alpha = 0

# --- Текст вступу ---
intro_text = [
    "On the planet EREVOS-9, a deadly virus has transformed",
    "native ants into towering monsters — THE GRAXIDS.",
    "The human outpost is under siege.",
    "Some AEGIS TURRETS still fire, but most are crippled.",
    "You are Commander RYN SOLAS, armed with the NULLSTAR RIFLE",
    "this is a pulse weapon made for close combat.",
    "Move between turrets, fight off the GRAXIDS," ,
    "and repair the damaged DEFENSES.",
    "Repel the swarm. Repair the turrets. Protect humanity. The hunt begins..."
]

# --- Кнопка Continue ---
button_rect = pygame.Rect(0, 0, 200, 50)
button_rect.bottomright = (WIDTH - 20, HEIGHT - 20)

# --- Текстові поверхні ---
text_surfaces = []
for line in intro_text:
    surf = font_text.render(line, True, YELLOW).convert_alpha()
    surf.set_alpha(0)
    text_surfaces.append(surf)

# --- Змінні ---
clock = pygame.time.Clock()
alpha = 0
button_phase = 0.0
fade_out = False
fade_alpha = 255
warp_start = False
warp_time = 0
post_warp_fade = False
fade_black_alpha = 0

# --- Warp налаштування ---
warp_speed = 0.06
MAX_WARP_SPEED = 3
warp_acceleration = 0.05
WARP_DURATION = 2  # секунди, скільки триватиме warp

# --- Зірки (x, y, z) ---
star_list = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.2, 1)) for _ in range(300)]

# --- Функція малювання зірок ---
def draw_stars(speed=1, warp=False):
    for i, (x, y, z) in enumerate(star_list):
        if warp:
            z -= speed * 0.05
        else:
            z -= 0.002
        if z <= 0.05:
            z = 1
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        sx = int(WIDTH / 2 + x / z * WIDTH / 2)
        sy = int(HEIGHT / 2 + y / z * HEIGHT / 2)
        size = int((1 - z) * (10 if warp else 3))
        brightness = min(255, int(180 + (1 - z) * 180))
        color = (brightness, brightness, 255)
        pygame.draw.circle(screen, color, (sx, sy), max(size, 1))
        star_list[i] = (x, y, z)

# --- Показ логотипу ---
def show_logo():
    global logo_alpha
    logo_time = 0
    showing = True
    while showing:
        screen.fill(BLACK)
        if logo_alpha < 255:
            logo_alpha += 3
        logo_surf.set_alpha(logo_alpha)
        screen.blit(logo_surf, (WIDTH//2 - logo_surf.get_width()//2,
                                HEIGHT//2 - logo_surf.get_height()//2))
        pygame.display.flip()
        clock.tick(75)
        logo_time += 1
        if logo_time > 250:  
            showing = False

    while logo_alpha > 0:
        screen.fill(BLACK)
        logo_alpha -= 5
        if logo_alpha < 0: logo_alpha = 0
        logo_surf.set_alpha(logo_alpha)
        screen.blit(logo_surf, (WIDTH//2 - logo_surf.get_width()//2,
                                HEIGHT//2 - logo_surf.get_height()//2))
        pygame.display.flip()
        clock.tick(75)

# --- Функція вступного екрану ---
def intro_screen():
    global alpha, button_phase, fade_out, fade_alpha, warp_start, warp_time, post_warp_fade, fade_black_alpha, warp_speed
    running = True
    text_total_height = len(text_surfaces) * 50
    base_y = HEIGHT // 2 - text_total_height // 2

    while running:
        screen.fill(BLACK)

        # --- Warp та зірки ---
        if warp_start:
            draw_stars(speed=warp_speed, warp=True)
            if warp_speed < MAX_WARP_SPEED:
                warp_speed += warp_acceleration
                if warp_speed > MAX_WARP_SPEED:
                    warp_speed = MAX_WARP_SPEED
            # Тривалість warp
            if time.time() - warp_time >= WARP_DURATION:
                post_warp_fade = True
        else:
            draw_stars(speed=1, warp=False)

        # --- Поява / зникання тексту ---
        if not fade_out:
            alpha = min(alpha + 2, 255)
        else:
            fade_alpha -= 12
            if fade_alpha <= 0 and not warp_start:
                warp_start = True
                warp_time = time.time()

        for idx, surf in enumerate(text_surfaces):
            surf.set_alpha(alpha if not fade_out else max(fade_alpha,0))
            x = WIDTH // 2 - surf.get_width() // 2
            y = base_y + idx * 50
            screen.blit(surf, (x, y))

        # --- Мерехтіння кнопки ---
        button_phase = (button_phase + 0.01) % 1
        t = abs(0.5 - button_phase) * 2
        color_val = int(100 + 155 * t)
        button_color = (color_val, color_val, color_val)
        button_text = font_button.render("Continue", True, button_color)
        button_text.set_alpha(255 if not fade_out else max(fade_alpha,0))
        screen.blit(button_text, button_rect.topleft)

        # --- Плавне затемнення після warp ---
        if post_warp_fade:
            fade_black_alpha = min(fade_black_alpha + 5, 255)
            black_surface = pygame.Surface((WIDTH, HEIGHT))
            black_surface.fill(BLACK)
            black_surface.set_alpha(fade_black_alpha)
            screen.blit(black_surface, (0,0))

        pygame.display.flip()
        clock.tick(75)

        # --- Події ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not fade_out:
                if button_rect.collidepoint(event.pos):
                    fade_out = True

        if post_warp_fade and fade_black_alpha >= 255:
            running = False

if __name__ == "__main__": 
    # --- Запуск логотипу та intro ---
    show_logo()
    intro_screen()

    # --- Поява тексту бою ---
    battle_text = "Entering the battlefield..."
    battle_surf = end_font.render(battle_text, True, WHITE).convert_alpha()
    battle_alpha = 0

    while battle_alpha < 255:
        screen.fill(BLACK)
        battle_alpha = min(battle_alpha + 3, 255)
        battle_surf.set_alpha(battle_alpha)
        screen.blit(battle_surf, (WIDTH//2 - battle_surf.get_width()//2,
                                HEIGHT//2 - battle_surf.get_height()//2))
        clock.tick(75)


    pygame.quit()

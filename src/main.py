import random
from bullet import Bullet
from camera import Camera
from entity import Entity
from hearts import showhearts
from info import Info
from globals import (
    SHOW_INTRO,
    ZOOM_SCALE,
    global_assets,
    NUM_MOBS,
)
import levels.level1 as lvl1
import pygame
from mob import Mob
from outro import game_over_screen
from player import Player

if SHOW_INTRO:
    from intro import init_intro, intro_screen, show_logo

# --- Initialization ---
if not pygame.get_init():
    _ = pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

# --- Display setup ---
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("RustEz")

if SHOW_INTRO:
    init_intro(screen, width, height)  # pyright: ignore[reportPossiblyUnboundVariable]
    show_logo()  # pyright: ignore[reportPossiblyUnboundVariable]
    intro_screen()  # pyright: ignore[reportPossiblyUnboundVariable]

bigrunning = True


def main():
    global bigrunning
    camera = Camera(width, height)
    player = Player(100, 100)

    global_assets.load()

    all_objects: list[Entity] = []
    all_objects += lvl1.map.createTilesArray()

    mobs = [
        Mob(player, random.randrange(-100, 100), random.randrange(-100, 100))
        for _ in range(NUM_MOBS)
    ]
    all_objects += mobs

    bullets: list[Bullet] = []

    collide_rects: list[pygame.Rect] = []
    collide_rects += lvl1.map.createCollisionRects()
    collide_info: list[Info] = []
    collide_info += lvl1.map.createInfoCollisionRects()
    all_objects += collide_info
    running = True

    world_surface = pygame.Surface((width / ZOOM_SCALE, height / ZOOM_SCALE))

    clock = pygame.time.Clock()
    while running:
        # Key handling
        direction = pygame.math.Vector2()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:  # game quit
            running = False
            bigrunning = False
        if keys[pygame.K_w]:
            direction.y = -1
        elif keys[pygame.K_s]:
            direction.y = 1
        else:
            direction.y = 0
        if keys[pygame.K_a]:
            direction.x = -1
            player.side = "left"
        elif keys[pygame.K_d]:
            direction.x = 1
            player.side = "right"
        else:
            direction.x = 0
        if direction.magnitude() != 0:
            direction = direction.normalize()
            player.state = "run"
        else:
            player.state = "idle"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                bigrunning = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # pyright: ignore[reportAny]
                bullets.append(
                    Bullet(
                        player.rect.x,
                        player.rect.y,
                        player.gun_angle,
                        direction * player.speed,
                    )
                )

        # player collision
        # Horizontal
        player.rect.x += int(direction.x * player.speed)
        for rect in collide_rects:
            if player.rect.colliderect(rect):
                if direction.x > 0:  # moving right
                    player.rect.right = rect.left
                elif direction.x < 0:  # moving left
                    player.rect.left = rect.right
        # Vertical
        player.rect.y += int(direction.y * player.speed)
        for rect in collide_rects:
            if player.rect.colliderect(rect):
                if direction.y > 0:  # moving down
                    player.rect.bottom = rect.top
                elif direction.y < 0:  # moving up
                    player.rect.top = rect.bottom

        for info in collide_info:
            if player.rect.colliderect(info.rect):
                # Handle collision
                info.show = True
            else:
                info.show = False

        camera.update(player.rect)
        _ = world_surface.fill((0, 0, 0))

        for obj in all_objects:
            if not isinstance(obj, Mob):
                obj.update()
            obj.draw(world_surface, camera)

        for mob in mobs:
            mob.update(player, mobs)  # pyright: ignore[reportArgumentType]
            if mob.should_remove:
                mobs.remove(mob)

        for bullet in bullets:
            bullet.update(collide_rects, mobs)
            if bullet.should_remove:
                bullets.remove(bullet)
            bullet.draw(world_surface, camera)

        player.update()
        player.draw(world_surface, camera)
        if player.health <= 0:
            running = False
        scaled_surface = pygame.transform.scale(world_surface, (width, height))
        _ = screen.blit(scaled_surface, (0, 0))

        showhearts(screen, player)
        pygame.display.flip()
        _ = clock.tick(60)


while bigrunning:
    main()
    if not bigrunning:
        break
    _ = game_over_screen()

pygame.quit()

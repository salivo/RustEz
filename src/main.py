import random

from camera import Camera
from entity import Entity
from globals import SHOW_INTRO, ZOOM_SCALE
import levels.level1 as lvl1
import pygame
from mob import Mob
from player import Player

if SHOW_INTRO:
    from intro import intro_screen, show_logo


_ = pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("RustEz")
info = pygame.display.Info()
width, height = info.current_w, info.current_h
camera = Camera(width, height)
player = Player(100, 100)


all_objects: list[Entity] = []
all_objects += lvl1.map.createTilesArray()
all_objects.append(player)

mobs = [
    Mob(player, random.randrange(0, 100, 10), random.randrange(0, 100, 10)),
    Mob(player, random.randrange(0, 100, 10), random.randrange(0, 100, 10)),
    Mob(player, random.randrange(0, 100, 10), random.randrange(0, 100, 10)),
    # Mob(player, 10, 20),
    # Mob(player, 20, 10),
    # Mob(player, 30, 30),
]
all_objects += mobs
# all_objects.append(mobs)


collide_rects: list[pygame.Rect] = []
collide_rects += lvl1.map.createCollisionRects()

running = True

if SHOW_INTRO:
    show_logo()  # pyright: ignore[reportPossiblyUnboundVariable]
    intro_screen()  # pyright: ignore[reportPossiblyUnboundVariable]


world_surface = pygame.Surface((width / ZOOM_SCALE, height / ZOOM_SCALE))

while running:
    _ = pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    direction = pygame.math.Vector2()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:  # game quit
        running = False

    if keys[pygame.K_UP]:
        direction.y = -1
    elif keys[pygame.K_DOWN]:
        direction.y = 1
    else:
        direction.y = 0
    if keys[pygame.K_LEFT]:
        direction.x = -1
    elif keys[pygame.K_RIGHT]:
        direction.x = 1
    else:
        direction.x = 0
    if direction.magnitude() != 0:
        direction = direction.normalize()
    # player collision
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

    camera.update(player.rect)
    _ = world_surface.fill((0, 0, 0))

    # Mobs movement
    for obj in all_objects:
        if isinstance(obj, Mob):
            obj.go(player)  # вызываем нужную функцию

    for obj in all_objects:
        obj.draw(world_surface, camera)
    scaled_surface = pygame.transform.scale(world_surface, (width, height))
    _ = screen.blit(scaled_surface, (0, 0))
    pygame.display.update()

pygame.quit()

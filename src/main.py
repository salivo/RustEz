import math
from camera import Camera
from entity import Entity
import levels.level1 as lvl1
import pygame
from mob import Mob

from player import Player

_ = pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("RustEz")
info = pygame.display.Info()
width, height = info.current_w, info.current_h
camera = Camera(width, height)
player = Player(32, 32)

mob = Mob(player)

all_objects: list[Entity] = []
all_objects += lvl1.map.createTilesArray()
all_objects.append(player)
all_objects.append(mob)

collide_rects: list[pygame.Rect] = []
collide_rects += lvl1.map.createCollisionRects()

running = True

while running:
    _ = pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    dx, dy = 0, 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dx = -player.speed
    if keys[pygame.K_RIGHT]:
        dx = player.speed
    if keys[pygame.K_UP]:
        dy = -player.speed
    if keys[pygame.K_DOWN]:
        dy = player.speed
    if dx != 0 and dy != 0:
        dx /= math.sqrt(2)
        dy /= math.sqrt(2)
    # player collistion
    player.rect.x += int(dx)
    for rect in collide_rects:
        if player.rect.colliderect(rect):
            if dx > 0:
                player.rect.right = rect.left
            elif dx < 0:
                player.rect.left = rect.right

    # Vertical
    player.rect.y += int(dy)
    for rect in collide_rects:
        if player.rect.colliderect(rect):
            if dy > 0:
                player.rect.bottom = rect.top
            elif dy < 0:
                player.rect.top = rect.bottom

    camera.update(player.rect)
    _ = screen.fill((0, 0, 0))
    for obj in all_objects:
        obj.draw(screen, camera)
    pygame.display.update()

pygame.quit()

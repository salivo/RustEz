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
player = Player()

mob = Mob(player)

all_objects: list[Entity] = []
all_objects += lvl1.map.createTilesArray()
all_objects.append(player)
all_objects.append(mob)

running = True
while running:
    _ = pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.rect.x += player.speed
    if keys[pygame.K_UP]:
        player.rect.y -= player.speed
    if keys[pygame.K_DOWN]:
        player.rect.y += player.speed

    camera.update(player.rect)
    # Drawing
    _ = screen.fill((0, 0, 0))
    for obj in all_objects:
        obj.draw(screen, camera)
    pygame.display.update()

pygame.quit()

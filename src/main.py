import camera
import levels.level1
import pygame

from player import Player

_ = pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("RustEz")
info = pygame.display.Info()
width, height = info.current_w, info.current_h
camera = camera.Camera(width, height)
player = Player()

speed = 5


all_objects = [player]

x = 0
y = 0
running = True
while running:
    _ = pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    camera.update(player)
    # Drawing
    _ = screen.fill((0, 0, 0))
    for obj in all_objects:
        obj.draw(screen, camera)
    pygame.display.update()

pygame.quit()

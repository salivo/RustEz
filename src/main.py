import camera
from draw import draw_map
import levels.level1
import pygame

from player import Player

_ = pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Simple Rectangle Movement")
info = pygame.display.Info()
width, height = info.current_w, info.current_h
camera = camera.Camera(width, height)
player = Player()
# Rectangle setup
x, y = 0, 0
width, height = 60, 40
speed = 5

# Main loop
running = True
while running:
    _ = pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    player.update(x, y)
    camera.update(player)
    print("Camera position:", player.x, player.y)
    # Drawing
    _ = screen.fill((0, 0, 0))
    draw_map(screen, camera, levels.level1.map)
    player.draw(screen, camera)
    pygame.display.update()

pygame.quit()

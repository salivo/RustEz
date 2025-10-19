import pygame

_ = pygame.init()

# Window setup
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Rectangle Movement")

# Rectangle setup
x, y = 150, 100
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

    # Drawing
    (_,) = screen.fill((0, 0, 0))
    (_,) = pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()

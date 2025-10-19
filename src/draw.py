import pygame
from camera import Camera
from levels import level1


def draw_map(screen: pygame.Surface, camera: Camera, map):
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            _ = pygame.draw.rect(
                screen, (255, 255, 255), (x * 32 + camera.x, y * 32 + camera.y, 32, 32)
            )

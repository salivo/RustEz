import pygame
from camera import Camera
from map import Map


def draw_map(screen: pygame.Surface, camera: Camera, map: Map):
    tilemap = map.tiles
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            _ = pygame.draw.rect(
                screen,
                (255, 255, 255),
                (x * 32 - camera.x, y * 32 - camera.y, 32, 32),
            )

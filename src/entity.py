import pygame

from camera import Camera


class Entity:
    def __init__(self):
        self.rect: pygame.Rect = pygame.Rect(0, 0, 32, 32)

    def draw(self, screen: pygame.Surface, camera: Camera):
        _ = pygame.draw.rect(
            screen,
            (255, 0, 0),
            rect=self.rect.move(-camera.x, -camera.y),
        )

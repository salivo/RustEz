import pygame

from camera import Camera


class Entity:
    def __init__(self, x: int = 0, y: int = 0):
        self.rect: pygame.Rect = pygame.Rect(x, y, 32, 32)
        self.health: int = 100
        self.should_remove: bool = False

    def draw(self, screen: pygame.Surface, camera: Camera):
        _ = pygame.draw.rect(
            screen,
            (255, 0, 0),
            rect=self.rect.move(-camera.x, -camera.y),
        )

    def update(self):
        pass

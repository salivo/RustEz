import pygame
from entity import Entity


class Bullet(Entity):
    def __init__(self, x: int = 0, y: int = 0, direction: int = 0):
        super().__init__()
        self.rect: pygame.Rect = pygame.Rect(x, y, 10, 10)
        self.direction: int = direction

    def update(self):
        pass

import pygame


class Entity:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.width: int = 32
        self.height: int = 32

    def update(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, screen: pygame.Surface):
        _ = pygame.draw.rect(
            screen, (255, 0, 0), (self.x, self.y, self.width, self.height)
        )

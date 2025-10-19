from typing import override
import pygame
import entity


class Player(entity.Entity):
    def __init__(self):
        super().__init__()
        self.x: int = 0
        self.y: int = 0
        self.width: int = 32
        self.height: int = 32

    @override
    def draw(self, screen: pygame.Surface):
        _ = pygame.draw.rect(
            screen, (255, 0, 0), (self.x, self.y, self.width, self.height)
        )

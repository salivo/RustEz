from typing import override
import pygame
from camera import Camera
import entity


class Player(entity.Entity):
    def __init__(self):
        super().__init__()
        self.x: int = 0
        self.y: int = 0
        self.width: int = 32
        self.height: int = 32
        self.speed: int = 5

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):  # pyright: ignore[reportIncompatibleMethodOverride]
        _ = pygame.draw.rect(
            screen,
            (0, 0, 255),
            (self.x - camera.x, self.y - camera.y, self.width, self.height),
        )

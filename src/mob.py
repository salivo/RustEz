import math
import entity
from player import Player
import pygame
from typing import override
from camera import Camera


class Mob(entity.Entity):
    def __init__(self, player: Player):
        super().__init__()
        self.x: int
        self.y: int
        self.width: int = 32
        self.height: int = 32
        self.type: int

    def rangeToPlayer(self, player: Player):
        return math.sqrt(
            math.pow((player.x - self.x), 2) + math.pow((player.y - self.y), 2)
        )

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):
        _ = pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.x - camera.x, self.y - camera.y, self.width, self.height),
        )


# def

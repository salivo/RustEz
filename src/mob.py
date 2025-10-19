import math
import entity
from player import Player
import pygame
from typing import override
from camera import Camera


class Mob(entity.Entity):
    def __init__(self, player: Player):
        super().__init__()
        self.type: int

    def rangeToPlayer(self, player: Player):
        return math.sqrt(
            math.pow((player.rect.x - self.rect.x), 2)
            + math.pow((player.rect.y - self.rect.y), 2)
        )

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):
        _ = pygame.draw.rect(
            screen,
            (0, 0, 255),
            self.rect.move(-camera.x, -camera.y),
        )


# def

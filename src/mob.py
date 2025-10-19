import math
import entity
from player import Player
import pygame
from typing import override
from camera import Camera
from globals import MOBS_SPEED


class Mob(entity.Entity):
    def __init__(self, player: Player, x, y):
        super().__init__()
        self.type: int
        self.rect.x = x
        self.rect.y = y

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

    def go(self, player: Player):
        # range = self.rangeToPlayer(player)
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = (dx**2 + dy**2) ** 0.5  # длина вектора до игрока

        if distance > 0:
            self.rect.x += int(MOBS_SPEED * dx / distance)
            self.rect.y += int(MOBS_SPEED * dy / distance)


# def

import math
from typing import override
import pygame
from entity import Entity
from globals import BULLET_SPEED

MAGIC_X = 10
MAGIC_Y = 19


class Bullet(Entity):
    def __init__(
        self, x: float, y: float, angle: float, player_velocity: pygame.Vector2
    ):
        super().__init__()
        self.pos: pygame.Vector2 = pygame.Vector2(x + MAGIC_X, y + MAGIC_Y)
        self.rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, 5, 5)
        self.angle: float = angle
        self.speed: float = BULLET_SPEED
        self.player_velocity: pygame.Vector2 = player_velocity

    @override
    def update(self):
        move_vec = (
            pygame.Vector2(
                math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))
            )
            * self.speed
        )
        move_vec += self.player_velocity
        self.pos += move_vec
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

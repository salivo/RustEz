import math
import entity
from player import Player
import pygame
from typing import override
from camera import Camera
from globals import MOBS_SPEED, TILE_SIZE, COLLISION_RADIUS, MOB_VISION_RANGE
import random


class Mob(entity.Entity):
    def __init__(self, player, x, y):
        super().__init__()
        self.type = 0
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)

    # def rangeToPlayer(self, player: Player):
    #     return math.sqrt(
    #         math.pow((player.rect.x - self.rect.x), 2)
    #         + math.pow((player.rect.y - self.rect.y), 2)
    #     )

    # @override
    def move_towards_player(self, player):
        if player is None:
            return
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0 and distance < MOB_VISION_RANGE:
            direction = pygame.Vector2(dx, dy) / distance
            self.vel += direction * random.uniform(MOBS_SPEED / 2, MOBS_SPEED)

    def avoid_others(self, mobs):
        if not mobs:
            return
        separation = pygame.Vector2(0, 0)
        count = 0
        for other in mobs:
            if other is self:
                continue
            dx = other.rect.centerx - self.rect.centerx
            dy = other.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if 0 < dist < COLLISION_RADIUS:
                diff = pygame.Vector2(dx, dy)
                if diff.length_squared() != 0:
                    diff.normalize_ip()
                separation -= diff / dist
                count += 1
        if count > 0 and separation.length() > 0:
            separation = separation.normalize() * MOBS_SPEED
            self.vel += separation * 0.5

    def limit_speed(self, max_speed=MOBS_SPEED):
        if self.vel.length() > max_speed:
            self.vel.scale_to_length(max_speed)

    # ---- Совместимая сигнатура ----
    def update(self, *args, **kwargs):
        # пытаемся получить player и mobs из позиционных или ключевых аргументов
        player = None
        mobs = None

        if len(args) >= 1:
            player = args[0]
        if len(args) >= 2:
            mobs = args[1]

        # или из kwargs
        player = kwargs.get("player", player)
        mobs = kwargs.get("mobs", mobs)

        # поведение
        self.move_towards_player(player)
        self.avoid_others(mobs)
        self.limit_speed()
        # применение скорости к позиции/rect
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.vel *= 0.9

        @override
        def draw(self, screen: pygame.Surface, camera: Camera):
            _ = pygame.draw.rect(
                screen,
                (0, 0, 255),
                self.rect.move(-camera.x, -camera.y),
            )


# def

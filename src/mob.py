import math
import entity
from player import Player
import pygame
from typing import override
from camera import Camera
from globals import (
    MOB_BITE_DAMAGE,
    MOBS_SPEED,
    TILE_SIZE,
    COLLISION_RADIUS,
    MOB_VISION_RANGE,
    MVR_MULTIPLIER,
    global_assets,
)
import random

from progressbar import draw_progress_bar_2


class Mob(entity.Entity):
    def __init__(self, player, x, y):
        super().__init__()
        self.type = 0
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)
        self.cooldown: int = 0
        self.image_count: int = 0
        self.frame: float = 0
        self.animation_speed: float = 0.1
        self.die_animation_speed: float = 0.25
        self.angle_to_player: float = 0
        self.dead_animation = False

    def getAngleToPlayer(self, player: Player) -> float:
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return math.degrees(math.atan2(dy, dx))

    def move_towards_player(self, player, is_event_time):
        if player is None:
            return
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0 and distance < (
            MOB_VISION_RANGE + is_event_time * MOB_VISION_RANGE * MVR_MULTIPLIER
        ):
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

    @override
    def update(self, player: Player, mobs: list[entity.Entity], is_event_time: bool):  # pyright: ignore[reportIncompatibleMethodOverride]
        # пытаемся получить player и mobs из позиционных или ключевых аргументов
        if self.health <= 0:
            if global_assets.mob_death_sound:
                _ = global_assets.mob_death_sound.play()
            self.should_remove: bool = True

        self.move_towards_player(player, is_event_time)
        self.avoid_others(mobs)
        self.limit_speed()
        # применение скорости к позиции/rect
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.vel *= 0.9

        if player.rect.colliderect(self.rect):
            if self.cooldown < 0:
                player.health -= MOB_BITE_DAMAGE
                self.cooldown = 50
        self.cooldown -= 1
        frame_count = 4
        if self.frame >= frame_count:
            self.frame = 0
        self.image_count = int(self.frame)
        self.frame += self.animation_speed

        # update angle
        self.angle_to_player = self.getAngleToPlayer(player)

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):
        if self.should_remove:
            frame_end = 7
            if self.frame < frame_end:
                self.frame += self.die_animation_speed
            self.image_count = int(self.frame)
<<<<<<< Updated upstream
=======
            # print(self.image_count)
>>>>>>> Stashed changes

        rotated_image = pygame.transform.rotate(
            global_assets.beetles[self.image_count], -self.angle_to_player + 90
        )
        rect = rotated_image.get_rect(center=self.rect.center)
        rect = rect.move(-camera.x, -camera.y)
        _ = screen.blit(rotated_image, rect)
        if not self.should_remove:
            draw_progress_bar_2(
                screen,
                rect.x,
                rect.y,
                30,
                5,
                self.health / 100,
            )

from typing import override
import pygame
from camera import Camera
import entity
from globals import PLAYER_SPEED, global_assets

PLAYER_MAGIC_OFFSET_TO_CENTER = 7


class Player(entity.Entity):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.rect: pygame.Rect = pygame.Rect(x, y, 20, 32)
        self.image_count = 0
        self.speed: int = PLAYER_SPEED
        self.frame: float = 0
        self.anim_speed: float = 0.1
        self.side: str = "right"
        self.state: str = "idle"
        self.animation_sets = {
            "idle_right": (0, 3),
            "idle_left": (4, 7),
            "run_right": (8, 11),
            "run_left": (12, 15),
        }

    def update(self):
        start, end = self.animation_sets[self.state + "_" + self.side]
        frame_count = end - start + 1
        self.frame += self.anim_speed
        if self.frame >= frame_count:
            self.frame = 0
        self.image_count = start + int(self.frame)

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):
        _ = screen.blit(
            global_assets.player[self.image_count],
            self.rect.move(-camera.x - PLAYER_MAGIC_OFFSET_TO_CENTER, -camera.y),
        )

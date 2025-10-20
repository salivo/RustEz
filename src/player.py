import math
from typing import override
import pygame
from camera import Camera
import entity
from globals import PLAYER_SPEED, ZOOM_SCALE, global_assets

PLAYER_MAGIC_OFFSET_TO_CENTER = 7


class Player(entity.Entity):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.rect: pygame.Rect = pygame.Rect(x, y, 20, 32)
        self.display_rect: pygame.Rect = pygame.Rect(x, y, 20, 32)
        self.image_count: int = 0
        self.speed: float = PLAYER_SPEED
        self.frame: float = 0
        self.anim_speed: float = 0.1
        self.side: str = "right"
        self.state: str = "idle"
        self.animation_sets: dict[str, tuple[int, int]] = {
            "idle_right": (0, 3),
            "idle_left": (4, 7),
            "run_right": (8, 11),
            "run_left": (12, 15),
        }
        self.gun_count: int = 0
        self.gun_angle: float = 0
        self.can_shoot: bool = True

    @override
    def update(self):
        start, end = self.animation_sets[self.state + "_" + self.side]
        frame_count = end - start + 1
        self.frame += self.anim_speed
        if self.frame >= frame_count:
            self.frame = 0
        self.image_count = start + int(self.frame)

        # calculate gun angle
        player_pos = pygame.Vector2(
            self.display_rect.centerx, self.display_rect.centery
        )
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert screen position -> world position
        world_mouse_x = mouse_x / ZOOM_SCALE
        world_mouse_y = mouse_y / ZOOM_SCALE
        world_mouse = pygame.Vector2(world_mouse_x, world_mouse_y)
        direction = world_mouse - player_pos
        self.gun_angle = math.degrees(math.atan2(-direction.y, direction.x))

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):
        self.display_rect = self.rect.move(
            -camera.x - PLAYER_MAGIC_OFFSET_TO_CENTER, -camera.y
        )
        _ = screen.blit(
            global_assets.player[self.image_count],
            self.display_rect,
        )

        image = global_assets.gun[self.gun_count]
        flipped_image = pygame.transform.flip(
            image, False, (self.gun_angle > 90 or self.gun_angle < -90)
        )
        rotated_image = pygame.transform.rotate(flipped_image, self.gun_angle)
        # Keep the center the same as the original rect
        rotated_rect = rotated_image.get_rect(
            center=self.rect.move(-camera.x - 1, -camera.y + 5).center
        )
        _ = screen.blit(rotated_image, rotated_rect.topleft)

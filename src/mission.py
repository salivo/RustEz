from typing import override
import pygame
from camera import Camera
from entity import Entity
from info import drawTextBox
from progressbar import draw_progress_bar


class Mission(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        show: bool = False,
        message: str = """
           Fixing turret
        """,
    ):
        super().__init__(x, y)
        self.rect: pygame.Rect = pygame.Rect(0, 0, 96, 96)
        self.rect.center = (x, y)
        self.show: bool = True
        self.message: str = message
        self.fixed_percent: float = 0.0
        self.fix_speed: float = 0.2

    @override
    def draw(self, screen: pygame.Surface, camera: Camera):
        draw_rect = self.rect.move(-camera.x, -camera.y - 30)
        draw_rect.width = 100
        draw_rect.height = 60
        if self.show:
            drawTextBox(
                draw_rect,
                screen,
                self.message,
            )
            draw_progress_bar(
                screen,
                draw_rect.x + 5,
                draw_rect.y + 30,
                draw_rect.width - 10,
                10,
                self.fixed_percent / 100,
            )

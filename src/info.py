from camera import Camera
from entity import Entity
import pygame

import entity


class Info(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        show: bool = False,
        message: str = "Gerniggerniggernig",
    ):
        super().__init__(x, y)
        self.rect: pygame.Rect = pygame.Rect(0, 0, 96, 96)
        self.rect.center = (x, y)
        self.show = False
        self.message = message

    def draw(self, screen: pygame.Surface, camera: Camera):
        if self.show:
            _ = pygame.draw.rect(
                screen,
                (255, 0, 0),
                rect=self.rect.move(-camera.x, -camera.y),
            )
            draw_rect = self.rect.move(-camera.x, -camera.y)
            draw_rect.centerx += 80  # Offset by 40 pixels on X-axis
            draw_rect.centery -= 80

            # Dark, semi-transparent background (using RGBA for transparency)
            popup_color = (60, 40, 100)  # A darker purple background
            pygame.draw.rect(
                screen, popup_color, draw_rect, border_radius=15
            )  # Rounded corners

            # Shadow effect (optional, gives depth to the pop-up)
            shadow_rect = draw_rect.move(5, 5)  # Slightly offset for the shadow
            pygame.draw.rect(
                screen, (30, 20, 50), shadow_rect, border_radius=15
            )  # Darker shadow color

            # White border around the pop-up (lighter border color)
            border_thickness = 4
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                draw_rect,
                border_radius=15,
                width=border_thickness,
            )

            # Render the message inside the pop-up
            font = pygame.font.Font(None, 32)  # Slightly smaller font for readability
            text = font.render(self.message, True, (255, 255, 255))  # White text
            text_rect = text.get_rect(
                center=draw_rect.center
            )  # Center the text in the pop-up
            screen.blit(text, text_rect)

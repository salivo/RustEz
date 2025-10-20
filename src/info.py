from camera import Camera
from entity import Entity
import pygame

import entity


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Wrap text to fit within a given width."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + " " + word)[0] <= max_width:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word  # Start new line with the current word
    if current_line:
        lines.append(current_line)  # Add the last line

    return lines


def drawTextBox(rect: pygame.Rect, screen: pygame.Surface, message: str):
    draw_rect = rect
    draw_rect.centerx += 80  # Offset by 80 pixels on X-axis
    draw_rect.centery -= 80  # Offset by 80 pixels on Y-axis
    draw_rect.width = 300  # Set the width to 300

    popup_color = (60, 40, 100)
    _ = pygame.draw.rect(screen, popup_color, draw_rect, border_radius=15)

    shadow_rect = draw_rect.move(5, 5)
    _ = pygame.draw.rect(screen, (30, 20, 50), shadow_rect, border_radius=15)

    border_thickness = 1
    _ = pygame.draw.rect(
        screen,
        (255, 255, 255),
        draw_rect,
        border_radius=15,
        width=border_thickness,
    )

    font = pygame.font.Font(None, 17)
    message_lines = message.strip().split("\n")

    y_offset = draw_rect.top + 10
    for line in message_lines:
        wrapped_text = wrap_text(line, font, draw_rect.width - 20)
        for line in wrapped_text:
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(draw_rect.left + 10, y_offset))
            _ = screen.blit(text, text_rect)
            y_offset += font.get_height()


class Info(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        show: bool = False,
        message="""
        Welcome, commander. Your current task is to:
        - Explore the map and locate broken turrets.
        - Defeat enemies and protect your base.
        - Return to me when you're done, so I can give you another assignment.
        """,
    ):
        super().__init__(x, y)
        self.rect: pygame.Rect = pygame.Rect(0, 0, 96, 96)
        self.rect.center = (x, y)
        self.show = False
        self.message = message

    def draw(self, screen: pygame.Surface, camera: Camera):
        if self.show:
            drawTextBox(self.rect.move(-camera.x, -camera.y), screen, self.message)

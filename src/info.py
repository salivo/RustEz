from camera import Camera
from entity import Entity
import pygame


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


def drawTextBox(draw_rect: pygame.Rect, screen: pygame.Surface, message: str):
    # Create a temporary surface with alpha channel
    temp_surface = pygame.Surface(draw_rect.size, pygame.SRCALPHA)

    # Colors with transparency
    popup_color = (60, 40, 100, 127)
    border_color = (255, 255, 255, 127)

    # Draw box
    pygame.draw.rect(
        temp_surface,
        popup_color,
        (0, 0, draw_rect.width, draw_rect.height),
        border_radius=15,
    )

    # Draw border
    border_thickness = 1
    pygame.draw.rect(
        temp_surface,
        border_color,
        (0, 0, draw_rect.width, draw_rect.height),
        border_radius=15,
        width=border_thickness,
    )

    # Draw text
    font = pygame.font.Font(None, 17)
    message_lines = message.strip().split("\n")
    y_offset = 10

    for line in message_lines:
        wrapped_text = wrap_text(line, font, draw_rect.width - 20)
        for wline in wrapped_text:
            text = font.render(wline, True, (255, 255, 255))
            temp_surface.blit(text, (10, y_offset))
            y_offset += font.get_height()

    # Finally, blit the transparent surface onto the main screen
    screen.blit(temp_surface, draw_rect.topleft)


class Info(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        show: bool = False,
        message="""
        Welcome, commander. Your current task is to:
        - Explore the map and locate broken turrets and power supplie.
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
        draw_rect = self.rect.move(-camera.x + 70, -camera.y - 90)
        draw_rect.width = 200
        draw_rect.height = 120
        if self.show:
            drawTextBox(
                draw_rect,
                screen,
                self.message,
            )

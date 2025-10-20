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
        message: str = "NIGGA MUEHEHEHEH NIGGA MUEHEHEHEH NIGGA MUEHEHEHEH NIGGA MUEHEHEHEH NIGGA MUEHEHEHEH NIGGA MUEHEHEHEH NIGGA MUEHEHEHEH",
    ):
        super().__init__(x, y)
        self.rect: pygame.Rect = pygame.Rect(0, 0, 96, 96)
        self.rect.center = (x, y)
        self.show = False
        self.message = message

    def draw(self, screen: pygame.Surface, camera: Camera):
        if self.show:
            # Adjust the rect position based on camera offset and offset it further
            draw_rect = self.rect.move(-camera.x, -camera.y)
            draw_rect.centerx += 80  # Offset by 80 pixels on X-axis
            draw_rect.centery -= 80  # Offset by 80 pixels on Y-axis
            draw_rect.width = 300  # Set the width to 300

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
            border_thickness = 1
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                draw_rect,
                border_radius=15,
                width=border_thickness,
            )

            # Render the message inside the pop-up
            font = pygame.font.Font(None, 17)  # Slightly smaller font for readability
            wrapped_text = self.wrap_text(
                self.message, font, draw_rect.width - 20
            )  # Wrap the text

            # Draw the wrapped text starting from the top-left corner with padding
            y_offset = (
                draw_rect.top + 10
            )  # Start from the top of the pop-up with padding
            for line in wrapped_text:
                text = font.render(line, True, (255, 255, 255))  # White text
                text_rect = text.get_rect(
                    topleft=(draw_rect.left + 10, y_offset)
                )  # Place text with padding
                screen.blit(text, text_rect)  # Blit the text
                y_offset += font.get_height()  # Move down for the next line

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        """Wrap text to fit within a given width."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # Check if the word can fit in the current line
            if font.size(current_line + " " + word)[0] <= max_width:
                current_line += " " + word if current_line else word
            else:
                # If the word doesn't fit, push the current line to the list and start a new line
                lines.append(current_line)
                current_line = word  # Start new line with the current word
        if current_line:
            lines.append(current_line)  # Add the last line

        return lines

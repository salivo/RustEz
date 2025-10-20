from pygame import Rect

from globals import ZOOM_SCALE


class Camera:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.x: int = 0
        self.y: int = 0

    def update(self, target: Rect):
        self.x = target.x - self.width // (2 * ZOOM_SCALE)
        self.y = target.y - self.height // (2 * ZOOM_SCALE)

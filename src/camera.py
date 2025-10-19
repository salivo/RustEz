from entity import Entity


class Camera:
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.x: int = 0
        self.y: int = 0

    def update(self, target: Entity):
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

import entity
from globals import PLAYER_SPEED


class Player(entity.Entity):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.speed: int = PLAYER_SPEED

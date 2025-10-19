import math
import entity
from player import Player


class Mob(entity.Entity):
    def __init__(self, player: Player):
        super().__init__()
        self.x: int = 0
        self.y: int = 0
        self.width: int = 32
        self.height: int = 32

    def rangeToPlayer(self, player: Player):
        return math.sqrt(
            math.pow((player.x - self.x), 2) + math.pow((player.y - self.y), 2)
        )

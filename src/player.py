import entity
from globals import PLAYER_SPEED


class Player(entity.Entity):
<<<<<<< HEAD
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.speed: int = 5
=======
    def __init__(self):
        super().__init__()
        self.speed: int = PLAYER_SPEED
>>>>>>> af88e1b (mobs brains)

import entity


class Player(entity.Entity):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.speed: int = 5

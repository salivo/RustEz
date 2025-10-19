import entity


class Player(entity.Entity):
    def __init__(self):
        super().__init__()
        self.x: int = 0
        self.y: int = 0
        self.width: int = 32
        self.height: int = 32

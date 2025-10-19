from typing import override
import pygame
from camera import Camera
import entity


class Player(entity.Entity):
    def __init__(self):
        super().__init__()
        self.speed: int = 5

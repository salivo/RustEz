from typing import override
import pygame

from globals import TILE_SIZE
from entity import Entity


class Tile(Entity):
    def __init__(self, x: int, y: int, tile_type: int):
        super().__init__()
        self.rect: pygame.Rect = pygame.Rect(
            x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        self.tile_type: int = tile_type

    @override
    def draw(self, screen: pygame.Surface, camera: pygame.Rect):  # pyright: ignore[reportIncompatibleMethodOverride]
        _ = pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect.move(-camera.x, -camera.y),
        )


class Map:
    def __init__(self):
        self.tiles: list[list[int]] = []

    def createTilesArray(self):
        tiles: list[Tile] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tiles.append(Tile(x, y, tile))
        return tiles

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
        color: tuple[int, int, int] = (255, 255, 255)
        if self.tile_type == 0:
            color = (255, 255, 255)
        elif self.tile_type == 1:
            color = (127, 127, 127)

        _ = pygame.draw.rect(
            screen,
            color,
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

    def createCollisionRects(self):
        collide_rects: list[pygame.Rect] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 1:
                    collide_rects.append(
                        pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
        return collide_rects

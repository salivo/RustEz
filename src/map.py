import pygame

from globals import TILE_SIZE


class Tile:
    def __init__(self, x: int, y: int, tile_type: int):
        self.rect: pygame.Rect = pygame.Rect(
            x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        self.tile_type: int = tile_type

    def draw(self, screen: pygame.Surface, camera: pygame.Rect):
        _ = pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect.move(-camera.x, -camera.y),
        )


class Map:
    def __init__(self):
        self.tiles: list[list[int]] = []

    def createTilesArray(self):
        tiles: list[list[Tile]] = []
        for y, row in enumerate(self.tiles):
            new_row: list[Tile] = []
            for x, tile in enumerate(row):
                new_row.append(Tile(x, y, tile))
            tiles.append(new_row)
        return tiles

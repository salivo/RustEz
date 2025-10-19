from typing import override
import pygame

from globals import TILE_SIZE
from entity import Entity


def load_tiles(path: str, size: int):
    sheet = pygame.image.load(path).convert_alpha()
    tiles = []
    for y in range(0, sheet.get_height(), size):
        for x in range(0, sheet.get_width(), size):
            tiles.append(sheet.subsurface(pygame.Rect(x, y, size, size)).copy())
    return tiles


class Tile(Entity):
    def __init__(self, x: int, y: int, tile_type: int, tileset: list[pygame.Surface]):
        super().__init__()
        self.rect: pygame.Rect = pygame.Rect(
            x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        self.tile_type: int = tile_type
        self.tileset = tileset

    @override
    def draw(self, screen: pygame.Surface, camera: pygame.Rect):  # pyright: ignore[reportIncompatibleMethodOverride]
        if self.tile_type == 0:
            screen.blit(self.tileset[0], self.rect.move(-camera.x, -camera.y))
        elif self.tile_type == 1:
            screen.blit(self.tileset[1], self.rect.move(-camera.x, -camera.y))
        elif self.tile_type == 2:
            screen.blit(self.tileset[2], self.rect.move(-camera.x, -camera.y))
        else:
            pygame.draw.rect(
                screen, (255, 255, 255), self.rect.move(-camera.x, -camera.y)
            )


class Map:
    def __init__(self):
        self.tiles: list[list[int]] = []

    def createTilesArray(self):
        tileset = load_tiles("assets/sprite_test.png", TILE_SIZE)
        tiles: list[Tile] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tiles.append(Tile(x, y, tile, tileset))
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

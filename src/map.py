from typing import override

import pygame
from info import Info

from globals import TILE_SIZE, global_assets
from entity import Entity
from globals import TILE_SIZE


def load_tiles(path: str, size: int):
    sheet = pygame.image.load(path).convert_alpha()
    tiles: list[pygame.Surface] = []
    for y in range(0, sheet.get_height(), size):
        for x in range(0, sheet.get_width(), size):
            tiles.append(sheet.subsurface(pygame.Rect(x, y, size, size)).copy())
    return tiles


class Tile(Entity):
    def __init__(self, x: int, y: int, tile_type: int, tile_style: int):
        super().__init__()
        self.rect: pygame.Rect = pygame.Rect(
            x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        self.tile_type: int = tile_type
        self.tile_style: int = tile_style

    @override
    def draw(self, screen: pygame.Surface, camera: pygame.Rect):  # pyright: ignore[reportIncompatibleMethodOverride]
        if self.tile_type == 0:
            return
        try:
            _ = screen.blit(
                global_assets.ground[self.tile_style],
                self.rect.move(-camera.x, -camera.y),
            )
        except Exception:
            _ = screen.blit(
                global_assets.ground[2],
                self.rect.move(-camera.x, -camera.y),
            )


class Map:
    def __init__(self):
        self.tiles: list[list[int]] = []

    def createTilesArray(self):
        tiles: list[Tile] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tiles.append(Tile(x, y, tile, 0))
        return tiles

    def createCollisionRects(self):
        collide_rects: list[pygame.Rect] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 2:
                    collide_rects.append(
                        pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
        return collide_rects

    def createInfoCollisionRects(self):
        collide_info: list[Info] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 5:
                    collide_info.append(
                        Info(
                            x * TILE_SIZE + TILE_SIZE // 2,
                            y * TILE_SIZE + TILE_SIZE // 2,
                        )
                    )
        return collide_info

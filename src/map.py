from typing import override

import pygame
from info import Info

from globals import TILE_SIZE, global_assets
from entity import Entity
from globals import TILE_SIZE
from mission import Mission


def simplifywall(tile: int):
    if tile == 2 or tile == 0:
        return 1
    else:
        return 0


def get_neighbors(grid, x: int, y: int):
    """
    Возвращает список из 8 значений соседних клеток вокруг (x, y)
    Порядок:
    1 2 3
    4 х 5
    6 7 8
    Если соседа нет (за границей), возвращает 0
    """
    rows = len(grid)
    cols = len(grid[0])

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    neighbors = []
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if grid[y][x] == 1:
            neighbors.append(0)
        elif 0 <= ny < rows and 0 <= nx < cols:
            neighbors.append(simplifywall(grid[ny][nx]))
        else:
            neighbors.append(1)
    return neighbors


# --- авто-тайл (9 вариантов) ---
def get_autotile_index(neighbors, center_type=1):
    """
    Возвращает индекс тайла из набора из 9 вариантов.
    Использует 4 основных направления (вверх, вниз, лево, право).
    Порядок соседей:
        1 2 3
        4 X 5
        6 7 8
    """

    # Преобразуем соседей — 1 если совпадает тип, иначе 0
    neighbors = [1 if n == center_type else 0 for n in neighbors]

    n1, n2, n3, n4, n5, n6, n7, n8 = neighbors

    top = n2
    left = n4
    right = n5
    bottom = n7

    # 0 — одиночный
    # 1 — верх
    # 2 — низ
    # 3 — лево
    # 4 — право
    # 5 — верхний левый
    # 6 — верхний правый
    # 7 — нижний левый
    # 8 — нижний правый
    # 9 — центр

    # if 1 == 1:
    #     return 0

    if not top and bottom and left and right:
        return 75  # ++
    elif not bottom and top and left and right:
        return 83  # ++
    elif not left and top and bottom and right:
        return 79
    elif not right and top and bottom and left:
        return 87  # ++
    elif not top and not left and bottom and right:
        return 65  # ++
    elif not top and not right and bottom and left:
        return 63  # ++
    elif not bottom and not left and top and right:
        return 67  # ++
    elif not bottom and not right and top and left:
        return 69  # ++
    elif left and top and bottom and right:
        return 55  # ++
    else:
        return 48  # ++


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
        try:
            if (
                self.tile_type == 0
                or self.tile_type == 1
                or self.tile_type == 2
                or self.tile_type == 5
            ):
                _ = screen.blit(
                    global_assets.ground_tiles[self.tile_style],
                    self.rect.move(-camera.x, -camera.y),
                )
            _ = screen.blit(
                global_assets.ground_tiles[self.tile_style],
                self.rect.move(-camera.x, -camera.y),
            )
            if self.tile_type == 3:
                _ = screen.blit(
                    global_assets.missions[1],
                    self.rect.move(-camera.x, -camera.y),
                )
            if self.tile_type == 6:
                _ = screen.blit(
                    global_assets.missions[3],
                    self.rect.move(-camera.x, -camera.y),
                )
            if self.tile_type == 5:
                _ = screen.blit(
                    global_assets.totem[0],
                    self.rect.move(-camera.x, -camera.y - TILE_SIZE),
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
                tiles.append(
                    Tile(
                        x,
                        y,
                        tile,
                        get_autotile_index(get_neighbors(self.tiles, x, y)),
                    )
                )
                #
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

    def createMissionCollisionRects(self):
        collide_info: list[Mission] = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 3:
                    collide_info.append(
                        Mission(
                            x * TILE_SIZE + TILE_SIZE // 2,
                            y * TILE_SIZE + TILE_SIZE // 2,
                        )
                    )
                elif tile == 6:
                    collide_info.append(
                        Mission(
                            x * TILE_SIZE + TILE_SIZE // 2,
                            y * TILE_SIZE + TILE_SIZE // 2,
                            message="Fixing power",
                        )
                    )
        return collide_info

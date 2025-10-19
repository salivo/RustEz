import pygame
import sys
import os
import json

# usage: python map_drawer.py 64x32 level2.gg
if len(sys.argv) < 3:
    print("Usage: python map_drawer.py WIDTHxHEIGHT filename.gg")
    sys.exit(1)

size_arg = sys.argv[1]
filename = sys.argv[2]

# parse map size
try:
    WIDTH_TILES, HEIGHT_TILES = map(int, size_arg.lower().split("x"))
except ValueError:
    print("Size format must be WIDTHxHEIGHT, e.g., 64x32")
    sys.exit(1)

# tile count (map)
TILE_SIZE = 20
WIDTH = WIDTH_TILES * TILE_SIZE
HEIGHT = HEIGHT_TILES * TILE_SIZE

# Load or create map
if os.path.exists(filename):
    with open(filename, "r") as f:
        try:
            data = json.load(f)
            map_data = data.get("map", [])
        except json.JSONDecodeError:
            map_data = []
else:
    map_data = []

# Ensure map size matches the parameter
map_data = [
    row[:WIDTH_TILES] + [0] * (WIDTH_TILES - len(row))
    for row in map_data[:HEIGHT_TILES]
]
while len(map_data) < HEIGHT_TILES:
    map_data.append([0] * WIDTH_TILES)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Map Drawer - {filename}")

clock = pygame.time.Clock()

colors = [
    (30, 30, 30),  # 0
    (200, 50, 50),  # 1
    (50, 200, 50),  # 2
    (50, 50, 200),  # 3
    (200, 200, 50),  # 4
    (200, 50, 200),  # 5
    (50, 200, 200),  # 6
]

current_tile = 1


def draw_map():
    for y in range(HEIGHT_TILES):
        for x in range(WIDTH_TILES):
            color = colors[map_data[y][x]]
            pygame.draw.rect(
                screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                1,
            )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif pygame.K_0 <= event.key <= pygame.K_6:
                current_tile = event.key - pygame.K_0
                print(f"Selected tile: {current_tile}")
            elif event.key == pygame.K_s:
                with open(filename, "w") as f:
                    json.dump({"map": map_data}, f)
                print(f"Saved map to {filename}")

    # Mouse drawing
    if pygame.mouse.get_pressed()[0]:  # left click
        mx, my = pygame.mouse.get_pos()
        gx, gy = mx // TILE_SIZE, my // TILE_SIZE
        if 0 <= gx < WIDTH_TILES and 0 <= gy < HEIGHT_TILES:
            map_data[gy][gx] = current_tile

    screen.fill((0, 0, 0))
    draw_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

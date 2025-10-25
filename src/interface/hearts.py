import pygame
from globals import global_assets
from entities.player import Player

HEART_SIZE = 32


def showhearts(screen: pygame.Surface, player: Player):
    heart_img = pygame.transform.scale(
        global_assets.hearts[0], (HEART_SIZE, HEART_SIZE)
    )
    half_heart_img = pygame.transform.scale(
        global_assets.hearts[1], (HEART_SIZE, HEART_SIZE)
    )
    no_heart_img = pygame.transform.scale(
        global_assets.hearts[2], (HEART_SIZE, HEART_SIZE)
    )
    max_hearts = 5  # 5 hearts total = 100 HP
    for i in range(max_hearts):
        _ = screen.blit(no_heart_img, (10 + i * HEART_SIZE, 10))
    full_hearts = player.health // 20
    has_half = (player.health % 20) >= 10
    for i in range(full_hearts):
        _ = screen.blit(heart_img, (10 + i * HEART_SIZE, 10))
    if has_half and full_hearts < max_hearts:
        _ = screen.blit(half_heart_img, (10 + full_hearts * HEART_SIZE, 10))

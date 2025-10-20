import pygame

from globals import OVERLAY_ALPHA


def make_dark_overlay(size, alpha=210):
    """One-time: create a dark, per-pixel-alpha surface."""
    overlay = pygame.Surface(size, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    return overlay


def light_circle(overlay, center_px, radius_px, soft_edges=True):
    """Each frame: clears a circular ‘hole’ in the overlay at center_px."""
    cx, cy = map(int, center_px)
    if soft_edges:
        steps = max(8, radius_px // 6)
        for i in range(steps, 0, -1):
            r = int(radius_px * i / steps)
            a = int(OVERLAY_ALPHA * (i - 1) / steps)  # fade to full dark
            pygame.draw.circle(overlay, (0, 0, 0, a), (cx, cy), r)
    else:
        pygame.draw.circle(overlay, (0, 0, 0, 0), (cx, cy), radius_px)

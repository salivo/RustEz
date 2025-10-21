from typing import Iterable

import pygame


class Minimap:
    """
    Standalone minimap for a top-down Pygame world.

    Usage:
        from minimap import Minimap, infer_world_bounds
        world_rect = infer_world_bounds(collide_rects, all_objects)
        minimap = Minimap(world_rect, size=(220, 220), margin=16)  # bottom-left by default
        ...
        minimap.draw(screen, collide_rects, player.rect, mobs, turrets, camera, world_surface)
    """

    def __init__(self, world_rect: pygame.Rect, size=(220, 220), margin=12):
        self.world_rect = world_rect.copy()
        self.size = size
        self.margin = margin
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

        # Scale to fit entire world into minimap surface
        sx = size[0] / max(1, world_rect.w)
        sy = size[1] / max(1, world_rect.h)
        self.scale = min(sx, sy)

        # Center the world inside the minimap surface (letterboxing if needed)
        self.offset_x = (size[0] - world_rect.w * self.scale) * 0.5
        self.offset_y = (size[1] - world_rect.h * self.scale) * 0.5

        # Theme
        self.bg = (8, 8, 12, 210)
        self.border = (200, 200, 220)
        self.wall_color = (70, 90, 120)
        self.player_color = (255, 255, 255)
        self.mob_color = (220, 60, 60)
        self.turret_color = (240, 200, 50)
        self.view_color = (180, 220, 255)
        self.info_color = (80, 200, 255)  # cyan for info

    # ---------------- internal helpers ----------------

    def _world_to_minimap(self, x: float, y: float) -> tuple[int, int]:
        mx = (x - self.world_rect.x) * self.scale + self.offset_x
        my = (y - self.world_rect.y) * self.scale + self.offset_y
        return int(mx), int(my)

    def _rect_world_to_minimap(self, rect: pygame.Rect) -> pygame.Rect:
        x, y = self._world_to_minimap(rect.x, rect.y)
        w = max(1, int(rect.w * self.scale))
        h = max(1, int(rect.h * self.scale))
        return pygame.Rect(x, y, w, h)

    # ---------------- public API ----------------

    def draw(
        self,
        screen: pygame.Surface,
        collide_rects: Iterable[pygame.Rect],
        player_rect: pygame.Rect,
        mobs: Iterable,
        turrets: Iterable,
        infos: Iterable,
        camera,  # expects .x, .y
        world_surface: pygame.Surface,
        corner: str = "bottomleft",  # default: bottom-left
    ) -> None:
        """Draw the minimap UI onto the given screen surface."""
        # background + frame
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(
            self.surface, self.bg, self.surface.get_rect(), border_radius=8
        )
        pygame.draw.rect(
            self.surface, self.border, self.surface.get_rect(), width=2, border_radius=8
        )

        # static geometry (walls/obstacles)
        for r in collide_rects:
            pygame.draw.rect(
                self.surface, self.wall_color, self._rect_world_to_minimap(r)
            )

        # player dot
        px, py = self._world_to_minimap(player_rect.centerx, player_rect.centery)
        pygame.draw.circle(self.surface, self.player_color, (px, py), 3)

        # mobs
        for m in mobs:
            try:
                cx, cy = self._world_to_minimap(m.rect.centerx, m.rect.centery)
                pygame.draw.circle(self.surface, self.mob_color, (cx, cy), 2)
            except Exception:
                # ignore entities without .rect
                pass

        # turrets
        for t in turrets:
            try:
                pygame.draw.rect(
                    self.surface,
                    self.turret_color,
                    self._rect_world_to_minimap(t.rect),
                    width=1,
                )
            except Exception:
                pass

        # infos
        for i in infos:
            try:
                pygame.draw.rect(
                    self.surface,
                    self.info_color,
                    self._rect_world_to_minimap(i.rect),
                    width=1,
                )
            except Exception:
                pass

        # place in chosen corner (default bottom-left)
        dst = self.surface.get_rect()
        if corner == "topleft":
            dst.topleft = (self.margin, self.margin)
        elif corner == "topright":
            dst.topright = (screen.get_width() - self.margin, self.margin)
        elif corner == "bottomright":
            dst.bottomright = (
                screen.get_width() - self.margin,
                screen.get_height() - self.margin,
            )
        else:  # "bottomleft"
            dst.bottomleft = (self.margin, screen.get_height() - self.margin)

        screen.blit(self.surface, dst.topleft)


# ---------- convenience: infer world bounds from existing geometry ----------
def infer_world_bounds(
    collide_rects: Iterable[pygame.Rect],
    objects: Iterable,
    fallback: pygame.Rect | None = None,
) -> pygame.Rect:
    """
    Build a world bounding rect from your level geometry + objects.
    If nothing is found, returns fallback or a generous default.
    """
    rects: list[pygame.Rect] = []
    rects.extend(collide_rects)
    for obj in objects:
        r = getattr(obj, "rect", None)
        if isinstance(r, pygame.Rect):
            rects.append(r)

    if not rects:
        if fallback is not None:
            return fallback.copy()
        return pygame.Rect(-2000, -2000, 4000, 4000)

    world = rects[0].copy()
    for r in rects[1:]:
        world.union_ip(r)
    world.inflate_ip(100, 100)  # add a small border
    return world

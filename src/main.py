import random

import pygame
import math
import levels.level1 as lvl1
import levels.level2 as lvl2
from bullet import Bullet
from camera import Camera
from entity import Entity
from globals import (
    MOB_VISION_RANGE,
    NUM_MOBS,
    OVERLAY_ALPHA,
    LIGHT_RADIUS_PX,
    SHOW_INTRO,
    SOFT_EDGES,
    TILE_SIZE,
    ZOOM_SCALE,
    global_assets,
)
from hearts import showhearts
from info import Info, drawTextBox
from lighting import light_circle, make_dark_overlay
from map import Tile
from minimap import Minimap, infer_world_bounds
from mob import Mob
from outro import game_over_screen
from player import Player
from mission import Mission
from tutorialcomp import tutorial_complete_screen

if SHOW_INTRO:
    from intro import init_intro, intro_screen, show_logo

# --- Initialization ---
if not pygame.get_init():
    _ = pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

global_assets.load()

# --- Display setup ---
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
overlay = make_dark_overlay(screen.get_size(), alpha=210)
pygame.display.set_caption("RustEz")

if SHOW_INTRO:
    init_intro(screen, width, height)  # pyright: ignore[reportPossiblyUnboundVariable]
    show_logo()  # pyright: ignore[reportPossiblyUnboundVariable]
    intro_screen()  # pyright: ignore[reportPossiblyUnboundVariable]

bigrunning = True


def main(lvl):
    global win
    win = False
    mission_checklist: list[bool] = [False, False]
    mission_count = 0
    conditions = [False, False, False]
    global bigrunning
    camera = Camera(width, height)
    player = Player(100, 100)

    all_objects: list[Entity] = []
    all_objects += lvl.map.createTilesArray()

    bullets: list[Bullet] = []
    mobs = []
    collide_rects: list[pygame.Rect] = []
    collide_rects += lvl.map.createCollisionRects()
    collide_info: list[Info] = []
    collide_info += lvl.map.createInfoCollisionRects()
    collide_missions: list[Mission] = []
    collide_missions += lvl.map.createMissionCollisionRects()
    running = True

    world_surface = pygame.Surface((width / ZOOM_SCALE, height / ZOOM_SCALE))

    frame = 0
    frame_speed = 1
    auto_shot_frame = 0

    clock = pygame.time.Clock()
    pygame.mixer.music.load("assets/theme.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    while running:
        frame += frame_speed
        auto_shot_frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                bigrunning = False
        # Key handling
        direction = pygame.math.Vector2()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # game quit
            running = False
            bigrunning = False
        if keys[pygame.K_w]:
            direction.y = -1
            conditions[0] = True
        elif keys[pygame.K_s]:
            direction.y = 1
            conditions[0] = True
        else:
            direction.y = 0
        if keys[pygame.K_a]:
            conditions[1] = True
            direction.x = -1
            player.side = "left"
        elif keys[pygame.K_d]:
            conditions[1] = True
            direction.x = 1
            player.side = "right"
        else:
            direction.x = 0
        if direction.magnitude() != 0:
            direction = direction.normalize()
            player.state = "run"
        else:
            player.state = "idle"

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and player.can_shoot:
            conditions[2] = True
            if auto_shot_frame >= 8:
                bullets.append(
                    Bullet(
                        player.rect.x,
                        player.rect.y,
                        player.gun_angle,
                        direction * player.speed,
                    )
                )
                auto_shot_frame = 0

        # player collision
        # Horizontal
        player.rect.x += int(direction.x * player.speed)
        for rect in collide_rects:
            if player.rect.colliderect(rect):
                if direction.x > 0:  # moving right
                    player.rect.right = rect.left
                elif direction.x < 0:  # moving left
                    player.rect.left = rect.right
        # Vertical
        player.rect.y += int(direction.y * player.speed)
        for rect in collide_rects:
            if player.rect.colliderect(rect):
                if direction.y > 0:  # moving down
                    player.rect.bottom = rect.top
                elif direction.y < 0:  # moving up
                    player.rect.top = rect.bottom

        for info in collide_info:
            if player.rect.colliderect(info.rect):
                info.show = True
            else:
                info.show = False
        in_turret_zone = False

        for mission in collide_missions:
            if player.rect.colliderect(mission.rect):
                mission.show = True
                in_turret_zone = True
                if mission.fixed_percent < 100:
                    mission.fixed_percent += mission.fix_speed
                else:
                    mission_checklist[mission_count] = True
                    mission_count += 1
                    mission.show = False
                    for object in all_objects:
                        if object.rect.colliderect(mission.rect):
                            if isinstance(object, Tile):
                                object.tile_style_overlay -= 1
                    if global_assets.turret_repaired:
                        _ = global_assets.turret_repaired.play()
                    collide_missions.remove(mission)
            else:
                mission.show = False

        player.can_shoot = not in_turret_zone

        is_event_time = in_turret_zone

        angle = random.uniform(0, 2 * math.pi)  # случайный угол
        msx = player.rect.centerx + MOB_VISION_RANGE * math.cos(angle)
        msy = player.rect.centery + MOB_VISION_RANGE * math.sin(angle)
        if frame >= 50 and is_event_time:
            new_mob = Mob(player, msx, msy)

            mobs.append(new_mob)
            all_objects.append(new_mob)
            frame = 0

        camera.update(player.rect)
        _ = world_surface.fill((43, 30, 64))

        for obj in all_objects:
            if not isinstance(obj, Mob):
                obj.update()
            obj.draw(world_surface, camera)

        for mob in mobs:
            mob.update(player, mobs, is_event_time)  # pyright: ignore[reportArgumentType]
            if mob.should_remove:
                mobs.remove(mob)

        for bullet in bullets:
            bullet.update(collide_rects, mobs)
            if bullet.should_remove:
                bullets.remove(bullet)
            bullet.draw(world_surface, camera)

        player.update()
        player.draw(world_surface, camera)

        _ = overlay.fill((0, 0, 0, OVERLAY_ALPHA))
        center_px = (
            int((player.rect.centerx - camera.x)),
            int((player.rect.centery - camera.y)),
        )
        radius_px = LIGHT_RADIUS_PX * TILE_SIZE
        light_circle(overlay, center_px, radius_px // ZOOM_SCALE, soft_edges=SOFT_EDGES)
        _ = world_surface.blit(overlay, (0, 0))

        for info in collide_info:
            info.draw(world_surface, camera)
        for mission in collide_missions:
            mission.draw(world_surface, camera)
        if player.health <= 0:
            running = False
        if False in conditions:
            drawTextBox(
                pygame.Rect((width - 460) / ZOOM_SCALE, 10, 150, 87),
                world_surface,
                """Movement:
                    - W-up,
                    - A-left,
                    - S-down,
                    - D-right,
                    - MouseClick-shoot
                """,
            )

        scaled_surface = pygame.transform.scale(world_surface, (width, height))
        _ = screen.blit(scaled_surface, (0, 0))

        world_rect = infer_world_bounds(collide_rects, all_objects)
        minimap = Minimap(world_rect, size=(220, 220), margin=16)
        minimap.draw(
            screen=screen,
            collide_rects=collide_rects,
            player_rect=player.rect,
            mobs=mobs,
            turrets=collide_missions,
            infos=collide_info,
            camera=camera,
            world_surface=world_surface,
            corner="bottomleft",
        )

        showhearts(screen, player)
        pygame.display.flip()
        _ = clock.tick(60)

        if False not in mission_checklist:
            running = False
            win = True
            _ = pygame.time.delay(1500)


levels = [lvl1, lvl2]
lvl_count = 0
while bigrunning:
    main(levels[lvl_count])
    pygame.mixer.music.stop()
    if not bigrunning:
        break
    if win:
        if global_assets.win:
            _ = global_assets.win.play()
        _ = tutorial_complete_screen()
        lvl_count += 1
        if lvl_count > len(levels):
            bigrunning = False
            break
    else:
        _ = game_over_screen()
pygame.quit()

from typing import Final

import pygame
from pygame.color import Color

FPS: Final[int] = 144
TPS: Final[int] = 60

WINDOW_WIDTH: Final[int] = 600
WINDOW_HEIGHT: Final[int] = 400

BACKGROUND: Final[Color] = Color(28, 17, 23)
MAP_BACKGROUND: Final[Color] = Color(219, 207, 151)
RED: Final[Color] = Color(182, 47, 49)
YELLOW: Final[Color] = Color(204, 170, 68)
WHITE: Final[Color] = Color(240, 240, 221)
BLUE: Final[Color] = Color(90, 140, 166)
GREEN: Final[Color] = Color(104, 110, 70)
CYAN: Final[Color] = Color(146, 232, 192)
WORLD_SIZE: Final[int] = 32
MAP_WORLD_SIZE: Final[int] = WORLD_SIZE // 4
TILES_WIDTH: Final[float] = WINDOW_WIDTH / WORLD_SIZE
TILES_HEIGHT: Final[float] = WINDOW_HEIGHT / WORLD_SIZE
MAP_TILES_WIDTH: Final[float] = WINDOW_WIDTH / MAP_WORLD_SIZE
MAP_TILES_HEIGHT: Final[float] = WINDOW_HEIGHT / MAP_WORLD_SIZE

SHOOT_COOLDOWN: Final[int] = TPS * 1
MELEE_COOLDOWN: Final[int] = TPS * 0.8
MELEE_RANGE: Final[float] = 1.8
ARROW_SPEED: Final[float] = 5
BANDAGE_HEAL_AMOUNT: Final[float] = 3
STEP_THRESHOLD: Final[float] = 1 ** 2 # dist squared

ENEMY_DAMAGE_EVENT: Final[str] = "enemyhit"
ENEMY_KILL_EVENT: Final[str] = "enemykill"
ENEMY_STEP_EVENT: Final[str] = "enemystep"
SWING_SWORD_EVENT: Final[str] = "swingsword"
PLAYER_DAMAGE_EVENT: Final[str] = "playerhit"
PLAYER_KILL_EVENT: Final[str] = "playerkill"
PLAYER_STEP_EVENT: Final[str] = "playerstep"
DENIED_LEVEL_UP_EVENT: Final[str] = "deniedlevelup"
LEVEL_FADE_EVENT: Final[str] = "levelup"
ADD_TRAIT_EVENT: Final[str] = "pickup"
SHOOT_EVENT: Final[str] = "shoot"

K_MOVE_UP: Final[int] = pygame.K_w
K_MOVE_LEFT: Final[int] = pygame.K_a
K_MOVE_DOWN: Final[int] = pygame.K_s
K_MOVE_RIGHT: Final[int] = pygame.K_d
K_OPEN_MAP: Final[int] = pygame.K_m
K_CLOSE: Final[int] = pygame.K_ESCAPE
K_OPEN_MENU: Final[int] = K_CLOSE
K_INTERACT: Final[int] = pygame.K_f
K_SELECT: Final[int] = pygame.K_RETURN
K_ATTACK: Final[int] = pygame.K_h
K_FIRE: Final[int] = pygame.K_j

DEFAULT_SAVE_NAMES: Final[list[str]] = ["Save 1", "Save 2", "Save 3"]

MAIN_TILESET: Final[int] = 0
MAP_TILESET: Final[int] = 1

MAP_SIZE: Final[int] = 80
AMOUNT_ROOMS: Final[int] = 15
ROOM_MIN_SIZE: Final[int] = 8
ROOM_MAX_SIZE: Final[int] = 15
HALLWAY_ROOM_CHANCE: Final[float] = 0.1
HALLWAY_ROOM_MIN_SIZE: Final[int] = 2
HALLWAY_ROOM_MAX_SIZE: Final[int] = 8
ENEMY_COUNT: Final[int] = 8

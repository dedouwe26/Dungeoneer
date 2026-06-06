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
WORLD_SIZE: Final[int] = 32
MAP_WORLD_SIZE: Final[int] = WORLD_SIZE // 2
TILES_WIDTH: Final[float] = WINDOW_WIDTH / WORLD_SIZE
TILES_HEIGHT: Final[float] = WINDOW_HEIGHT / WORLD_SIZE
MAP_TILES_WIDTH: Final[float] = WINDOW_WIDTH / MAP_WORLD_SIZE
MAP_TILES_HEIGHT: Final[float] = WINDOW_HEIGHT / MAP_WORLD_SIZE

SHOOT_COOLDOWN: Final[int] = TPS * 1
MELEE_COOLDOWN: Final[int] = TPS * 0.8
SHOOTING_RANGE: Final[float] = 8
MELEE_RANGE: Final[float] = 1.1
ARROW_SPEED: Final[float] = 5
BANDAGE_HEAL_AMOUNT: Final[float] = 3

ENEMY_DAMAGE_EVENT: Final[str] = "enemyhit"
ENEMY_KILL_EVENT: Final[str] = "enemykill"
SWING_SWORD_EVENT: Final[str] = "swingsword"
PLAYER_DAMAGE_EVENT: Final[str] = "playerhit"
PLAYER_KILL_EVENT: Final[str] = "playerkill"
DENIED_LEVEL_UP_EVENT: Final[str] = "deniedlevelup"
LEVEL_UP_EVENT: Final[str] = "levelup"
PICKUP_EVENT: Final[str] = "pickup"

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

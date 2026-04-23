from typing import Final

import pygame


ENEMY_DAMAGE_SOUND: str = "hit"
PLAYER_DAMAGE_SOUND: str = "hit"
LEVEL_UP_SOUND: str = "levelup"
PICKUP_SOUND: str = "pickup"

K_MOVE_UP: Final[int] = pygame.K_w
K_MOVE_LEFT: Final[int] = pygame.K_a
K_MOVE_DOWN: Final[int] = pygame.K_s
K_MOVE_RIGHT: Final[int] = pygame.K_d
K_OPEN_MAP: Final[int] = pygame.K_r
K_CLOSE: Final[int] = pygame.K_ESCAPE
K_OPEN_MENU: Final[int] = K_CLOSE
K_INTERACT: Final[int] = pygame.K_f
K_SELECT: Final[int] = pygame.K_RETURN
M_ATTACK: Final[int] = 0
M_FIRE: Final[int] = 1

FPS: Final[int] = 144
TPS: Final[int] = 60

DEFAULT_SAVE_NAMES: list[str] = ["Save 1", "Save 2", "Save 3"]

MAIN_TILESET: Final[int] = 0
MAP_TILESET: Final[int] = 1

SIZE: Final[int] = 80
AMOUNT_ROOMS: Final[int] = 15
ROOM_MIN_SIZE: Final[int] = 8
ROOM_MAX_SIZE: Final[int] = 15
HALLWAY_ROOM_CHANCE: Final[float] = 0.1
HALLWAY_ROOM_MIN_SIZE: Final[int] = 2
HALLWAY_ROOM_MAX_SIZE: Final[int] = 8

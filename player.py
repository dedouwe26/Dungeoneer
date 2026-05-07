import math
from random import Random
from typing import Callable, Generator

import config


class Player:
    x: float
    y: float
    max_health: float = 10
    health: float = max_health
    speed: float = 8
    crit_chance: float = 0.05
    strength: float = 1
    bow_cooldown: int = 0  # in ticks
    sword_cooldown: int = 0  # in ticks
    facing: bool = False  # False for east
    on_event: Callable[[str], None]
    collide: Callable[[float, float], bool]

    def __init__(
        self, on_event: Callable[[str], None], collide: Callable[[float, float], bool]
    ) -> None:
        self.on_event = on_event
        self.collide = collide

    def calculate_bandage_count(self) -> int:
        return (
            2
            if self.health < self.max_health * 0.3
            else 1
            if self.health <= self.max_health * 0.5
            else 0
        )

    def heal(self, amount: float):
        self.health = min(self.health + amount, self.max_health)

    def add_trait(self, random: Random):
        match random.randint(0, 3 if self.crit_chance != 1 else 2):
            case 0:
                self.max_health *= 1.1
            case 1:
                self.speed *= 1.1
            case 3:
                self.crit_chance = min(self.crit_chance + 0.1, 1)
            case 2:
                self.strength *= 1.1

    def tile_x(self):
        return math.floor(self.x)

    def tile_y(self):
        return math.floor(self.y)

    def distance_from(self, x: float, y: float) -> float:
        return math.hypot(abs(self.x - x), abs(self.y - y))

    def iterate_neighbouring_tiles(self) -> Generator[tuple[int, int], None, None]:
        for x in range(self.tile_x() - 1, self.tile_x() + 2):
            for y in range(self.tile_y() - 1, self.tile_y() + 2):
                yield (x, y)

    def teleport(self, x: float, y: float):
        self.x = x
        self.y = y

    def damage(self, damage: float):
        if damage > 0:
            self.on_event(config.PLAYER_DAMAGE_EVENT)
        self.health -= damage

    def move(self, dx: float, dy: float):
        if self.collide(self.x + dx, self.y + dy):
            return
        self.x += dx * self.speed
        self.y += dy * self.speed

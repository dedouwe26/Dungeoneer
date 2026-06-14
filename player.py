import math
from typing import Callable, Generator

from pygame import Vector2

import config


class Player:
    x: float
    y: float
    max_health: float = 10
    speed: float = 3
    strength: float = 1
    arrow_strength: float = 0.5
    bow_range: float = 6

    health: float = max_health
    bow_cooldown: int = 0  # in ticks
    sword_cooldown: int = 0  # in ticks
    facing: bool = False  # False for east
    on_event: Callable[[str], None]
    collide: Callable[[float, float], Vector2]
    prev_step: Vector2
    coins: int = 100

    def __init__(
        self,
        on_event: Callable[[str], None],
        collide: Callable[[float, float], Vector2],
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
        self.prev_step = Vector2(self.x, self.y)

    def damage(self, damage: float):
        if damage > 0:
            self.on_event(config.PLAYER_DAMAGE_EVENT)
        self.health -= damage
        if self.health <= 0:
            self.on_event(config.PLAYER_KILL_EVENT)

    def try_step(self):
        p = Vector2(self.x, self.y)
        d = self.prev_step.distance_squared_to(p)
        if d > (config.STEP_THRESHOLD / self.speed * 2):
            self.on_event(config.PLAYER_STEP_EVENT)
            self.prev_step = p

    def move(self, dx: float, dy: float):
        dx *= self.speed
        dy *= self.speed
        col = self.collide(self.x + dx, self.y + dy)
        dx *= col.x
        dy *= col.y
        if dx > 0:
            self.facing = False
        if dx < 0:
            self.facing = True
        self.x += dx
        self.y += dy
        self.try_step()

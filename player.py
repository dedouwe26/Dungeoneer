import math
from typing import Callable


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
    on_sound: Callable[[str], None]
    collide: Callable[[float, float], bool]

    def __init__(
        self, on_sound: Callable[[str], None], collide: Callable[[float, float], bool]
    ) -> None:
        self.on_sound = on_sound
        self.collide = collide

    def calculate_bandage_count(self) -> int:
        return (
            2
            if self.health < self.max_health * 0.3
            else 1
            if self.health <= self.max_health * 0.5
            else 0
        )

    def distance_from(self, x: float, y: float) -> float:
        return math.hypot(abs(self.x - x), abs(self.y - y))

    def teleport(self, x: float, y: float):
        self.x = x
        self.y = y

    def damage(self, damage: float):
        if damage > 0:
            self.on_sound(Game.PLAYER_DAMAGE_SOUND)
        self.health -= damage

    def move(self, dx: float, dy: float):
        if self.collide(self.x + dx, self.y + dy):
            return
        self.x += dx * self.speed
        self.y += dy * self.speed

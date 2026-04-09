import math


class Player:
    x: float
    y: float
    max_health: float = 10
    health: float = max_health
    speed: float = 8
    crit_chance: float = 0.05
    strength: float = 1
    bow_cooldown: int = 0  # in ticks
    facing: bool = False  # False for east

    def __init__(self) -> None:
        pass

    def calculate_bandage_count(self) -> int:
        return 1  # TODO: impl

    def distance_from(self, x: float, y: float) -> float:
        return math.hypot(abs(self.x - x), abs(self.y - y))

    def teleport(self, x: float, y: float):
        self.x = x
        self.y = y

    def damage(self, damage: float):
        self.health -= damage

    def move(self, dx: float, dy: float):
        self.x += dx * self.speed
        self.y += dy * self.speed

    # TODO: Impl other functions (MAYBE IN Game), ranged, interact, melee

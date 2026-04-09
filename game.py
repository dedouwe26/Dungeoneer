# We do not care about rendering here,
# just game logic...
# This file does not depend on other files
# in this codebase.


from enum import Enum
from random import Random
from typing import Any, Final

from map import Map
from player import Player


class Projectile:
    pass


class Enemy:
    # TODO: Collision, also for player, through Game.???
    x: float
    y: float
    strength: float
    attack_cooldown: int = 0
    attack_speed: int
    attack_range: float
    speed: float

    def __init__(self, x: float, y: float, level: int, random: Random) -> None:
        self.x = x
        self.y = y
        self.strength = 1  # TODO: make formula
        self.speed = 1  # TODO: make formula
        self.attack_range = 2 # TODO: You know the drill...
        self.attack_speed = 10 # TODO: I don't need to type it anymore. Lower is faster...

    def attack(self, player: Player):
        if self.attack_cooldown != 0:
            return

        self.attack_cooldown = self.attack_speed
        player.damage(self.strength)

    def move_closer_to(self, x: float, y: float):
        distance = self.speed / 

    def tick(self, deltatime: float, player: Player):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        d = player.distance_from(self.x, self.y)
        if self.attack_range < d < 10:
            self.move_closer_to(player.x, player.y)
        if self.attack_range >= d:
            self.attack(player)
class Tile(Enum):
    empty = 0
    floor = 1
    chest = 2
    entrance = 3
    exit = 4
    bandage = 5

    def has_ground(self) -> bool:
        return self in (self.floor, self.chest, self.entrance, self.exit, self.bandage)


# This class must supply an interface
# used by the rendering of the screens.
class Game:
    TPS: Final[int] = 60

    level: int
    current_random_state: tuple[Any, ...]
    random: Random
    current_map: Map
    player: Player
    enemies: list[Enemy]
    projectiles: list[Projectile]

    def __init__(self) -> None:
        self.level = 1
        self.random = Random()
        self.current_random_state = self.random.getstate()

    def calculate_bandage_count(self):
        return self.player.calculate_bandage_count()

    def generate(self):
        self.current_map = Map(self.random, self.level)
        self.current_map.generate(self.calculate_bandage_count())
        for _ in range(10):
            position = self.random.choice(
                [(x, y) for x, y, t in self.current_map.enumerate() if t == Tile.floor]
            )
            self.enemies.append(
                Enemy(position[0] + 0.5, position[1] + 0.5, self.level, self.random)
            )

    def can_level_up(self):
        return (
            len(self.enemies) == 0
            and self.player.distance_from(
                self.current_map.end[0], self.current_map.end[1]
            )
            < 1
        )

    def level_up(self):
        """Does not check for requirements."""
        self.level += 1
        self.current_random_state = self.random.getstate()
        self.projectiles = []
        self.generate()
        self.player.teleport(self.current_map.start)

    def tick(self, deltatime: float):
        for enemy in self.enemies:
            enemy.tick(deltatime)

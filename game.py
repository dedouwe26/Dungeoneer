# We do not care about rendering here,
# just game logic...
# This file does not depend on other files
# in this codebase.


from random import Random
from typing import Any, Callable

from config import LEVEL_UP_SOUND
from enemy import Enemy
from map import Map, Tile
from player import Player


class Projectile:
    pass


# This class must supply an interface
# used by the rendering of the screens.
class Game:
    level: int
    current_random_state: tuple[Any, ...]
    random: Random
    current_map: Map
    player: Player
    enemies: list[Enemy]
    projectiles: list[Projectile]
    on_sound: Callable[[str], None]

    def __init__(self, on_sound: Callable[[str], None]) -> None:
        self.on_sound = on_sound

    def new_game(self):
        self.player = Player(self.on_sound, self.collide)
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
                Enemy(
                    position[0] + 0.5,
                    position[1] + 0.5,
                    self.random,
                    self.level,
                    self.on_sound,
                    self.collide,
                )
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
        self.on_sound(LEVEL_UP_SOUND)
        self.player.teleport(self.current_map.start[0], self.current_map.start[1])

    def collide(self, x: float, y: float) -> bool:
        return False

    def interact(self):
        # TODO: Check for chests, potions, exits, etc...
        pass

    def ranged(self):
        # TODO: Find closest enemy.
        # TODO: Check if in range.
        # TODO: Shoot! + Cooldown
        pass

    def melee(self):
        # TODO: Swing sword.
        # TODO: Check for enemies.
        # TODO: Cooldown.
        pass

    def tick(self, deltatime: float):
        for enemy in self.enemies:
            enemy.tick(deltatime, self.player)

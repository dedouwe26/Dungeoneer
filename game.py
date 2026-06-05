# We do not care about rendering here,
# just game logic...

import math
from random import Random
from re import S
from sre_compile import dis
from typing import Any, Callable

from pygame import Rect, Vector2

import config
from enemy import Enemy
from map import Map, Tile
from player import Player


class Projectile:
    enemy: Enemy
    angle: float
    x: float
    y: float

    def __init__(self, x: float, y: float, enemy: Enemy) -> None:
        self.enemy = enemy
        self.x = x
        self.y = y

    def tick(self, deltatime: float) -> bool:
        dx = self.enemy.x - self.x
        dy = self.enemy.y - self.y
        print("projectile tick", config.ARROW_SPEED, dx, dy, deltatime)
        if dx <= config.ARROW_SPEED and dy <= config.ARROW_SPEED:
            print("distance closed")
            return True
        print("projectile tick2")
        self.angle = math.degrees(math.atan2(-dy, dx))
        # Normalize
        d = math.hypot(dx, dy)
        dx /= d
        dy /= d
        self.x += deltatime * config.ARROW_SPEED * dx
        self.y += deltatime * config.ARROW_SPEED * dy
        print("wating for next", self.angle)
        return False


# This class must supply an interface
# used by the rendering of the screens.
class Game:
    level: int
    game_over: bool = False
    current_random_state: tuple[Any, ...]
    random: Random
    current_map: Map
    player: Player
    enemies: list[Enemy] = []
    projectiles: list[Projectile] = []
    shoot_cooldown: int = 0
    melee_cooldown: int = 0
    on_event: Callable[[str], None]
    is_initialized: bool = False

    def __init__(self, on_event: Callable[[str], None]) -> None:
        self.on_event = on_event
        print("initialized game")

    def new_game(self):
        print("new game")
        self.player = Player(self.on_event, self.collide)
        self.level = 1
        self.random = Random()
        self.current_random_state = self.random.getstate()
        self.generate()
        self.is_initialized = True
        self.game_over = False

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
                    self.on_event,
                    self.collide,
                )
            )

        self.player.teleport(self.current_map.start[0], self.current_map.start[1])

    def can_level_up(self):
        return (
            len(self.enemies) == 0
            and self.player.distance_from(
                self.current_map.end[0], self.current_map.end[1]
            )
            < 1
            and not self.game_over
        )

    def level_up(self):
        """Does not check for requirements."""
        self.level += 1
        self.current_random_state = self.random.getstate()
        self.projectiles = []
        self.generate()
        self.player.teleport(self.current_map.start[0], self.current_map.start[1])
        self.on_event(config.LEVEL_UP_EVENT)

    def collide(self, x: float, y: float, width: float = 0.68) -> Vector2:
        cx = math.floor(x)
        cy = math.floor(y)
        l = x - width / 2
        r = l + width
        height = 0.1
        t = y - height
        b = t + height
        for x1 in range(cx - 1, cx + 2):
            for y1 in range(cy - 1, cy + 2):
                if not self.current_map.get_tile(x1, y1).has_collision():
                    continue
                n = y1 <= t < y1 + 1
                e = x1 <= r < x1 + 1
                s = y1 <= b < y1 + 1
                w = x1 <= l < x1 + 1
                nw = n and w
                ne = n and e
                sw = s and w
                se = s and e
                if nw or ne or sw or se:
                    return Vector2(0, 0)
        return Vector2(1, 1)

    def interact(self):
        for x, y in self.player.iterate_neighbouring_tiles():
            tile = self.current_map.get_tile(x, y)
            match tile:
                case Tile.bandage:
                    self.player.heal(config.BANDAGE_HEAL_AMOUNT)
                    self.current_map.set_tile(x, y, Tile.empty)
                    # FIXME: The previous does not account for reloading through saves.
                case Tile.exit:
                    if not self.can_level_up():
                        self.on_event(config.DENIED_LEVEL_UP_EVENT)
                        continue
                    self.level_up()
                    break
                case Tile.chest:
                    self.player.add_trait(self.random)
                    break
        pass

    def ranged(self):
        if self.shoot_cooldown > 0:
            return
        print("ranged fire")
        enemy: Enemy | None = None
        distance: float | None = None
        for e in self.enemies:
            d = self.player.distance_from(e.x, e.y)
            if (
                d < config.SHOOTING_RANGE
                and (distance is None or d < distance)
                or distance is None
            ):
                distance = d
                enemy = e

        if enemy is not None:
            self.projectiles.append(Projectile(self.player.x, self.player.y, enemy))
            self.shoot_cooldown = config.SHOOT_COOLDOWN

    def melee(self):
        if self.melee_cooldown > 0:
            return
        print("melee attack")
        self.on_event(config.SWING_SWORD_EVENT)
        for enemy in self.enemies:
            d = self.player.distance_from(enemy.x, enemy.y)
            if d <= config.MELEE_RANGE:
                enemy.damage(self.player.strength)

        self.melee_cooldown = config.MELEE_COOLDOWN

    def tick(self, deltatime: float):
        if self.game_over:
            return
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.melee_cooldown > 0:
            self.melee_cooldown -= 1

        for enemy in self.enemies:
            enemy.tick(deltatime, self.player)

        for projectile in self.projectiles:
            if projectile.tick(deltatime):
                projectile.enemy.damage(self.player.strength)
                self.projectiles.remove(projectile)

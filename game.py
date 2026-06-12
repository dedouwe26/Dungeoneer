# We do not care about rendering here,
# just game logic...

import math
from typing import Any, Callable

from pygame import Vector2

import config
from enemy import Enemy
from map import Map, Tile
from player import Player
from seed import Seed


class Projectile:
    enemy: Enemy
    angle: float = 0
    x: float
    y: float

    def __init__(self, x: float, y: float, enemy: Enemy) -> None:
        self.enemy = enemy
        self.x = x
        self.y = y

    def tick(self, deltatime: float) -> bool:
        dx = self.enemy.x - self.x
        dy = self.enemy.y - self.y
        d = math.hypot(dx, dy)
        if d <= 0.1:
            return True
        self.angle = math.degrees(math.atan2(-dy, dx))
        # Normalize
        dx /= d
        dy /= d
        self.x += deltatime * config.ARROW_SPEED * dx
        self.y += deltatime * config.ARROW_SPEED * dy
        return False


# This class must supply an interface
# used by the rendering of the screens.
class Game:
    level: int
    game_over: bool = False
    current_random_state: tuple[Any, ...]
    seed: Seed
    current_map: Map
    player: Player

    enemies: list[Enemy] = []
    projectiles: list[Projectile] = []
    proj_angle: float
    on_event: Callable[[str], None]
    is_initialized: bool = False

    def __init__(self, seed: Seed, on_event: Callable[[str], None]) -> None:
        self.seed = seed
        self.on_event = on_event
        print("initialized game")

    def new_game(self):
        print("new game")
        self.player = Player(self.on_event, self.collide)
        self.level = 0
        self.create()
        self.is_initialized = True
        self.game_over = False

    def calculate_bandage_count(self):
        return self.player.calculate_bandage_count()

    def create(self):
        print(f"creating level {self.level}")
        self.enemies = []
        self.projectiles = []
        self.current_map = Map(self.seed, self.level)
        if self.level == 0: # Lobby
            self.current_map.generate_lobby()
            self.player.teleport(self.current_map.start[0], self.current_map.start[1])
        else:
            self.current_map.generate(self.calculate_bandage_count())
            for _ in range(config.ENEMY_COUNT):
                position = self.seed.game().choice(
                    [(x, y) for x, y, t in self.current_map.enumerate() if t == Tile.floor]
                )
                self.enemies.append(
                    Enemy(
                        position[0] + 0.5,
                        position[1] + 0.5,
                        self.seed.game(),
                        self.level,
                        self.on_event,
                        self.collide,
                    )
                )

        self.player.teleport(self.current_map.start[0], self.current_map.start[1])

    def can_level_up(self):
        return (
            len(self.enemies) == 0
            and not self.game_over
        )
        
    def escape(self):
        self.level = 0
        self.on_event(config.LEVEL_FADE_EVENT)

    def level_up(self):
        """Does not check for requirements."""
        self.level += 1
        self.on_event(config.LEVEL_FADE_EVENT)

    def collide(self, x: float, y: float, width: float = 0.68) -> Vector2:
        cx = math.floor(x)
        cy = math.floor(y)
        left = x - width / 2
        r = left + width
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
                w = x1 <= left < x1 + 1
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
                    break
                case Tile.exit:
                    if not self.can_level_up():
                        self.on_event(config.DENIED_LEVEL_UP_EVENT)
                        continue
                    self.level_up()
                    break
                case Tile.chest:
                    self.player.coins += self.level
                    self.on_event(config.ADD_TRAIT_EVENT)
                    self.current_map.set_tile(x, y, Tile.floor)
                    # FIXME: The previous does not account for reloading through saves.
                    break
                case Tile.escape:
                    self.escape()
                    break

    def ranged(self):
        if self.player.bow_cooldown > 0:
            return
        enemy: Enemy | None = None
        distance: float | None = None
        for e in self.enemies:
            d = self.player.distance_from(e.x, e.y)
            if d > self.player.bow_range:
                continue
            if (
                distance is None or d < distance
            ):
                distance = d
                enemy = e

        if enemy is not None:
            proj = Projectile(self.player.x, self.player.y, enemy)
            proj.tick(0.010)
            self.proj_angle = proj.angle
            self.projectiles.append(proj)
            self.on_event(config.SHOOT_EVENT)
            self.player.bow_cooldown = config.SHOOT_COOLDOWN

    def melee(self):
        if self.player.sword_cooldown > 0:
            return
        print("melee attack")
        self.on_event(config.SWING_SWORD_EVENT)
        for enemy in self.enemies:
            d = self.player.distance_from(enemy.x, enemy.y)
            if d <= config.MELEE_RANGE:
                enemy.damage(self.player.strength)

        self.player.sword_cooldown = config.MELEE_COOLDOWN

    def tick(self, deltatime: float):
        if self.game_over:
            return
        if self.player.bow_cooldown > 0:
            self.player.bow_cooldown -= 1
        if self.player.sword_cooldown > 0:
            self.player.sword_cooldown -= 1

        for projectile in self.projectiles:
            if projectile.tick(deltatime):
                projectile.enemy.damage(self.player.arrow_strength)
                print("projectile damaged")
                self.projectiles.remove(projectile)

        delqueue = []
        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            if not enemy.tick(deltatime, self.player):
                delqueue.append(i)
        for i in delqueue:
            del self.enemies[i]
            
    def variant_arrow(self) -> int:
        v = min(max(0, math.floor(self.player.arrow_strength * 2) - 1), 8)
        print(v)
        return 
    def variant_bow(self) -> int:
        return 0 if self.player.bow_range < 7 else 1
    def variant_sword(self) -> int:
        return min(max(0, math.floor(self.player.strength) - 1), 7)
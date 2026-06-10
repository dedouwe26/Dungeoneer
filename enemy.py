import math
from random import Random
from typing import Callable

from pygame import Vector2

import config
from player import Player


class Enemy:
    x: float
    y: float
    variant: int
    is_melee: bool
    strength: float
    attack_cooldown: int = 0
    attack_speed: int
    attack_range: float
    health: float
    max_health: float
    speed: float
    facing: bool
    collide: Callable[[float, float], Vector2]
    on_event: Callable[[str], None]
    prev_step: Vector2

    def __init__(
        self,
        x: float,
        y: float,
        random: Random,
        level: int,
        on_event: Callable[[str], None],
        collide: Callable[[float, float], Vector2],
    ) -> None:
        self.x = x
        self.y = y
        self.strength = random.uniform(0.5, 1.1) * level
        self.speed = max(min(random.uniform(0.5, 1) * level, 2.5), 0.5)
        self.max_health = random.uniform(0.5, 1.1) * 5 * level
        self.health = self.max_health
        self.facing = bool(random.getrandbits(1))
        self.attack_range = 1  # TODO: You know the drill...
        self.attack_speed = (
            config.TPS
            // 2  # TODO: I don't need to type it anymore. Oh and lower is faster...
        )
        self.collide = collide
        self.on_event = on_event
        self.variant = random.randint(0, 10)
        self.is_melee = bool(random.getrandbits(1))
        self.prev_step = Vector2(x, y)

    def damage(self, damage: float):
        if damage > 0:
            self.on_event(config.ENEMY_DAMAGE_EVENT)
        self.health -= damage

    def attack(self, player: Player):
        if self.attack_cooldown != 0:
            return

        self.attack_cooldown = self.attack_speed
        player.damage(self.strength)

    def try_step(self):
        p = Vector2(self.x, self.y)
        d = self.prev_step.distance_squared_to(p)
        if d > (config.STEP_THRESHOLD / self.speed / 3):
            self.on_event(config.ENEMY_STEP_EVENT)
            self.prev_step = p

    def move_closer_to(self, x: float, y: float, deltatime: float):
        dx = x - self.x
        dy = y - self.y
        distance = math.hypot(dx, dy)
        offset_x = (dx / distance) * self.speed * deltatime
        offset_y = (dy / distance) * self.speed * deltatime
        col = self.collide(self.x + offset_x, self.y + offset_y)
        offset_x *= col.x
        offset_y *= col.y
        self.x += offset_x
        self.y += offset_y
        self.try_step()
        self.facing = offset_x > 0

    def tick(self, deltatime: float, player: Player) -> bool:
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        d = player.distance_from(self.x, self.y)
        if self.attack_range < d < 6:
            self.move_closer_to(player.x, player.y, deltatime)
        if self.attack_range >= d:
            self.attack(player)
        if self.health <= 0:
            self.on_event(config.ENEMY_KILL_EVENT)
            return False
        return True

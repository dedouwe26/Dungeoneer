import math
from random import Random
from typing import Callable

import config
from player import Player


class Enemy:
    x: float
    y: float
    strength: float
    attack_cooldown: int = 0
    attack_speed: int
    attack_range: float
    health: float
    max_health: float
    speed: float
    facing: bool
    collide: Callable[[float, float], bool]
    on_event: Callable[[str], None]

    def __init__(
        self,
        x: float,
        y: float,
        random: Random,
        level: int,
        on_event: Callable[[str], None],
        collide: Callable[[float, float], bool],
    ) -> None:
        self.x = x
        self.y = y
        self.strength = round(random.uniform(0.5, 1.1), 2) * level
        self.speed = max(min(round(random.uniform(0.3, 0.8), 2) * level, 2.5), 0.5)
        self.max_health = round(random.uniform(0.5, 1.1), 2) * level
        self.health = self.max_health
        self.facing = bool(random.getrandbits(1))
        self.attack_range = 2  # TODO: You know the drill...
        self.attack_speed = (
            10  # TODO: I don't need to type it anymore. Oh and lower is faster...
        )
        self.collide = collide
        self.on_event = on_event

    def damage(self, damage: float):
        if damage > 0:
            self.on_event(config.ENEMY_DAMAGE_EVENT)
        self.health -= damage

    def attack(self, player: Player):
        if self.attack_cooldown != 0:
            return

        self.attack_cooldown = self.attack_speed
        player.damage(self.strength)

    def move_closer_to(self, x: float, y: float, deltatime: float):
        dx = x - self.x
        dy = y - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            offset_x = (dx / distance) * self.speed * deltatime
            offset_y = (dy / distance) * self.speed * deltatime
            if self.collide(self.x + offset_x, self.y + offset_y):
                return
            self.x += offset_x
            self.y += offset_y
            self.facing = offset_y > 0

    def tick(self, deltatime: float, player: Player):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        d = player.distance_from(self.x, self.y)
        if self.attack_range < d < 10:
            self.move_closer_to(player.x, player.y, deltatime)
        if self.attack_range >= d:
            self.attack(player)

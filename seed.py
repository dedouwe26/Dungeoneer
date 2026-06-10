from random import Random
from typing import Any


class Seed:
	game_random_state: tuple[Any, ...]
	game_random: Random
	
	
	def __init__(self) -> None:
		self.game_random = Random()
		self.game_random_state = self.game_random.getstate()

	def seed(self, seed: tuple[Any, ...]):
		self.game_random.setstate(seed)
		self.game_random_state = self.game_random.getstate()

	def game(self) -> Random:
		return self.game_random

	# def rendering(self, offset: int) -> int:
	# 	r = Random()
	# 	r.setstate(self.game_random_state)
	# 	return r.random()
		
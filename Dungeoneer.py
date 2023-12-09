import random
from Player import *

TileType = {"WALL": "■", "FLOOR": "", "BARRIER": "▨", "CHEST": "◊", "ENEMY": "⚉","ENEMY2": "⚇", "BASE": "⌂", "AID": "⛨"}

class Seed:
    seed: list[int]
    def __init__(self, seed: list[int] = [random.randint(0,255) for _ in range(7)]):
        self.seed = seed
    def __str__(self) -> str:
        seed = "&"
        for token in self.seed:
            seed += token.to_bytes().hex()
        return seed
    def GetRandom(self) -> random.Random:
        return random.Random(self.__str__())
class Map:
    name: str
    data: list[list[str]]
    def __init__(self, name: str, seed: Seed):
        self.name = name
    def __str__(self) -> str:
        world=""
        for row in self.data:
            for char in row:
                world+=char
            world+="\n"

class World:
    maps: list[Map]
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
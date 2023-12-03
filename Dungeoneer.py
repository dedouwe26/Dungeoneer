import random

class Seed:
    seed: list[int]
    def __init__(self, seed = [random.randint(0,255) for _ in range(7)]):
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
    data: list[int]
    hasChest: bool
    def __init__(self, name: str, seed: Seed):
        self.name = name
        self.hasChest = bool(seed.GetRandom().getrandbits(1))

class World:
    def __init__(self, seed: Seed):
        self.seed = seed

if __name__ == "__main__":
    worldseed = Seed()
    mainmap = Map("mainmap", worldseed)
    world = World(worldseed)
    print(mainmap.hasChest)
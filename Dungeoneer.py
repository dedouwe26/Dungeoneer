import random

TileType = {"WALL": "■", "FLOOR": "□", "BARRIER": "▨", "CHEST": "◊", "ENEMY": "⚉","ENEMY2": "⚇", "BASE": "⌂", "AID": "⛨"}

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
    mapSeed: Seed
    level: int
    data: list[list[str]]
    def __init__(self, level: int, seed: Seed):
        self.mapSeed = seed
        self.level = level
        self.data = [[TileType["WALL"]]]
    def __str__(self) -> str:
        world=""
        for row in self.data:
            for char in row:
                world+=char
            world+="\n"

IMGWIDTH = 16
IMGHEIGHT = 16

class Player:
    currentSeed: Seed
    isInHub: bool = True
    CurrentMap: Map
    OptionsOpened: bool = False
    X: int = 0
    Y: int = 0
    def __init__(self, seed: Seed):
        self.currentSeed = seed
        self.CurrentMap = Map(0, seed)
    def GetImage(self) -> str:
        return "aaa"
    def Move(self, x: int, y: int) -> str:
        self.X+=x
        self.Y+=y

class Dungeoneer:
    players: dict[int, Player] = {}
    def getPlayer(self, userID: int) -> Player:
        return self.players[userID] if userID in self.players else self.createPlayer(userID)
    def createPlayer(self, id) -> Player:
        player = Player(Seed(id))
        self.players[id] = player
        return player

if __name__ == "__main__":
    pass
import random

TileType = {"FILLED": "#", "FLOOR": " ", "CHEST": "@", "ENEMY": ".", "ENTRANCE": "^", "EXIT": "v", "BANDAGE": "=", "WALL": "_"}

# One tile: 16x16px
# player view size: 16x12 tiles
# screen ratio: (4/3)
TILE_SIZE = 16

# Generator settings
MAP_SIZE =  80
AMOUNT_ROOMS = 15
ROOM_MIN_SIZE = 8
ROOM_MAX_SIZE = 15
HALLWAY_ROOM_CHANCE = 0.1
HALLWAY_ROOM_MIN_SIZE = 2
HALLWAY_ROOM_MAX_SIZE = 8

class Seed:
    seed: int
    def __init__(self, seed: int = random.randint(0,1099511627775), seedKey: str = None):
        if seedKey==None:
            self.seed = seed
        elif seedKey!="":
            self.seed = int(seedKey.removeprefix("&"), 16)
        else:
            self.seed = seed

    def __str__(self) -> str:
        return "&"+hex(self.seed).removeprefix("0x")
    def GetRandom(self) -> random.Random:
        return random.Random(self.__str__())
    def Add(self, lvl: int):
        self.seed += lvl
        return self
        
class Map:
    mapSeed: Seed
    level: int
    rooms: list[tuple[int, int, int, int]] = []
    enemys = list[tuple[int, float, float]]
    map = list[list[str]]
    startPos: tuple[float, float]
    bandages = list[tuple[int, int]]
    chestPos = tuple[int, int]
    def __init__(self, level: int, seed: Seed, enemyCount: int, bandageCount: int = 0):
        self.level = level
        self.mapSeed = seed.Add(self.level)
        self.Generate(enemyCount, bandageCount)

    def Generate(self, enemyCount: int, bandageCount: int):
        self.map = [[TileType["FILLED"] for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        rand: random.Random = self.mapSeed.GetRandom()

        # Generate rooms
        for _ in range(AMOUNT_ROOMS):
            width: int = rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            height: int = rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

            x: int = rand.randint(0, MAP_SIZE - width)
            y: int = rand.randint(0, MAP_SIZE - height)

            # No overlapping (with 1 between)
            while any(
                x-1 < room[0] + room[2] and x-1 + width+1 > room[0] and
                y-1 < room[1] + room[3] and y-1 + height+1 > room[1]
                for room in self.rooms
            ):
                width = rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                height = rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                x = rand.randint(0, MAP_SIZE - width)
                y = rand.randint(0, MAP_SIZE - height)

            self.rooms.append((x, y, width, height))

        # Fill in the rooms
        for room in self.rooms:
            for i in range(room[0], room[0] + room[2]):
                for j in range(room[1], room[1] + room[3]):
                    self.map[i][j] = TileType["FLOOR"]
        
        # Generate hallways
        for i in range(len(self.rooms) - 1):
            # Calculate room centers
            x0: int = self.rooms[i][0] + self.rooms[i][2] // 2
            y0: int = self.rooms[i][1] + self.rooms[i][3] // 2
            x1: int = self.rooms[i + 1][0] + self.rooms[i + 1][2] // 2
            y1: int = self.rooms[i + 1][1] + self.rooms[i + 1][3] // 2
            
            # x hallway
            while x0 != x1:
                self.map[x0][y0] = TileType["FLOOR"]
                x0 += 1 if x0 < x1 else -1

                # Hallway room
                if rand.random() < HALLWAY_ROOM_CHANCE/2:
                    hallway_room_width = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_height = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for i in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for j in range(hallway_room_y, hallway_room_y + hallway_room_height):
                            self.map[i][j] = TileType["FLOOR"]
            # y hallway
            while y0 != y1:
                self.map[x0][y0] = TileType["FLOOR"]
                y0 += 1 if y0 < y1 else -1

                # Hallway room
                if rand.random() < HALLWAY_ROOM_CHANCE / 2:
                    hallway_room_width = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_height = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for i in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for j in range(hallway_room_y, hallway_room_y + hallway_room_height):
                            self.map[i][j] = TileType["FLOOR"]
            
        # Calculate starting position
        self.startPos = (self.rooms[0][0]+self.rooms[0][2]/2, self.rooms[0][1]+self.rooms[0][3]/2)

        # Post-Process

        # entrance
        self.map[self.rooms[0][0] + self.rooms[0][2] // 2][self.rooms[0][1] + self.rooms[0][3] // 2] = TileType["ENTRANCE"]
        # exit
        self.map[self.rooms[AMOUNT_ROOMS-1][0] + self.rooms[AMOUNT_ROOMS-1][2] // 2][self.rooms[AMOUNT_ROOMS-1][1] + self.rooms[AMOUNT_ROOMS-1][3] // 2] = TileType["EXIT"]
        
        # Chest
        floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if self.map[i][j] == TileType["FLOOR"]]

        self.chestPos = random.choice(floor_positions)
        self.map[self.chestPos[0]][self.chestPos[1]] = TileType["CHEST"]

        # Enemy's
        floor_positions = [(rand.getrandbits(1), float(i), float(j)) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if self.map[i][j] == TileType["FLOOR"]]
        self.enemys = random.sample(floor_positions, min(enemyCount, len(floor_positions)))

        # Bandages (health dependent)
        floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if self.map[i][j] == TileType["FLOOR"]]
        self.bandages = random.sample(floor_positions, min(bandageCount, len(floor_positions)))

        for position in self.bandages:
            self.map[position[0]][position[1]] = TileType["BANDAGE"]

    def toMap(self) -> str:
        tempmap = self.map
        for enemy in self.enemys:
            tempmap[round(enemy[1])][round(enemy[2])] = TileType["ENEMY"]
        return "\n".join([" ".join(row) for row in tempmap])
    def toRenderMap(self) -> list[tuple[str, int, int]]:
        result: list[tuple[str, int, int]] = []
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if self.map[y+1][x] == TileType["FLOOR"] and tile == TileType["FILLED"]:
                    tile = TileType["WALL"]
                result.append((tile, x*TILE_SIZE, y*TILE_SIZE))
                


class Player:
    playerSeed: Seed
    isInShop: bool = True
    currentMap: Map
    optionsOpened: bool = False
    level: float = 0
    maxHealth: float = 10
    health: float = maxHealth
    x: float = 0
    y: float = 0
    def LoadData(self, path: str):
        with open(path, "r") as file:
            lines = file.readlines()
            self.level = float(lines[0])
            self.isInShop = bool(lines[1])
            self.playerSeed = Seed(0, lines[2])
            self.x = float(lines[3])
            self.y = float(lines[4])
            self.health = float(lines[5])
            self.maxHealth = float(lines[6])
    def SaveData(self, path: str):
        with open(path, "w") as file:
            file.write(f"{self.level}\n{self.isInShop}\n{self.playerSeed}\n{self.x}\n{self.y}\n{self.health}\n{self.maxHealth}")
    def __init__(self, seed: Seed):
        self.playerSeed = seed
    def AmountBandages(self) -> int:
        # health < 30% : 2, health <= 50% : 1, health > 50% : 0
        return 2 if self.health < self.maxHealth*.3 else 1 if self.health <= self.maxHealth*.5 else 0
    def getCameraOffset(self, width: int, height: int) -> tuple[int, int]:
        self.x
    def Move(self, x: int, y: int):
        self.x+=x
        self.y+=y
    def NextLevel(self):
        self.level+=1
        self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
        self.x = self.currentMap.startPos[0]
        self.y = self.currentMap.startPos[1]

if __name__ == "__main__":
    print(f"Dungeoneer\n{'  '.join([TileType[key]+' = '+key for key in TileType])}")
    seed: Seed = Seed(seedKey=input("seed (nothing for random): "))
    print("Using seed: "+str(seed))
    map: Map = Map(0, seed, 20, 2)
    print(map.toMap())
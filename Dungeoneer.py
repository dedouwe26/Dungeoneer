import random


# One tile: 16x16px
# player view size: 16x12 tiles
# screen ratio: (4/3)
SCREEN_WIDTH = 800 # 320
SCREEN_HEIGHT = 600 # 240
WORLD_SIZE = 3
RAW_TILE_SIZE = 16
TILE_SIZE = RAW_TILE_SIZE*WORLD_SIZE


# Generator settings
MAP_SIZE =  80
AMOUNT_ROOMS = 15
ROOM_MIN_SIZE = 8
ROOM_MAX_SIZE = 15
HALLWAY_ROOM_CHANCE = 0.1
HALLWAY_ROOM_MIN_SIZE = 2
HALLWAY_ROOM_MAX_SIZE = 8

class Tile:
    EMPTY = "#"
    FLOOR = " "
    CHEST = "@"
    ENTRANCE = "^"
    EXIT = "v"
    BANDAGE = "="

    ENEMY = "."

    TYPES = {"EMPTY": EMPTY, "FLOOR":FLOOR, "CHEST":CHEST, "ENTRANCE":ENTRANCE, "EXIT":EXIT, "BANDAGE":BANDAGE, "ENEMY":ENEMY}

    type: str
    def __init__(self, type: str):
        self.type = type
    def hasFloor(self) -> bool:
        return self.type in [self.FLOOR, self.CHEST, self.ENTRANCE, self.EXIT, self.BANDAGE]
    def __str__(self) -> str:
        return self.type
    def __eq__(self, other: object) -> bool:
        return self.type == other.type if isinstance(other, Tile) else self.type == other if isinstance(other, str) else False

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
    renderMap: list[tuple[str, int, int]]
    mapSeed: Seed
    level: int
    rooms: list[tuple[int, int, int, int]] = []
    enemys: list[tuple[float, float]] = []
    map: list[list[Tile]]
    startPos: tuple[float, float]
    endPos: tuple[float, float]
    bandages: list[tuple[int, int]] = []
    chestPos: tuple[int, int]
    chestState: int = 0 # 0 not opened 1 opened 2 looted
    def __init__(self, level: int, seed: Seed, enemyCount: int, bandageCount: int = 0):
        self.level = level
        self.mapSeed = seed.Add(self.level)
        self.Generate(enemyCount, bandageCount)

    def Generate(self, enemyCount: int, bandageCount: int):
        self.map = [[Tile(Tile.EMPTY) for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
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
                    self.map[i][j].type = Tile.FLOOR
        
        # Generate hallways
        for i in range(len(self.rooms) - 1):
            # Calculate room centers
            x0: int = self.rooms[i][0] + self.rooms[i][2] // 2
            y0: int = self.rooms[i][1] + self.rooms[i][3] // 2
            x1: int = self.rooms[i + 1][0] + self.rooms[i + 1][2] // 2
            y1: int = self.rooms[i + 1][1] + self.rooms[i + 1][3] // 2
            
            # x hallway
            while x0 != x1:
                self.map[x0][y0].type = Tile.FLOOR
                x0 += 1 if x0 < x1 else -1

                # Hallway room
                if rand.random() < HALLWAY_ROOM_CHANCE/2:
                    hallway_room_width = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_height = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for j in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for k in range(hallway_room_y, hallway_room_y + hallway_room_height):
                            self.map[j][k].type = Tile.FLOOR
            # y hallway
            while y0 != y1:
                self.map[x0][y0].type = Tile.FLOOR
                y0 += 1 if y0 < y1 else -1

                # Hallway room
                if rand.random() < HALLWAY_ROOM_CHANCE / 2:
                    hallway_room_width = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_height = rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for j in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for k in range(hallway_room_y, hallway_room_y + hallway_room_height):
                            self.map[j][k].type = Tile.FLOOR
            
        # Calculate starting and ending positions
        self.startPos = (round(self.rooms[0][0]+self.rooms[0][2]/2)+.5, round(self.rooms[0][1]+self.rooms[0][3]/2)+.5)
        self.endPos = (round(self.rooms[len(self.rooms)-1][0]+self.rooms[len(self.rooms)-1][2]/2)+.5, round(self.rooms[len(self.rooms)-1][1]+self.rooms[len(self.rooms)-1][3]/2)+.5)
        
        # Post-Process

        # entrance
        self.map[round(self.rooms[0][0]+self.rooms[0][2]/2)][round(self.rooms[0][1]+self.rooms[0][3]/2)].type = Tile.ENTRANCE
        # exit
        self.map[round(self.rooms[len(self.rooms)-1][0]+self.rooms[len(self.rooms)-1][2]/2)][round(self.rooms[len(self.rooms)-1][1]+self.rooms[len(self.rooms)-1][3]/2)].type = Tile.EXIT
        
        # Chest
        floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if self.map[i][j] == Tile.FLOOR]

        self.chestPos = rand.choice(floor_positions)
        floor_positions.remove(self.chestPos)
        self.map[self.chestPos[0]][self.chestPos[1]].type = Tile.CHEST

        # Enemy's
        for i in range(enemyCount):
            position = rand.choice(floor_positions)
            floor_positions.remove(position)
            self.enemys.append((float(position[0]), float(position[1])))

        # Bandages (health dependent)
        self.bandages = rand.sample(floor_positions, min(bandageCount, len(floor_positions)))

        for position in self.bandages:
            self.map[position[0]][position[1]].type = Tile.BANDAGE

        self.GenerateRenderMap()

    def toMap(self) -> str:
        tempmap = self.map
        for enemy in self.enemys:
            tempmap[round(enemy[0])][round(enemy[1])].type = Tile.ENEMY
        return "\n".join([" ".join(row) for row in tempmap])
    def GenerateRenderMap(self):
        self.renderMap = []
        for x, row in enumerate(self.map):
            for y in range(len(row)-1):
                tile = row[y]
                # If floor
                if tile.hasFloor():
                    self.renderMap.append(("floor", x, y))

                    # Shadows
                    try:
                        if self.map[x+1][y]==Tile.EMPTY:
                            self.renderMap.append(("shadowpatchright", x, y))
                    except IndexError:
                        self.renderMap.append(("shadowpatchright", x, y))

                    if self.map[x-1][y]==Tile.EMPTY:
                        self.renderMap.append(("shadowpatchleft", x, y))

                    try:
                        if self.map[x][y+1]==Tile.EMPTY:
                            self.renderMap.append(("shadowpatchbottom", x, y))
                    except IndexError:
                        self.renderMap.append(("shadowpatchbottom", x, y))

                    if self.map[x][y-1]==Tile.EMPTY:
                        self.renderMap.append(("shadowpatchtop", x, y))

                    # Walls
                    if self.map[x][y-1]==Tile.EMPTY:
                        left = False
                        right = False
                        try:
                            left = self.map[x+1][y].hasFloor() and self.map[x+1][y-1] == Tile.EMPTY
                        except IndexError:
                            left = True
                        right = self.map[x-1][y].hasFloor() and self.map[x-1][y-1] == Tile.EMPTY
                        
                        if left and right:
                            self.renderMap.append(("wall", x, y-1-4/RAW_TILE_SIZE))
                        elif not left and not right:
                            self.renderMap.append(("wallboth", x, y-1-4/RAW_TILE_SIZE))
                        elif left:
                            self.renderMap.append(("wallleft", x, y-1-4/RAW_TILE_SIZE))
                        elif right:
                            self.renderMap.append(("wallright", x, y-1-4/RAW_TILE_SIZE))
                    
                    if tile == Tile.CHEST:
                        self.renderMap.append(("closedchest", x, y))
                    elif tile == Tile.ENTRANCE:
                        self.renderMap.append(("entrance", x, y))
                    elif tile == Tile.EXIT:
                        self.renderMap.append(("exit", x, y))
                    elif tile == Tile.BANDAGE:
                        self.renderMap.append(("bandage", x, y))
                # If empty
                if tile == Tile.EMPTY:
                    try:
                        if self.map[x][y+1] == Tile.FLOOR:
                            continue
                    except IndexError:
                        pass
                    isWall = False
                    try:
                        if self.map[x][y+2] == Tile.FLOOR and self.map[x][y+1] == Tile.EMPTY:
                            isWall = True
                    except IndexError:
                        pass
                    if self.map[x][y-1] == Tile.FLOOR:
                        self.renderMap.append(("topedge", x, y))
                    if self.map[x-1][y] == Tile.FLOOR:
                        self.renderMap.append(("leftsideedge", x, y))
                    try:
                        if self.map[x+1][y] == Tile.FLOOR:
                            self.renderMap.append(("rightsideedge", x, y))
                    except IndexError:
                        pass
                    # Inner corner
                    if self.map[x][y-1] == Tile.FLOOR and self.map[x-1][y] == Tile.FLOOR:
                        self.renderMap.append(("innercornertopleft", x, y))

                    try:
                        if self.map[x][y+1] == Tile.FLOOR and self.map[x-1][y] == Tile.FLOOR:
                            self.renderMap.append(("innercornerbottomleft", x, y))
                    except IndexError:
                        pass

                    try:
                        if self.map[x][y-1] == Tile.FLOOR and self.map[x+1][y] == Tile.FLOOR:
                            self.renderMap.append(("innercornertopright", x, y))
                    except IndexError:
                        pass

                    try:
                        if self.map[x][y+1] == Tile.FLOOR and self.map[x+1][y] == Tile.FLOOR:
                            self.renderMap.append(("innercornerbottomright", x, y))
                    except IndexError:
                        pass
                    # Outer corner
                    if self.map[x-1][y-1] == Tile.FLOOR and self.map[x-1][y] == Tile.EMPTY and self.map[x][y-1] == Tile.EMPTY:
                        self.renderMap.append(("outercornertopleft", x, y))

                    try:
                        if self.map[x-1][y+1] == Tile.FLOOR and self.map[x-1][y] == Tile.EMPTY and self.map[x][y+1] == Tile.EMPTY:
                            self.renderMap.append(("outercornerbottomleft", x, y))
                    except IndexError:
                        pass

                    try:
                        if self.map[x+1][y-1] == Tile.FLOOR and self.map[x+1][y] == Tile.EMPTY and self.map[x][y-1] == Tile.EMPTY:
                            self.renderMap.append(("outercornertopright", x, y))
                    except IndexError:
                        pass

                    try:
                        if self.map[x+1][y+1] == Tile.FLOOR and self.map[x+1][y] == Tile.EMPTY and self.map[x][y+1] == Tile.EMPTY:
                            self.renderMap.append(("outercornerbottomright", x, y))
                    except IndexError:
                        pass







        return self.renderMap
                


class Player:
    speed: float = 8
    facing: bool = False
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
            self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
    def SaveData(self, path: str):
        with open(path, "w") as file:
            file.write(f"{self.level}\n{self.isInShop}\n{self.playerSeed}\n{self.x}\n{self.y}\n{self.health}\n{self.maxHealth}")
    def __init__(self, seed: Seed):
        self.playerSeed = seed
        self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
        self.x = self.currentMap.startPos[0]
        self.y = self.currentMap.startPos[1]
    def AmountBandages(self) -> int:
        # health < 30% : 2, health <= 50% : 1, health > 50% : 0
        return 2 if self.health < self.maxHealth*.3 else 1 if self.health <= self.maxHealth*.5 else 0
    def getCameraOffset(self) -> tuple[int, int]:
        return (-(self.x*TILE_SIZE-SCREEN_WIDTH/2), -(self.y*TILE_SIZE-SCREEN_HEIGHT/2))
    def Collide(self, x: float, y: float) -> bool:
        return False
    def Move(self, x: float, y: float):
        if not self.Collide(x*self.speed, y*self.speed):
            self.x+=x*self.speed
            self.y+=y*self.speed
        self.facing = True if x < 0 else False
    def NextLevel(self):
        self.level+=1
        self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
        self.x = self.currentMap.startPos[0]
        self.y = self.currentMap.startPos[1]

if __name__ == "__main__":
    print(f"Dungeoneer\n{'  '.join([Tile.TYPES[key]+' = '+key for key in Tile.TYPES])}")
    seed: Seed = Seed(seedKey=input("seed (nothing for random): "))
    print("Using seed: "+str(seed))
    map: Map = Map(0, seed, 20, 2)
    print(map.toMap())

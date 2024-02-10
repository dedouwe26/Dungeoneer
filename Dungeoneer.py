import math
import os
import random

# One tile: 16x16px
# player view size: 16x12 tiles
# screen ratio: (4/3)
SCREEN_WIDTH = 800 # 320
SCREEN_HEIGHT = 600 # 240
WORLD_SIZE = 3 # 2
RAW_TILE_SIZE = 16
TILE_SIZE = RAW_TILE_SIZE*WORLD_SIZE
MAP_TILE_SIZE = 8


# Generator settings
MAP_SIZE = 80
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
    def Reset(self):
        self.seed = random.randint(0,1099511627775)
    def __init__(self, seed: int = random.randint(0,1099511627775), seedKey: str = ""):
        if seedKey!="":
            self.seed = int(seedKey.removeprefix("&"), 16)
        else:
            self.seed = seed

    def __str__(self) -> str:
        return "&"+hex(self.seed).removeprefix("0x")
    def GetRandom(self) -> random.Random:
        return random.Random(self.__str__())
    def Add(self, lvl: int):
        return Seed(self.seed+lvl)

class Enemy:
    x: float
    y: float
    collisionMap: list[list[Tile]]
    health: float
    maxHealth: float
    strength: float
    speed: float
    facing: bool = False
    variation: str
    cooldown: float = 0
    def __init__(self, collisionMap: list[list[Tile]], x: float, y: float, level: int, random: random.Random):
        self.collisionMap = collisionMap
        self.x = x
        self.y = y
        self.variation = random.choice(["greenenemy0", "greenenemy1", "greenenemy2", "greenenemy3", "greenenemy4", "greenenemy5",
                                        "redenemy0", "redenemy1", "redenemy2", "redenemy3", "redenemy4", "redenemy5"])
        self.strength = round(random.uniform(0.5, 1.1), 2)*level
        self.speed = max(min(round(random.uniform(0.3, 0.8), 2)*level, 2.5), 0.5)
        self.maxHealth = round(random.uniform(0.5, 1.1), 2)*level
        self.health = self.maxHealth
    def Update(self, playerX: float, playerY: float, deltaTime: float) -> bool:
        if abs(math.hypot(self.x-playerX, self.y-playerY))<=0.7:
            if self.cooldown <= 0:
                self.cooldown = 1
                return True
            self.cooldown -= deltaTime
            return False
        if abs(math.hypot(self.x-playerX, self.y-playerY))<=4:
            dx = playerX - self.x
            dy = playerY - self.y
            magnitude = (dx**2 + dy**2)**0.5
            if magnitude > 0:
                offsetX = (dx / magnitude) * self.speed * deltaTime
                offsetY = (dy / magnitude) * self.speed * deltaTime
                if not self.Collide(self.x+offsetX, self.y+offsetY):
                    self.x += offsetX
                    self.y += offsetY
                    self.facing = offsetX > 0
        return False
    def Hit(self, damage: float) -> bool:
        self.health -= damage
        return self.health <= 0
    def Collide(self, x: float, y: float) -> bool:
        x = math.floor(x+1.5/RAW_TILE_SIZE)
        y = math.floor(y+1+7.5/RAW_TILE_SIZE)
        return (self.collisionMap[x][y] in [Tile.EMPTY, Tile.CHEST]) if 0 <= x < len(self.collisionMap) and 0 <= y < len(self.collisionMap[0]) else False

class Map:
    projectiles: list[tuple[float, float, Enemy]] = []
    renderMap: list[tuple[str, int, int]]
    mapSeed: Seed
    level: int
    rooms: list[tuple[int, int, int, int]] = []
    enemies: list[Enemy] = []
    map: list[list[Tile]]
    startPos: tuple[float, float]
    endPos: tuple[float, float]
    bandages: list[tuple[int, int]] = []
    chestPos: tuple[int, int]
    collisionMap: list[list[Tile]]
    chestState: bool = False
    def Reset(self):
        self.projectiles = []
        self.rooms = []
        self.enemies = []
        self.bandages = []
        self.chestState = False
    def __init__(self, level: int, seed: Seed, enemyCount: int, bandageCount: int = 0):
        self.Reset()
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

        self.collisionMap = self.map

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
            self.enemies.append(Enemy(self.collisionMap, float(position[0]), float(position[1]), self.level+1, rand))

        # Bandages (health dependent)
        self.bandages = rand.sample(floor_positions, min(bandageCount, len(floor_positions)))

        for position in self.bandages:
            self.map[position[0]][position[1]].type = Tile.BANDAGE

        # Generate render map
        self.GenerateRenderMap()
    def GetTile(self, x: int, y: int) -> Tile:
        return self.map[x][y] if len(self.map) > x >= 0 and len(self.map[0]) > y >= 0 else Tile(Tile.EMPTY)
    def toMap(self) -> str:
        tempmap = self.map
        for enemy in self.enemies:
            tempmap[round(enemy.x)][round(enemy.y)].type = Tile.ENEMY
        return "\n".join([" ".join([str(tile) for tile in row]) for row in tempmap])
    def GenerateMapRenderMap(self, playerX: float, playerY: float) -> list[tuple[str, int, int]]:
        renderMap = []
        for x in range(-1, MAP_SIZE+1):
            for y in range(-1, MAP_SIZE+1):
                tile = self.GetTile(x,y)
                # If floor
                if tile.hasFloor():
                    renderMap.append(("floor", x, y))
                    
                    if tile==Tile.ENTRANCE:
                        renderMap.append(("entrance", x, y))
                    if tile==Tile.EXIT:
                        renderMap.append(("exit", x, y))
                    if tile==Tile.CHEST:
                        renderMap.append(("chest", x, y))
                    if tile==Tile.BANDAGE:
                        renderMap.append(("bandage", x, y))
                if tile==Tile.EMPTY:
                    if self.GetTile(x+1,y).hasFloor():
                        renderMap.append(("leftedge", x, y))
                    if self.GetTile(x-1,y).hasFloor():
                        renderMap.append(("rightedge", x, y))
                    if self.GetTile(x,y+1).hasFloor():
                        renderMap.append(("topedge", x, y))
                    if self.GetTile(x,y-1).hasFloor():
                        renderMap.append(("bottomedge", x, y))

                    if self.GetTile(x+1,y+1).hasFloor() and self.GetTile(x+1,y)==Tile.EMPTY and self.GetTile(x,y+1)==Tile.EMPTY:
                        renderMap.append(("topleftcorner", x, y))
                    if self.GetTile(x-1,y+1).hasFloor() and self.GetTile(x-1,y)==Tile.EMPTY and self.GetTile(x,y+1)==Tile.EMPTY:
                        renderMap.append(("toprightcorner", x, y))
                    if self.GetTile(x-1,y-1).hasFloor() and self.GetTile(x-1,y)==Tile.EMPTY and self.GetTile(x,y-1)==Tile.EMPTY:
                        renderMap.append(("bottomrightcorner", x, y))
                    if self.GetTile(x+1,y-1).hasFloor() and self.GetTile(x+1,y)==Tile.EMPTY and self.GetTile(x,y-1)==Tile.EMPTY:
                        renderMap.append(("bottomleftcorner", x, y))
        renderMap.append(("player", math.floor(playerX), math.floor(playerY)))
        for enemy in self.enemies:
            renderMap.append(("enemy", math.floor(enemy.x), math.floor(enemy.y)))
        return renderMap
    def GenerateRenderMap(self):
        self.renderMap = []
        for x in range(-1, MAP_SIZE+1):
            for y in range(-1, MAP_SIZE+1):
                tile = self.GetTile(x,y)
                # If floor
                if tile.hasFloor():
                    self.renderMap.append(("floor", x, y))

                    # Shadows
                    if self.GetTile(x+1,y)==Tile.EMPTY:
                        self.renderMap.append(("shadowpatchright", x, y))

                    if self.GetTile(x-1,y)==Tile.EMPTY:
                        self.renderMap.append(("shadowpatchleft", x, y))

                    if self.GetTile(x,y+1)==Tile.EMPTY:
                        self.renderMap.append(("shadowpatchbottom", x, y))

                    if self.GetTile(x,y-1)==Tile.EMPTY:
                        self.renderMap.append(("shadowpatchtop", x, y))

                    # Walls
                    if self.GetTile(x,y-1)==Tile.EMPTY:
                        left = self.GetTile(x+1,y).hasFloor() and self.GetTile(x+1,y-1) == Tile.EMPTY

                        right = self.GetTile(x-1,y).hasFloor() and self.GetTile(x-1,y-1) == Tile.EMPTY
                        
                        if left and right:
                            self.renderMap.append(("wall", x, y-1))
                        elif not left and not right:
                            self.renderMap.append(("wallboth", x, y-1))
                        elif left:
                            self.renderMap.append(("wallleft", x, y-1))
                        elif right:
                            self.renderMap.append(("wallright", x, y-1))
                    
                    if tile == Tile.CHEST:
                        self.renderMap.append(("closedchest" if not self.chestState else "emptychest", x, y))
                    elif tile == Tile.ENTRANCE:
                        self.renderMap.append(("entrance", x, y))
                    elif tile == Tile.EXIT:
                        self.renderMap.append(("exit", x, y))
                    elif tile == Tile.BANDAGE:
                        self.renderMap.append(("bandage", x, y))
                # If empty
                if tile == Tile.EMPTY:
                    if self.GetTile(x,y+1).hasFloor():
                        continue
                    wallRight=self.GetTile(x+1,y+1).hasFloor() and self.GetTile(x+1,y) == Tile.EMPTY
                    wallLeft=self.GetTile(x-1,y+1).hasFloor() and self.GetTile(x-1,y) == Tile.EMPTY

                    if self.GetTile(x,y-1).hasFloor():
                        self.renderMap.append(("topedge", x, y))
                    if self.GetTile(x-1,y).hasFloor() or wallLeft:
                        self.renderMap.append(("leftsideedge", x, y))
                    if self.GetTile(x+1, y).hasFloor() or wallRight:
                        self.renderMap.append(("rightsideedge", x, y))
                    # Inner corner
                    if self.GetTile(x, y-1).hasFloor() and self.GetTile(x+1, y).hasFloor():
                        self.renderMap.append(("innercornerbottomleft", x, y))

                    if self.GetTile(x, y-1).hasFloor() and self.GetTile(x-1, y).hasFloor():
                        self.renderMap.append(("innercornerbottomright", x, y))

                    # Outer corner
                    if wallRight:
                        self.renderMap.append(("outercornertopleft", x, y))

                    if self.GetTile(x+1, y-1).hasFloor() and self.GetTile(x+1, y) == Tile.EMPTY and self.GetTile(x, y-1) == Tile.EMPTY:
                        self.renderMap.append(("outercornerbottomleft", x, y))

                    if wallLeft:
                        self.renderMap.append(("outercornertopright", x, y))
                        
                    if self.GetTile(x-1, y-1).hasFloor() and self.GetTile(x-1, y) == Tile.EMPTY and self.GetTile(x, y-1) == Tile.EMPTY:
                        self.renderMap.append(("outercornerbottomright", x, y))
        return self.renderMap
                
class Player:
    facing: bool = False
    playerSeed: Seed
    hasMapOpen: bool = False
    currentMap: Map
    optionsOpened: bool = False
    level: int = 0
    maxHealth: int = 10 # yellow
    health: float = maxHealth 
    speed: float = 4 # green
    critchange: float = 0.05 # blue
    strength: float = 1 # red
    x: float = 0
    y: float = 0
    dead: bool = False
    bowCooldown: float = 0
    drops: list[tuple[float, float, str]] = []
    errorFade: bool = False
    nextMapFade: bool = False
    def LoadData(self, path: str):
        with open(path, "r") as file:
            lines = file.readlines()
            self.level = int(lines[0])
            self.playerSeed = Seed(0, lines[1])
            self.x = float(lines[2])
            self.y = float(lines[3])
            self.health = float(lines[4])
            self.maxHealth = int(lines[5])
            self.critchange = float(lines[6])
            self.speed = float(lines[7])
            self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
    def SaveData(self, path: str):
        if not os.path.isdir("./saves"):
            os.mkdir("saves")
        with open(os.path.abspath(path), "w") as file:
            file.write(f"{self.level}\n{self.playerSeed}\n{self.x}\n{self.y}\n{self.health}\n{self.maxHealth}\n{self.critchange}\n{self.speed}")
    def __init__(self, seed: Seed):
        self.playerSeed = seed
        self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
        self.x = self.currentMap.startPos[0]
        self.y = self.currentMap.startPos[1]
    def AmountBandages(self) -> int:
        # health < 30% : 2, health <= 50% : 1, health > 50% : 0
        return 2 if self.health < self.maxHealth*.3 else 1 if self.health <= self.maxHealth*.5 else 0
    def getCameraOffset(self) -> tuple[float, float]:
        return (-(self.x*TILE_SIZE-SCREEN_WIDTH/2), -(self.y*TILE_SIZE-SCREEN_HEIGHT/2))
    def Hit(self, damage: float) -> bool:
        self.health-=damage
        self.dead = self.health <= 0
        return self.dead
    def Melee(self) -> tuple[bool, bool, list[tuple[float, float]]]:
        hit: tuple[bool, bool, list[tuple[float, float]]] = [False, False, []]
        for enemy in self.currentMap.enemies:
            if abs(math.hypot(self.x-enemy.x, self.y-enemy.y)) >= 2.2:
                continue
            crit = random.random() < self.critchange
            if crit:
                hit[2].append((enemy.x+random.random(), enemy.y+random.random(), 1))
            if enemy.Hit(self.strength + (self.strength*0.3 if crit else 0)):
                self.currentMap.enemies.remove(enemy)
                hit[1] = True
                del enemy
            else:
                hit[0] = True
        return hit
    def Range(self):
        if self.bowCooldown <= 0:

            for enemy in self.currentMap.enemies:
                self.bowCooldown=1
                if abs(math.hypot(self.x-enemy.x, self.y-enemy.y)) >= 10:
                    continue
                self.currentMap.projectiles.append([self.x, self.y, enemy])  
                break
    def Heal(self):
        # Add 10% health
        self.health=min(self.health+self.maxHealth*.1, self.maxHealth)
    def Interact(self) -> bool:
        for drop in self.drops:
            if abs(math.hypot(self.x-drop[0], self.y-drop[1])) < 1:
                if drop[2] == "bluepotion":
                    # crit
                    self.critchange=min(self.critchange+0.05, 1)
                elif drop[2] == "yellowpotion":
                    # max health
                    self.maxHealth+=1
                elif drop[2] == "redpotion":
                    # strength
                    self.strength+=1
                elif drop[2] == "greenpotion":
                    # speed
                    self.speed+=1
                self.drops.remove(drop)
                return True
        for tile in [(self.currentMap.GetTile(math.floor(self.x-1), math.floor(self.y-1)), -1, -1), (self.currentMap.GetTile(math.floor(self.x-1), math.floor(self.y)), -1, 0), (self.currentMap.GetTile(math.floor(self.x-1), math.floor(self.y+1)), -1, 1),
                     (self.currentMap.GetTile(math.floor(self.x), math.floor(self.y-1)), 0, -1), (self.currentMap.GetTile(math.floor(self.x), math.floor(self.y)), 0, 0), (self.currentMap.GetTile(math.floor(self.x), math.floor(self.y+1)), 0, 1),
                     (self.currentMap.GetTile(math.floor(self.x+1), math.floor(self.y-1)), 1, -1),(self.currentMap.GetTile(math.floor(self.x+1), math.floor(self.y)), 1, 0),(self.currentMap.GetTile(math.floor(self.x+1), math.floor(self.y+1)), 1, 1)]:
            if tile[0]==Tile.CHEST and not self.currentMap.chestState:
                self.currentMap.chestState = True
                self.drops.append((self.x, self.y, self.currentMap.mapSeed.GetRandom().choice(["redpotion", "greenpotion", "yellowpotion", "bluepotion"])))
                self.currentMap.GenerateRenderMap()
            elif tile[0]==Tile.BANDAGE:
                self.Heal()
                self.currentMap.map[math.floor(self.x+tile[1])][math.floor(self.y+tile[2])].type = Tile.FLOOR
                self.currentMap.GenerateRenderMap()
            elif tile[0]==Tile.EXIT:
                if len(self.currentMap.enemies)!=0:
                    self.errorFade = True
                else:
                    self.nextMapFade = True
    def Collide(self, x: float, y: float) -> bool:
        return self.currentMap.GetTile(math.floor(x+1.5/RAW_TILE_SIZE), math.floor(y+7.5/RAW_TILE_SIZE)) in ([Tile.EMPTY, Tile.CHEST] if not self.currentMap.chestState else [Tile.EMPTY])
    def Move(self, x: float, y: float):
        if self.dead:
            return
        if not self.Collide(self.x+x*self.speed, self.y+y*self.speed):
            self.x+=x*self.speed
            self.y+=y*self.speed
        if x!=0:
            self.facing = True if x < 0 else False
    def NextLevel(self) -> bool:
        self.level+=1
        self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
        self.x = self.currentMap.startPos[0]
        self.y = self.currentMap.startPos[1]
    def Reset(self):
        self.playerSeed.Reset()
        self.maxHealth = 10
        self.health = self.maxHealth
        self.speed = 4
        self.strength = 1
        self.bowCooldown = 0
        self.drops = []
        self.level = 0
        self.errorFade = self.nextMapFade = self.hasMapOpen = self.facing = self.dead = False
        
        self.currentMap = Map(self.level, self.playerSeed, 10, bandageCount=self.AmountBandages())
        self.x = self.currentMap.startPos[0]
        self.y = self.currentMap.startPos[1]
        

class Menu:
    opened: bool = True
    cursor: int = 0
    current: str = "Main"
    _mainmenu: list[str] = ["New Game", "Load Game", "Save Game", "Exit"]
    def Select(self) -> str:
        if self.current == "Main":
            if self.cursor == 0 or self.cursor == 3:
                self.opened = False
                if self.cursor == 0:
                    return "n"
                else:
                    return "e"
            elif self.cursor == 1:
                self.cursor = 0
                self.current = "Load Game"
            elif self.cursor == 2:
                self.cursor = 0
                self.current = "Save Game"
        elif self.current == "Load Game":
            self.opened = False
            if self.cursor == 0:
                return "l1"
            elif self.cursor == 1:
                return "l2"
            elif self.cursor == 2:
                return "l3"
        elif self.current == "Save Game":
            self.opened = False
            if self.cursor == 0:
                return "s1"
            elif self.cursor == 1:
                return "s2"
            elif self.cursor == 2:
                return "s3"
        return ""
    def Back(self):
        self.current = "Main"
    def Up(self):
        if self.cursor-1 >= 0:
            self.cursor -= 1
    def Down(self):
        if self.current == "Main" and self.cursor+1 < len(self._mainmenu):
            self.cursor += 1
        elif self.cursor+1 < 3: 
            self.cursor += 1
    def getRenderText(self) -> list[tuple[str, bool]]:
        if self.current == "Main":
            return [("New Game", self.cursor==0), ("Load Game", self.cursor==1), ("Save Game", self.cursor==2), ("Exit", self.cursor==3)]
        else:
            return [("Game 1", self.cursor==0), ("Game 2", self.cursor==1), ("Game 3", self.cursor==2)]


if __name__ == "__main__":
    print(f"Dungeoneer\n{'  '.join([Tile.TYPES[key]+' = '+key for key in Tile.TYPES])}")
    seed: Seed = Seed(seedKey=input("seed (nothing for random): "))
    print("Using seed: "+str(seed))
    map: Map = Map(0, seed, 20, 2)
    print(map.toMap())

# Made by: @dedouwe26 (0xDED)
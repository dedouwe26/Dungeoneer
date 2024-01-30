import random

TileType = {"FILLED": "#", "FLOOR": " ", "CHEST": "@", "ENEMY": ".", "ENTRANCE": "^", "EXIT": "v", "BANDAGE": "="}

# Generator settings
MAP_SIZE =  80
AMOUNT_ROOMS = 15
ROOM_MIN_SIZE = 8
ROOM_MAX_SIZE = 15
HALLWAY_ROOM_CHANCE = 0.1
HALLWAY_ROOM_MIN_SIZE = 2
HALLWAY_ROOM_MAX_SIZE = 8

class Map:
    rand: random.Random
    rooms: list[tuple[int, int, int, int]] = []
    enemys: list[tuple[float, float]]
    map: list[list[str]]
    startPos: tuple[float, float]
    endPos: tuple[float, float]
    bandages: list[tuple[int, int]]
    chestPos: tuple[int, int]
    def __init__(self, rand: random.Random, enemyCount: int, bandageCount: int = 0):
        self.rand = rand
        self.Generate(enemyCount, bandageCount)

    def Generate(self, enemyCount: int, bandageCount: int):
        self.map = [[TileType["FILLED"] for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

        # Generate rooms
        for _ in range(AMOUNT_ROOMS):
            width: int = self.rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            height: int = self.rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

            x: int = self.rand.randint(0, MAP_SIZE - width)
            y: int = self.rand.randint(0, MAP_SIZE - height)

            # No overlapping (with 1 between)
            while any(
                x-1 < room[0] + room[2] and x-1 + width+1 > room[0] and
                y-1 < room[1] + room[3] and y-1 + height+1 > room[1]
                for room in self.rooms
            ):
                width = self.rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                height = self.rand.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                x = self.rand.randint(0, MAP_SIZE - width)
                y = self.rand.randint(0, MAP_SIZE - height)

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
                if self.rand.random() < HALLWAY_ROOM_CHANCE/2:
                    hallway_room_width = self.rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_height = self.rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for j in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for k in range(hallway_room_y, hallway_room_y + hallway_room_height):
                            self.map[j][k] = TileType["FLOOR"]
            # y hallway
            while y0 != y1:
                self.map[x0][y0] = TileType["FLOOR"]
                y0 += 1 if y0 < y1 else -1

                # Hallway room
                if self.rand.random() < HALLWAY_ROOM_CHANCE / 2:
                    hallway_room_width = self.rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_height = self.rand.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for j in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for k in range(hallway_room_y, hallway_room_y + hallway_room_height):
                            self.map[j][k] = TileType["FLOOR"]
            
        # Calculate starting and ending positions
        self.startPos = (self.rooms[0][0]+self.rooms[0][2]/2, self.rooms[0][1]+self.rooms[0][3]/2)
        self.endPos = (self.rooms[len(self.rooms)-1][0]+self.rooms[len(self.rooms)-1][2]/2, self.rooms[len(self.rooms)-1][1]+self.rooms[len(self.rooms)-1][3]/2)
        
        # Post-Process

        # entrance
        self.map[round(self.startPos[0])][round(self.startPos[1])] = TileType["ENTRANCE"]
        # exit
        self.map[round(self.endPos[0])][round(self.endPos[1])] = TileType["EXIT"]
        
        # Chest
        floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if self.map[i][j] == TileType["FLOOR"]]

        self.chestPos = self.rand.choice(floor_positions)
        floor_positions.remove(self.chestPos)
        self.map[self.chestPos[0]][self.chestPos[1]] = TileType["CHEST"]

        # Enemy's
        for i in range(enemyCount):
            position = self.rand.choice(floor_positions)
            floor_positions.remove(position)
            self.enemys.append(position)

        # Bandages
        self.bandages = self.rand.sample(floor_positions, min(bandageCount, len(floor_positions)))

        for position in self.bandages:
            self.map[position[0]][position[1]] = TileType["BANDAGE"]

    def toMap(self) -> str:
        tempmap: list[list[str]] = self.map
        for enemy in self.enemys:
            tempmap[round(enemy[0])][round(enemy[1])] = TileType["ENEMY"]
        return "\n".join([" ".join(row) for row in tempmap])

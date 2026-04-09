from random import Random
from typing import Final, Generator

from game import Tile


class Map:
    SIZE: Final[int] = 80
    AMOUNT_ROOMS: Final[int] = 15
    ROOM_MIN_SIZE: Final[int] = 8
    ROOM_MAX_SIZE: Final[int] = 15
    HALLWAY_ROOM_CHANCE: Final[float] = 0.1
    HALLWAY_ROOM_MIN_SIZE: Final[int] = 2
    HALLWAY_ROOM_MAX_SIZE: Final[int] = 8

    random: Random
    level: int
    map: list[list[Tile]]
    start: tuple[float, float]
    end: tuple[float, float]

    def __init__(self, random: Random, level: int) -> None:
        self.random = random
        self.level = level
        self.map = [[Tile.empty for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def generate(self, bandage_count: int):
        rooms = []

        # Generate rooms
        for _ in range(self.AMOUNT_ROOMS):
            width = self.random.randint(self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
            height = self.random.randint(self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)

            x = self.random.randint(0, self.SIZE - width)
            y = self.random.randint(0, self.SIZE - height)

            # No overlapping (with 1 between)
            while any(
                x - 1 < room[0] + room[2]
                and x - 1 + width + 1 > room[0]
                and y - 1 < room[1] + room[3]
                and y - 1 + height + 1 > room[1]
                for room in rooms
            ):
                width = self.random.randint(self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
                height = self.random.randint(self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
                x = self.random.randint(0, self.SIZE - width)
                y = self.random.randint(0, self.SIZE - height)

            rooms.append((x, y, width, height))

        # Fill in the rooms
        for room in rooms:
            for i in range(room[0], room[0] + room[2]):
                for j in range(room[1], room[1] + room[3]):
                    self.map[i][j] = Tile.floor

        # Generate hallways
        for i in range(len(rooms) - 1):
            # Calculate room centers
            x0 = rooms[i][0] + rooms[i][2] // 2
            y0 = rooms[i][1] + rooms[i][3] // 2
            x1 = rooms[i + 1][0] + rooms[i + 1][2] // 2
            y1 = rooms[i + 1][1] + rooms[i + 1][3] // 2

            # x hallway
            while x0 != x1:
                self.map[x0][y0] = Tile.floor
                x0 += 1 if x0 < x1 else -1

                # Hallway room
                if self.random.random() < self.HALLWAY_ROOM_CHANCE / 2:
                    hallway_room_width = self.random.randint(
                        self.HALLWAY_ROOM_MIN_SIZE, self.HALLWAY_ROOM_MAX_SIZE
                    )
                    hallway_room_height = self.random.randint(
                        self.HALLWAY_ROOM_MIN_SIZE, self.HALLWAY_ROOM_MAX_SIZE
                    )
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for j in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for k in range(
                            hallway_room_y, hallway_room_y + hallway_room_height
                        ):
                            self.map[j][k] = Tile.floor
            # y hallway
            while y0 != y1:
                self.map[x0][y0] = Tile.floor
                y0 += 1 if y0 < y1 else -1

                # Hallway room
                if self.random.random() < self.HALLWAY_ROOM_CHANCE / 2:
                    hallway_room_width = self.random.randint(
                        self.HALLWAY_ROOM_MIN_SIZE, self.HALLWAY_ROOM_MAX_SIZE
                    )
                    hallway_room_height = self.random.randint(
                        self.HALLWAY_ROOM_MIN_SIZE, self.HALLWAY_ROOM_MAX_SIZE
                    )
                    hallway_room_x = x0 - hallway_room_width // 2
                    hallway_room_y = y0 - hallway_room_height // 2

                    for j in range(hallway_room_x, hallway_room_x + hallway_room_width):
                        for k in range(
                            hallway_room_y, hallway_room_y + hallway_room_height
                        ):
                            self.map[j][k] = Tile.floor

        # Calculate starting and ending positions
        start = (
            round(rooms[0][0] + rooms[0][2] / 2),
            round(rooms[0][1] + rooms[0][3] / 2),
        )
        last_room = len(rooms) - 1
        end = (
            round(rooms[last_room][0] + rooms[last_room][2] / 2),
            round(rooms[last_room][1] + rooms[last_room][3] / 2),
        )
        self.start = (start[0] + 0.5, start[1] + 0.5)
        self.end = (end[0] + 0.5, end[1] + 0.5)

        # Post-process
        self.map[int(start[0])][int(self.start[1])] = Tile.entrance
        self.map[int(end[0])][int(end[1])] = Tile.exit

        # Chest
        floor_positions = [
            (i, j)
            for i in range(self.SIZE)
            for j in range(self.SIZE)
            if self.map[i][j] == Tile.floor
        ]

        chest_pos = self.random.choice(floor_positions)
        floor_positions.remove(chest_pos)
        self.map[chest_pos[0]][chest_pos[1]] = Tile.chest

        # Bandages (health dependent)
        bandages = self.random.sample(
            floor_positions, min(bandage_count, len(floor_positions))
        )

        for position in bandages:
            self.map[position[0]][position[1]] = Tile.bandage

    def enumerate(self) -> Generator[tuple[int, int, Tile]]:
        for x, column in enumerate(self.map):
            for y, tile in enumerate(column):
                yield (x, y, tile)

    def get_tile(self, x: int, y: int) -> Tile:
        return (
            self.map[x][y]
            if len(self.map) > x >= 0 and len(self.map[x]) > y >= 0
            else Tile.empty
        )

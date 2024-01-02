import random

FLOOR = ' '
WALL = '#'
ENEMY = '.'
CHEST = '@'
BANDAGE = "="
ENTRANCE = "^"
EXIT = "v"

AMOUNT_ROOMS = 12
BANDAGE_AMOUNT = 2
MAP_SIZE =  80
ENEMY_COUNT = 80
ROOM_MIN_SIZE = 8
ROOM_MAX_SIZE = 15
HALLWAY_ROOM_CHANCE = 0.1
HALLWAY_ROOM_MIN_SIZE = 2
HALLWAY_ROOM_MAX_SIZE = 8

def generate_room():
    width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    x = random.randint(0, MAP_SIZE - width)
    y = random.randint(0, MAP_SIZE - height)
    return (x, y, width, height)

def generate_dungeon():
    dungeon: list[list[str]] = [[WALL for _ in range(80)] for _ in range(80)]
    rooms: list[tuple[int, int, int, int]] = []

    for _ in range(AMOUNT_ROOMS):
        room = generate_room()

        while any(not (room[0]-1 + room[2] <= existingRoom[0]-1 or
                  existingRoom[0]-1 + existingRoom[2] <= room[0]-1 or
                  room[1]-1 + room[3] <= existingRoom[1]-1 or
                  existingRoom[1] + existingRoom[3] <= room[1]-1) 
                  for existingRoom in rooms):
            room = generate_room()

        rooms.append(room)

    for i in range(len(rooms) - 1):
        room1_center = (rooms[i][0] + rooms[i][2] // 2, rooms[i][1] + rooms[i][3] // 2)
        room2_center = (rooms[i + 1][0] + rooms[i + 1][2] // 2, rooms[i + 1][1] + rooms[i + 1][3] // 2)

        # Generate hallways
        x, y = room1_center
        while x != room2_center[0]:
            dungeon[x][y] = FLOOR
            x += 1 if x < room2_center[0] else -1

            # Hallway room
            if random.random() < HALLWAY_ROOM_CHANCE:
                hallway_room_width = random.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                hallway_room_height = random.randint(HALLWAY_ROOM_MIN_SIZE, HALLWAY_ROOM_MAX_SIZE)
                hallway_room_x = x - hallway_room_width // 2
                hallway_room_y = y - hallway_room_height // 2

                for i in range(hallway_room_x, hallway_room_x + hallway_room_width):
                    for j in range(hallway_room_y, hallway_room_y + hallway_room_height):
                        dungeon[i][j] = FLOOR

        while y != room2_center[1]:
            dungeon[x][y] = FLOOR
            y += 1 if y < room2_center[1] else -1

    # Fill rooms
    for room in rooms:
        for i in range(room[0], room[0] + room[2]):
            for j in range(room[1], room[1] + room[3]):
                dungeon[i][j] = FLOOR

    # Post-Process
            
    # entrance
    dungeon[rooms[0][0] + rooms[0][2] // 2][rooms[0][1] + rooms[0][3] // 2] = ENTRANCE
    # exit
    dungeon[rooms[AMOUNT_ROOMS-1][0] + rooms[AMOUNT_ROOMS-1][2] // 2][rooms[AMOUNT_ROOMS-1][1] + rooms[AMOUNT_ROOMS-1][3] // 2] = EXIT
    
    # Enemy's
    floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if dungeon[i][j] == FLOOR]
    enemy_positions = random.sample(floor_positions, min(ENEMY_COUNT, len(floor_positions)))

    for position in enemy_positions:
        dungeon[position[0]][position[1]] = ENEMY

    # Chest
    floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if dungeon[i][j] == FLOOR]

    chest_position = random.choice(floor_positions)
    dungeon[chest_position[0]][chest_position[1]] = CHEST

    # Bandages (health dependent)
    floor_positions = [(i, j) for i in range(MAP_SIZE) for j in range(MAP_SIZE) if dungeon[i][j] == FLOOR]
    bandage_positions = random.sample(floor_positions, min(BANDAGE_AMOUNT, len(floor_positions)))

    for position in bandage_positions:
        dungeon[position[0]][position[1]] = BANDAGE

    return dungeon

dungeon_map = generate_dungeon()
for row in dungeon_map:
    print(' '.join(map(str, row)))
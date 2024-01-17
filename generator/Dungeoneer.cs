namespace Dungeoneer
{
    public struct GeneratorConfig
    {
        public int mapSize = 80;
        public int amountRooms = 15;
        public int roomMinSize = 8;
        public int roomMaxSize = 15;
        public float hallwayRoomChance = 0.1f;
        public int hallwayRoomMinSize = 2;
        public int hallwayRoomMaxSize = 8;
        public GeneratorConfig() {}
    }
    public struct Coordinate
    {
        public float x;
        public float y;
    }
    public struct Position
    {
        public int x;
        public int y;
    }
    public struct Room
    {
        public int x;
        public int y;
        public int width;
        public int height;
    }
    public enum Tile 
    {
        Filled,
        Floor,
        Chest,
        Enemy,
        Entrance,
        Exit,
        Bandage
    }
    public static class TileMethods 
    {
        public static char GetIcon(this Tile tile)
        {
            switch (tile)
            {
                case Tile.Filled:
                    return '#';
                case Tile.Floor:
                    return ' ';
                case Tile.Chest:
                    return '@';
                case Tile.Enemy:
                    return '.';
                case Tile.Entrance:
                    return '^';
                case Tile.Exit:
                    return 'v';
                case Tile.Bandage:
                    return '=';
                default:
                    return '\0';
            }
        }
}
    
    public class Map
    {
        public Coordinate startPos = new();
        public Coordinate endPos = new();
        public Position chestPos = new();
        public Random random = new();
        public List<Room> rooms = new();
        public List<List<Tile>> map = new();
        public List<Coordinate> enemys = new();
        public List<Position> bandages = new();
        public GeneratorConfig config = new();

        public Map(GeneratorConfig config, Random rand, int enemyCount = 0, int bandageCount = 0) 
        {
            this.config = config;
            random = rand;
            Generate(enemyCount, bandageCount);
        }
        public void Generate(int enemyCount, int bandageCount)
        {
            for (int i = 0; i < config.mapSize; i++)
            {
                List<Tile> row = new();
                for (int j = 0; j < config.mapSize; j++)
                {
                    row.Add(Tile.Filled);
                }
                map.Add(row);
            }

            // Generate rooms
            for (int i = 0; i < config.amountRooms; i++)
            {
                int width = random.Next(config.roomMinSize, config.roomMaxSize);
                int height = random.Next(config.roomMinSize, config.roomMaxSize);
                int x = random.Next(0, config.mapSize - width);
                int y = random.Next(0, config.mapSize - height);

                // No overlapping (with 1 tile between)
                foreach (Room room in rooms)
                {
                    if (x-1 < room.x + room.width && x-1 + width+1 > room.x && y-1 < room.y + room.height && y-1 + height+1 > room.y) 
                    {
                        width = random.Next(config.roomMinSize, config.roomMaxSize);
                        height = random.Next(config.roomMinSize, config.roomMaxSize);
                        x = random.Next(0, config.mapSize - width);
                        y = random.Next(0, config.mapSize - height);
                    }
                }
                rooms.Add(new Room {x=x, y=y, width=width, height=height});
            }

            // Fill in the rooms
            foreach (Room room in rooms)
            {
                for (int x = room.x; x < room.x + room.width; x++)
                {
                    for (int y = room.y; y < room.y + room.height; y++)
                    {
                        map[x][y] = Tile.Floor;
                    }
                }
            }

            // Generate hallways
            for (int i = 0; i < rooms.Count-1; i++)
            {
                // Calculate room centers
                int x0 = rooms[i].x + rooms[i].width / 2;
                int y0 = rooms[i].y + rooms[i].height / 2;
                int x1 = rooms[i+1].x + rooms[i+1].width / 2;
                int y1 = rooms[i+1].y + rooms[i+1].height / 2;

                // x hallway
                while (x0!=x1)
                {
                    map[x0][y0] = Tile.Floor;
                    x0 += x0 < x1 ? 1:-1;

                    // Hallway room
                    if (random.NextDouble() < config.hallwayRoomChance/2) 
                    {
                        int roomWidth = random.Next(config.hallwayRoomMinSize, config.hallwayRoomMaxSize);
                        int roomHeight = random.Next(config.hallwayRoomMinSize, config.hallwayRoomMaxSize);
                        int roomX = (int)MathF.Round(x0 - roomWidth/2);
                        int roomY = (int)MathF.Round(y0 - roomHeight/2);

                        for (int j = roomX; j < roomX + roomWidth; j++)
                        {
                            for (int k = roomY; k < roomY + roomHeight; k++)
                            {
                                map[j][k] = Tile.Floor;
                            }
                        }
                    }
                }

                // y hallway
                while (y0!=y1)
                {
                    map[x0][y0] = Tile.Floor;
                    y0 += y0 < y1 ? 1:-1;

                    // Hallway room
                    if (random.NextDouble() < config.hallwayRoomChance/2) 
                    {
                        int roomWidth = random.Next(config.hallwayRoomMinSize, config.hallwayRoomMaxSize);
                        int roomHeight = random.Next(config.hallwayRoomMinSize, config.hallwayRoomMaxSize);
                        int roomX = (int)MathF.Round(x0 - roomWidth/2);
                        int roomY = (int)MathF.Round(y0 - roomHeight/2);

                        for (int j = roomX; j < roomX + roomWidth; j++)
                        {
                            for (int k = roomY; k < roomY + roomHeight; k++)
                            {
                                map[j][k] = Tile.Floor;
                            }
                        }
                    }
                }
            }

            // Calculate starting and ending positions
            startPos = new Coordinate {x=rooms[0].x + rooms[0].width/2, y=rooms[0].y + rooms[0].height/2};
            endPos = new Coordinate {x=rooms[^1].x + rooms[^1].width/2, y=rooms[^1].y + rooms[^1].height/2};

            // Post-Process

            // Entrance
            map[(int)MathF.Round(startPos.x)][(int)MathF.Round(startPos.y)] = Tile.Entrance;
            // Exit
            map[(int)MathF.Round(endPos.x)][(int)MathF.Round(endPos.y)] = Tile.Entrance;

            // Get floor positions
            List<Position> floors = new List<Position>();
            for (int x = 0; x < map.Count; x++)
            {
                for (int y = 0; y < map[x].Count; y++)
                {
                    if(map[x][y] == Tile.Floor)
                    {
                        floors.Add(new Position {x = x, y = y});
                    }
                }
            }

            // Chest
            int index = random.Next(floors.Count);
            chestPos = floors[index];
            floors.RemoveAt(index);
            map[chestPos.x][chestPos.y] = Tile.Chest;

            // Enemy's
            for (int i = 0; i < enemyCount; i++)
            {
                index = random.Next(floors.Count);
                enemys.Add(new Coordinate {x = floors[index].x, y = floors[index].y});
                floors.RemoveAt(index);
            }

            // Bandages
            for (int i = 0; i < bandageCount; i++)
            {
                index = random.Next(floors.Count);
                bandages.Add(floors[index]);
                map[floors[index].x][floors[index].y] = Tile.Bandage;
            }

        }
        public string ToMap()
        {
            List<List<Tile>> tempmap = map;
            foreach (Coordinate enemy in enemys)
            {
                tempmap[(int)MathF.Round(enemy.y)][(int)MathF.Round(enemy.x)] = Tile.Enemy;
            }
            string result = "";
            for (int x = 0; x < tempmap.Count; x++)
            {
                List<Tile> row = tempmap[x];
                for (int y = 0; y < tempmap.Count; y++)
                {
                    result += row[y].GetIcon()+" ";
                }
                result+="\n";
            }
            return result;
        }
    }
}
# Dungeoneer
Dungeoneer is an infinite dungeon game with generated dungeons. Generate random levels or use a seed.
It's built in python and can be played on a pc.
## how to play
Keys:
W: up (menu)
A: to the left
S: down (menu)
D: to the right
Q: sword stroke
E: arrow shooting
R: open map
F: Open chest, pick up bandage, drink potion, select menu, next level at exit.
ESC: Open menu
 
Go to next level: Kill all enemies (on map: a face) and go to exit.
 
In game:
Bottom left you will see a bar with your lives, next to it in yellow you will see your maximum lives.
Above the life bar you will see your speed and above that you will see the critical chance (for extra strength on a sword strike) and above that you will see your strength.
Bottom right is your level and top center is the number of enemies left.
 
Map:
Face: enemy
Arrow: Player
Chest: chest
Cross: exit
Plus: Bandage
stairs: entrance
## Usage
You can use the code in the generator folder in C# and in Python.
You must add proper credit.
## Workings
First a grid is generated with each the tile on filled. <br>
Then there are the amount of rooms generated with no collision and a wall between each. <br>
The hallways are generated between 0-1 1-2 2-3 etc, by first calculating the center of both the rooms and then moving a point first in the x axis and then in the y axis while setting each iteration the current tile to floor. <br>
There's a random chance that at each tile in the hallway a hallway room is generated. <br>
Then it adds the starting and ending tiles: entrance and exit. <br>
The chest is randomly placed and the enemy's are randomly placed on floor tiles.
Just like the bandages.
## Tiles
<table><tr><th>Name</th><th>Icon</th></tr><tr><th>Filled</th><th>#</th></tr><tr><th>Floor</th><th>(space)</th></tr><tr><th>Enemy</th><th>.</th></tr><tr><th>Bandage</th><th>=</th></tr><tr><th>Chest</th><th>@</th></tr></table>
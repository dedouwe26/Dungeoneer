from Dungeoneer import *
import sys
import pygame
from pygame.locals import *

SPEED = 4

BANDAGE_IMG = pygame.image.load("assets/bandage.png")
CHEST_IMG = pygame.image.load("assets/chest.png")
ENEMY1_IMG = pygame.image.load("assets/enemy1.png")
ENEMY2_IMG = pygame.image.load("assets/enemy2.png")
ENTRANCE_IMG = pygame.image.load("assets/entrance.png")
EXIT_IMG = pygame.image.load("assets/exit.png")
EXITCLOSED_IMG = pygame.image.load("assets/exitclosed.png")
FILLED_IMG = pygame.image.load("assets/filled.png")
FLOOR_IMG = pygame.image.load("assets/floor.png")
LOGO_IMG = pygame.image.load("assets/logo.png")
PLAYER_IMG = pygame.image.load("assets/player.png")
WALL_IMG = pygame.image.load("assets/wall.png")

# Keybinds:
# ^ move up
# v move down
# < move left
# > move right

class Dungeoneer:
    lastTime: int
    isRunning: bool = True
    player: Player
    gameDisplay: pygame.Surface
    FPS: pygame.time.Clock
    def __init__(self):
        self.player = Player(Seed())
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((320, 240)) # Gameshell size.
        pygame.display.set_caption('Dungeoneer') 
        pygame.display.set_icon(LOGO_IMG)
        self.FPS = pygame.time.Clock()
        self.FPS.tick(60) # The refresh rate of gameshell.
        self.lastTime = pygame.time.get_ticks()
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                else:
                    self.onEvent(event)
            t = pygame.time.get_ticks()
            deltaTime = (t - self.lastTime) / 1000.0
            self.lastTime = t
            self.update(deltaTime)
    def update(self, deltaTime):
        
        velocity = [0, 0]
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            velocity[1]+=SPEED*deltaTime
        if pressed_keys[K_DOWN]:
            velocity[1]-=SPEED*deltaTime
        if pressed_keys[K_LEFT]:
            velocity[0]+=SPEED*deltaTime
        if pressed_keys[K_RIGHT]:
            velocity[0]-=SPEED*deltaTime

        
        self.player.Move(velocity[0], velocity[1])
        # print(self.player.x, self.player.y, self.player.getCameraOffset())
        self.gameDisplay.fill((68,45,22))
        offset = self.player.getCameraOffset()
        for tile in self.player.currentMap.toRenderMap():
            self.gameDisplay.blit(FILLED_IMG if tile[0] == TileType["FILLED"] else FLOOR_IMG if tile[0] == TileType["FLOOR"] else CHEST_IMG if tile[0] == TileType["CHEST"] else ENTRANCE_IMG if tile[0] == TileType["ENTRANCE"] else EXIT_IMG if tile[0] == TileType["EXIT"] else WALL_IMG if tile[0] == TileType["WALL"] else BANDAGE_IMG, (tile[1]*16+offset[0], tile[2]*16+offset[1]))

        self.gameDisplay.blit(PLAYER_IMG, (152, 112))
        pygame.display.update()
    def exit(self):
        self.isRunning = False
        pygame.quit()
        sys.exit()
    def onEvent(self, event: pygame.event.Event):
        pass

Dungeoneer()
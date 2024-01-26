from shutil import move
from Dungeoneer import *
import sys
import pygame
from pygame.locals import *

rawtileset = pygame.image.load('assets/tileset.png')
tileset: pygame.Surface = pygame.transform.scale(rawtileset, (rawtileset.get_size()[0]*WORLD_SIZE, rawtileset.get_size()[1]*WORLD_SIZE))
del rawtileset

hitSound: pygame.mixer.Sound = None
killSound: pygame.mixer.Sound = None
levelUpSound: pygame.mixer.Sound = None
pickUpSound: pygame.mixer.Sound = None

tileRects: dict[str, pygame.Rect] = {
    "shadowpatchbottom": pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE),
    "shadowpatchtop": pygame.Rect(TILE_SIZE, 0, TILE_SIZE, TILE_SIZE),
    "shadowpatchright": pygame.Rect(2*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE),
    "shadowpatchleft": pygame.Rect(0, TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "exit": pygame.Rect(TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "entrance": pygame.Rect(2*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "wallleft": pygame.Rect(3*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "wall": pygame.Rect(4*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "wallright": pygame.Rect(5*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "wallboth": pygame.Rect(7*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "goldsword": pygame.Rect(6*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE*2),
    "ironsword": pygame.Rect(7*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE*2),
    "closedchest": pygame.Rect(0, 2*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "emptychest": pygame.Rect(0, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "fullchest": pygame.Rect(0, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "armoredplayer": pygame.Rect(TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "player": pygame.Rect(TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "mirroredarmoredplayer": pygame.Rect(tileset.get_size()[0]-2*TILE_SIZE, 3*TILE_SIZE, -TILE_SIZE, TILE_SIZE),
    "mirroredplayer": pygame.Rect(tileset.get_size()[0]-2*TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redpotion": pygame.Rect(2*TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenpotion": pygame.Rect(3*TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "yellowpotion": pygame.Rect(4*TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "bluepotion": pygame.Rect(4*TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "bandage": pygame.Rect(3*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "floor": pygame.Rect(TILE_SIZE, 2*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "rightsideedge": pygame.Rect(2*TILE_SIZE, 2*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "leftsideedge": pygame.Rect(3*TILE_SIZE, 2*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "topedge": pygame.Rect(4*TILE_SIZE, 2*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "innercornerbottomleft": pygame.Rect(5*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "innercornerbottomright": pygame.Rect(6*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "outercornertopleft": pygame.Rect(5*TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "outercornertopright": pygame.Rect(6*TILE_SIZE, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "outercornerbottomleft": pygame.Rect(5*TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "outercornerbottomright": pygame.Rect(6*TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenenemy0": pygame.Rect(0, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenenemy1": pygame.Rect(TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenenemy2": pygame.Rect(2*TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenenemy3": pygame.Rect(0, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenenemy4": pygame.Rect(TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "greenenemy5": pygame.Rect(3*TILE_SIZE, 5*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redenemy0": pygame.Rect(6*TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redenemy1": pygame.Rect(7*TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redenemy2": pygame.Rect(2*TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redenemy3": pygame.Rect(3*TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redenemy4": pygame.Rect(4*TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "redenemy5": pygame.Rect(5*TILE_SIZE, 6*TILE_SIZE, TILE_SIZE, TILE_SIZE),
}
LOGO_IMG = pygame.image.load('assets/logo.png')
# Keybinds:
# ^ move up
# v move down
# < move left
# > move right

class Dungeoneer:
    moveUp: bool = False
    moveDown: bool = False
    moveLeft: bool = False
    moveRight: bool = False
    lastTime: int
    isRunning: bool = True
    player: Player
    gameDisplay: pygame.Surface
    FPS: pygame.time.Clock
    def __init__(self):
        self.player = Player(Seed())
        pygame.init()
        pygame.mixer.init()
        hitSound = pygame.mixer.Sound("assets/kill.wav")
        killSound = pygame.mixer.Sound('assets/kill.wav')
        levelUpSound = pygame.mixer.Sound('assets/levelup.wav')
        pickUpSound = pygame.mixer.Sound('assets/pickup.wav')
        self.gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Gameshell size.
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
        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            
            velocity = [0, 0]
            if self.moveUp:
                velocity[1]-=deltaTime
            if self.moveDown:
                velocity[1]+=deltaTime
            if self.moveLeft:
                velocity[0]-=deltaTime
            if self.moveRight:
                velocity[0]+=deltaTime
            self.player.Move(velocity[0], velocity[1])
            # print(self.player.x, self.player.y, self.player.getCameraOffset())

        self.gameDisplay.fill((28,17,23))
        offset = self.player.getCameraOffset()
        for tile in self.player.currentMap.renderMap:
            self.gameDisplay.blit(tileset, (offset[0]+tile[1]*TILE_SIZE, offset[1]+tile[2]*TILE_SIZE), tileRects[tile[0]])
        self.gameDisplay.blit(pygame.transform.flip(tileset, self.player.facing, False), (SCREEN_WIDTH/2-TILE_SIZE/2,SCREEN_HEIGHT/2-TILE_SIZE/2), tileRects["mirroredplayer"] if self.player.facing else tileRects["player"])
        pygame.display.update()
        self.FPS.tick(60)
    def exit(self):
        self.isRunning = False
        pygame.quit()
        sys.exit()
    def onEvent(self, event: pygame.event.Event):
        if event.type == KEYDOWN:
            if event.dict["key"]==K_UP:
                self.moveUp = True
            elif event.dict["key"]==K_DOWN:
                self.moveDown = True
            elif event.dict["key"]==K_LEFT:
                self.moveLeft = True
            elif event.dict["key"]==K_RIGHT:
                self.moveRight = True
        elif event.type == KEYUP:
            if event.dict["key"]==K_UP:
                self.moveUp = False
            elif event.dict["key"]==K_DOWN:
                self.moveDown = False
            elif event.dict["key"]==K_LEFT:
                self.moveLeft = False
            elif event.dict["key"]==K_RIGHT:
                self.moveRight = False
        

Dungeoneer()
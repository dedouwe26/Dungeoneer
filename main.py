from Dungeoneer import *
import sys
import pygame
from pygame.locals import *

rawtileset = pygame.image.load('assets/tileset.png')
tileset: pygame.Surface = pygame.transform.scale(rawtileset, (rawtileset.get_size()[0]*WORLD_SIZE, rawtileset.get_size()[1]*WORLD_SIZE))
del rawtileset
mirroredTileset: pygame.Surface = pygame.transform.flip(tileset, True, False)

mapTileset = pygame.image.load('assets/maptileset.png')

mapTileRects: dict[str, pygame.Rect] = {
    "floor": pygame.Rect(MAP_TILE_SIZE, 0, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "player": pygame.Rect(2*MAP_TILE_SIZE, 0, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "enemy": pygame.Rect(3*MAP_TILE_SIZE, 0, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "exit": pygame.Rect(4*MAP_TILE_SIZE, 0, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "chest": pygame.Rect(5*MAP_TILE_SIZE, 0, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "bandage": pygame.Rect(4*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "entrance": pygame.Rect(5*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "bottomedge": pygame.Rect(0, MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "rightedge": pygame.Rect(MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "leftedge": pygame.Rect(0, 2*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "topedge": pygame.Rect(MAP_TILE_SIZE, 2*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "topleftcorner": pygame.Rect(2*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "toprightcorner": pygame.Rect(3*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "bottomleftcorner": pygame.Rect(2*MAP_TILE_SIZE, 2*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
    "bottomrightcorner": pygame.Rect(3*MAP_TILE_SIZE, 2*MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE),
}

tileRects: dict[str, pygame.Rect] = {
    "healthbackground": pygame.Rect(5*TILE_SIZE, 2*TILE_SIZE, TILE_SIZE*3, TILE_SIZE/2),
    "healthforeground": pygame.Rect(5*TILE_SIZE, 2*TILE_SIZE+TILE_SIZE/2, TILE_SIZE*3, TILE_SIZE/2),
    "fullhealth": pygame.Rect(3*TILE_SIZE, 0, TILE_SIZE*3, TILE_SIZE/2),
    "health": pygame.Rect(3*TILE_SIZE, TILE_SIZE/2, TILE_SIZE*3, TILE_SIZE/2),

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
    "mirroredarmoredplayer": pygame.Rect(tileset.get_size()[0]-2*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
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
# (space) SELECT open / close map
# u X Melee
# k B Range
# j A Interact
# (enter) START Menu


class Dungeoneer:
    hitSound: pygame.mixer.Sound
    killSound: pygame.mixer.Sound
    levelUpSound: pygame.mixer.Sound
    pickUpSound: pygame.mixer.Sound
    font: pygame.font.Font
    moveUp: bool = False
    moveDown: bool = False
    moveLeft: bool = False
    moveRight: bool = False
    lastTime: int
    isRunning: bool = True
    player: Player
    gameDisplay: pygame.Surface
    FPS: pygame.time.Clock
    deathAlphaLevel: float = 0
    mapOffset: tuple[float, float] = [0, 0]
    isSwinging: bool = False
    swing: float = 0
    def __init__(self):
        self.player = Player(Seed())
        pygame.init()
        pygame.mixer.init()
        self.font = pygame.font.Font("assets/PublicPixel.ttf", 9*WORLD_SIZE)
        self.hitSound = pygame.mixer.Sound("assets/hit.wav")
        self.killSound = pygame.mixer.Sound('assets/kill.wav')
        self.levelUpSound = pygame.mixer.Sound('assets/levelup.wav')
        self.pickUpSound = pygame.mixer.Sound('assets/pickup.wav')
        self.gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeoneer') 
        pygame.display.set_icon(LOGO_IMG)
        self.FPS = pygame.time.Clock()
        self.FPS.tick(60)
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
    def update(self, deltaTime: float):
        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            if self.player.hasMapOpen:
                self.mapOffset = [self.mapOffset[0] + (8*MAP_TILE_SIZE if self.moveLeft else -8*MAP_TILE_SIZE if self.moveRight else 0) * deltaTime, self.mapOffset[1] + (8*MAP_TILE_SIZE if self.moveUp else -8*MAP_TILE_SIZE if self.moveDown else 0) * deltaTime]
            else:
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
        if not self.player.dead:
            for enemy in self.player.currentMap.enemys:
                if enemy.Update(self.player.x-.5, self.player.y-.5, deltaTime):
                    pygame.mixer.Sound.play(self.hitSound)
                    if self.player.Hit(enemy.strength):
                        pygame.mixer.Sound.play(self.killSound)

        self.gameDisplay.fill((219, 207, 151) if self.player.hasMapOpen else (28,17,23))

        if self.player.hasMapOpen and not self.player.dead:
            for tile in self.player.currentMap.GenerateMapRenderMap(self.player.x, self.player.y):
                self.gameDisplay.blit(mapTileset, (self.mapOffset[0]+tile[1]*MAP_TILE_SIZE, self.mapOffset[1]+tile[2]*MAP_TILE_SIZE), mapTileRects[tile[0]])
        elif not (self.player.dead and self.deathAlphaLevel == 255):
            offset = self.player.getCameraOffset()

            for tile in self.player.currentMap.renderMap:
                self.gameDisplay.blit(tileset, (offset[0]+tile[1]*TILE_SIZE, offset[1]+tile[2]*TILE_SIZE), tileRects[tile[0]])
            
            for enemy in self.player.currentMap.enemys:
                self.gameDisplay.blit(mirroredTileset if enemy.facing else tileset, (offset[0]+enemy.x*TILE_SIZE, offset[1]+enemy.y*TILE_SIZE), tileRects[enemy.variation] if not enemy.facing else pygame.Rect(tileset.get_size()[0]-tileRects[enemy.variation].left-TILE_SIZE, tileRects[enemy.variation].top, tileRects[enemy.variation].width, tileRects[enemy.variation].height))

            # TODO: Draw projectiles

            if not self.player.dead:
                # TODO: Draw sword and animation
                if self.isSwinging:
                    self.swing+=deltaTime*3
                    cropped = pygame.Surface((tileRects["ironsword"].width, tileRects["ironsword"].height))
                    cropped.blit(tileset, (0,0), tileRects["ironsword"])
                    self.gameDisplay.blit(cropped, (100, 100), tileRects["ironsword"])
                    if self.swing>=1:
                        self.swing = 0
                        self.isSwinging = False
                else:
                    self.gameDisplay.blit(tileset, (SCREEN_WIDTH/2-(TILE_SIZE),SCREEN_HEIGHT/2-TILE_SIZE*1.5), tileRects["ironsword"])
                self.gameDisplay.blit(mirroredTileset if self.player.facing else tileset, (SCREEN_WIDTH/2-TILE_SIZE/2,SCREEN_HEIGHT/2-TILE_SIZE/2), tileRects["mirroredplayer"] if self.player.facing else tileRects["player"])
            del offset

            # draw UI
            # Health
            self.gameDisplay.blit(tileset, (0, SCREEN_HEIGHT-TILE_SIZE/2), tileRects["healthbackground"])

            percentageHealth = self.player.health / self.player.maxHealth

            if percentageHealth >= 1:
                self.gameDisplay.blit(tileset, (0, SCREEN_HEIGHT-TILE_SIZE/2), tileRects["fullhealth"])
            else:
                self.gameDisplay.blit(tileset, ((percentageHealth*46-46)*WORLD_SIZE, SCREEN_HEIGHT-TILE_SIZE/2), tileRects["health"])

            self.gameDisplay.blit(tileset, (0, SCREEN_HEIGHT-TILE_SIZE/2), tileRects["healthforeground"])

            # Level
            text = self.font.render(str(self.player.level), False, (180, 207, 30))
            rect = text.get_rect()
            rect.bottom = SCREEN_HEIGHT
            rect.left = 3*TILE_SIZE+(3*WORLD_SIZE)
            self.gameDisplay.blit(text, rect)

        if self.player.dead:
            self.deathAlphaLevel = min(255, self.deathAlphaLevel+deltaTime*30)
            alphaSurf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            alphaSurf.set_alpha(self.deathAlphaLevel)
            alphaSurf.fill((0,0,0))
            self.gameDisplay.blit(alphaSurf, (0,0), pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            text = self.font.render("Game Over", False, (182, 47, 49))
            rect = text.get_rect()
            rect.centerx = SCREEN_WIDTH/2
            rect.bottom = SCREEN_HEIGHT/2
            self.gameDisplay.blit(text, rect)

            text = self.font.render("You've reached level "+str(self.player.level), False, (204, 170, 68))
            text.set_alpha(self.deathAlphaLevel/100*255)
            rect = text.get_rect()
            rect.centerx = SCREEN_WIDTH/2
            rect.top = SCREEN_HEIGHT/2
            self.gameDisplay.blit(text, rect)


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
            elif event.dict["key"]==K_SPACE:
                self.player.hasMapOpen = not self.player.hasMapOpen
                if self.player.hasMapOpen:
                    self.mapOffset = [-(round(self.player.x)*MAP_TILE_SIZE)+SCREEN_WIDTH/2, -(round(self.player.y)*MAP_TILE_SIZE)+SCREEN_HEIGHT/2]
            elif event.dict["key"]==K_u:
                self.isSwinging = True
                hit = self.player.Melee()
                if hit[0]:
                    pygame.mixer.Sound.play(self.hitSound)
                if hit[1]:
                    pygame.mixer.Sound.play(self.killSound)
            elif event.dict["key"]==K_k:
                hit = self.player.Range()
                if hit[0]:
                    pygame.mixer.Sound.play(self.hitSound)
                if hit[1]:
                    pygame.mixer.Sound.play(self.killSound)
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
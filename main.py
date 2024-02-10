import traceback
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
    "arrow": pygame.Rect(4*TILE_SIZE, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "crit": pygame.Rect(0, 4*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "closedchest": pygame.Rect(0, 2*TILE_SIZE, TILE_SIZE, TILE_SIZE),
    "emptychest": pygame.Rect(0, 3*TILE_SIZE, TILE_SIZE, TILE_SIZE),
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
# ^ move up .w
# v move down .s
# < move left .a
# > move right .d
# (space) SELECT open / close map .r
# u X Melee .q
# k B Range .e
# j A Interact .f
# (enter) START Menu .esc

# (. keybinds)
PC = True


class Dungeoneer:
    menu: Menu = Menu()
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
    player: Player = None
    gameDisplay: pygame.Surface
    FPS: pygame.time.Clock
    deathAlphaLevel: float = 0
    mapOffset: tuple[float, float] = [0, 0]
    isSwinging: bool = False
    swing: float = 1
    fadeLvl: float = 0
    downFade: bool = False
    crits: list[tuple[float, float, float]] = []
    def __init__(self):
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
            pygame.display.update()
            self.FPS.tick(60)
    def update(self, deltaTime: float):
        if self.menu.opened:
            self.gameDisplay.fill((28,17,23))
            icon = pygame.transform.scale(LOGO_IMG, (50*WORLD_SIZE, 50*WORLD_SIZE))
            rect = icon.get_rect(centerx=SCREEN_WIDTH/2, top = TILE_SIZE*2)
            self.gameDisplay.blit(icon, rect)
            offset = rect.bottom + TILE_SIZE
            for text in self.menu.getRenderText():
                if text[1]:
                    self.font.set_underline(True)
                text = self.font.render(text[0], False, (218, 209, 212))
                rect = text.get_rect()
                rect.centerx = SCREEN_WIDTH/2
                rect.top = offset
                self.gameDisplay.blit(text, rect)
                offset += rect.height + TILE_SIZE
                self.font.set_underline(False)
            return

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
            for enemy in self.player.currentMap.enemies:
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
            
            for enemy in self.player.currentMap.enemies:
                self.gameDisplay.blit(mirroredTileset if enemy.facing else tileset, (offset[0]+enemy.x*TILE_SIZE, offset[1]+enemy.y*TILE_SIZE), tileRects[enemy.variation] if not enemy.facing else pygame.Rect(tileset.get_size()[0]-tileRects[enemy.variation].left-TILE_SIZE, tileRects[enemy.variation].top, tileRects[enemy.variation].width, tileRects[enemy.variation].height))

            for drop in self.player.drops:
                self.gameDisplay.blit(tileset, (offset[0]+drop[0]*TILE_SIZE, offset[1]+drop[1]*TILE_SIZE), tileRects[drop[2]])

            for i in range(len(self.player.currentMap.projectiles)):
                if not i < len(self.player.currentMap.projectiles):
                    continue
                projectile = self.player.currentMap.projectiles[i]
                direction = [projectile[2].x - projectile[0], projectile[2].y - projectile[1]]
                distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
                if not distance < 0.5:
                    direction = [direction[0] / distance, direction[1] / distance]
                    angle = math.degrees(math.atan2(-direction[1], direction[0]))-45
                    projectile[0] += direction[0] * deltaTime * 7
                    projectile[1] += direction[1] * deltaTime * 7
                    cropped = pygame.Surface((tileRects["arrow"].width, tileRects["arrow"].height), pygame.SRCALPHA)
                    cropped.blit(tileset, (0,0), tileRects["arrow"])
                    self.gameDisplay.blit(pygame.transform.rotate(cropped, angle), (offset[0]+projectile[0]*TILE_SIZE, offset[1]+projectile[1]*TILE_SIZE))
                else:
                    if projectile[2].Hit(self.player.strength*0.5):
                        del self.player.currentMap.projectiles[i]
                        if projectile[2] in self.player.currentMap.enemies:
                            pygame.mixer.Sound.play(self.killSound)
                            self.player.currentMap.enemies.remove(projectile[2])
                    else:
                        pygame.mixer.Sound.play(self.hitSound)
                        del self.player.currentMap.projectiles[i]
            self.player.bowCooldown-=deltaTime*0.6

            sword = tileRects["goldsword"] if self.player.strength >= 10 else tileRects["ironsword"]
            player = (tileRects["armoredplayer"], tileRects["mirroredarmoredplayer"]) if self.player.maxHealth >= 20 else (tileRects["player"], tileRects["mirroredplayer"])

            if not self.player.dead:
                if self.isSwinging:
                    self.swing-=deltaTime*3
                    cropped = pygame.Surface((sword.width, sword.height), pygame.SRCALPHA)
                    cropped.blit(tileset, (0,0), sword)
                    rotated = pygame.transform.rotate(pygame.transform.flip(cropped, False, True), -self.swing*180+90)
                    offset = pygame.Vector2(0, -TILE_SIZE).rotate(self.swing*180+90)

                    self.gameDisplay.blit(rotated, rotated.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)+offset))
                    if self.swing<=0:
                        self.swing = 1
                        self.isSwinging = False
                else:
                    self.gameDisplay.blit(tileset, (SCREEN_WIDTH/2-TILE_SIZE if self.player.facing else SCREEN_WIDTH/2,SCREEN_HEIGHT/2-TILE_SIZE*1.5), sword)
                self.gameDisplay.blit(mirroredTileset if self.player.facing else tileset, (SCREEN_WIDTH/2-TILE_SIZE/2,SCREEN_HEIGHT/2-TILE_SIZE/2), player[1] if self.player.facing else player[0])

            for i in range(len(self.crits)):
                if not i < len(self.crits):
                    continue
                crit = self.crits[i]
                self.gameDisplay.blit(tileset, (offset[0]+crit[0]*TILE_SIZE, offset[1]+crit[1]*TILE_SIZE), tileRects["crit"])
                self.crits[i] = (crit[0], crit[1], crit[2]-deltaTime)
                if crit[2]-deltaTime<=0:
                    del self.crits[i]
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

            # maxhealth
            text = self.font.render(str(self.player.maxHealth), False, (227, 178, 58))
            maxhealthrect = text.get_rect()
            maxhealthrect.bottom = SCREEN_HEIGHT
            maxhealthrect.left = 3*TILE_SIZE+(3*WORLD_SIZE)
            self.gameDisplay.blit(text, maxhealthrect)
            # Level
            text = self.font.render(str(self.player.level), False, (180, 207, 30))
            rect = text.get_rect()
            rect.bottom = SCREEN_HEIGHT
            rect.right = SCREEN_WIDTH
            self.gameDisplay.blit(text, rect)
            # Speed
            text = self.font.render(str(self.player.speed), False, (100, 148, 56))
            rect = text.get_rect()
            rect.bottom = SCREEN_HEIGHT-(10*WORLD_SIZE)
            rect.left = 0
            self.gameDisplay.blit(text, rect)
            # crit
            text = self.font.render(str(self.player.critchange*100)+"%", False, (0, 39, 94))
            rect = text.get_rect()
            rect.bottom = SCREEN_HEIGHT-(20*WORLD_SIZE)
            rect.left = 0
            self.gameDisplay.blit(text, rect)
            # strength
            text = self.font.render(str(self.player.strength), False, (208, 70, 72))
            rect = text.get_rect()
            rect.bottom = SCREEN_HEIGHT-(30*WORLD_SIZE)
            rect.left = 0
            self.gameDisplay.blit(text, rect)
            # enemies left
            text = self.font.render(str(len(self.player.currentMap.enemies)), False, (240, 240, 221))
            rect = text.get_rect()
            rect.top = 0
            rect.centerx = SCREEN_WIDTH/2
            self.gameDisplay.blit(text, rect)

            if self.player.nextMapFade or self.player.errorFade:
                if self.player.nextMapFade and self.fadeLvl == 0:
                    pygame.mixer.Sound.play(self.levelUpSound)
                if not self.downFade:
                    self.fadeLvl = min((255 if self.player.nextMapFade else 128), self.fadeLvl+deltaTime*(90 if self.player.errorFade else 80))
                    self.downFade = not (self.fadeLvl < (255 if self.player.nextMapFade else 70))
                else: 
                    self.fadeLvl = max(0, self.fadeLvl-deltaTime*(50 if self.player.errorFade else 60))
                    self.downFade = self.fadeLvl > 0
                    if self.player.nextMapFade:
                        self.player.nextMapFade = self.fadeLvl > 0
                    if self.player.errorFade:
                        self.player.errorFade = self.fadeLvl > 0
                
                if self.player.nextMapFade:
                    if self.fadeLvl == 255:
                        self.player.NextLevel()
                        


                fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade.set_alpha(self.fadeLvl)
                fade.fill((182, 47, 49) if self.player.errorFade else (0,0,0))
                self.gameDisplay.blit(fade, (0,0), fade.get_rect())

        if self.player.dead:
            self.deathAlphaLevel = min(255, self.deathAlphaLevel+deltaTime*30)
            alphaSurf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            alphaSurf.set_alpha(self.deathAlphaLevel)
            alphaSurf.fill((0,0,0))
            self.gameDisplay.blit(alphaSurf, (0,0), alphaSurf.get_rect())
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

    def exit(self):
        self.isRunning = False
        pygame.quit()
        sys.exit()
    def onEvent(self, event: pygame.event.Event):
        if event.type == KEYDOWN:
            if event.dict["key"]==K_w if PC else K_UP:
                if self.menu.opened:
                    self.menu.Up()
                else:
                    self.moveUp = True
            elif event.dict["key"]==K_s if PC else K_DOWN:
                if self.menu.opened:
                    self.menu.Down()
                else:
                    self.moveDown = True
            elif (not self.menu.opened) and event.dict["key"]==K_a if PC else K_LEFT:
                self.moveLeft = True
            elif (not self.menu.opened) and event.dict["key"]==K_d if PC else K_RIGHT:
                self.moveRight = True
            elif (not self.menu.opened) and event.dict["key"]==K_r if PC else K_SPACE:
                self.player.hasMapOpen = not self.player.hasMapOpen
                if self.player.hasMapOpen:
                    self.mapOffset = [-(round(self.player.x)*MAP_TILE_SIZE)+SCREEN_WIDTH/2, -(round(self.player.y)*MAP_TILE_SIZE)+SCREEN_HEIGHT/2]
            elif (not self.menu.opened) and event.dict["key"]==K_q if PC else K_u:
                self.isSwinging = True
                hit = self.player.Melee()
                if hit[0]:
                    pygame.mixer.Sound.play(self.hitSound)
                if hit[1]:
                    pygame.mixer.Sound.play(self.killSound)
                if len(hit[2])>0:
                    self.crits.extend(hit[2])
            elif event.dict["key"]==K_e if PC else K_k:
                if self.menu.opened:
                    self.menu.Back()
                else:
                    self.player.Range()
            elif event.dict["key"]==K_f if PC else K_j:
                if self.menu.opened:
                    self.menuEvent(self.menu.Select())
                else:
                    if self.player.Interact():
                        pygame.mixer.Sound.play(self.pickUpSound)
            elif event.dict["key"]==K_ESCAPE if PC else K_RETURN:
                if self.player!=None:
                    self.menu.opened = not self.menu.opened
                    if self.menu.opened:
                        self.menu.current = "Main"
        elif event.type == KEYUP:
            if self.menu.opened:
                return
            elif event.dict["key"]==K_w if PC else K_UP:
                self.moveUp = False
            elif event.dict["key"]==K_s if PC else K_DOWN:
                self.moveDown = False
            elif event.dict["key"]==K_a if PC else K_LEFT:
                self.moveLeft = False
            elif event.dict["key"]==K_d if PC else K_RIGHT:
                self.moveRight = False
    def menuEvent(self, event: str):
        if event == "n":
            if self.player==None:
                self.player = Player(Seed())
            else:
                self.player.Reset()
        elif event == "l1":
            if self.player==None:
                self.player = Player(Seed(1))
            self.player.LoadData("./saves/save1.dat")
        elif event == "l2":
            if self.player==None:
                self.player = Player(Seed(1))
            self.player.LoadData("./saves/save2.dat")
        elif event == "l3":
            if self.player==None:
                self.player = Player(Seed(1))
            self.player.LoadData("./saves/save3.dat")
        elif event == "s1":
            self.player.SaveData("./saves/save1.dat")
        elif event == "s2":
            self.player.SaveData("./saves/save2.dat")
        elif event == "s3":
            self.player.SaveData("./saves/save3.dat")
        elif event == "e":
            pygame.quit()
            sys.exit()
try:
    Dungeoneer()
except Exception as e:
    traceback.print_exception(e, e, e.__traceback__)
    pygame.quit()
    sys.exit(-1)

# Made by: @dedouwe26 (0xDED)
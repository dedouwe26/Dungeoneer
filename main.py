from Dungeoneer import *
import sys
import pygame
from pygame.locals import *

SPEED = 0.1

BANDAGE_IMG = pygame.image.load("assets/bandage.png")
CHEST_IMG = pygame.image.load("assets/chest.png")
ENEMY1_IMG = pygame.image.load("assets/enemy1.png")
ENEMY2_IMG = pygame.image.load("assets/enemy2.png")
ENTRANCE_IMG = pygame.image.load("assets/entrance.png")
EXIT_IMG = pygame.image.load("assets/exit.png")
FILLED_IMG = pygame.image.load("assets/filled.png")
FLOOR_IMG = pygame.image.load("assets/floor.png")
LOGO_IMG = pygame.image.load("assets/logo.png")
PLAYER_IMG = pygame.image.load("assets/player.png")
WALL_IMG = pygame.image.load("assets/wall.png")

class Dungeoneer:
    player: Player
    displaySurf: pygame.Surface
    FPS: pygame.time.Clock
    def __init__(self):
        self.player = Player(Seed())
        pygame.init()
        self.displaySurf = pygame.display.set_mode((320, 240)) # Gameshell size.
        pygame.display.set_caption('Dungeoneer') 
        pygame.display.set_icon(LOGO_IMG)
        self.FPS = pygame.time.Clock()
        self.FPS.tick(60) # The refresh rate of gameshell.
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                else:
                    self.onEvent(event)
            self.update()
    def update(self):
        velocity = [0, 0]
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            velocity[1]-=SPEED
        if pressed_keys[K_DOWN]:
            velocity[1]+=SPEED
        if pressed_keys[K_LEFT]:
            velocity[0]-=SPEED
        if pressed_keys[K_RIGHT]:
            velocity[0]+=SPEED

        # map = self.player.getRenderData()
        self.player.Move(velocity[0], velocity[1])
        pygame.display.update()
    def exit(self):
        pygame.quit()
        sys.exit()
    def onEvent(self, event: pygame.event.Event):
        if event.type == WINDOWRESIZED:
            print(event.dict)


Dungeoneer()
from Dungeoneer import *
import sys
import pygame
from pygame.locals import *

SPEED = 0.1

class Dungeoneer:
    player: Player
    displaySurf: pygame.Surface
    FPS: pygame.time.Clock
    def __init__(self):
        self.player = Player(Seed())
        pygame.init()
        self.displaySurf: pygame.Surface = pygame.display.set_mode((320, 240)) # Gameshell size.
        pygame.display.set_caption('Dungeoneer') 
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

        # sizePerPixel = self.displaySurf.get_size()[]
        self.player.Move(velocity[0], velocity[1])
        # pygame.transform.scale(self.displaySurf, pygame.trans)
        pygame.display.update()
    def exit(self):
        pygame.quit()
        sys.exit()
    def onEvent(self, event: pygame.event.Event):
        if event.type == WINDOWRESIZED:
            print(event.dict)


Dungeoneer()
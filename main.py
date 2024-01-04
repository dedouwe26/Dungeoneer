from Dungeoneer import *
import sys
import pygame
from pygame.locals import *

class Dungeoneer:
    player: Player
    DISPLAYSURF: pygame.Surface
    FPS: pygame.time.Clock
    def __init__(self):
        self.player = Player()
        pygame.init()
        self.DISPLAYSURF: pygame.Surface = pygame.display.set_mode((320, 240)) # Gameshell size.
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
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.moveUp = True
        elif pressed_keys[K_PAGEDOWN]:
            self.moveDown = True
        elif pressed_keys[K_LEFT]:
            self.moveLeft = True
        elif pressed_keys[K_RIGHT]:
            self.moveRight = True

        pygame.display.update()
    def exit(self):
        pygame.quit()
        sys.exit()
    def onEvent(self, event: pygame.event.Event):
        pass


Dungeoneer()
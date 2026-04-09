import math
from pathlib import Path
from typing import Final
import pygame
from assetloader import AssetLoader
from game import Game
from savemanager import SaveManager
from screen import MainScreen, MapScreen, MenuScreen, Screen


class Main:
    K_MOVE_UP: Final[int] = pygame.K_w
    K_MOVE_LEFT: Final[int] = pygame.K_a
    K_MOVE_DOWN: Final[int] = pygame.K_s
    K_MOVE_RIGHT: Final[int] = pygame.K_d
    K_OPEN_MAP: Final[int] = pygame.K_r
    K_CLOSE: Final[int] = pygame.K_ESCAPE
    K_OPEN_MENU: Final[int] = K_CLOSE
    K_INTERACT: Final[int] = pygame.K_f
    M_ATTACK: Final[int] = 0
    M_FIRE: Final[int] = 1

    FPS: Final[int] = 144

    asset_loader: AssetLoader
    save_manager: SaveManager
    game: Game
    game_display: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool = True
    last_tick: int = 0
    last_frame: int = 0
    event_queue: list[int]
    current_screen: Screen

    def __init__(self) -> None:
        # Initialize Pygame.
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        # Load assets.
        self.asset_loader = AssetLoader(Path("./assets/assets.json"))

        pygame.display.set_caption("Dungeoneer")
        pygame.display.set_icon(self.asset_loader.get_logo())

        self.game = Game()

    def is_paused(self) -> bool:
        return isinstance(self.current_screen, MenuScreen)

    def start(self):
        one_over_tps: float = 1 / Game.TPS
        one_over_fps: float = 1 / self.FPS
        while self.is_running:
            self.fetch_events()

            dt = self.clock.tick()

            self.last_tick += dt
            if self.last_tick >= one_over_tps:
                self.tick()
                self.last_tick = 0

            self.last_frame += dt
            if self.last_frame >= one_over_fps:
                self.render()
                self.last_frame = 0

    def change_screen(self, new_screen: Screen):
        self.current_screen = new_screen

    def handle_keydown(self, key: int):
        if not self.is_paused():
            match key:
                case self.K_OPEN_MENU:
                    self.change_screen(MenuScreen(self))
                case self.K_OPEN_MAP:
                    self.change_screen(MapScreen(self))
        elif key == self.K_MOVE_RIGHT:
            self.change_screen(MainScreen(self))
        self.current_screen.keydown(key)

    def fetch_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.stop()
                case pygame.KEYDOWN:
                    self.handle_keydown(event.dict["key"])
                case pygame.KEYUP:
                    self.current_screen.keyup(event.dict["key"])
                case pygame.MOUSEBUTTONDOWN:
                    print(event.dict)

    def handle_movement(self):
        keystate = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keystate[self.K_MOVE_DOWN]:
            dy = 1
        if keystate[self.K_MOVE_LEFT]:
            dx = -1
        if keystate[self.K_MOVE_RIGHT]:
            dx += 1
        if keystate[self.K_MOVE_UP]:
            dy += -1
        if dx != 0 or dy != 0:
            d = math.hypot(dx, dy)
            dx /= d
            dy /= d
            self.current_screen.move(dx, dy)

    def tick(self):
        self.handle_movement()
        if not self.is_paused():
            self.game.tick(self.last_tick)

    def render(self):
        self.current_screen.render()
        pygame.display.update()

    def stop(self):
        self.is_running = False
        pygame.quit()

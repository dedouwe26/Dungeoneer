import math
from pathlib import Path
from typing import Callable
import pygame
from assetloader import AssetLoader
import config
from game import Game
from savemanager import SaveManager
from seed import Seed


class Application:
    asset_loader: AssetLoader
    save_manager: SaveManager
    game: Game
    display: pygame.Surface
    real_display: pygame.Surface
    clock: pygame.time.Clock
    is_running: bool = True
    last_tick: int = 0
    last_frame: int = 0
    on_render: Callable[[float], None]
    on_tick: Callable[[float], None]
    on_keydown: Callable[[int], None]
    on_keyup: Callable[[int], None]
    on_game_event: Callable[[str], None]
    seed: Seed
    scale: float = 1

    def __init__(self) -> None:
        print("Starting Dungeoneer...")

        # Initialize Pygame.
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        # Load utilities.
        self.seed = Seed()
        self.asset_loader = AssetLoader(Path("./assets/assets.json"))
        self.save_manager = SaveManager(Path("./saves/"))

        # Load window surface.
        self.real_display = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), vsync=1, flags=pygame.RESIZABLE
        )
        self.display = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags=pygame.SRCALPHA)
        self.update_scale(self.real_display.get_width(), self.real_display.get_height())

        # Set window properties.
        pygame.display.set_caption("Dungeoneer")
        pygame.display.set_icon(self.asset_loader.get_logo())

        self.game = Game(self.seed, self.game_event)

    def game_event(self, event_name: str):
        if self.on_game_event is None:
            return
        print("event:", event_name)
        self.on_game_event(event_name)

    def play_sound(self, sound_name: str):
        sound = self.asset_loader.get_sound(sound_name)
        if sound is None:
            return
        sound.play()

    def start(self):
        one_over_tps: float = 1 / config.TPS
        one_over_fps: float = 1 / config.FPS
        while self.is_running:
            self.handle_events()
            dt = self.clock.tick()

            self.last_tick += dt
            if self.last_tick >= one_over_tps:
                self.on_tick(self.last_tick / 1000)
                self.last_tick = 0

            self.last_frame += dt
            if self.last_frame >= one_over_fps:
                self.on_render(self.last_frame / 1000)
                dis = pygame.transform.scale(
                    self.display,
                    (
                        self.scale * self.display.get_width(),
                        self.scale * self.display.get_height(),
                    ),
                )
                self.real_display.fill(config.BACKGROUND)
                self.real_display.blit(
                    dis,
                    dis.get_rect(
                        centerx=self.real_display.get_width() / 2,
                        centery=self.real_display.get_height() / 2,
                    ),
                )
                pygame.display.update()
                self.last_frame = 0

    def update_scale(self, w, h):
        dw = w / config.WINDOW_WIDTH
        dh = h / config.WINDOW_HEIGHT
        self.scale = min(dw, dh)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self.on_keydown(event.dict["key"])
                case pygame.KEYUP:
                    self.on_keyup(event.dict["key"])
                case pygame.VIDEORESIZE:
                    self.update_scale(event.dict["w"], event.dict["h"])
                case pygame.QUIT:
                    self.stop()

    def is_key_pressed(self, key: int) -> bool:
        keystate = pygame.key.get_pressed()
        return keystate[key]

    def handle_movement(self) -> tuple[float, float]:
        dx = 0
        dy = 0
        if self.is_key_pressed(config.K_MOVE_DOWN):
            dy = 1
        if self.is_key_pressed(config.K_MOVE_LEFT):
            dx = -1
        if self.is_key_pressed(config.K_MOVE_RIGHT):
            dx += 1
        if self.is_key_pressed(config.K_MOVE_UP):
            dy += -1
        if dx != 0 or dy != 0:
            d = math.hypot(dx, dy)
            dx /= d
            dy /= d
            return (dx, dy)
        return (0, 0)
    
    def get_variant(self, x: int, y: int, n: str, tileset: str = config.MAIN_TILESET) -> int:
        asset = self.asset_loader.get_tile_variants(tileset, n)
        if self.game.level == 0:
            return asset[0]
        # choices = asset[1]
        # del choices[asset[0]]
        # return choices[0]
        return 0 # NOTE: No impl because no need yet, when: add variant soa to map randomized

    def stop(self):
        self.is_running = False
        print("Stopping!")
        pygame.quit()

from abc import ABC
import math
from typing import Final

from pygame import Color, Rect, Surface
import pygame

from application import Application
from assetloader import AssetLoader
import config
from game import Game
from map import Tile
from savemanager import SaveManager


class Screen(ABC):
    assets: AssetLoader
    saves: SaveManager
    game: Game
    app: Application
    display: Surface
    width: int
    height: int

    def __init__(self, app: Application) -> None:
        super().__init__()
        print("screen initialized")
        self.app = app
        self.display = app.display
        self.width, self.height = self.display.get_size()
        self.assets = app.asset_loader
        self.saves = app.save_manager
        self.game = app.game
        app.on_tick = self.tick
        app.on_render = self.render
        app.on_keydown = self.keydown
        app.on_keyup = self.keyup
        app.on_game_event = self.on_event

    def on_event(self, event_name: str):
        self.app.play_sound(event_name)

    def move(self, dx: float, dy: float):
        pass

    def render(self, deltatime: float):
        pass

    def tick(self, deltatime: float):
        dir = self.app.handle_movement()
        if dir != (0, 0):
            self.move(dir[0], dir[1])

        self.game.tick(deltatime)

    def keydown(self, key: int):
        pass

    def keyup(self, key: int):
        pass


current_screen: Screen


def switch_screen(new_screen: Screen):
    global current_screen
    current_screen = new_screen


class MainScreen(Screen):
    def calculate_screen(self, x: float, y: float) -> tuple[float, float]:
        px = self.game.player.x
        py = self.game.player.y
        return (x - (px - self.width / 2), y - (py - self.height / 2))

    def render_in_world(self, x: int, y: int, surface: Surface, rect: Rect):
        screen = self.calculate_screen(x, y)
        self.display.blit(surface, screen, rect)

    def render_tile(self, x: int, y: int, surface: Surface, tile: Tile):
        rect = self.assets.get_tile(config.MAIN_TILESET, tile.value)
        if rect is None:
            if tile != Tile.empty:
                print(f"unknown tile: {tile.value}")
            return
        if tile.has_ground() and tile != Tile.floor:
            self.render_tile(x, y, surface, Tile.floor)
        self.render_in_world(x, y, surface, rect)

    def render_map(self):
        surface = self.assets.get_tileset_surface(config.MAIN_TILESET)
        if surface is None:
            print(f"unknown tileset: MAIN_TILESET: {config.MAIN_TILESET}")
            return
        for x, y, tile in self.game.current_map.enumerate():
            self.render_tile(x, y, surface, tile)
        pass

    def render_enemies(self):
        pass

    def render_projectiles(self):
        pass

    def render_player(self):
        tile = self.assets.get_tile(config.MAIN_TILESET, Tile.floor.value)
        surface = self.assets.get_tileset_surface(config.MAIN_TILESET)
        if tile is None or surface is None:
            print("aJJHKFDKJF")
            return
        self.display.blit(surface, surface.get_rect())  # , (0, 0), tile)

    def render_ui(self):
        pass

    def render(self, deltatime: float):
        self.display.fill(config.BACKGROUND)
        self.render_map()
        self.render_enemies()
        self.render_projectiles()
        self.render_player()
        # TODO: Render effects
        self.render_ui()


class MapScreen(Screen):
    pass


class MenuScreen(Screen):
    FOREGROUND: Final[Color] = Color(219, 207, 151)
    MENU: Final[int] = 0
    LOAD_GAME: Final[int] = 1
    SAVE_GAME: Final[int] = 2
    state: int
    selected: int
    entries: list[str]

    def __init__(self, app: Application) -> None:
        super().__init__(app)
        self.change_state(self.MENU)

    def render_item(self, index: int, text: str):
        self.assets.font.set_underline(self.selected == index)
        surface = self.assets.font.render(
            text, False, self.FOREGROUND, config.BACKGROUND
        )
        self.display.blit(
            surface, surface.get_rect(centerx=self.width / 2, top=100 + index * 40)
        )

    def render_entries(self):
        for i, name in enumerate(self.entries):
            self.render_item(i, name)

    def tick(self, deltatime: float):
        pass

    def render(self, deltatime: float):
        self.display.fill(config.BACKGROUND)
        icon = self.assets.get_logo()
        icon = pygame.transform.scale(
            icon, ((icon.get_width() / icon.get_height()) * 100, 100)
        )
        rect = icon.get_rect(centerx=self.width / 2, top=16)
        self.display.blit(icon, rect)
        self.render_entries()

    def keydown(self, key: int):
        match key:
            case config.K_SELECT:
                match self.state:
                    case self.MENU:
                        match self.selected:
                            case 0:
                                self.choose_new_game()
                            case 1:
                                self.change_state(self.LOAD_GAME)
                            case 2:
                                self.change_state(self.SAVE_GAME)
                            case 3:
                                self.app.stop()
                    case self.LOAD_GAME:
                        self.load_game()
                    case self.SAVE_GAME:
                        self.save_game()
            case config.K_MOVE_UP:
                if self.selected > 0:
                    self.selected -= 1
            case config.K_MOVE_DOWN:
                if self.selected < len(self.entries):
                    self.selected += 1
            case config.K_CLOSE:
                if self.state == self.MENU:
                    if self.game.is_initialized:
                        switch_screen(MainScreen(self.app))
                else:
                    self.change_state(self.MENU)

    def change_state(self, new_state: int):
        self.selected = 0
        match new_state:
            case self.MENU:
                self.entries = ["New Game ", "Load Game", "Save Game", "  Quit   "]
            case self.SAVE_GAME:
                self.entries = self.saves.fetch_saves()
            case self.LOAD_GAME:
                self.entries = self.saves.fetch_saves()
        self.state = new_state

    def choose_new_game(self):
        self.game.new_game()
        switch_screen(MainScreen(self.app))

    def load_game(self):
        self.saves.load(self.game, self.entries[self.selected])
        switch_screen(MainScreen(self.app))

    def save_game(self):
        self.saves.save(self.game, self.entries[self.selected])
        self.change_state(self.MENU)


if __name__ == "__main__":
    app = Application()
    switch_screen(MenuScreen(app))
    app.start()

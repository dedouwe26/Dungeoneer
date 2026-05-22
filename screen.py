from abc import ABC
from typing import Final

from pygame import Color, Rect, Surface
import pygame

from application import Application
from assetloader import AssetLoader
import config
from game import Game
from map import Map, Tile
from savemanager import SaveManager


class Screen(ABC):
    mainset: Surface
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
        mainset = self.assets.get_tileset_surface(config.MAIN_TILESET)
        if mainset is None:
            raise Exception("no main tileset")
        self.mainset = mainset
        self.saves = app.save_manager
        self.game = app.game
        app.on_tick = self.tick
        app.on_render = self.render
        app.on_keydown = self.keydown
        app.on_keyup = self.keyup
        app.on_game_event = self.on_event

    def map(self) -> Map:
        return self.game.current_map

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
    def __init__(self, app: Application) -> None:
        super().__init__(app)

    def calculate_screen(self, x: float, y: float) -> tuple[float, float]:
        px = self.game.player.x
        py = self.game.player.y

        return (  # TODO: Conversion from game coords to screen coords.
            (x - px) * config.WORLD_SIZE + self.width / 2,
            (y - py) * config.WORLD_SIZE + self.height / 2,
        )

    def render_in_world(self, x: float, y: float, surface: Surface, rect: Rect):
        screen = self.calculate_screen(x, y)
        self.display.blit(surface, screen, rect)

    def render_tile(self, x: int, y: int, tile: Tile):
        def empty(x2, y2):
            return self.map().get_tile(x + x2, y + y2) == Tile.empty

        def edge(x1, y1):
            left = not empty(x1 - 1, y1)
            right = not empty(x1 + 1, y1)
            top = not empty(x1, y1 - 1)
            bottom = not empty(x1, y1 + 1)
            if left:
                r2(x1, y1 - 1, "leftedge")
            if right:
                r2(x1, y1 - 1, "rightedge")
            if top:
                r2(x1, y1 - 1, "topedge")
            if bottom:
                lw = left or empty(x1 - 1, y1 + 1)
                rw = right or empty(x1 + 1, y1 + 1)
                if lw and rw:
                    r2(x1, y1, "wallboth")
                elif lw:
                    r2(x1, y1, "wallleft")
                elif rw:
                    r2(x1, y1, "wallright")
                else:
                    r2(x1, y1, "wall")
            if left and top:
                r2(x1, y1 - 1, "innercornernw")
            if right and top:
                r2(x1, y1 - 1, "innercornerne")
            if not empty(x1 - 1, y1 - 1) and empty(x1 - 1, y1) and empty(x1, y1 - 1):
                r2(x1, y1 - 1, "outercornerse")
            if not empty(x1 + 1, y1 - 1) and empty(x1 + 1, y1) and empty(x1, y1 - 1):
                r2(x1, y1 - 1, "outercornersw")
            if not empty(x1 - 1, y1 + 1) and empty(x1 - 1, y1) and empty(x1, y1 + 1):
                r2(x1, y1, "outercornerne")
            if not empty(x1 + 1, y1 + 1) and empty(x1 + 1, y1) and empty(x1, y1 + 1):
                r2(x1, y1, "outercornernw")

        def r(x2, y2, s):
            t = self.assets.get_tile(config.MAIN_TILESET, s)
            if t is None:
                return
            self.render_in_world(x + x2, y + y2, self.mainset, t)

        def r2(x2, y2, s):  # TODO: Render opacity when player walks behind
            r(x2, y2, s)

        n = empty(0, -1)
        e = empty(1, 0)
        s = empty(0, 1)
        w = empty(-1, 0)
        ne = empty(1, -1)
        se = empty(1, 1)
        sw = empty(-1, 1)
        nw = empty(-1, -1)

        if tile != Tile.empty:
            if tile.has_ground() and not s:
                r(0, 0, "floor")
                if w:
                    r(0, 0, "shadowpatchleft")
                if e:
                    r(0, 0, "shadowpatchright")
                if s:
                    r(0, 0, "shadowpatchbottom")
                if n:
                    r(0, 0, "shadowpatchtop")

            if tile != Tile.floor and not s:
                r(0, 0, tile.value)

            if n:
                edge(0, -1)
            if e:
                edge(1, 0)
            if s:
                edge(0, 1)
            if w:
                edge(-1, 0)
            if ne:
                edge(1, -1)
            if se:
                edge(1, 1)
            if sw:
                edge(-1, 1)
            if nw:
                edge(-1, -1)

    def render_map(self):
        for x, y, tile in self.map().enumerate():
            self.render_tile(x, y, tile)

    def render_character(
        self,
        x: float,
        y: float,
        tileset: int,
        tile: str,
        variant: int = 0,
        flip: bool = False,
    ):
        surface = self.assets.get_tileset_surface(tileset, flip)
        rect = self.assets.get_tile(tileset, tile, variant, flip)
        if surface is None or rect is None:
            print("unable to render character: could not find assets")
            return
        self.render_in_world(
            x - rect.width / config.WORLD_SIZE / 2,
            y - rect.height / config.WORLD_SIZE,
            surface,
            rect,
        )

    def render_enemies(self):
        for enemy in self.game.enemies:
            self.render_character(
                enemy.x,
                enemy.y,
                config.MAIN_TILESET,
                "redenemy" if enemy.is_melee else "greenenemy",
                enemy.variant,
            )

    def render_projectiles(self):
        pass

    def render_player(self):
        self.render_character(
            self.game.player.x,
            self.game.player.y,
            config.MAIN_TILESET,
            "player",
            flip=self.game.player.facing,
        )

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

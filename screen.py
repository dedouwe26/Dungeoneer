from abc import ABC
import math
from typing import Final

from pygame import Color, Rect, Surface, Vector2
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

    def initialize_app_callbacks(self):
        self.app.on_tick = self.tick
        self.app.on_render = self.render
        self.app.on_keydown = self.keydown
        self.app.on_keyup = self.keyup
        self.app.on_game_event = self.on_event

    def map(self) -> Map:
        return self.game.current_map

    def on_event(self, event_name: str):
        self.app.play_sound(event_name)

    def move(self, dx: float, dy: float):
        pass

    def render(self, deltatime: float):
        dir = self.app.handle_movement()
        if dir != (0, 0):
            self.move(dir[0] * deltatime, dir[1] * deltatime)

    def tick(self, deltatime: float):
        self.game.tick(deltatime)

    def keydown(self, key: int):
        pass

    def keyup(self, key: int):
        pass


current_screen: Screen


def switch_screen(new_screen: Screen):
    global current_screen
    current_screen = new_screen
    current_screen.initialize_app_callbacks()


should_block_input: bool = False
effects: list[list] = []


def reset():
    global should_block_input, effects
    should_block_input = False
    effects = []


def render_effects():
    deleted = []
    for i in range(len(effects)):
        effect = effects[i]
        effect[1](effect[0])
        effects[i][0] -= 1
        if effects[i][0] == 0:
            deleted.append(i)
    for i in deleted:
        del effects[i]


class MainScreen(Screen):
    def __init__(self, app: Application) -> None:
        super().__init__(app)

    def calculate_screen(self, x: float, y: float) -> tuple[float, float]:
        px = self.game.player.x
        py = self.game.player.y

        return (
            (x - px) * config.WORLD_SIZE + self.width / 2,
            (y - py) * config.WORLD_SIZE + self.height / 2,
        )

    def render_in_world(
        self, x: float, y: float, source: Surface, rect: Rect, opacity: float = 1
    ):
        screen = self.calculate_screen(x, y)
        x = screen[0]
        y = screen[1]
        temp = pygame.Surface((rect.w, rect.h)).convert()
        temp.blit(self.display, (0, 0), Rect(x, y, rect.w, rect.h))
        temp.blit(source, (0, 0), rect)
        temp.set_alpha(round(opacity * 255))
        self.display.blit(temp, screen)

    def render_tile(self, x: int, y: int, tile: Tile):
        def empty(x2, y2):
            return self.map().get_tile(x + x2, y + y2) == Tile.empty

        def r2(x2, y2, s):
            t = self.assets.get_tile(config.MAIN_TILESET, s)
            if t is None:
                return
            self.render_in_world(
                x + x2,
                y + y2,
                self.mainset,
                t,
                self.calculate_loweropacity(x + x2, y + y2),
            )

        def r(x2, y2, s):
            t = self.assets.get_tile(config.MAIN_TILESET, s)
            if t is None:
                return
            self.render_in_world(
                x + x2,
                y + y2,
                self.mainset,
                t,
                self.calculate_upperopacity(x + x2, y + y2),
            )

        n = empty(0, -1)
        e = empty(1, 0)
        s = empty(0, 1)
        w = empty(-1, 0)

        if tile != Tile.empty:
            if tile.has_ground():
                r2(0, 0, "floor")
                if w:
                    r2(0, 0, "shadowpatchleft")
                if e:
                    r2(0, 0, "shadowpatchright")
                if s:
                    r2(0, 0, "shadowpatchbottom")
                if n:
                    r2(0, 0, "shadowpatchtop")
            if tile != Tile.floor:
                r2(0, 0, tile.value)
            return
        n = not n
        e = not e
        s = not s
        w = not w
        if w:
            r(0, -1, "leftedge")
        if e:
            r(0, 0 - 1, "rightedge")
        if n:
            r(0, 0 - 1, "topedge")
        if s:
            lw = w or empty(-1, 1)
            rw = e or empty(1, 1)
            if lw and rw:
                r(0, 0, "wallboth")
            elif lw:
                r(0, 0, "wallleft")
            elif rw:
                r(0, 0, "wallright")
            else:
                r(0, 0, "wall")
        if w and n:
            r(0, 0 - 1, "innercornernw")
        if e and n:
            r(0, 0 - 1, "innercornerne")
        if not empty(-1, -1) and not w and not n:
            r(0, 0 - 1, "outercornerse")
        if not empty(1, -1) and not e and not n:
            r(0, -1, "outercornersw")
        if not empty(-1, 1) and not w and not s:
            r(0, 0, "outercornerne")
        if not empty(1, 1) and not e and not s:
            r(0, 0, "outercornernw")

    def calculate_upperopacity(self, x: int, y: int) -> float:
        if (
            self.map().get_tile(x, y + 1) != Tile.empty
            or self.map().get_tile(x, y) == Tile.empty
        ):
            return 1
        a = [Vector2(x - self.game.player.x, y - self.game.player.y + 1)]
        a.extend([Vector2(x - e.x, y - e.y + 1) for e in self.game.enemies])
        p = None
        dm = 10000
        for ap in a:
            d = ap.distance_squared_to((0, 0))
            if d < dm:
                dm = d
                p = ap
        if p is None or p.y < 0:
            return 1
        d = (abs(p.x + 0.5) + p.y) / 2
        return min(d * 0.5, 1)

    def calculate_loweropacity(self, x: int, y: int) -> float:
        if (
            self.map().get_tile(x, y + 1) != Tile.empty
            or self.map().get_tile(x, y) == Tile.empty
        ):
            return 1
        a = [Vector2(x - self.game.player.x, y - self.game.player.y + 1)]
        a.extend([Vector2(x - e.x, y - e.y + 1) for e in self.game.enemies])
        p = None
        dm = 10000
        for ap in a:
            d = ap.distance_squared_to((0, 0))
            if d < dm:
                dm = d
                p = ap
        if p is None or p.y < 0:
            return 0
        d = (abs(p.x + 0.5) + p.y) / 2
        return 1 - self.calculate_upperopacity(x, y)

    def render_map(self):
        half_width = math.ceil(config.TILES_WIDTH / 2)
        half_height = math.ceil(config.TILES_HEIGHT / 2)
        for x in range(
            math.floor(self.game.player.x - half_width),
            math.ceil(self.game.player.x + half_width),
        ):
            for y in range(
                math.floor(self.game.player.y - half_height),
                math.ceil(self.game.player.y + half_height),
            ):
                self.render_tile(x, y, self.map().get_tile(x, y))

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
                enemy.facing,
            )

    def render_projectiles(self):
        t = self.assets.get_tile(config.MAIN_TILESET, "arrow")
        if t is None:
            print("could not find arrow tile")
            return
        for projectile in self.game.projectiles:
            screen = self.calculate_screen(projectile.x, projectile.y)
            surf = Surface((t.width, t.height), flags=pygame.SRCALPHA)
            surf.blit(self.mainset, (0, 0), t)
            surf = pygame.transform.rotate(surf, projectile.angle - 45)
            screen = (
                screen[0] - surf.get_width() / 2,
                screen[1] - surf.get_height() / 2,
            )
            self.display.blit(surf, screen)

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
        super().render(deltatime)
        self.display.fill(config.BACKGROUND)
        self.render_map()
        self.render_enemies()
        self.render_player()
        self.render_projectiles()
        render_effects()
        self.render_ui()

    def on_event(self, event_name: str):
        def player_kill(i: int):
            sec_passed = (-i - 1) / config.FPS
            alpha = min(255, round(255 * (sec_passed)))
            gameover = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            gameover.fill(config.BACKGROUND)
            gameover.set_alpha(alpha)
            self.display.blit(gameover, (0, 0), gameover.get_rect())

            text = self.assets.get_font().render("Game Over", False, config.RED)
            rect = text.get_rect()
            rect.centerx = self.width // 2
            rect.bottom = self.height // 2
            self.display.blit(text, rect)

            text = self.assets.get_font().render(
                "You've reached level " + str(self.game.level), False, config.YELLOW
            )
            text.set_alpha(alpha // 100 * 255)
            rect = text.get_rect()
            rect.centerx = self.width // 2
            rect.top = self.height // 2
            self.display.blit(text, rect)

        def fade(i: int):
            interval = 1 - (i / (config.FPS * 1))
            if interval >= 0.5:
                interval = 1 - interval
            alpha = min(255, round(255 * interval * 2))
            surf = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            surf.fill(config.BACKGROUND)
            surf.set_alpha(alpha)
            self.display.blit(surf, (0, 0), surf.get_rect())
<<<<<<< HEAD
            if i == (config.FPS * 1 - 1):
                should_block_input = False
=======
            if i == (config.FPS*1 - 1):
                self.should_block_input = False
        def deny(i: int):
            interval = 1 - (i / (config.FPS*1))
            if interval >= 0.5:
                interval = 1 - interval
            alpha = min(255, round(255 * abs(math.sin(interval*math.tau))))
            surf = Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            surf.fill(config.BACKGROUND)
            surf.set_alpha(alpha)
            self.display.blit(surf, (0, 0), surf.get_rect())
>>>>>>> main

        super().on_event(event_name)
        match event_name:
            case config.PLAYER_KILL_EVENT:
                should_block_input = True
                self.game.game_over = True
                effects.append([-1, player_kill])
            case config.LEVEL_UP_EVENT:
<<<<<<< HEAD
                should_block_input = True
                effects.append([config.FPS * 1, fade])
=======
                self.should_block_input = True
                self.effects.append([config.FPS*1, fade])
            case config.DENIED_LEVEL_UP_EVENT:
                self.effects.append([config.FPS*1, deny])

>>>>>>> main

    def move(self, dx: float, dy: float):
        if should_block_input:
            return
        self.game.player.move(dx, dy)

    def keydown(self, key: int):
        match key:
            case config.K_OPEN_MENU:
                switch_screen(MenuScreen(self.app))
            case config.K_OPEN_MAP:
                if should_block_input:
                    return
                switch_screen(MapScreen(self))
            case config.K_INTERACT:
                if should_block_input:
                    return
                self.game.interact()
                # TODO: Interact, attack, fire
            case config.K_ATTACK:
                if should_block_input:
                    return
                self.game.melee()
            case config.K_FIRE:
                if should_block_input:
                    return
                self.game.ranged()


class MapScreen(Screen):
    x: float
    y: float
    maptileset: Surface
    parent: MainScreen

    def __init__(self, mainscreen: MainScreen) -> None:
        super().__init__(mainscreen.app)
        self.parent = mainscreen
        self.x = self.game.player.x
        self.y = self.game.player.y
        t = self.assets.get_tileset_surface(config.MAP_TILESET)
        if t is None:
            raise Exception("no map tileset")
        self.maptileset = t

    def calculate_screen(self, x: float, y: float):
        return (
            (x - self.x) * config.MAP_WORLD_SIZE + self.width / 2,
            (y - self.y) * config.MAP_WORLD_SIZE + self.height / 2,
        )

    def render(self, deltatime: float):
        super().render(deltatime)
        self.display.fill(config.MAP_BACKGROUND)
        half_width = math.ceil(config.MAP_TILES_WIDTH / 2)
        half_height = math.ceil(config.MAP_TILES_HEIGHT / 2)
        for x in range(math.floor(self.x - half_width), math.ceil(self.x + half_width)):
            for y in range(
                math.floor(self.y - half_height), math.ceil(self.y + half_height)
            ):
                self.render_tile(x, y, self.map().get_tile(x, y))

    def render_tile(self, x: int, y: int, tile: Tile):
        def empty(x2, y2):
            return self.map().get_tile(x + x2, y + y2) == Tile.empty

        def r(s):
            t = self.assets.get_tile(config.MAP_TILESET, s)
            if t is None:
                return
            screen = self.calculate_screen(x, y)
            self.display.blit(self.maptileset, screen, t)

        if tile != Tile.empty:
            if tile.has_ground():
                r("floor")
            if tile != Tile.floor:
                r(tile.value)
        else:
            n = not empty(0, -1)
            e = not empty(1, 0)
            s = not empty(0, 1)
            w = not empty(-1, 0)
            if n:
                r("topedge")
            if s:
                r("bottomedge")
            if e:
                r("rightedge")
            if w:
                r("leftedge")
            # if not empty(-1, -1) and not w and not n:
            #     r("outercornerse")
            # if not empty(1, -1) and not e and not n:
            #     r("outercornersw")
            # if not empty(-1, 1) and not w and not s:
            #     r("outercornerne")
            # if not empty(1, 1) and not e and not s:
            #     r("outercornernw")

    def on_event(self, event_name: str):
        print("map event")
        switch_screen(self.parent)
        self.parent.on_event(event_name)

    def tick(self, deltatime: float):
        return self.parent.tick(deltatime)

    def keydown(self, key: int):
        match key:
            case config.K_CLOSE:
                switch_screen(self.parent)
            case config.K_OPEN_MAP:
                switch_screen(self.parent)

    def move(self, dx: float, dy: float):
        self.x += dx * 8
        self.y += dy * 8


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
        reset()
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

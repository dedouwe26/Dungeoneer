from abc import ABC, abstractmethod
from typing import Final

from pygame import Color, Surface

from assetloader import AssetLoader
import config
from game import Game


class Screen(ABC):
    width: int
    height: int
    asset_loader: AssetLoader
    game: Game
    display: Surface

    def __init__(self, asset_loader: AssetLoader, game: Game, display: Surface) -> None:
        super().__init__()
        self.display = display
        self.asset_loader = asset_loader
        self.game = game
        self.width, self.height = self.display.get_size()

    @abstractmethod
    def move(self, dx: float, dy: float):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def keydown(self, key: int):
        pass

    @abstractmethod
    def keyup(self, key: int):
        pass


class MainScreen(Screen):
    def move(self, dx: float, dy: float):
        pass

    def render(self):
        pass

    def keydown(self, key: int):
        pass

    def keyup(self, key: int):
        pass


class MapScreen(Screen):
    def move(self, dx: float, dy: float):
        pass

    def render(self):
        pass

    def keydown(self, key: int):
        pass

    def keyup(self, key: int):
        pass


class MenuScreen(Screen):
    BACKGROUND: Final[Color] = Color(28, 17, 23)
    MENU: Final[int] = 0
    LOAD_GAME: Final[int] = 1
    SAVE_GAME: Final[int] = 2
    state: int
    selected: int
    save_names: list[str]

    def __init__(self, asset_loader: AssetLoader, game: Game, display: Surface) -> None:
        super().__init__(asset_loader, game, display)
        self.change_state(self.MENU)

    def render_item(self, index: int, text: str):
        pass

    def render_menu(self):
        self.render_item(0, "New Game ")
        self.render_item(1, "Load Game")
        self.render_item(2, "Save Game")
        self.render_item(3, "  Quit   ")

    def render_list(self):
        for i, name in enumerate(self.save_names):
            self.render_item(i, name)

    def render(self):
        self.display.fill(self.BACKGROUND)
        icon = self.assets.get_logo()
        self.display.blit(icon, icon.get_rect(center_x=self.width / 2, top=16))
        match self.state:
            case self.MENU:
                self.render_menu()
            case self.LOAD_GAME:
                self.render_list()
            case self.SAVE_GAME:
                self.render_list()

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
                                self.main.stop()
                    case self.LOAD_GAME:
                        self.load_game()
                    case self.SAVE_GAME:
                        self.save_game()
            case config.K_MOVE_UP:
                pass
            case config.K_MOVE_DOWN:
                pass

    def change_state(self, new_state: int):
        self.selected = 0
        match new_state:
            case self.MENU:
                self.length = 4
            case self.SAVE_GAME:
                self.save_names = self.save_manager.fetch_saves()
                self.length = len(self.save_names)
            case self.LOAD_GAME:
                self.save_names = self.save_manager.fetch_saves()
                self.length = len(self.save_names)
        self.state = new_state

    def choose_new_game(self):
        self.game.new_game()
        self.main.change_screen(MainScreen(self.main))

    def load_game(self):
        self.main.save_manager.load(self.game(), self.save_names[self.selected])
        self.main.change_screen(MainScreen(self.main))

    def save_game(self):
        self.main.save_manager.save(self.game(), self.save_names[self.selected])
        self.change_state(self.MENU)

    def keyup(self, key: int):
        pass

    def move(self, dx: float, dy: float):
        pass

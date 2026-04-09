from abc import ABC, abstractmethod

from assetloader import AssetLoader
from game import Game
from main import Main


class Screen(ABC):
    main: Main

    def __init__(self, main: Main) -> None:
        super().__init__()
        self.main = main

    def assets(self) -> AssetLoader:
        return self.main.asset_loader

    def game(self) -> Game:
        return self.main.game

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
    def move(self, dx: float, dy: float):
        pass

    def render(self):
        pass

    def keydown(self, key: int):
        pass

    def keyup(self, key: int):
        pass

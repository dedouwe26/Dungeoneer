import os
import json
from pathlib import Path

from game import Game


class SaveManager:
    save_path: Path
    latest_save: str

    def __init__(self, save_path: Path) -> None:
        self.save_path = save_path

    def fetch_saves(self) -> list[str]:
        filenames = next(os.walk(self.save_path), (None, None, []))[2]
        return [Path(name).stem for name in filenames]

    def store(self, game: Game, save_name: str):
        # TODO: Implement for game.
        self.latest_save = save_name
        path = self.save_path / Path(save_name + ".json")
        with open(path, "w") as file:
            pass

    def load(self, game: Game, save_name: str):
        # TODO: Implement for game.
        self.latest_save = save_name
        path = self.save_path / Path(save_name + ".json")
        with open(path, "r") as file:
            parsed = json.load(file)
        print(parsed)

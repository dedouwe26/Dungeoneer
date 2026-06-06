import os
import json
from pathlib import Path

from config import DEFAULT_SAVE_NAMES
from game import Game


class SaveManager:
    save_path: Path
    latest_save: str

    def __init__(self, save_path: Path) -> None:
        self.save_path = save_path.absolute()
        if not self.save_path.is_dir():
            self.save_path.mkdir()

    def fetch_saves(self) -> list[str]:
        filenames = next(os.walk(self.save_path), (None, None, []))[2]
        if len(filenames) == 0:
            for name in DEFAULT_SAVE_NAMES:
                with open(self.save_path / Path(name + ".json"), "w") as f:
                    json.dump({}, f)
            filenames = next(os.walk(self.save_path), (None, None, []))[2]
        ret = [Path(name).stem for name in filenames]
        ret.sort()
        return ret

    def save(self, game: Game, save_name: str):
        if game.game_over: return
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

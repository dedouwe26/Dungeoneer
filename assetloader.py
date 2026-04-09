import json
from pathlib import Path
import random
from typing import Final

import pygame


class AssetLoader:
    MAIN_TILESET: Final[int] = 0
    MAP_TILESET: Final[int] = 1

    logo: pygame.Surface
    font: pygame.font.Font
    tilesets: list[
        tuple[pygame.Surface, int, dict[str, pygame.Rect | list[pygame.Rect]]]
    ]
    sounds: dict[str, pygame.mixer.Sound]

    def parse_tile(self, tile, tilesize: int) -> pygame.Rect:
        x = 0
        y = 0
        w = 0
        h = 0
        if "x" in tile:
            x = tile["x"] * tilesize
        if "rawx" in tile:
            x = tile["x"]
        if "y" in tile:
            y = tile["x"] * tilesize
        if "rawy" in tile:
            y = tile["x"]
        if "w" in tile:
            w = tile["w"] * tilesize
        if "raww" in tile:
            w = tile["raww"]
        if "h" in tile:
            h = tile["h"] * tilesize
        if "rawh" in tile:
            h = tile["rawh"]
        return pygame.Rect(x, y, w, h)

    def __init__(self, assetDescriptor: Path) -> None:
        assetDirectory = assetDescriptor.parent

        with open(assetDescriptor, "r") as file:
            self.descriptor = json.load(file)

        self.tilesets = []
        for tileset in self.descriptor["tilesets"]:
            tiles = {}
            tilesize = tileset["tilesize"]
            for tile in tileset["tiles"]:
                if "variants" in tileset["tiles"][tile]:
                    variants = []
                    for t in tileset["tiles"][tile]["variants"]:
                        variants.append(self.parse_tile(t, tilesize))
                    tiles[tile] = variants
                else:
                    tiles[tile] = self.parse_tile(tileset["tiles"][tile], tilesize)

            path = assetDirectory / Path(tileset["source"])
            self.tilesets.append((pygame.image.load(path.resolve()), tilesize, tiles))

        self.logo = pygame.image.load(
            (assetDirectory / Path(self.descriptor["logo"])).resolve()
        )

        self.font = pygame.font.Font(
            assetDirectory / Path(self.descriptor["font"]), self.descriptor["fontsize"]
        )

        for sound in self.descriptor["sounds"]:
            path = Path(self.descriptor["sounds"][sound])
            self.sounds[sound] = pygame.mixer.Sound(assetDirectory / path)

    def get_font(self) -> pygame.font.Font:
        return self.font

    def get_tileset_surface(self, tileset: int) -> pygame.Surface | None:
        if len(self.tilesets) <= tileset:
            return None
        return self.tilesets[tileset][0]

    def get_tile(self, tileset: int, tilename: str) -> pygame.Rect | None:
        if len(self.tilesets) <= tileset:
            return None
        if tilename not in self.tilesets[tileset][2]:
            return None
        tile = self.tilesets[tileset][2][tilename]
        if isinstance(tile, pygame.Rect):
            return tile
        else:
            return random.choice(tile)

    def get_logo(self) -> pygame.Surface:
        return self.logo

    def get_sound(self, id: str) -> pygame.mixer.Sound | None:
        if id in self.sounds:
            return self.sounds[id]
        return None

import json
from pathlib import Path
import random

import pygame

import config


class AssetLoader:
    logo: pygame.Surface
    font: pygame.font.Font
    tilesets: list[
        tuple[
            pygame.Surface,
            int,
            dict[str, pygame.Rect | list[pygame.Rect]],
            pygame.Surface,
        ]
    ] = []
    sounds: dict[str, pygame.mixer.Sound] = {}

    def parse_tile(self, tile, tilesize: int, scale: int) -> pygame.Rect:
        x = 0
        y = 0
        w = tilesize
        h = tilesize
        if "x" in tile:
            x = tile["x"] * tilesize
        if "rawx" in tile:
            x = tile["rawx"]
        if "y" in tile:
            y = tile["y"] * tilesize
        if "rawy" in tile:
            y = tile["rawy"]
        if "w" in tile:
            w = tile["w"] * tilesize
        if "raww" in tile:
            w = tile["raww"]
        if "h" in tile:
            h = tile["h"] * tilesize
        if "rawh" in tile:
            h = tile["rawh"]
        x *= scale
        y *= scale
        w *= scale
        h *= scale
        return pygame.Rect(x, y, w, h)

    def __init__(self, assetDescriptor: Path) -> None:
        assetDirectory = assetDescriptor.parent

        with open(assetDescriptor, "r") as file:
            self.descriptor = json.load(file)

        self.tilesets = []
        for tileset in self.descriptor["tilesets"]:
            tiles = {}
            tilesize = tileset["tilesize"]
            scale = config.WORLD_SIZE / tilesize
            for tile in tileset["tiles"]:
                if "variants" in tileset["tiles"][tile]:
                    variants = []
                    for t in tileset["tiles"][tile]["variants"]:
                        variants.append(self.parse_tile(t, tilesize, scale))
                    tiles[tile] = variants
                else:
                    tiles[tile] = self.parse_tile(
                        tileset["tiles"][tile], tilesize, scale
                    )

            path = assetDirectory / Path(tileset["source"])
            old = pygame.image.load(path.resolve())
            scaled = pygame.transform.scale(
                old,
                (
                    old.get_width() * scale,
                    old.get_height() * scale,
                ),
            )
            del old
            self.tilesets.append(
                (scaled, tilesize, tiles, pygame.transform.flip(scaled, True, False))
            )

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

    def get_tileset_surface(
        self, tileset: int, flipped: bool = False
    ) -> pygame.Surface | None:
        if len(self.tilesets) <= tileset:
            return None
        if flipped:
            return self.tilesets[tileset][3]
        return self.tilesets[tileset][0]

    def get_tile(
        self, tileset: int, tilename: str, variant: int = 0, flipped: bool = False
    ) -> pygame.Rect | None:
        if len(self.tilesets) <= tileset:
            return None
        if tilename not in self.tilesets[tileset][2]:
            return None
        tile = self.tilesets[tileset][2][tilename]
        if not isinstance(tile, pygame.Rect):
            tile = tile[variant % len(tile)]

        if flipped:
            s = self.get_tileset_surface(tileset)
            if s is None:
                return
            return pygame.Rect(
                s.get_width() - tile.x - tile.width, tile.y, tile.width, tile.height
            )
        return tile

    def get_tile_size(self, tileset: int) -> int | None:
        if len(self.tilesets) <= tileset:
            return None
        return self.tilesets[tileset][1]

    def get_logo(self) -> pygame.Surface:
        return self.logo

    def get_sound(self, id: str) -> pygame.mixer.Sound | None:
        if id in self.sounds:
            return self.sounds[id]
        return None

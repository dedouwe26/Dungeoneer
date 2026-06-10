import json
from pathlib import Path
from random import Random

import pygame

import config  # noqa: F401

class AssetLoader:
    logo: pygame.Surface
    font: pygame.font.Font
    tilesets: list[
        tuple[
            pygame.Surface, # main surface
            int, # tilesize
            dict[str, tuple[ # tile
                list[pygame.Rect], # variants
                int, # lobby variant
                list[float] # chances for each variant
            ]], # tiles
            pygame.Surface, # flipped surface
        ]
    ] = []
    sounds: dict[str, pygame.mixer.Sound] = {}
    level_random: Random

    def parse_raw_tile(self, tile, tilesize: int, scale: int) -> pygame.Rect:
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
            scale = eval(tileset["virtualsize"])

            for tile in tileset["tiles"]: # tile
                t = tileset["tiles"][tile]

                if "variants" in t: # raw tile
                    variants = []
                    for t in t["variants"]:
                        variants.append(self.parse_raw_tile(t, tilesize, scale))
                    variants = variants
                else:
                    variants = [self.parse_raw_tile(
                        t, tilesize, scale
                    )]

                # optional variations
                lobby_variant = 0
                chances = [1 / len(variants) for i in range(len(variants))]
                if "lobbyvariant" in t:
                    lobby_variant = t["lobbyvariant"]
                if "chances" in t:
                    chances = t["chances"]
                tiles[tile] = (variants, lobby_variant, chances)

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
        tiles = self.tilesets[tileset][2][tilename][0]
        tile = tiles[variant % len(tiles)]
        if flipped:
            s = self.get_tileset_surface(tileset)
            if s is None:
                return
            return pygame.Rect(
                s.get_width() - tile.x - tile.width, tile.y, tile.width, tile.height
            )
        return tile
    
    def get_tile_variants(self, tileset: int, tilename: str) -> tuple[int, list[float]]:
        if len(self.tilesets) <= tileset:
            return None
        if tilename not in self.tilesets[tileset][2]:
            return None
        tile = self.tilesets[tileset][2][tilename]
        return (tile[1], tile[2])

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

from functools import lru_cache

from PySide6.QtGui import QImage

from foundry.core.graphics_set.GraphicsSet import GraphicsSet
from foundry.core.palette import ColorPalette, PaletteGroup
from foundry.core.tiles import MASK_COLOR
from foundry.game.gfx.drawable import bit_reverse

PIXEL_OFFSET = 8  # both bits describing the color of a pixel are in separate 8 byte chunks at the same index

BACKGROUND_COLOR_INDEX = 0


@lru_cache(2**10)
class Tile:
    SIDE_LENGTH = 8  # pixel
    WIDTH = SIDE_LENGTH
    HEIGHT = SIDE_LENGTH

    PIXEL_COUNT = WIDTH * HEIGHT
    SIZE = 2 * PIXEL_COUNT // 8  # 1 pixel is defined by 2 bits

    def __init__(
        self,
        object_index: int,
        palette_group: PaletteGroup,
        palette_index: int,
        graphics_set: GraphicsSet,
        mirrored=False,
    ):
        start = object_index * Tile.SIZE

        self.cached_tiles = dict()

        self.palette = palette_group[palette_index]

        self.data = bytearray()
        self.pixels = bytearray()
        self.mask_pixels = bytearray()

        self.data = bytearray(bytes(graphics_set))[start : start + Tile.SIZE]

        if mirrored:
            self._mirror()

        for i in range(Tile.PIXEL_COUNT):
            byte_index = i // Tile.HEIGHT
            bit_index = 2 ** (7 - (i % Tile.WIDTH))

            left_bit = right_bit = 0

            if self.data[byte_index] & bit_index:
                left_bit = 1

            if self.data[PIXEL_OFFSET + byte_index] & bit_index:
                right_bit = 1

            color_index = (right_bit << 1) | left_bit

            color: int = self.palette[color_index]

            # add alpha values
            if color_index == 0:
                self.pixels.extend(MASK_COLOR)
            else:
                self.pixels.extend(ColorPalette.from_default()[color].to_qt().toTuple()[:3])

        assert len(self.pixels) == 3 * Tile.PIXEL_COUNT

    def as_image(self, tile_length=8):
        if tile_length not in self.cached_tiles.keys():
            width = height = tile_length

            image = QImage(self.pixels, self.WIDTH, self.HEIGHT, QImage.Format_RGB888)

            image = image.scaled(width, height)

            self.cached_tiles[tile_length] = image

        return self.cached_tiles[tile_length]

    def _mirror(self):
        for byte in range(len(self.data)):
            self.data[byte] = bit_reverse[self.data[byte]]

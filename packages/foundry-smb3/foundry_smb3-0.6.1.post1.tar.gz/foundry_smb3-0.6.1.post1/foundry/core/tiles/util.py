from collections.abc import Generator
from functools import cache, lru_cache

from attr import attrs
from PySide6.QtGui import QImage

from foundry.core.graphics_set.GraphicsSet import GraphicsSet
from foundry.core.palette import Color, Palette
from foundry.core.tiles import (
    BYTES_PER_TILE,
    MASK_COLOR,
    PIXEL_OFFSET,
    PIXELS,
    TILE_SIZE,
)


@attrs(slots=True, auto_attribs=True, frozen=True, eq=True, hash=True)
class _Tile:
    """
    A representation of a tile inside the game.

    Attributes
    ----------
    index: int
        The tile index that define the graphics from the GraphicsSet.
    palette: Palette
        The palette.
    graphics_set: GraphicsSet
        The base of all images generated for the tile.
    """

    index: int
    palette: Palette
    graphics_set: GraphicsSet

    @cache
    def __bytes__(self) -> bytes:
        return bytes(self.graphics_set)[self.index * BYTES_PER_TILE : (self.index + 1) * BYTES_PER_TILE]

    @property
    def pixels_indexes(self) -> Generator[int, None, None]:
        """
        Provides a generator that generates the pixels in order from top to bottom of the tile.

        Yields
        -------
        Generator[int, None, None]
            A generator of pixels from top to bottom in 2BPP format.
        """
        for i in range(PIXELS):
            byte_index = i // TILE_SIZE.height
            bit_index = 2 ** (7 - (i % TILE_SIZE.width))

            yield (int(bool(bytes(self)[PIXEL_OFFSET + byte_index] & bit_index)) << 1) | int(
                bool(bytes(self)[byte_index] & bit_index)
            )

    @property
    def pixels(self) -> bytes:
        """
        Generates a series of bytes in RGB color format that represents the tile.

        Returns
        -------
        bytes
            That represent an RGB tile image.
        """
        pixels = bytearray()
        assert isinstance(self.palette, Palette)

        for pixel_index in self.pixels_indexes:
            if pixel_index == 0:
                pixels.extend(MASK_COLOR)
            else:
                pixels.extend(self.palette[pixel_index, Color].to_rgb_bytes())

        return bytes(pixels)


def _tile_to_image(tile: _Tile, scale_factor: int = 1) -> QImage:
    """
    Generates a QImage of a tile from the NES.

    Parameters
    ----------
    tile : _Tile
        The dataclass instance that represents a tile inside the game.
    scale_factor : int, optional
        The multiple of 8 that the image will be created as, by default 1.

    Returns
    -------
    QImage
        That represents the tile.
    """
    image = QImage(tile.pixels, TILE_SIZE.width, TILE_SIZE.height, QImage.Format_RGB888)
    return image.scaled(TILE_SIZE.width * scale_factor, TILE_SIZE.height * scale_factor)


@lru_cache(2**10)
def cached_tile_to_image(
    tile_index: int,
    palette: Palette,
    graphics_set: GraphicsSet,
    scale_factor: int = 1,
) -> QImage:
    """
    Generates and caches a NES tile with a given palette and graphics as a QImage.

    Parameters
    ----------
    tile_index: int
        The tile index into the graphics set.
    palette : Palette
        The specific palette to use for the tile.
    graphics_set : GraphicsSet
        The specific graphics to use for the tile.
    scale_factor : int, optional
        The multiple of 8 that the image will be created as, by default 1

    Returns
    -------
    QImage
        That represents the tile.

    Notes
    -----
    Since this method is being cached, it is expected that every parameter is hashable and immutable.  If this does not
    occur, there is a high chance of an errors to linger throughout the program.
    """
    return _tile_to_image(_Tile(tile_index, palette, graphics_set), scale_factor)


def tile_to_image(tile_index: int, palette: Palette, graphics_set: GraphicsSet, scale_factor: int = 1) -> QImage:
    """
    Generates a tile with a given palette and graphics as a QImage.

    Parameters
    ----------
    tile_index: int
        The tile index into the graphics set.
    palette : Palette
        The specific palette to use for the tile.
    graphics_set : GraphicsSet
        The specific graphics to use for the tile.
    scale_factor : int, optional
        The multiple of 8 that the image will be created as, by default 1

    Returns
    -------
    QImage
        That represents the tile.
    """
    return cached_tile_to_image(tile_index, palette, graphics_set, scale_factor)

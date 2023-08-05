from PySide6.QtCore import QPoint, QSize

from foundry.core.graphics_set.GraphicsSet import GraphicsSet
from foundry.core.palette import PaletteGroup
from foundry.game.File import ROM
from foundry.game.gfx.drawable.Block import Block
from foundry.game.gfx.objects.MapObject import MapObject
from foundry.game.level.LevelLike import LevelLike
from foundry.smb3parse.levels.world_map import (
    WORLD_MAP_HEIGHT,
    WORLD_MAP_SCREEN_SIZE,
    WORLD_MAP_SCREEN_WIDTH,
)
from foundry.smb3parse.levels.world_map import WorldMap as _WorldMap
from foundry.smb3parse.objects.object_set import WORLD_MAP_OBJECT_SET

OVERWORLD_GRAPHIC_SET = 0


class WorldMap(LevelLike):
    def __init__(self, world_index):
        self._internal_world_map = _WorldMap.from_world_number(ROM(), world_index)

        super().__init__(0, self._internal_world_map.layout_address)

        self.name = f"World {world_index} - Overworld"

        self.graphics_set = GraphicsSet.from_tileset(OVERWORLD_GRAPHIC_SET)
        self.palette_group = PaletteGroup.from_tileset(WORLD_MAP_OBJECT_SET, 0)

        self.object_set = WORLD_MAP_OBJECT_SET
        self.tsa_data = ROM.get_tsa_data(self.object_set)

        self.world = 0
        self.level_number = world_index

        self.objects = []

        self._load_objects()

        self._calc_size()

    def _load_objects(self):
        self.objects.clear()

        for index, world_position in enumerate(self._internal_world_map.gen_positions()):
            screen_offset = (index // WORLD_MAP_SCREEN_SIZE) * WORLD_MAP_SCREEN_WIDTH

            x = screen_offset + (index % WORLD_MAP_SCREEN_WIDTH)
            y = (index // WORLD_MAP_SCREEN_WIDTH) % WORLD_MAP_HEIGHT

            block = Block(
                world_position.tile(),
                self.palette_group,
                self.graphics_set,
                self.tsa_data,
            )

            self.objects.append(MapObject(block, x, y))

        assert len(self.objects) % WORLD_MAP_HEIGHT == 0

    def _calc_size(self):
        self.width = len(self.objects) // WORLD_MAP_HEIGHT
        self.height = WORLD_MAP_HEIGHT

        self.size = self.width, self.height

    def add_object(self, obj, _):
        self.objects.append(obj)

        self.objects.sort(key=self._array_index)

    @property
    def q_size(self):
        return QSize(*self.size) * Block.SIDE_LENGTH

    @staticmethod
    def _array_index(obj):
        return obj.y_position * WORLD_MAP_SCREEN_WIDTH + obj.x_position

    def get_object_names(self):
        return [obj.name for obj in self.objects]

    def draw(self, dc, zoom, transparency=None, show_expansion=None):
        for obj in self.objects:
            obj.draw(dc, Block.SIDE_LENGTH * zoom, transparency)

    def index_of(self, obj):
        return self.objects.index(obj)

    def get_all_objects(self):
        return self.objects

    def object_at(self, x, y):
        point = QPoint(x, y)

        for obj in reversed(self.objects):
            if obj.rect.contains(point):
                return obj

        return None

    def to_bytes(self):
        return_array = bytearray(len(self.objects))

        for obj in self.objects:
            index = self._array_index(obj)

            return_array[index] = obj.to_bytes()

        return self.layout_address, return_array

    def from_bytes(self, data, _=None):
        offset, obj_bytes = data

        self.layout_address = offset
        self._load_objects(obj_bytes)

        self._calc_size()

    def get_object(self, index):
        return self.objects[index]

    def remove_object(self, obj):
        self.objects.remove(obj)

    def level_at_position(self, x: int, y: int):
        assert isinstance(x, int)
        assert isinstance(y, int)

        screen = x // WORLD_MAP_SCREEN_WIDTH + 1

        x %= WORLD_MAP_SCREEN_WIDTH

        return self._internal_world_map.level_for_position(screen, y, x)

    def level_name_at_position(self, x: int, y: int) -> str:
        screen = x // WORLD_MAP_SCREEN_WIDTH + 1

        x %= WORLD_MAP_SCREEN_WIDTH

        return self._internal_world_map.level_name_for_position(screen, y, x)

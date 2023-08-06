from PySide6.QtCore import Signal, SignalInstance
from PySide6.QtWidgets import QVBoxLayout, QWidget

from foundry.game.gfx.objects.EnemyItem import EnemyObject
from foundry.game.gfx.objects.LevelObject import LevelObject
from foundry.game.gfx.objects.ObjectLike import ObjectLike
from foundry.gui.TabbedToolBox import TabbedToolBox


class ObjectToolBar(QWidget):
    selected: SignalInstance = Signal(ObjectLike)  # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(200)
        self.setMinimumWidth(50)
        self.tileset = -1
        self.bg_palette_index = 0
        self.spr_palette_index = 0

        self.tool_box = TabbedToolBox()
        self.tool_box.selected_index.connect(self.select_object)

        layout.addWidget(self.tool_box, stretch=1)

    def set_object_set(
        self, object_set_index: int, graphic_set_index: int = -1, bg_palette_index: int = 0, spr_palette_index: int = 0
    ):
        if (
            self.tileset == object_set_index
            and self.bg_palette_index == bg_palette_index
            and self.spr_palette_index == spr_palette_index
        ):
            return
        self.tileset = object_set_index
        self.bg_palette_index = bg_palette_index
        self.spr_palette_index = spr_palette_index
        self.tool_box.set_object_set(object_set_index, graphic_set_index, bg_palette_index, spr_palette_index)

    def select_object(self, tab_index: int, object_index: int):
        item = self.tool_box.select_object(tab_index, object_index)
        self.selected.emit(item)

    def add_recent_object(self, level_object: EnemyObject | LevelObject):
        self.tool_box.add_recent_object(level_object)

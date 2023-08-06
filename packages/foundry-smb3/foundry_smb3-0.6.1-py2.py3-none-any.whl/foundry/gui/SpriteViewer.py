from attr import attrs
from PySide6.QtCore import Signal, SignalInstance
from PySide6.QtGui import QCloseEvent, QMouseEvent, QPainter, QPaintEvent, QResizeEvent
from PySide6.QtWidgets import QLayout, QStatusBar, QToolBar, QWidget

from foundry import icon
from foundry.core.geometry import Point, Size
from foundry.core.graphics_set.GraphicsSet import GraphicsSet
from foundry.core.palette import PaletteGroup
from foundry.core.sprites import SPRITE_SIZE
from foundry.game.gfx.drawable.Sprite import Sprite
from foundry.gui.CustomChildWindow import CustomChildWindow


@attrs(slots=True, auto_attribs=True)
class SpriteViewerModel:
    graphics_set: GraphicsSet
    palette_group: PaletteGroup
    palette_index: int


class SpriteViewerController(CustomChildWindow):
    graphics_set_changed: SignalInstance = Signal(GraphicsSet)  # type: ignore
    palette_group_changed: SignalInstance = Signal(PaletteGroup)  # type: ignore
    palette_index_changed: SignalInstance = Signal(int)  # type: ignore
    sprite_selected: SignalInstance = Signal(int)  # type: ignore
    destroyed: SignalInstance = Signal()  # type: ignore

    def __init__(
        self,
        parent: QWidget | None,
        graphics_set: GraphicsSet,
        palette_group: PaletteGroup,
        palette_index: int,
    ):
        super().__init__(parent, "Sprite Viewer")

        self.model = SpriteViewerModel(graphics_set, palette_group, palette_index)
        self.view = SpriteViewerView(self, graphics_set, palette_group, palette_index)
        self.setCentralWidget(self.view)
        self.toolbar = QToolBar(self)

        self.toolbar.setMovable(False)

        self.view.sprite_selected.connect(self.sprite_selected.emit)

        self.zoom_out_action = self.toolbar.addAction(icon("zoom-out.png"), "Zoom Out")
        self.zoom_in_action = self.toolbar.addAction(icon("zoom-in.png"), "Zoom In")

        def change_zoom(offset: int):
            self.view.zoom += offset

        self.zoom_out_action.triggered.connect(lambda *_: change_zoom(-1))  # type: ignore
        self.zoom_in_action.triggered.connect(lambda *_: change_zoom(1))  # type: ignore

        self.addToolBar(self.toolbar)
        self.setStatusBar(QStatusBar(self))

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def closeEvent(self, event: QCloseEvent):
        self.toolbar.close()
        self.destroyed.emit()
        super().closeEvent(event)

    @property
    def graphics_set(self) -> GraphicsSet:
        return self.model.graphics_set

    @graphics_set.setter
    def graphics_set(self, value: GraphicsSet):
        self.model.graphics_set = value
        self.view.graphics_set = value
        self.graphics_set_changed.emit(self.graphics_set)
        self.view.update()

    @property
    def palette_group(self) -> PaletteGroup:
        return self.model.palette_group

    @palette_group.setter
    def palette_group(self, value: PaletteGroup):
        self.model.palette_group = value
        self.view.palette_group = value
        self.palette_group_changed.emit(self.palette_group)
        self.view.update()

    @property
    def palette_index(self) -> int:
        return self.model.palette_index

    @palette_index.setter
    def palette_index(self, value: int):
        self.model.palette_index = value
        self.view.palette_index = value
        self.palette_index_changed.emit(self.palette_index)
        self.view.update()


class SpriteViewerView(QWidget):
    sprite_selected: SignalInstance = Signal(int)  # type: ignore
    mouse_moved: SignalInstance = Signal(int, int, int, str)  # type: ignore

    SPRITES = 32
    SPRITES_PER_ROW = 16
    SPRITES_PER_COLUMN = 2

    def __init__(
        self,
        parent: QWidget | None,
        graphics_set: GraphicsSet,
        palette_group: PaletteGroup,
        palette_index: int,
        zoom: int = 4,
    ):
        super().__init__(parent)

        self.setMouseTracking(True)

        self.graphics_set = graphics_set
        self.palette_group = palette_group
        self.palette_index = palette_index
        self.zoom = zoom

    def resizeEvent(self, event: QResizeEvent):
        self.update()

    @property
    def zoom(self) -> int:
        return self._zoom

    @zoom.setter
    def zoom(self, value: int):
        self._zoom = value
        self.setFixedSize(
            self.SPRITES_PER_ROW * SPRITE_SIZE.width * self.zoom,
            self.SPRITES_PER_COLUMN * SPRITE_SIZE.height * self.zoom,
        )

    @property
    def sprite_size(self) -> Size:
        return Size(SPRITE_SIZE.width * self.zoom, SPRITE_SIZE.height * self.zoom)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = Point.from_qpoint(event.pos()) // Point(self.sprite_size.width, self.sprite_size.height)

        dec_index = pos.y * self.SPRITES_PER_ROW + pos.x
        hex_index = hex(dec_index).upper().replace("X", "x")

        self.mouse_moved.emit(pos.x, pos.y, dec_index, hex_index)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = Point.from_qpoint(event.pos()) // Point(self.sprite_size.width, self.sprite_size.height)

        index = pos.y * self.SPRITES_PER_ROW + pos.x
        self.sprite_selected.emit(index)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        for i in range(self.SPRITES):
            sprite = Sprite(
                i * 2,
                self.palette_group,
                self.palette_index,
                self.graphics_set,
            )

            x = (i % self.SPRITES_PER_ROW) * self.sprite_size.width
            y = (i // self.SPRITES_PER_ROW) * self.sprite_size.height

            sprite.draw(painter, x, y, SPRITE_SIZE.width * self.zoom, SPRITE_SIZE.height * self.zoom, transparent=True)

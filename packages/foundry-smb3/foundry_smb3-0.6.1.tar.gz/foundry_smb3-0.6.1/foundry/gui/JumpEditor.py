from PySide6.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QVBoxLayout,
    QWidget,
)

from foundry.game.gfx.objects.Jump import Jump
from foundry.gui.CustomDialog import CustomDialog
from foundry.gui.Spinner import Spinner

JUMP_ACTIONS = {
    "Downward Pipe 1": 0,
    "Upward Pipe": 1,
    "Downward Pipe 2": 2,
    "Right Pipe": 3,
    "Left Pipe": 4,
    "Jump on Noteblock": 7,
    "Door": 8,
}


JUMP_INDEXES = [0, 1, 2, 3, 4, 0, 0, 5, 6, 0, 0, 0, 0, 0, 0, 0]


VERT_POSITIONS = ["00", "05", "08", "12", "16", "20", "23", "24"]

MAX_SCREEN_INDEX = 0x0F
MAX_HORIZ_POSITION = 0xFF


class JumpEditor(CustomDialog):
    def __init__(
        self, parent: QWidget | None, jump: Jump, is_horizontal: bool, suggested_max_size: int = MAX_SCREEN_INDEX
    ):
        super().__init__(parent, "Jump Editor")

        self.jump = jump
        self.is_horizontal = is_horizontal

        self.screen_spinner = Spinner(parent=self, maximum=suggested_max_size, base=10)

        position_layout = QFormLayout()
        position_layout.addRow("Jump on screen:", self.screen_spinner)

        level_group_box = QGroupBox("Level point")
        level_group_box.setLayout(position_layout)

        self.exit_action = QComboBox(self)
        self.exit_action.addItems(JUMP_ACTIONS.keys())

        self.exit_horizontal = Spinner(parent=self, maximum=MAX_HORIZ_POSITION, base=10)

        self.exit_vertical = QComboBox(self)
        self.exit_vertical.addItems(VERT_POSITIONS)

        exit_layout = QFormLayout()
        exit_layout.addRow("Exit action:", self.exit_action)
        exit_layout.addRow("Exit point x:", self.exit_horizontal)
        exit_layout.addRow("Exit point y:", self.exit_vertical)

        exit_group_box = QGroupBox("Exit options")
        exit_group_box.setLayout(exit_layout)

        button_box = QDialogButtonBox()
        self.ok_button = button_box.addButton(QDialogButtonBox.Ok)
        self.ok_button.pressed.connect(self.on_ok)
        button_box.addButton(QDialogButtonBox.Cancel).pressed.connect(self.close)

        main_layout = QVBoxLayout()
        main_layout.addWidget(level_group_box)
        main_layout.addWidget(exit_group_box)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)

        self._set_widget_values()

    def _set_widget_values(self):
        self.screen_spinner.setValue(self.jump.screen_index)

        self.exit_action.setCurrentIndex(JUMP_INDEXES[self.jump.exit_action])
        self.exit_horizontal.setValue(self.jump.exit_horizontal)
        self.exit_vertical.setCurrentIndex(self.jump.exit_vertical & 0b111)

    @staticmethod
    def edit_jump(parent: QWidget | None, jump: Jump, is_horizontal: bool, suggested_max_size: int = MAX_SCREEN_INDEX):
        jump_editor = JumpEditor(parent, jump, is_horizontal, suggested_max_size)

        jump_editor.exec_()

        return jump_editor.jump

    def on_ok(self):
        self.jump = Jump.from_properties(
            self.screen_spinner.value(),
            JUMP_ACTIONS[self.exit_action.currentText()],
            self.exit_horizontal.value(),
            self.exit_vertical.currentIndex() if self.is_horizontal else self.exit_vertical.currentIndex() + 8,
        )

        self.close()

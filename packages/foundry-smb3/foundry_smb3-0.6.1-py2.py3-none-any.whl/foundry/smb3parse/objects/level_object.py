from foundry.smb3parse.levels import DEFAULT_HORIZONTAL_HEIGHT
from foundry.smb3parse.objects import InLevelObject


class LevelObject(InLevelObject):
    def __init__(self, data: bytearray):
        super().__init__(data)

        if len(data) not in [3, 4]:
            raise ValueError(f"Length of the given data must be 3 or 4, was {len(data)}.")

        self.domain = data[0] >> 5
        self.y = data[0] & 0b0001_1111

        if self.y > DEFAULT_HORIZONTAL_HEIGHT:
            raise ValueError(
                f"Data designating y value cannot be higher than {DEFAULT_HORIZONTAL_HEIGHT}, was {self.y}."
            )

        self.id = data[1]
        self.x = data[2]

        if len(data) == 4:
            self.additional_length = data[3]

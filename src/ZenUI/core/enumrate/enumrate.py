from enum import Enum, IntEnum, IntFlag, auto


class ZWindowType(IntEnum):
    Frameless = auto()
    Translucent = auto()

class ZState(IntEnum):
    Idle = auto()
    Hover = auto()
    Pressed = auto()
    Hidden = auto()
    Showing = auto()

class ZDirection(IntEnum):
    Vertical = auto()
    Horizontal = auto()
    Diagonal = auto()
    DiagonalReverse = auto()
    Custom = auto()

class ZPosition(IntEnum):
    Top = auto()
    Bottom = auto()
    Left = auto()
    Right = auto()
    TopLeft = auto()
    TopRight = auto()
    BottomLeft = auto()
    BottomRight = auto()
    Center = auto()
    Custom = auto()

class ZButtonStyle(IntEnum):
    Normal = auto()
    Flat = auto()

class ZWrapMode(IntEnum):
    NoWrap = auto()
    WordWrap = auto()
    WrapAnywhere = auto()

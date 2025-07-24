from dataclasses import dataclass
from PySide6.QtGui import QColor

__all__ = ['ZFramelessWindowStyleData','ZButtonStyleData','ZTitleBarButtonData',
            'ZTextBlockStyleData','ZToolTipStyleData','ZToggleButtonStyleData',
            'ZNavBarButtonStyleData','ZNavBarToggleButtonStyleData','ZPageStyleData',
            'ZScrollPageStyleData','ZSliderStyleData']



@dataclass
class ZFramelessWindowStyleData:
    Body: QColor

@dataclass
class ZTitleBarButtonData:
    Icon: QColor
    IconHover: QColor
    IconPressed: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor

@dataclass
class ZPageStyleData:
    Body: QColor
    Border: QColor
    Radius: int

@dataclass
class ZScrollPageStyleData:
    Body: QColor
    Border: QColor
    Handle: QColor
    HandleBorder: QColor
    Radius: int

@dataclass
class ZButtonStyleData:
    Text: QColor
    Icon: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor
    Border: QColor
    Radius: int

@dataclass
class ZNavBarButtonStyleData:
    Icon: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor
    Radius: int

@dataclass
class ZNavBarToggleButtonStyleData:
    Icon: QColor
    IconToggled: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor    
    BodyToggled: QColor
    BodyToggledHover: QColor
    BodyToggledPressed: QColor
    Radius: int

@dataclass
class ZToggleButtonStyleData:
    Text: QColor
    TextToggled: QColor
    Icon: QColor
    IconToggled: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor
    BodyToggled: QColor
    BodyToggledHover: QColor
    BodyToggledPressed: QColor
    Border: QColor
    BorderToggled: QColor
    Radius: int

@dataclass
class ZSliderStyleData:
    Track: QColor
    TrackBorder: QColor
    TrackFilledStart: QColor
    TrackFilledEnd: QColor
    HandleInner: QColor
    HandleOuter: QColor
    HandleBorder: QColor
    Radius: int

@dataclass
class ZToolTipStyleData:
    Text: QColor
    Body: QColor
    Border: QColor
    Radius: int

@dataclass
class ZTextBlockStyleData:
    Text: QColor
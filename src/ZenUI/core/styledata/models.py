from dataclasses import dataclass
from PySide6.QtGui import QColor
from typing import Union

__all__ = ['ZFramelessWindowStyleData','ZButtonStyleData','ZTitleBarButtonData',
            'ZTextBlockStyleData','ZToolTipStyleData','ZToggleButtonStyleData',
            'ZNavBarButtonStyleData','ZNavBarToggleButtonStyleData','ZPageStyleData',
            'ZScrollPageStyleData','ZSliderStyleData','ZCardStyleData','StyleDataType']



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
    Radius: float

@dataclass
class ZScrollPageStyleData:
    Body: QColor
    Border: QColor
    Handle: QColor
    HandleBorder: QColor
    Radius: float

@dataclass
class ZButtonStyleData:
    Text: QColor
    Icon: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor
    Border: QColor
    Radius: float

@dataclass
class ZNavBarButtonStyleData:
    Icon: QColor
    Body: QColor
    BodyHover: QColor
    BodyPressed: QColor
    Radius: float

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
    Radius: float

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
    Radius: float

@dataclass
class ZSliderStyleData:
    Track: QColor
    TrackBorder: QColor
    FillAreaStart: QColor
    FillAreaEnd: QColor
    FillAreaBorder: QColor
    HandleInner: QColor
    HandleOuter: QColor
    HandleBorder: QColor

@dataclass
class ZToolTipStyleData:
    Text: QColor
    Body: QColor
    Border: QColor
    Radius: float

@dataclass
class ZTextBlockStyleData:
    Body: QColor
    Border: QColor
    Text: QColor
    Radius: float


@dataclass
class ZCardStyleData:
    Body: QColor
    Border: QColor
    Radius: float


StyleDataType = Union[ZButtonStyleData, ZTitleBarButtonData,ZFramelessWindowStyleData,
                      ZTextBlockStyleData,ZToolTipStyleData, ZToggleButtonStyleData,
                      ZNavBarButtonStyleData,ZNavBarToggleButtonStyleData,ZPageStyleData,
                      ZScrollPageStyleData,ZSliderStyleData,ZCardStyleData]
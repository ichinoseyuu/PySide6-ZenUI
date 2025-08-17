from dataclasses import dataclass
from PySide6.QtGui import QColor
from typing import Union,TypeVar

__all__ = ['ZFramelessWindowStyleData','ZButtonStyleData','ZTitleBarButtonStyleData',
            'ZTextBlockStyleData','ZToolTipStyleData','ZToggleButtonStyleData',
            'ZNavBarButtonStyleData','ZNavBarToggleButtonStyleData','ZPageStyleData',
            'ZScrollPageStyleData','ZSliderStyleData','ZCardStyleData','ZTextBoxStyleData',
            'ZRichTextBlockStyleData','StyleDataT','StyleDataUnion']


@dataclass
class ZFramelessWindowStyleData:
    Body: QColor

@dataclass
class ZTitleBarButtonStyleData:
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
    Text: QColor
    TextBackSectcted: QColor
    Body: QColor
    Border: QColor
    Radius: float

@dataclass
class ZRichTextBlockStyleData:
    Text: QColor
    TextBackSectcted: QColor
    Body: QColor
    Border: QColor
    Radius: float

@dataclass
class ZTextBoxStyleData:
    Text: QColor
    TextBackSectcted: QColor
    Cursor: QColor
    Mask: QColor
    Underline: QColor
    UnderlineFocused: QColor
    Body: QColor
    BodyHover: QColor
    BodyFocused: QColor
    Border: QColor
    Radius: float

@dataclass
class ZCardStyleData:
    Body: QColor
    Border: QColor
    Radius: float


StyleDataUnion = Union[ZButtonStyleData, ZTitleBarButtonStyleData,ZFramelessWindowStyleData,
                      ZTextBlockStyleData,ZToolTipStyleData, ZToggleButtonStyleData,
                      ZNavBarButtonStyleData,ZNavBarToggleButtonStyleData,ZPageStyleData,
                      ZScrollPageStyleData,ZSliderStyleData,ZCardStyleData,ZTextBoxStyleData,
                      ZRichTextBlockStyleData]

# 定义类型变量，用于StyleData的泛型
StyleDataT = TypeVar('StyleDataT', bound='StyleDataUnion')
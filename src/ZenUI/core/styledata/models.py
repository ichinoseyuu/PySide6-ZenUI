from dataclasses import dataclass
from PySide6.QtGui import QColor
from typing import Union,TypeVar

__all__ = [
    'ZFramelessWindowStyleData',
    'ZButtonStyleData',
    'ZTitleBarButtonStyleData',
    'ZTextBlockStyleData',
    'ZToolTipStyleData',
    'ZToggleButtonStyleData',
    'ZNavBarButtonStyleData',
    'ZNavBarToggleButtonStyleData',
    'ZScrollPanelStyleData',
    'ZSliderStyleData',
    'ZTextBoxStyleData',
    'ZRichTextBlockStyleData',
    'ZPanelStyleData',
    'ZSwitchStyleData',
    'ZNavigationBarStyleData',
    'ZComboBoxStyleData',
    'ZComboBoxItemStyleData',
    'ZComboBoxItemViewStyleData',
    'StyleDataT',
    'StyleDataUnion'
    ]


@dataclass
class ZFramelessWindowStyleData:
    Body: QColor = None

@dataclass
class ZTitleBarButtonStyleData:
    Icon: QColor = None
    IconHover: QColor = None
    IconPressed: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None

@dataclass
class ZPanelStyleData:
    Body: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZScrollPanelStyleData:
    Body: QColor = None
    Border: QColor = None
    Handle: QColor = None
    HandleBorder: QColor = None
    Radius: float = None

@dataclass
class ZButtonStyleData:
    Text: QColor = None
    Icon: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZNavBarButtonStyleData:
    Icon: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None
    Radius: float = None

@dataclass
class ZNavBarToggleButtonStyleData:
    Icon: QColor = None
    IconToggled: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None
    BodyToggled: QColor = None
    BodyToggledHover: QColor = None
    BodyToggledPressed: QColor = None
    Radius: float = None

@dataclass
class ZToggleButtonStyleData:
    Text: QColor = None
    TextToggled: QColor = None
    Icon: QColor = None
    IconToggled: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None
    BodyToggled: QColor = None
    BodyToggledHover: QColor = None
    BodyToggledPressed: QColor = None
    Border: QColor = None
    BorderToggled: QColor = None
    Radius: float = None

@dataclass
class ZSliderStyleData:
    Track: QColor = None
    TrackBorder: QColor = None
    FillAreaStart: QColor = None
    FillAreaEnd: QColor = None
    FillAreaBorder: QColor = None
    HandleInner: QColor = None
    HandleOuter: QColor = None
    HandleBorder: QColor = None

@dataclass
class ZToolTipStyleData:
    Text: QColor = None
    Body: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZTextBlockStyleData:
    Text: QColor = None
    TextBackSectcted: QColor = None
    Body: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZRichTextBlockStyleData:
    Text: QColor = None
    TextBackSectcted: QColor = None
    Body: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZTextBoxStyleData:
    Text: QColor = None
    TextBackSectcted: QColor = None
    Cursor: QColor = None
    Mask: QColor = None
    Underline: QColor = None
    UnderlineFocused: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyFocused: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZSwitchStyleData:
    Body: QColor = None
    Border: QColor = None
    Handle: QColor = None
    HandleToggled: QColor = None

@dataclass
class ZNavigationBarStyleData:
    Indicator: QColor = None

@dataclass
class ZComboBoxStyleData:
    Text: QColor = None
    Icon: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZComboBoxItemStyleData:
    Text: QColor = None
    Body: QColor = None
    BodyHover: QColor = None
    BodyPressed: QColor = None
    Border: QColor = None
    Radius: float = None

@dataclass
class ZComboBoxItemViewStyleData:
    Body: QColor = None
    Border: QColor = None
    Radius: float = None

StyleDataUnion = Union[
    ZButtonStyleData,
    ZTitleBarButtonStyleData,
    ZFramelessWindowStyleData,
    ZTextBlockStyleData,
    ZToolTipStyleData,
    ZToggleButtonStyleData,
    ZNavBarButtonStyleData,
    ZNavBarToggleButtonStyleData,
    ZScrollPanelStyleData,
    ZSliderStyleData,
    ZTextBoxStyleData,
    ZRichTextBlockStyleData,
    ZPanelStyleData,
    ZSwitchStyleData,
    ZNavigationBarStyleData,
    ZComboBoxStyleData,
    ZComboBoxItemStyleData,
    ZComboBoxItemViewStyleData
    ]

# 定义类型变量，用于StyleData的泛型
StyleDataT = TypeVar('StyleDataT', bound='StyleDataUnion')
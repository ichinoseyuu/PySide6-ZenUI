from dataclasses import dataclass
from PySide6.QtGui import QColor

__all__ = ['ZFramelessWindowStyleData','ZButtonStyleData','ZTitleBarButtonData',
            'ZTextBlockStyleData','ZToolTipStyleData','ZToggleButtonStyleData',
            'ZNavBarButtonStyleData','ZNavBarToggleButtonStyleData','ZPageStyleData',
            'ZScrollPageStyleData']

@dataclass
class ZFramelessWindowStyleData:
    body: QColor

@dataclass
class ZTitleBarButtonData:
    icon: QColor
    iconhover: QColor
    iconpressed: QColor
    body: QColor
    bodyhover: QColor
    bodypressed: QColor

@dataclass
class ZPageStyleData:
    body: QColor
    border: QColor
    radius: int

@dataclass
class ZScrollPageStyleData:
    body: QColor
    border: QColor
    handlebody: QColor
    handleborder: QColor
    radius: int

@dataclass
class ZButtonStyleData:
    text: QColor
    icon: QColor
    body: QColor
    bodyhover: QColor
    bodypressed: QColor
    border: QColor
    radius: int

@dataclass
class ZNavBarButtonStyleData:
    icon: QColor
    body: QColor
    bodyhover: QColor
    bodypressed: QColor
    radius: int

@dataclass
class ZNavBarToggleButtonStyleData:
    icon: QColor
    icontoggled: QColor
    body: QColor
    bodyhover: QColor
    bodypressed: QColor    
    bodytoggled: QColor
    bodytoggledhover: QColor
    bodytoggledpressed: QColor
    radius: int

@dataclass
class ZToggleButtonStyleData:
    text: QColor
    texttoggled: QColor
    icon: QColor
    icontoggled: QColor
    body: QColor
    bodyhover: QColor
    bodypressed: QColor
    bodytoggled: QColor
    bodytoggledhover: QColor
    bodytoggledpressed: QColor
    border: QColor
    bordertoggled: QColor
    radius: int

@dataclass
class ZToolTipStyleData:
    text: QColor
    body: QColor
    border: QColor
    radius: int
    flash: QColor

@dataclass
class ZTextBlockStyleData:
    text: QColor
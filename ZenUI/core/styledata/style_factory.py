from typing import Union, Dict, Any
from PySide6.QtGui import QColor
from .models import (ZButtonStyleData, ZTitleBarButtonData, ZFramelessWindowStyleData,
                    ZTextBlockStyleData, ZToolTipStyleData , ZToggleButtonStyleData,
                    ZNavBarButtonStyleData,ZNavBarToggleButtonStyleData)

StyleDataType = Union[ZButtonStyleData, ZTitleBarButtonData,ZFramelessWindowStyleData,
                      ZTextBlockStyleData,ZToolTipStyleData,ZToggleButtonStyleData,
                      ZNavBarButtonStyleData,ZNavBarToggleButtonStyleData]

class ZStyleDataFactory:
    @staticmethod
    def create(name: str, data: Dict[str, Any]) -> StyleDataType:
        factories = {
            'ZTextBlock': lambda d: ZTextBlockStyleData(
                text=QColor(d.get('text')),
            ),
            'ZButton': lambda d: ZButtonStyleData(
                text=QColor(d.get('text')),
                icon=QColor(d.get('icon')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed')),
                border=QColor(d.get('border')),
                radius=int(d.get('radius'))
            ),
            'ZToggleButton': lambda d: ZToggleButtonStyleData(
                text=QColor(d.get('text')),
                texttoggled=QColor(d.get('texttoggled')),
                icon=QColor(d.get('icon')),
                icontoggled=QColor(d.get('icontoggled')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed')),
                bodytoggled=QColor(d.get('bodytoggled')),
                bodytoggledhover=QColor(d.get('bodytoggledhover')),
                bodytoggledpressed=QColor(d.get('bodytoggledpressed')),
                border=QColor(d.get('border')),
                bordertoggled=QColor(d.get('bordertoggled')),
                radius=int(d.get('radius'))
            ),
            'ZThemeButton': lambda d: ZTitleBarButtonData(
                icon=QColor(d.get('icon')),
                iconhover=QColor(d.get('iconhover')),
                iconpressed=QColor(d.get('iconpressed')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed'))
            ),
            'ZNavBarButton': lambda d: ZNavBarButtonStyleData(
                icon=QColor(d.get('icon')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed')),
                radius=int(d.get('radius'))
            ),
            'ZNavBarToggleButton': lambda d: ZNavBarToggleButtonStyleData(
                icon=QColor(d.get('icon')),
                icontoggled=QColor(d.get('icontoggled')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed')),
                bodytoggled=QColor(d.get('bodytoggled')),
                bodytoggledhover=QColor(d.get('bodytoggledhover')),
                bodytoggledpressed=QColor(d.get('bodytoggledpressed')),
                radius=int(d.get('radius'))
            ),
            'ZMinimizeButton': lambda d: ZTitleBarButtonData(
                icon=QColor(d.get('icon')),
                iconhover=QColor(d.get('iconhover')),
                iconpressed=QColor(d.get('iconpressed')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed'))
            ),
            'ZMaximizeButton': lambda d: ZTitleBarButtonData(
                icon=QColor(d.get('icon')),
                iconhover=QColor(d.get('iconhover')),
                iconpressed=QColor(d.get('iconpressed')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed'))
            ),
            'ZCloseButton': lambda d: ZTitleBarButtonData(
                icon=QColor(d.get('icon')),
                iconhover=QColor(d.get('iconhover')),
                iconpressed=QColor(d.get('iconpressed')),
                body=QColor(d.get('body')),
                bodyhover=QColor(d.get('bodyhover')),
                bodypressed=QColor(d.get('bodypressed'))
            ),
            'ZFramelessWindow': lambda d: ZFramelessWindowStyleData(
                body=QColor(d.get('body')),
            ),
            'ZToolTip': lambda d: ZToolTipStyleData(
                text=QColor(d.get('text')),
                body=QColor(d.get('body')),
                border=QColor(d.get('border')),
                radius=int(d.get('radius')),
                flash=QColor(d.get('flash'))
            )
        }
        return factories[name](data)
from typing import Union, Dict, Any
from .models import (ZButtonStyleData, ZTitleBarButtonData, ZFramelessWindowStyleData,
                    ZTextBlockStyleData,ZToolTipStyleData)

StyleDataType = Union[ZButtonStyleData, ZTitleBarButtonData,ZFramelessWindowStyleData,
                      ZTextBlockStyleData,ZToolTipStyleData]

class ZStyleDataFactory:
    @staticmethod
    def create(name: str, data: Dict[str, Any]) -> StyleDataType:
        factories = {
            'ZTextBlock': lambda d: ZTextBlockStyleData(
                text=d.get('text')
            ),
            'ZButton': lambda d: ZButtonStyleData(
                text=d.get('text'),
                icon=d.get('icon'),
                body=d.get('body'),
                bodyhover=d.get('bodyhover'),
                bodypressed=d.get('bodypressed'),
                border=d.get('border'),
                radius=int(d.get('radius'))
            ),
            'ZMinimizeButton': lambda d: ZTitleBarButtonData(
                icon=d.get('icon'),
                iconhover=d.get('iconhover'),
                iconpressed=d.get('iconpressed'),
                body=d.get('body'),
                bodyhover=d.get('bodyhover'),
                bodypressed=d.get('bodypressed')
            ),
            'ZMaximizeButton': lambda d: ZTitleBarButtonData(
                icon=d.get('icon'),
                iconhover=d.get('iconhover'),
                iconpressed=d.get('iconpressed'),
                body=d.get('body'),
                bodyhover=d.get('bodyhover'),
                bodypressed=d.get('bodypressed')
            ),
            'ZCloseButton': lambda d: ZTitleBarButtonData(
                icon=d.get('icon'),
                iconhover=d.get('iconhover'),
                iconpressed=d.get('iconpressed'),
                body=d.get('body'),
                bodyhover=d.get('bodyhover'),
                bodypressed=d.get('bodypressed')
            ),
            'ZFramelessWindow': lambda d: ZFramelessWindowStyleData(
                body=d.get('body')
            ),
            'ZToolTip': lambda d: ZToolTipStyleData(
                text=d.get('text'),
                body=d.get('body'),
                border=d.get('border'),
                radius=int(d.get('radius')),
                flash=d.get('flash')
            )
        }
        return factories[name](data)
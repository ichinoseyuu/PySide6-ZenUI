from typing import Dict, Any
from types import MappingProxyType
from ..color import ZColorTool
ACCENT_COLOR_LIGHT: str = '#38b9f2'

ACCENT_COLOR_DARK: str = '#955595'

DARK_THEME: Dict[str, Dict[str, Any]] = MappingProxyType({
            'ZTextBlock':{
                'text': '#dcdcdc'
                },
            'ZPage': {
                'body': '#272727',
                'border': '#1d1d1d',
                'radius': 5
                },
            'ZButton': {
                'text': '#dcdcdc',
                'icon': '#dcdcdc',
                'body': '#2d2d2d',
                'bodyhover': '#323232',
                'bodypressed': '#272727',
                'border': '#323232',
                'radius': 5
                },
            'ZToggleButton': {
                'text': '#dcdcdc',
                'texttoggled': '#dcdcdc',
                'icon': '#dcdcdc',
                'icontoggled': '#dcdcdc',
                'body': '#2d2d2d',
                'bodyhover': '#323232',
                'bodypressed': '#272727',
                'bodytoggled': ACCENT_COLOR_DARK,
                'bodytoggledhover': ZColorTool.adjust(ACCENT_COLOR_DARK, 0.05,0.05),
                'bodytoggledpressed': ZColorTool.adjust(ACCENT_COLOR_DARK, 0.1,0.1),
                'border': '#323232',
                'bordertoggled':ACCENT_COLOR_DARK,
                'radius': 5
                },
            'ZNavBarButton': {
                'icon': '#dcdcdc',
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#14ffffff',
                'radius': 5
                },
            'ZNavBarToggleButton': {
                'icon': '#dcdcdc',
                'icontoggled': ACCENT_COLOR_DARK,
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#14ffffff',
                'bodytoggled': '#10ffffff',
                'bodytoggledhover': '#22ffffff',
                'bodytoggledpressed': '#16ffffff',
                'radius': 5
                },
            'ZThemeButton': {
                'icon': '#dcdcdc',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#12ffffff'
                },
            'ZMinimizeButton': {
                'icon': '#dcdcdc',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#12ffffff'
                },
            'ZMaximizeButton': {
                'icon': '#dcdcdc',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#12ffffff'
                },
            'ZCloseButton': {
                'icon': '#dcdcdc',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00e81b23',
                'bodyhover': '#ffe81b23',
                'bodypressed': '#fff1707a'
                },
            'ZFramelessWindow': {
                'body': '#202020'
                },
            'ZToolTip': {
                'text': '#dcdcdc',
                'body': '#2e2e2e',
                'border': '#252525',
                'radius': 5,
                'flash': '#ffffff',
                },
            })


LIGHT_THEME: Dict[str, Dict[str, Any]] = MappingProxyType({
            'ZTextBlock':{
                'text': '#333333'
                },
            'ZPage': {
                'body': '#f9f9f9',
                'border': '#e5e5e5',
                'radius': 5
                },
            'ZButton': {
                'text': '#333333',
                'icon': '#333333',
                'body': '#ffffff',
                'bodyhover': '#f2f2f2',
                'bodypressed': '#ebebeb',
                'border': '#dee2e6',
                'radius': 5
                },
            'ZToggleButton': {
                'text': '#333333',
                'texttoggled': '#333333',
                'icon': '#333333',
                'icontoggled': '#333333',
                'body': '#ffffff',
                'bodyhover': '#f2f2f2',
                'bodypressed': '#ebebeb',
                'bodytoggled': ACCENT_COLOR_LIGHT,
                'bodytoggledhover': ZColorTool.adjust(ACCENT_COLOR_LIGHT, -0.05),
                'bodytoggledpressed': ZColorTool.adjust(ACCENT_COLOR_LIGHT, -0.1),
                'border': '#dee2e6',
                'bordertoggled':ACCENT_COLOR_LIGHT,
                'radius': 5
                },
            'ZNavBarButton': {
                'icon': '#555555',
                'body': '#00000000',
                'bodyhover': "#16000000",
                'bodypressed': '#10000000',
                'radius': 5
                },
            'ZNavBarToggleButton': {
                'icon': '#555555',
                'icontoggled': ACCENT_COLOR_LIGHT,
                'body': '#00000000',
                'bodyhover': '#16000000',
                'bodypressed': '#10000000',
                'bodytoggled': '#0d000000',
                'bodytoggledhover': '#18000000',
                'bodytoggledpressed': '#12000000',
                'radius': 5
                },
            'ZThemeButton': {
                'icon': '#333333',
                'iconhover': '#000000',
                'iconpressed': '#000000',
                'body': '#00000000',
                'bodyhover': '#1a000000',
                'bodypressed': '#12000000'
                },
            'ZMinimizeButton': {
                'icon': '#333333',
                'iconhover': '#000000',
                'iconpressed': '#000000',
                'body': '#00000000',
                'bodyhover': '#1a000000',
                'bodypressed': '#12000000'
                },
            'ZMaximizeButton': {
                'icon': '#333333',
                'iconhover': '#000000',
                'iconpressed': '#000000',
                'body': '#00000000',
                'bodyhover': '#1a000000',
                'bodypressed': '#12000000'
                },
            'ZCloseButton': {
                'icon': '#333333',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00e81b23',
                'bodyhover': '#ffe81b23',
                'bodypressed': '#fff1707a'
                },
            'ZFramelessWindow': {
                'body': '#f3f3f3'
                },
            'ZToolTip': {
                'text': '#333333',
                'body': '#f3f3f3',
                'border': '#dee2e6',
                'radius': 5,
                'flash': '#bfbfbf',
                },
            })


THEME_DATA = {
    'Dark': DARK_THEME,
    'Light': LIGHT_THEME
    }
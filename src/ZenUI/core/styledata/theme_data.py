from typing import Dict, Any
from types import MappingProxyType
from .stylekey import ZStyleDataKey as K
from ..color import ZColorTool

__all__ = ['ACCENT_COLOR_LIGHT', 'ACCENT_COLOR_DARK', 'THEME_DATA', 'DARK_THEME', 'LIGHT_THEME']

ACCENT_COLOR_LIGHT: str = '#38b9f2'

ACCENT_COLOR_DARK: str = '#955595'

DARK_THEME: Dict[str, Dict[str, Any]] = MappingProxyType({
            'ZCard': {
                K.Body: '#202020',
                K.Border: '#1d1d1d',
                K.Radius: 5.0
                },
            'ZTextBox': {
                K.Text: '#dcdcdc',
                K.TextBackSectcted: '#50955595',
                K.Cursor: ZColorTool.adjust(ACCENT_COLOR_DARK, 0.2),
                K.Mask: '#909090',
                K.Underline: '#505050',
                K.UnderlineFocused: ACCENT_COLOR_DARK,
                K.Body: '#2d2d2d',
                K.BodyHover: '#323232',
                K.BodyFocused: '#1f1f1f',
                K.Border: '#323232',
                K.Radius: 5.0
                },
            'ZTextBlock':{
                K.Text: '#dcdcdc',
                K.TextBackSectcted: '#50955595',
                K.Body: '#00000000',
                K.Border: '#00000000',
                K.Radius: 5.0
                },
            'ZRichTextBlock':{
                K.Text: '#dcdcdc',
                K.TextBackSectcted: '#50955595',
                K.Body: '#00000000',
                K.Border: '#00000000',
                K.Radius: 5.0
                },
            'ZPage': {
                K.Body: '#272727',
                K.Border: '#1d1d1d',
                K.Radius: 5.0
                },
            'ZScrollPage': {
                K.Body: '#272727',
                K.Border: '#1d1d1d',
                K.Handle: "#454545",
                K.HandleBorder: '#4d4d4d',
                K.Radius: 5.0
                },
            'ZSlider': {
                K.Track: '#464646',
                K.TrackBorder: '#585858',
                K.FillAreaStart: ACCENT_COLOR_DARK,
                K.FillAreaEnd: ZColorTool.adjust(ACCENT_COLOR_DARK, 0.2),
                K.FillAreaBorder: ACCENT_COLOR_DARK,
                K.HandleInner: ZColorTool.adjust(ACCENT_COLOR_DARK, 0.2),
                K.HandleOuter: '#464646',
                K.HandleBorder: '#505050'
                },
            'ZButton': {
                K.Text: '#dcdcdc',
                K.Icon: '#dcdcdc',
                K.Body: '#2d2d2d',
                K.BodyHover: '#323232',
                K.BodyPressed: '#272727',
                K.Border: '#323232',
                K.Radius: 5.0
                },
            'ZToggleButton': {
                K.Text: '#dcdcdc',
                K.TextToggled: '#dcdcdc',
                K.Icon: '#dcdcdc',
                K.IconToggled: '#dcdcdc',
                K.Body: '#2d2d2d',
                K.BodyHover: '#323232',
                K.BodyPressed: '#272727',
                K.BodyToggled: ACCENT_COLOR_DARK,
                K.BodyToggledHover: ZColorTool.adjust(ACCENT_COLOR_DARK, 0.05,0.05),
                K.BodyToggledPressed: ZColorTool.adjust(ACCENT_COLOR_DARK, 0.1,0.1),
                K.Border: '#323232',
                K.BorderToggled:ACCENT_COLOR_DARK,
                K.Radius: 5.0
                },
            'ZNavBarButton': {
                K.Icon: '#dcdcdc',
                K.Body: '#00ffffff',
                K.BodyHover: '#1affffff',
                K.BodyPressed: '#14ffffff',
                K.Radius: 5.0
                },
            'ZNavBarToggleButton': {
                K.Icon: '#dcdcdc',
                K.IconToggled: ACCENT_COLOR_DARK,
                K.Body: '#00ffffff',
                K.BodyHover: '#1affffff',
                K.BodyPressed: '#14ffffff',
                K.BodyToggled: '#10ffffff',
                K.BodyToggledHover: '#22ffffff',
                K.BodyToggledPressed: '#16ffffff',
                K.Radius: 5.0
                },
            'ZThemeButton': {
                K.Icon: '#dcdcdc',
                K.IconHover: '#ffffff',
                K.IconPressed: '#ffffff',
                K.Body: '#00ffffff',
                K.BodyHover: '#1affffff',
                K.BodyPressed: '#12ffffff'
                },
            'ZMinimizeButton': {
                K.Icon: '#dcdcdc',
                K.IconHover: '#ffffff',
                K.IconPressed: '#ffffff',
                K.Body: '#00ffffff',
                K.BodyHover: '#1affffff',
                K.BodyPressed: '#12ffffff'
                },
            'ZMaximizeButton': {
                K.Icon: '#dcdcdc',
                K.IconHover: '#ffffff',
                K.IconPressed: '#ffffff',
                K.Body: '#00ffffff',
                K.BodyHover: '#1affffff',
                K.BodyPressed: '#12ffffff'
                },
            'ZCloseButton': {
                K.Icon: '#dcdcdc',
                K.IconHover: '#ffffff',
                K.IconPressed: '#ffffff',
                K.Body: '#00e81b23',
                K.BodyHover: '#ffe81b23',
                K.BodyPressed: '#fff1707a'
                },
            'ZFramelessWindow': {
                K.Body: '#202020'
                },
            'ZToolTip': {
                K.Text: '#bfbfbf',
                K.Body: '#2e2e2e',
                K.Border: '#323232',
                K.Radius: 5.0
                },
            })


LIGHT_THEME: Dict[str, Dict[str, Any]] = MappingProxyType({
            'ZCard': {
                K.Body: '#f3f3f3',
                K.Border: '#e5e5e5',
                K.Radius: 5.0
                },
            'ZTextBox': {
                K.Text: '#333333',
                K.TextBackSectcted: '#5038b9f2',
                K.Cursor: ACCENT_COLOR_LIGHT,
                K.Mask: '#808080',
                K.Underline: '#cdcdcd',
                K.UnderlineFocused: ACCENT_COLOR_LIGHT,
                K.Body: '#f9f9f9',
                K.BodyHover: '#f5f5f5',
                K.BodyFocused: '#ffffff',
                K.Border: '#dee2e6',
                K.Radius: 3.0
                },
            'ZTextBlock':{
                K.Text: '#333333',
                K.TextBackSectcted: '#5038b9f2',
                K.Body: '#00ffffff',
                K.Border: '#00ffffff',
                K.Radius: 5.0
                },
            'ZRichTextBlock':{
                K.Text: '#333333',
                K.TextBackSectcted: '#5038b9f2',
                K.Body: '#00ffffff',
                K.Border: '#00ffffff',
                K.Radius: 5.0
                },
            'ZPage': {
                K.Body: '#ffffff',
                K.Border: '#e5e5e5',
                K.Radius: 5.0
                },
            'ZScrollPage': {
                K.Body: '#f9f9f9',
                K.Border: '#e5e5e5',
                K.Handle: "#cfcfcf",
                K.HandleBorder: '#cdcdcd',
                K.Radius: 5.0
                },
            'ZSlider': {
                K.Track: '#e5e5e5',
                K.TrackBorder: '#d8d8d8',
                K.FillAreaStart: ACCENT_COLOR_LIGHT,
                K.FillAreaEnd: ZColorTool.adjust(ACCENT_COLOR_LIGHT, 0.2),
                K.FillAreaBorder: ACCENT_COLOR_LIGHT,
                K.HandleInner: ZColorTool.adjust(ACCENT_COLOR_LIGHT, 0.2),
                K.HandleOuter: '#ffffff',
                K.HandleBorder: '#e6e6e6'
                },
            'ZButton': {
                K.Text: '#333333',
                K.Icon: '#333333',
                K.Body: '#ffffff',
                K.BodyHover: '#f2f2f2',
                K.BodyPressed: '#ebebeb',
                K.Border: '#dee2e6',
                K.Radius: 5.0
                },
            'ZToggleButton': {
                K.Text: '#333333',
                K.TextToggled: '#333333',
                K.Icon: '#333333',
                K.IconToggled: '#333333',
                K.Body: '#ffffff',
                K.BodyHover: '#f2f2f2',
                K.BodyPressed: '#ebebeb',
                K.BodyToggled: ZColorTool.adjust(ACCENT_COLOR_LIGHT, 0.05,0.05),
                K.BodyToggledHover: ACCENT_COLOR_LIGHT,
                K.BodyToggledPressed: ZColorTool.adjust(ACCENT_COLOR_LIGHT, -0.1),
                K.Border: '#dee2e6',
                K.BorderToggled: '#00dee2e6',
                K.Radius: 5.0
                },
            'ZNavBarButton': {
                K.Icon: '#555555',
                K.Body: '#00000000',
                K.BodyHover: "#16000000",
                K.BodyPressed: '#10000000',
                K.Radius: 5.0
                },
            'ZNavBarToggleButton': {
                K.Icon: '#555555',
                K.IconToggled: ACCENT_COLOR_LIGHT,
                K.Body: '#00000000',
                K.BodyHover: '#16000000',
                K.BodyPressed: '#10000000',
                K.BodyToggled: '#0d000000',
                K.BodyToggledHover: '#18000000',
                K.BodyToggledPressed: '#12000000',
                K.Radius: 5.0
                },
            'ZThemeButton': {
                K.Icon: '#333333',
                K.IconHover: '#000000',
                K.IconPressed: '#000000',
                K.Body: '#00000000',
                K.BodyHover: '#1a000000',
                K.BodyPressed: '#12000000'
                },
            'ZMinimizeButton': {
                K.Icon: '#333333',
                K.IconHover: '#000000',
                K.IconPressed: '#000000',
                K.Body: '#00000000',
                K.BodyHover: '#1a000000',
                K.BodyPressed: '#12000000'
                },
            'ZMaximizeButton': {
                K.Icon: '#333333',
                K.IconHover: '#000000',
                K.IconPressed: '#000000',
                K.Body: '#00000000',
                K.BodyHover: '#1a000000',
                K.BodyPressed: '#12000000'
                },
            'ZCloseButton': {
                K.Icon: '#333333',
                K.IconHover: '#ffffff',
                K.IconPressed: '#ffffff',
                K.Body: '#00e81b23',
                K.BodyHover: '#ffe81b23',
                K.BodyPressed: '#fff1707a'
                },
            'ZFramelessWindow': {
                K.Body: '#f3f3f3'
                },
            'ZToolTip': {
                K.Text: '#555555',
                K.Body: '#f9f9f9',
                K.Border: '#dee2e6',
                K.Radius: 5.0
                },
            })


THEME_DATA = {
    'Dark': DARK_THEME,
    'Light': LIGHT_THEME
    }
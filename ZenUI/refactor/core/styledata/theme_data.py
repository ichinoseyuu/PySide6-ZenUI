from typing import Dict, Any
from types import MappingProxyType
DARK_THEME: Dict[str, Dict[str, Any]] = MappingProxyType({
            'ZTextBlock':{
                'text': '#dcdcdc'
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
            'ZMinimizeButton': {
                'icon': '#dcdcdc',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#33ffffff'
                },
            'ZMaximizeButton': {
                'icon': '#dcdcdc',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00ffffff',
                'bodyhover': '#1affffff',
                'bodypressed': '#33ffffff'
                },
            'ZCloseButton': {
                'icon': '#f0f0f0',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00e81b23',
                'bodyhover': '#ffe81b23',
                'bodypressed': '#fff1707a'
                },
            'ZFramelessWindow': {
                'body': '#202020'
                },
            })


LIGHT_THEME: Dict[str, Dict[str, Any]] = MappingProxyType({
            'ZTextBlock':{
                'text': '#333333'
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
            'ZMinimizeButton': {
                'icon': '#333333',
                'iconhover': '#000000',
                'iconpressed': '#000000',
                'body': '#00000000',
                'bodyhover': '#1a000000',
                'bodypressed': '#33000000'
                },
            'ZMaximizeButton': {
                'icon': '#333333',
                'iconhover': '#000000',
                'iconpressed': '#000000',
                'body': '#00000000',
                'bodyhover': '#1a000000',
                'bodypressed': '#33000000'
                },
            'ZCloseButton': {
                'icon': '#202020',
                'iconhover': '#ffffff',
                'iconpressed': '#ffffff',
                'body': '#00e81b23',
                'bodyhover': '#ffe81b23',
                'bodypressed': '#fff1707a'
                },
            'ZFramelessWindow': {
                'body': '#f3f3f3'
                },
            })

THEME_DATA = {
    'Dark': DARK_THEME,
    'Light': LIGHT_THEME
    }
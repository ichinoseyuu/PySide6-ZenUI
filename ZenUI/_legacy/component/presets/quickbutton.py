from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import overload
from ZenUI._legacy.component.button import ZPushButton
from ZenUI._legacy.component.button import ZToggleButton
from ZenUI._legacy.core import ZSize

class ZQuickButton:
    '快捷预设'
    # region 导航栏按钮
    @staticmethod
    def navbarButton(parent,
                         name: str,
                         text: str = None,
                         icon: QIcon = None,
                         icon_size: ZSize = None,
                         min_height: int = 36,
                         radius = 4,
                         padding = 12):
        '''
        导航栏按钮
        - 文字、图标居左
        - 无背景
        - 悬停时背景变色,
        - 按下时背景变色，
        '''
        return ZPushButton(parent=parent,
                             name=name,
                             text=text,
                             icon=icon,
                             icon_size=icon_size,
                             min_height=min_height,
                             fixed_stylesheet=f'border-radius: {radius}px;\ntext-align: left;\npadding-left: {padding}px;',
                             hover_stylesheet=f'border-radius: {radius}px;',
                             pressed_stylesheet=f'border-radius: {radius}px;',
                             idle_style=ZPushButton.IdleStyle.None_,
                             hover_style=ZPushButton.HoverStyle.Color,
                             pressed_style=ZPushButton.PressedStyle.Color)
    # region 填充按钮
    @staticmethod
    def fillButton(parent,
                     name: str,
                     text: str = None,
                     icon: QIcon = None,
                     icon_size: ZSize = None,
                     min_size: ZSize = None,
                     max_size: ZSize = None,
                     fixed_size: ZSize = None,
                     tooltip: str = None,
                     radius=4):
        '''
        渐变按钮
        - 纯色背景
        - 悬停时高亮
        - 按下时高亮
        '''
        sheet = f'border-radius: {radius}px;'
        return ZPushButton(parent=parent,
                             name=name,
                             text=text,
                             icon=icon,
                             icon_size=icon_size,
                             min_size=min_size,
                             max_size=max_size,
                             tooltip=tooltip,
                             fixed_size=fixed_size,
                             fixed_stylesheet=sheet,
                             hover_stylesheet=sheet,
                             pressed_stylesheet=sheet,
                             idle_style=ZPushButton.IdleStyle.Monochrome,
                             hover_style=ZPushButton.HoverStyle.Color,
                             pressed_style=ZPushButton.PressedStyle.Color)

    # region 渐变按钮
    @staticmethod
    def gradientButton(parent,
                     name: str,
                     text: str = None,
                     icon: QIcon = None,
                     icon_size: ZSize = None,
                     min_size: ZSize = None,
                     max_size: ZSize = None,
                     fixed_size: ZSize = None,
                     tooltip: str = None,
                     radius=4):
        '''
        渐变按钮
        - 背景渐变
        - 悬停时高亮
        - 按下时高亮
        '''
        sheet = f'border-radius: {radius}px;'
        return ZPushButton(parent=parent,
                             name=name,
                             text=text,
                             icon=icon,
                             icon_size=icon_size,
                             min_size=min_size,
                             max_size=max_size,
                             tooltip=tooltip,
                             fixed_size=fixed_size,
                             fixed_stylesheet=sheet,
                             hover_stylesheet=sheet,
                             pressed_stylesheet=sheet,
                             idle_style=ZPushButton.IdleStyle.Gradient,
                             hover_style=ZPushButton.HoverStyle.Color,
                             pressed_style=ZPushButton.PressedStyle.Color)


    # region 透明按钮
    @staticmethod
    def transButton(parent,
                     name: str,
                     text: str = None,
                     icon: QIcon = None,
                     icon_size: ZSize = None,
                     min_size: ZSize = None,
                     max_size: ZSize = None,
                     fixed_size: ZSize = None,
                     tooltip: str = None,
                     radius=4):
        '''
        透明按钮
        - 背景透明无边框
        - 悬停时高亮
        - 按下时高亮
        '''
        sheet = f'border-radius: {radius}px;'
        return ZPushButton(parent=parent,
                             name=name,
                             text=text,
                             icon=icon,
                             icon_size=icon_size,
                             min_size=min_size,
                             max_size=max_size,
                             tooltip=tooltip,
                             fixed_size=fixed_size,
                             fixed_stylesheet=sheet,
                             hover_stylesheet=sheet,
                             pressed_stylesheet=sheet,
                             idle_style=ZPushButton.IdleStyle.None_,
                             hover_style=ZPushButton.HoverStyle.Color,
                             pressed_style=ZPushButton.PressedStyle.Color)


    # region 文本按钮
    @staticmethod
    def textButton(parent,
                     name: str,
                     text: str = None,
                     min_size: ZSize = None,
                     max_size: ZSize = None,
                     fixed_size: ZSize = None,
                     tooltip: str = None,
                     radius=4):
        '''
        文本按钮
        - 无背景
        - 悬停时文字变色
        - 按下时文字变色
        '''
        sheet = f'border-radius: {radius}px;'
        return ZPushButton(parent=parent,
                             name=name,
                             text=text,
                             min_size=min_size,
                             max_size=max_size,
                             tooltip=tooltip,
                             fixed_size=fixed_size,
                             fixed_stylesheet=sheet,
                             hover_stylesheet=sheet,
                             pressed_stylesheet=sheet,
                             idle_style=ZPushButton.IdleStyle.None_,
                             hover_style=ZPushButton.HoverStyle.Text,
                             pressed_style=ZPushButton.PressedStyle.Text)


    # region 图标按钮
    @staticmethod
    def iconButton(parent,
                     name: str,
                     icon: QIcon = None,
                     icon_size: ZSize = None,
                     min_size: ZSize = None,
                     max_size: ZSize = None,
                     fixed_size: ZSize = None,
                     tooltip: str = None,
                     radius=4):
        '''
        图标按钮
        - 无背景
        - 悬停时图标变色
        - 按下时图标变色
        '''
        sheet = f'border-radius: {radius}px;'
        return ZPushButton(parent=parent,
                             name=name,
                             icon=icon,
                             icon_size=icon_size,
                             min_size=min_size,
                             max_size=max_size,
                             tooltip=tooltip,
                             fixed_size=fixed_size,
                             fixed_stylesheet=sheet,
                             hover_stylesheet=sheet,
                             pressed_stylesheet=sheet,
                             idle_style=ZPushButton.IdleStyle.None_,
                             hover_style=ZPushButton.HoverStyle.Icon,
                             pressed_style=ZPushButton.PressedStyle.Icon)


    # region 导航栏切换按钮
    @staticmethod
    def navbarToggleButton(parent,
                         name: str,
                         text: str,
                         icon: QIcon,
                         icon_size: ZSize,
                         min_height: int,
                         radius=4,
                         padding=12):
        '''
        导航栏切换按钮
        - 文字、图标居左、有指示条
        - 无背景
        - 悬停时背景变色,
        - 按下时无变化，
        - 选中状态时文字、图标变色、背景变色
        '''
        return ZToggleButton(parent=parent,
                             name=name,
                             text=text,
                             icon=icon,
                             icon_size=icon_size,
                             min_height=min_height,
                             fixed_stylesheet=f'border-radius: {radius}px;\ntext-align: left;\npadding-left: {padding}px;',
                             hover_stylesheet=f'border-radius: {radius}px;',
                             pressed_stylesheet=f'border-radius: {radius}px;',
                             indicator_stylesheet=f'border-radius: 2px;',
                             indicator_pos=ZToggleButton.IndicatorPos.Left,
                             indicator_width=4,
                             indicator_margin=2,
                             indicator_padding=12,
                             checked_style=ZToggleButton.CheckedStyle.Icon|ZToggleButton.CheckedStyle.Text,
                             hover_style=ZToggleButton.HoverStyle.Color,
                             pressed_style=ZToggleButton.PressedStyle.None_,
                             indicator=ZToggleButton.Indicator.Enabled)

    # region 切换按钮
    @staticmethod
    def toggleButton(parent,
                     name: str,
                     text: str = None,
                     icon: QIcon = None,
                     icon_size: ZSize = None,
                     min_size: ZSize = None,
                     max_size: ZSize = None,
                     fixed_size: ZSize = None,
                     tooltip: str = None,
                     radius=4):
        '''
        切换按钮
        - 无指示条
        - 无背景
        - 悬停时背景变色,
        - 按下时背景变色,
        - 选中状态时文字、图标变色
        '''
        sheet = f'border-radius: {radius}px;'
        return ZToggleButton(parent=parent,
                             name=name,
                             text=text,
                             icon=icon,
                             icon_size=icon_size,
                             min_size=min_size,
                             max_size=max_size,
                             tooltip=tooltip,
                             fixed_size=fixed_size,
                             fixed_stylesheet=sheet,
                             hover_stylesheet=sheet,
                             pressed_stylesheet=sheet,
                             checked_style=ZToggleButton.CheckedStyle.Icon|ZToggleButton.CheckedStyle.Text,
                             hover_style=ZToggleButton.HoverStyle.Color,
                             pressed_style=ZToggleButton.PressedStyle.Color,
                             indicator=ZToggleButton.Indicator.Disabled)
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import IntFlag
from textwrap import dedent
from ZenUI._legacy.component.basewidget.widget import ZWidget
from ZenUI._legacy.component.layout.column import ZColumnLayout
from ZenUI._legacy.component.layout.row import ZRowLayout
from ZenUI._legacy.core import Zen,ZColorTool,ZMargins

class WindowPanel(ZWidget):
    '''窗口面板'''
    class Style(IntFlag):
        '''背景样式'''
        Monochrome = 1 << 0
        '纯色'
        Gradient = 1 << 1
        '渐变'
        Border = 1 << 2
        '边框'

    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 fixed_stylesheet: str = None,
                 style: Style = Style.Monochrome,
                 layout: Zen.Layout = Zen.Layout.Column,
                 margins: ZMargins = ZMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Zen.Alignment = None):
        super().__init__(parent, name)
        if fixed_stylesheet: self.setFixedStyleSheet(fixed_stylesheet)
        self._style = style
        if layout == Zen.Layout.Row:
            self.setLayout(ZRowLayout(parent=self, margins=margins, spacing=spacing, alignment=alignment))
        if layout == Zen.Layout.Column:
            self.setLayout(ZColumnLayout(parent=self, margins=margins, spacing=spacing, alignment=alignment))
        self._init_style()
        self.updateStyle()


    def _init_style(self):
        bg_style = self._style & (self.Style.Monochrome| self.Style.Gradient)
        if bin(bg_style).count('1') > 1:
            raise ValueError("Monochrome and Gradient are mutually exclusive")

        if self._style & self.Style.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)

        self._color_sheet.loadColorConfig(Zen.WidgetType.Window)
        self._colors.overwrite(self._color_sheet.getSheet())
        self._bg_color_a = self._colors.background_a
        self._bg_color_b = self._colors.background_b
        self._border_color = self._colors.border
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        if not self.objectName(): raise ValueError("Widget must have a name")

        sheet = [f'#{self.objectName()}{{']

        if self._stylesheet_fixed: sheet.append(self._stylesheet_fixed)

        if self._style & self.Style.Monochrome:
            sheet.append(f"background-color: {self._bg_color_a};")

        if self._style & self.Style.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet.append(dedent(f"""\
                background-color: qlineargradient(
                x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
                stop:0 {self._bg_color_a}, stop:1 {self._bg_color_b});"""))

        if self._style & self.Style.Border:
            sheet.append(f"border-color: {self._border_color};}}")
        else:
            sheet.append("border: none;}")

        self._stylesheet_cache = '\n'.join(sheet)
        self._stylesheet_dirty = False
        return self._stylesheet_cache


    def _theme_changed_handler(self, theme):
        self._colors.overwrite(self._color_sheet.getSheet(theme))

        if self._style & self.Style.Monochrome:
            self.setColor(self._colors.background_a)

        if self._style & self.Style.Gradient:
            self.setColor(self._colors.background_a,self._colors.background_b)

        if self._style & self.Style.Border:
            self.setBorderColor(self._colors.border)
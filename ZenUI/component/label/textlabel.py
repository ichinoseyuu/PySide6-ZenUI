from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.label.abclabel import ABCLabel
from ZenUI.core import Zen,ColorSheet,ColorTool
class ZenTextLabel(ABCLabel):
    """ZenUI文本标签"""
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 word_wrap: bool = False,
                 alignment: Zen.Alignment = Zen.Alignment.Center
                 ):
        super().__init__(parent = parent,
                         name=name,
                         text=text,
                         word_wrap=word_wrap,
                         alignment=alignment)
        self._color_sheet = ColorSheet(Zen.WidgetType.TextLabel) # 颜色表
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_text_color.setCurrent(ColorTool.toArray(self._text_color))
        self._fixed_stylesheet = 'background-color: transparent;'
        self._schedule_update()

    # region Override
    def reloadStyleSheet(self):
        sheet = f'color: {self._text_color};'
        if self._fixed_stylesheet:
            return sheet +'\n'+self._fixed_stylesheet
        else:
            return sheet

    def _theme_changed_handler(self, theme):
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))


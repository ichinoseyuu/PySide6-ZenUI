from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Property,Qt
from PySide6.QtGui import QCursor
from ..widget.zenwidget import ZenWidget
from ..label.abstract_label import ABCLabel
from ....core import ZenExpAnim, Zen, ZenGlobal,ZenColor,ColorGroup
class HoverLayer(ZenWidget):
    def __init__(self, parent: QWidget | None= None):
        super().__init__(parent)
        self._fixed_stylesheet = "border-radius: 4px;\nborder: 1px solid transparent;"
        self._schedule_update()

    def reloadStyleSheet(self):
        sheet = f'background-color: {self._bg_color_a};'
        if self._fixed_stylesheet:
            return self._fixed_stylesheet +'\n'+ sheet
        else:
            return sheet


class BodyLayer(ZenWidget):
    def __init__(self, parent: QWidget | None= None):
        super().__init__(parent)
        self._bg_color_a = ZenGlobal.ui.color_group.fromToken(Zen.ColorRole.Button_BG_A)
        self._bg_color_b = ZenGlobal.ui.color_group.fromToken(Zen.ColorRole.Button_BG_B)
        self._anim_bg_color_a.setCurrent(ZenColor.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZenColor.toArray(self._bg_color_b))
        self.setFixedStyleSheet("border-radius: 4px;\nborder: 1px solid transparent;")
        self._schedule_update()

    # region StyleSheet
    def reloadStyleSheet(self):
        if self.isWidgetFlagOn(Zen.WidgetFlag.GradientColor):
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = f'background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});'
        else:
            sheet = f'background-color: {self._bg_color_a};'
        if self._fixed_stylesheet:
            return self._fixed_stylesheet +'\n'+ sheet
        else:
            return sheet


    # region Slot
    def _theme_changed_handler(self, color_group: ColorGroup):
        self.setColorTo(color_group.fromToken(Zen.ColorRole.Button_BG_A), color_group.fromToken(Zen.ColorRole.Button_BG_B))

class TextLayer(ABCLabel):
    def __init__(self, parent: QWidget | None= None):
        super().__init__(parent)
        self._schedule_update()

    # region StyleSheet
    def reloadStyleSheet(self):
        if self._fixed_stylesheet:
            return self._fixed_stylesheet +'\n'+ f'color: {self._text_color};'
        else:
            return f'color: {self._text_color};'

    # region Slot
    def _theme_changed_handler(self, color_group: ColorGroup):
        self.setTextColorTo(color_group.fromToken(Zen.ColorRole.Button_Text))

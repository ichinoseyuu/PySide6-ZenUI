from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.button.abcbutton import ABCButton
from ZenUI.core import Zen, ColorTool, ColorSheet
class ZenPushButton(ABCButton):
    def __init__(self, parent=None, name=None, text=None, icon=None):
        super().__init__(parent, name, text, icon)
        self._color_sheet = ColorSheet(Zen.WidgetType.PushButton) 
        self._fixed_stylesheet = 'border: 1px solid transparent;\nborder-radius: 2px;'
        self.flashLayer()._fixed_stylesheet = self._fixed_stylesheet
        self.hoverLayer()._fixed_stylesheet = self._fixed_stylesheet
        self.setWidgetFlag(Zen.WidgetFlag.GradientColor)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_bg_color_a.setCurrent(ColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ColorTool.toArray(self._bg_color_b))
        self._anim_text_color.setCurrent(ColorTool.toArray(self._text_color))
        self._schedule_update()

    # region StyleSheet
    def reloadStyleSheet(self):
        if self.isWidgetFlagOn(Zen.WidgetFlag.GradientColor):
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = f'color: {self._text_color};\nbackground-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});'
        else:
            sheet = f'color: {self._text_color};\nbackground-color: {self._bg_color_a};'
        is_apply_to_children = self.isWidgetFlagOn(Zen.WidgetFlag.StyleSheetApplyToChildren)
        if is_apply_to_children:
            if self._fixed_stylesheet:
                return self._fixed_stylesheet +'\n'+ sheet
            else:
                return sheet
        else:
            if not self.objectName(): raise ValueError("Widget must have a name when StyleSheetApplyToChildren is False")
            if self._fixed_stylesheet:
                return f"#{self.objectName()}"+"{\n"+  sheet +'\n'+self._fixed_stylesheet +"\n}"
            else:
                return f"#{self.objectName()}"+"{\n"+ sheet +"\n}"

    # region Slot
    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Background_A), self._color_sheet.getColor(theme, Zen.ColorRole.Background_B))
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.button.abcbutton import ABCButton
from ZenUI.core import Zen, ColorTool,ColorSheet
class ZenTransButton(ABCButton):
    """ZenUI透明按钮"""
    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ColorSheet(Zen.WidgetType.TansButton) 
        self.setFixedStyleSheet('border-radius: 5px;\nborder: 1px solid transparent;')
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_text_color.setCurrent(ColorTool.toArray(self._text_color))
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)
        self._anim_icon_color.setCurrent(ColorTool.toArray(self._icon_color))


    def reloadStyleSheet(self):
        is_apply_to_children = self.isWidgetFlagOn(Zen.WidgetFlag.StyleSheetApplyToChildren)
        if is_apply_to_children:
            return self._fixed_stylesheet +'\n'+ f'color: {self._text_color};\nbackground-color: transparent;'
        else:
            if not self.objectName(): raise ValueError("Widget must have a name when StyleSheetApplyToChildren is False")
            return f"#{self.objectName()}"+"{\n"+ f'color: {self._text_color};\nbackground-color: transparent;' +'\n'+self._fixed_stylesheet +"\n}"


    def _theme_changed_handler(self, theme):
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Icon))






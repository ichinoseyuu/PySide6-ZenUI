from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.button.abctabbutton import ABCTabButton,ButtonLayer
from ZenUI.core import Zen, ColorTool,ColorSheet
class ZenTabButton(ABCTabButton):
    """标签按钮"""
    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ColorSheet(self, Zen.WidgetType.TabButton)
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_text_color.setCurrent(ColorTool.toArray(self._text_color))
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)
        self._anim_icon_color.setCurrent(ColorTool.toArray(self._icon_color))
        self._tab_layer._fixed_stylesheet = 'border-radius: 3px;\nborder: 1px solid transparent;'
        if self._tab_pos == Zen.Position.Left:
            self._fixed_stylesheet = f'text-align: left;\npadding-left: {self._tab_width+2*self._tab_offset}px;\nborder-radius: 4px;\nborder: 1px solid transparent;'
            return
        if self._tab_pos == Zen.Position.Right:
            self._fixed_stylesheet = f'text-align: right;\npadding-right: {self._tab_width+2*self._tab_offset}px;\nborder-radius: 4px;\nborder: 1px solid transparent;'
            return
        if self._tab_pos == Zen.Position.Top:
            self._fixed_stylesheet = f'padding-top: {self._tab_width+self._tab_offset}px;\nborder-radius: 4px;\nborder: 1px solid transparent;'
            return
        self._fixed_stylesheet = f'padding-bottom: {self._tab_width+self._tab_offset}px;\nborder-radius: 4px;\nborder: 1px solid transparent;'


    def reloadStyleSheet(self):
        return self._fixed_stylesheet +'\n'+ f'color: {self._text_color};\nbackground-color: transparent;'


    def _theme_changed_handler(self, theme):
        if self.isChecked():
            self._tab_layer.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected))
            self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected))
            self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected))
            return
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Icon))

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     size = event.size()
    #     #self._tab_layer.resize(6, 2*size.height()/3)
    #     #self._tab_layer.setMoveAnchor((size.width()-4)/2, self._tab_layer.height()/2)
    #     #self._tab_layer.move(size.width()/2, size.height()/2)
    #     if self._tab_pos == Zen.Position.Left:
    #         self._tab_layer.setGeometry(4, size.height()/6, 6, 2*size.height()/3)

    def _toggled_handler(self, is_checked):
        if is_checked:
            self._tab_layer.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected))
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected))
            return
        self._tab_layer.setColorTo(ColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Selected)))
        self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))
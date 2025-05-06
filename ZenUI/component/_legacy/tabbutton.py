from ZenUI.component.button.abstract_tab_button import ABCTabButton
from ZenUI.core import Zen, ZColorTool,ZColorSheet
class ZTabButton(ABCTabButton):
    """标签按钮"""
    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.TabButton)
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))
        self._layer_tab._fixed_stylesheet = 'border-radius: 2px;\nborder: 1px solid transparent;'
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
            self._layer_tab.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A))
            self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A))
            self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A))
            return
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Icon))

    def _toggled_handler(self, is_checked):
        if is_checked:
            self._layer_tab.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected_A))
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected_A))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected_A))
            return
        self._layer_tab.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Selected_A)))
        self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

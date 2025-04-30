from ZenUI.component.button.abcbutton import ABCButton
from ZenUI.core import Zen, ZColorTool,ZColorSheet
class ZTransButton(ABCButton):
    """透明按钮"""
    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.TansButton)
        self._fixed_stylesheet = 'border: 1px solid transparent;\nborder-radius: 2px;'
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))


    def reloadStyleSheet(self):
        # if self._fixed_stylesheet:
        #     return self._fixed_stylesheet +'\n'+ f'color: {self._text_color};\nbackground-color: transparent;'
        # return f'color: {self._text_color};\nbackground-color: transparent;'
        return self._fixed_stylesheet +'\n'+ f'color: {self._text_color};\nbackground-color: transparent;'


    def _theme_changed_handler(self, theme):
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Icon))






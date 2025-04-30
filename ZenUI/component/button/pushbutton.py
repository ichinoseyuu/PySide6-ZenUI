from ZenUI.component.button.abcbutton import ABCButton
from ZenUI.core import Zen, ZColorTool, ZColorSheet
class ZPushButton(ABCButton):
    '''触发按钮'''
    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.PushButton)
        self._fixed_stylesheet = 'border: 1px solid transparent;\nborder-radius: 2px;'
        self.setWidgetFlag(Zen.WidgetFlag.GradientColor)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))

    def reloadStyleSheet(self):
        if self.isWidgetFlagOn(Zen.WidgetFlag.GradientColor):
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = f'color: {self._text_color};\nbackground-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});'
        else:
            sheet = f'color: {self._text_color};\nbackground-color: {self._bg_color_a};'
        if self._fixed_stylesheet:
            return self._fixed_stylesheet +'\n'+ sheet
        return sheet


    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Background_A), self._color_sheet.getColor(theme, Zen.ColorRole.Background_B))
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))

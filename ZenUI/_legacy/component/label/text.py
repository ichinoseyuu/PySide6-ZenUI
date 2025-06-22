from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.component.label.abclabel import ABCLabel
from ZenUI._legacy.core import Zen,ZColorSheet, ZColorTool
class ZTextLabel(ABCLabel):
    """文本标签"""
    def __init__(self,
                 parent: ZWidget = None,
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

    # region Override
    def _init_style(self):
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.TextLabel) # 颜色表
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))

    def reloadStyleSheet(self):
        sheet = f'color: {self._text_color};\nbackground-color: transparent;'
        if self._fixed_stylesheet:
            return sheet +'\n'+self._fixed_stylesheet
        else:
            return sheet

    def _theme_changed_handler(self, theme):
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))


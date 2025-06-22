from textwrap import dedent
from ZenUI._legacy.component.basewidget import ZLayer
class ScrollBarLayer(ZLayer):
    '滚动条颜色层'
    def __init__(self, parent = None):
        super().__init__(parent)
        self._init_style()
        self.updateStyle()

    def _init_style(self):
        self._anim_bg_color_a.setBias(0.1)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        #判断背景层样式
        sheet = dedent(f'''\
            background-color: {self._bg_color_a};
            border: none;''')
        return self._stylesheet_fixed +'\n'+ sheet
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.label.abstract_label import ABCLabel
from ZenUI.core import Zen,ZColorSheet,ZColorTool
from PySide6.QtSvgWidgets import QSvgWidget

class Layer(ZWidget):
    """按钮层级"""
    def _init_style(self):
        self._anim_bg_color_a.setBias(0.1)

    def reloadStyleSheet(self):
        if self._fixed_stylesheet:
            return self._fixed_stylesheet +'\n'+ f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'
        else:
            return f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'


class Text(ABCLabel):
    """文本层"""
    def __init__(self,
                 parent: ZWidget = None,
                 text: str = None,
                 alignment: Zen.Alignment = Zen.Alignment.Center):
        super().__init__(parent = parent,
                         text=text,
                         alignment=alignment)

    # region Override
    def reloadStyleSheet(self):
        return f'background-color: transparent;\ncolor: {self._text_color};'
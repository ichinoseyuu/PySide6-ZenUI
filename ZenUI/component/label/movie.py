from PySide6.QtGui import QMovie
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.label.abclabel import ABCLabel
from ZenUI.core import Zen

class ZMovieLabel(ABCLabel):
    """文本标签"""
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 movie: QMovie = None,
                 alignment: Zen.Alignment = Zen.Alignment.Center):
        super().__init__(parent = parent,
                         name=name,
                         movie=movie,
                         alignment=alignment)

    # region Override
    def reloadStyleSheet(self):
        return 'background-color: transparent;'

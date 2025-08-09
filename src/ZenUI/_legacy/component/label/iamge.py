from PySide6.QtGui import QPixmap,QImage
from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.component.label.abclabel import ABCLabel
from ZenUI._legacy.core import Zen

class ZImageLabel(ABCLabel):
    """文本标签"""
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 image: QPixmap|QImage = None,
                 alignment: Zen.Alignment = Zen.Alignment.Center):
        super().__init__(parent = parent,
                         name=name,
                         image=image,
                         alignment=alignment)

    # region Override

    def reloadStyleSheet(self):
        return 'background-color: transparent;'

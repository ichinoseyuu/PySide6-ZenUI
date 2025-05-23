from ZenUI.component.label.abstract_label import ABCLabel
from ZenUI.component.widget.widget import ZWidget
from ZenUI.core import Zen
from PySide6.QtGui import QPixmap,QImage
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

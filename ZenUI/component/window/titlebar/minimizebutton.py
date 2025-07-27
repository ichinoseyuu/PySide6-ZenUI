from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton


class ZMinimizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

    def paintEvent(self, e):
        painter = QPainter(self)
        # draw background
        painter.setBrush(self._body_color_mgr.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._icon_color_mgr.color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)

from PySide6.QtCore import Qt, QLineF
from PySide6.QtGui import QPainter, QPen
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton

class ZCloseButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(self._background_style.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))
        r = self.devicePixelRatioF()

        pen = QPen(self._icon_style.color, 1.2 * 1/r)  # 增加线宽
        pen.setCapStyle(Qt.RoundCap)  # 设置线段端点为圆形
        pen.setJoinStyle(Qt.RoundJoin)  # 设置线段连接处为圆形
        pen.setCosmetic(True)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        w, h = self.width(), self.height()
        iw = ih = 10
        x = w/2 - iw/2
        y = h/2 - ih/2
        lines = [
            QLineF(x, y, x + iw, y + ih),        # 左上到右下
            QLineF(x + iw, y, x, y + ih)         # 右上到左下
        ]
        painter.drawLines(lines)
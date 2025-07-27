from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QPainterPath
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton

class ZMaximizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

    def setMaxState(self, isMax):
        if self._isMax == isMax: return
        self._isMax = isMax
        self.update()

    def toggleMaxState(self):
        self._isMax = not self._isMax
        self.update()

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

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self._isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)

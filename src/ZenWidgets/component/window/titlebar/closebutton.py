from PySide6.QtCore import Qt,QLineF
from PySide6.QtGui import QPainter, QPen,QColor
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton
from ZenWidgets.core import ZDebug

class ZCloseButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_style_()

    def _init_style_(self):
        super()._init_style_()
        self._layerColorCtrl.color = QColor('#00E81B23')

    def hoverHandler(self):
        self._layerColorCtrl.setAlphaFTo(1.0)

    def leaveHandler(self):
        self._layerColorCtrl.toTransparent()

    def pressHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.6)

    def releaseHandler(self):
        self._layerColorCtrl.setAlphaFTo(1.0)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(self._layerColorCtrl.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))
        r =self.devicePixelRatioF()
        pen = QPen(self._iconColorCtrl.color, 1.2 * 1/r)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        w, h = self.width(), self.height()
        iw = ih = 10
        x = w/2 - iw/2
        y = h/2 - ih/2
        lines = [
            QLineF(x, y, x + iw, y + ih),
            QLineF(x + iw, y, x, y + ih)
        ]
        painter.drawLines(lines)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        e.accept()
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter,QPen
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton
from ZenWidgets.core import ZDebug

class ZMinimizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_style_()

    def hoverHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.2)

    def leaveHandler(self):
        self._layerColorCtrl.toTransparent()

    def pressHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.4)

    def releaseHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.2)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(self._layerColorCtrl.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._iconColorCtrl.color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        e.accept()
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter,QPen
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton
from ZenWidgets.component.base import ZStyleController
from ZenWidgets.core import ZDebug
from ZenWidgets.gui import ZTitleBarButtonStyleData

class ZMinimizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._styleCtrl = ZStyleController[ZTitleBarButtonStyleData](self, 'ZTitleBarButton')
        self._styleCtrl.styleChanged.connect(self._style_change_handler_)
        self._init_style_()

    def _init_style_(self):
        data = self._styleCtrl.data
        self._iconColorCtrl.color = data.Icon
        self._layerColorCtrl.color = data.Layer

    def _style_change_handler_(self):
        data = self._styleCtrl.data
        self._layerColorCtrl.setColor(data.Layer)
        self._iconColorCtrl.setColorTo(data.Icon)

    def hoverHandler(self):
        self._layerColorCtrl.color = self._styleCtrl.data.Layer
        self._layerColorCtrl.setAlphaTo(26)

    def leaveHandler(self):
        self._layerColorCtrl.setAlphaTo(0)

    def pressHandler(self):
        self._layerColorCtrl.setAlphaTo(18)

    def releaseHandler(self):
        self._layerColorCtrl.setAlphaTo(26)

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
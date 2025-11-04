from PySide6.QtCore import Qt,QLineF,Slot
from PySide6.QtGui import QPainter, QPen,QColor
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton
from ZenWidgets.component.base import StyleController
from ZenWidgets.core import ZDebug
from ZenWidgets.gui import ZCloseButtonStyleData

class ZCloseButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._styleCtrl = StyleController[ZCloseButtonStyleData](self, 'ZCloseButton')
        self._styleCtrl.styleChanged.connect(self._style_change_handler_)
        self._init_style_()

    def _init_style_(self):
        data =self._styleCtrl.data
        self._layerColorCtrl.color = data.Layer
        self._iconColorCtrl.color = data.Icon

    def _style_change_handler_(self):
        self._iconColorCtrl.setColorTo(self._styleCtrl.data.Icon)

    def hoverHandler(self):
        self._layerColorCtrl.setColorTo(self._styleCtrl.data.LayerHover)

    def leaveHandler(self):
        self._layerColorCtrl.setColorTo(self._styleCtrl.data.Layer)

    def pressHandler(self):
        self._layerColorCtrl.setColorTo(self._styleCtrl.data.LayerPressed)

    def releaseHandler(self):
        self._layerColorCtrl.setColorTo(self._styleCtrl.data.LayerHover)

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
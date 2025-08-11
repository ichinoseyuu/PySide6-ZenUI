from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from ZenUI.component.base import StyleData
from ZenUI.core import ZTitleBarButtonStyleData
from .abctitlebarbutton import ZABCTitleBarButton


class ZMinimizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._style_data = StyleData[ZTitleBarButtonStyleData](self, 'ZMinimizeButton')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

    @property
    def styleData(self): return self._style_data

    def _initStyle(self):
        data = self._style_data.data
        self._body_cc.color = data.Body
        self._icon_cc.color = data.Icon
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._body_cc.setColorTo(data.Body)
        self._icon_cc.setColorTo(data.Icon)

    def hoverHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)

    def leaveHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)

    def pressHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyPressed)

    def releaseHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)

    def paintEvent(self, e):
        painter = QPainter(self)
        # draw background
        painter.setBrush(self._body_cc.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._icon_cc.color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)

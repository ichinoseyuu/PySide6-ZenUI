from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton


class ZMinimizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZMinimizeButton")

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZMinimizeButton", theme.name)
        self._background_style.setColorTo(self._style_data.body)
        self._icon_style.setColorTo(self._style_data.icon)

    def hoverHandler(self):
        self._background_style.setColorTo(self._style_data.bodyhover)
        self._icon_style.setColorTo(self._style_data.iconhover)

    def leaveHandler(self):
        self._background_style.setColorTo(self._style_data.body)
        self._icon_style.setColorTo(self._style_data.icon)

    def pressHandler(self):
        self._background_style.setColorTo(self._style_data.bodypressed)
        self._icon_style.setColorTo(self._style_data.iconpressed)

    def releaseHandler(self):
        self._background_style.setColorTo(self._style_data.body)
        self._icon_style.setColorTo(self._style_data.icon)

    def paintEvent(self, e):
        painter = QPainter(self)
        # draw background
        painter.setBrush(self._background_style.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._icon_style.color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)

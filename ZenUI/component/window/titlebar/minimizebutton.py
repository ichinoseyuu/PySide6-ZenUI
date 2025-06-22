from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton


class ZMinimizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZMinimizeButton"))

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZMinimizeButton", theme.name)
        self.setIconColorTo(QColor(self._style_data.icon))
        self.setBackgroundColorTo(QColor(self._style_data.body))

    def hoverHandler(self):
        self.setBackgroundColorTo(self._style_data.bodyhover)
        self.setIconColorTo(QColor(self._style_data.iconhover))

    def leaveHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def pressHandler(self):
        self.setBackgroundColorTo(self._style_data.bodypressed)
        self.setIconColorTo(QColor(self._style_data.iconpressed))

    def releaseHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def paintEvent(self, e):
        painter = QPainter(self)
        # draw background
        painter.setBrush(self._color_bg)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._color_icon, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)

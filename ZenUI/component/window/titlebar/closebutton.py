from PySide6.QtCore import Qt, QLineF
from PySide6.QtGui import QPainter, QPen
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton

class ZCloseButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZCloseButton")

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZCloseButton", theme.name)
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
        r = self.devicePixelRatioF()
        painter.setBrush(self._background_style.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))

        pen = QPen(self._icon_style.color, 1.2 * r)  # 增加线宽
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
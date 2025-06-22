from PySide6.QtCore import Qt, QLineF
from PySide6.QtGui import QColor, QPainter, QPen
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton

class ZCloseButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZCloseButton"))

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZCloseButton", theme.name)
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
        painter.setRenderHints(QPainter.Antialiasing)

        r = self.devicePixelRatioF()
        painter.setBrush(self._color_bg)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))

        pen = QPen(self._color_icon, 1.1 * r)  # 增加线宽
        pen.setCapStyle(Qt.RoundCap)  # 设置线段端点为圆形
        pen.setJoinStyle(Qt.RoundJoin)  # 设置线段连接处为圆形
        pen.setCosmetic(True)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        w, h = self.width(), self.height()
        iw = ih = 9
        x = w/2 - iw/2
        y = h/2 - ih/2
        lines = [
            QLineF(x, y, x + iw, y + ih),        # 左上到右下
            QLineF(x + iw, y, x, y + ih)         # 右上到左下
        ]
        painter.drawLines(lines)
from PySide6.QtCore import Qt, QLineF
from PySide6.QtGui import QPainter, QPen
from ZenUI.component.base import StyleData
from ZenUI.core import ZTitleBarButtonStyleData,ZDebug
from .abctitlebarbutton import ZABCTitleBarButton

class ZCloseButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._style_data = StyleData[ZTitleBarButtonStyleData](self, 'ZCloseButton')
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
        data = self._style_data.data
        self._body_cc.setColorTo(data.BodyHover)
        self._icon_cc.setColorTo(data.IconHover)

    def leaveHandler(self):
        data = self._style_data.data
        self._body_cc.setColorTo(data.Body)
        self._icon_cc.setColorTo(data.Icon)

    def pressHandler(self):
        data = self._style_data.data
        self._body_cc.setColorTo(data.BodyPressed)
        self._icon_cc.setColorTo(data.IconPressed)

    def releaseHandler(self):
        data = self._style_data.data
        self._body_cc.setColorTo(data.Body)
        self._icon_cc.setColorTo(data.Icon)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(self._body_cc.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))
        r = self.devicePixelRatioF()

        pen = QPen(self._icon_cc.color, 1.2 * 1/r)  # 增加线宽
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
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
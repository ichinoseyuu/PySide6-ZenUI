from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPath
from ZenUI.core import ZGlobal
from .abctitlebarbutton import ZABCTitleBarButton

class ZMaximizeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZMaximizeButton"))

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZMaximizeButton", theme.name)
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

    def setMaxState(self, isMax):
        if self._isMax == isMax: return
        self._isMax = isMax
        self.update()

    def toggleMaxState(self):
        self._isMax = not self._isMax
        self.update()

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

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self._isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)

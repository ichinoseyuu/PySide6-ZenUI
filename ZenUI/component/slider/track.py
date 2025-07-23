from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import BackGroundStyle,BorderStyle,CornerStyle,MoveExpAnimation

class SliderTrack(QWidget):
    def __init__(self, parent:QWidget = None):
        super().__init__(parent)
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._corner_style = CornerStyle(self)
        self._move_animation = MoveExpAnimation(self)

    @property
    def backgroundStyle(self):
        return self._background_style

    @property
    def borderStyle(self):
        return self._border_style

    @property
    def cornerStyle(self):
        return self._corner_style

    @property
    def moveAnimation(self):
        return self._move_animation

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._corner_style.radius
        # draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(rect, radius, radius)
        # draw border
        painter.setPen(QPen(self._border_style.color, self._border_style.width))
        painter.setBrush(Qt.NoBrush)
        # adjust border width
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            radius,
            radius
        )

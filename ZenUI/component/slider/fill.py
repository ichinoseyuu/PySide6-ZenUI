from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import GradientBackGroundStyle,BorderStyle,CornerStyle,MoveExpAnimation,ResizeExpAnimation

class SliderFill(QWidget):
    def __init__(self, parent:QWidget = None):
        super().__init__(parent)
        self._background_style = GradientBackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._corner_style = CornerStyle(self)
        self._move_animation = MoveExpAnimation(self)
        self._resize_animation = ResizeExpAnimation(self)

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
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        radius = self._corner_style.radius

        # 创建圆角路径
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # 绘制背景
        if self._background_style.type == self._background_style.Type.Linear:
            x1, y1, x2, y2 = self.background.linearPoints
            gradient = QLinearGradient(
                rect.width() * x1,
                rect.height() * y1,
                rect.width() * x2,
                rect.height() * y2
            )
        elif self._background_style.type == self._background_style.Type.Radial:
            center = QPointF(self.width() / 2, self.height() / 2)
            gradient = QRadialGradient(center, self.background.radialRadius, center)
        elif self._background_style.type == self._background_style.Type.Conical:
            center = QPointF(self.width() / 2, self.height() / 2)
            gradient = QConicalGradient(center, self._background_style.conicalAngle)

        # 设置渐变颜色
        if not self._background_style.reverse:
            gradient.setColorAt(0.0, self._background_style.colorStart)
            gradient.setColorAt(1.0, self._background_style.colorEnd)
        else:
            gradient.setColorAt(0.0, self._background_style.colorEnd)
            gradient.setColorAt(1.0, self._background_style.colorStart)

        # 用圆角路径填充渐变
        painter.fillPath(path, gradient)
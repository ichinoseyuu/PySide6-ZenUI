from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorController,LinearGradientController,FloatController,LocationController,SizeController

class SliderFill(QWidget):
    def __init__(self, parent:QWidget = None):
        super().__init__(parent)
        self._body_cc = LinearGradientController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._location_ctrl = LocationController(self)
        self._size_ctrl = SizeController(self)

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def locationCtrl(self): return self._location_ctrl

    @property
    def sizeCtrl(self): return self._size_ctrl

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        radius = self._radius_ctrl.value

        # 计算内部矩形（考虑边框宽度）
        inner_rect = QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5)
        # 创建圆角路径（基于inner_rect）
        path = QPainterPath()
        path.addRoundedRect(inner_rect, radius, radius)

        # 绘制渐变背景
        x1, y1, x2, y2 = self._body_cc.linearPoints
        gradient = QLinearGradient(
            inner_rect.width() * x1 + inner_rect.left(),
            inner_rect.height() * y1 + inner_rect.top(),
            inner_rect.width() * x2 + inner_rect.left(),
            inner_rect.height() * y2 + inner_rect.top()
        )
        if not self._body_cc.reverse:
            gradient.setColorAt(0.0, self._body_cc.colorStart)
            gradient.setColorAt(1.0, self._body_cc.colorEnd)
        else:
            gradient.setColorAt(0.0, self._body_cc.colorEnd)
            gradient.setColorAt(1.0, self._body_cc.colorStart)
        painter.fillPath(path, gradient)

        # 绘制边框
        painter.setPen(QPen(
            self._border_cc.color,
            1,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
        ))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(inner_rect, radius, radius)

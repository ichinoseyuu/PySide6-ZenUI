from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorController,FloatController,LocationController

class SliderTrack(QWidget):
    def __init__(self, parent:QWidget = None):
        super().__init__(parent)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._loacation_ctrl = LocationController(self)

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def loactionCtrl(self): return self._loacation_ctrl

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._radius_ctrl.value
        # 计算内部矩形（考虑边框宽度）
        inner_rect = QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5)
        # 绘制背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_cc.color)
        painter.drawRoundedRect(inner_rect, radius, radius)
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


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorManager,FloatManager,LocationManager

class SliderTrack(QWidget):
    def __init__(self, parent:QWidget = None):
        super().__init__(parent)
        self._body_color_mgr = ColorManager(self)
        self._border_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)
        self._loacation_mgr = LocationManager(self)

    @property
    def bodyColorMgr(self): return self._body_color_mgr

    @property
    def borderColorMgr(self): return self._border_color_mgr

    @property
    def radiusMgr(self): return self._radius_mgr

    @property
    def loactionMgr(self): return self._loacation_mgr

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._radius_mgr.value
        # 计算内部矩形（考虑边框宽度）
        inner_rect = QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5)
        # 绘制背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_color_mgr.color)
        painter.drawRoundedRect(inner_rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(
            self._border_color_mgr.color,
            1,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
        ))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(inner_rect, radius, radius)


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorManager,LinearGradientManager,FloatManager,LocationManager,SizeManager

class SliderFill(QWidget):
    def __init__(self, parent:QWidget = None):
        super().__init__(parent)
        self._body_color_mgr = LinearGradientManager(self)
        self._border_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)
        self._location_mgr = LocationManager(self)
        self._size_mgr = SizeManager(self)

    @property
    def bodyColorMgr(self): return self._body_color_mgr

    @property
    def borderColorMgr(self): return self._border_color_mgr

    @property
    def radiusMgr(self): return self._radius_mgr

    @property
    def locationMgr(self): return self._location_mgr

    @property
    def sizeMgr(self): return self._size_mgr

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        radius = self._radius_mgr.value

        # 计算内部矩形（考虑边框宽度）
        inner_rect = QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5)
        # 创建圆角路径（基于inner_rect）
        path = QPainterPath()
        path.addRoundedRect(inner_rect, radius, radius)

        # 绘制渐变背景
        x1, y1, x2, y2 = self._body_color_mgr.linearPoints
        gradient = QLinearGradient(
            inner_rect.width() * x1 + inner_rect.left(),
            inner_rect.height() * y1 + inner_rect.top(),
            inner_rect.width() * x2 + inner_rect.left(),
            inner_rect.height() * y2 + inner_rect.top()
        )
        if not self._body_color_mgr.reverse:
            gradient.setColorAt(0.0, self._body_color_mgr.colorStart)
            gradient.setColorAt(1.0, self._body_color_mgr.colorEnd)
        else:
            gradient.setColorAt(0.0, self._body_color_mgr.colorEnd)
            gradient.setColorAt(1.0, self._body_color_mgr.colorStart)
        painter.fillPath(path, gradient)

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


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorController,FloatController,LocationController
from ZenUI.core import ZGlobal,TipPos
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ZenUI.component.slider.slider import ZSlider

class SliderHandle(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 radius: int = 6):
        super().__init__(parent)
        self._radius = radius
        self.resize(2*radius, 2*radius)

        self._inner_scale_normal = 0.4      # 正常状态的内圈大小
        self._inner_scale_hover = 0.6       # 悬停状态的内圈大小
        self._inner_scale_pressed = 0.5     # 按下状态的内圈大小
        self._inner_scale_released = 0.6    # 释放状态的内圈大小

        self._outer_scale_normal = 0.8      # 正常状态的外圈大小
        self._outer_scale_hover = 1.0       # 悬停状态的外圈大小
        self._outer_scale_pressed = 1.0     # 按下状态的外圈大小
        self._outer_scale_released = 1.0    # 释放状态的外圈大小

        self._inner_scale_ctrl = FloatController(self)
        self._outer_scale_ctrl = FloatController(self)

        self._inner_cc = ColorController(self)
        self._outer_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._location_ctrl = LocationController(self)

        self._inner_scale_ctrl.setValue(self._inner_scale_normal)
        self._outer_scale_ctrl.setValue(self._outer_scale_normal)

    @property
    def innerColorCtrl(self): return self._inner_cc

    @property
    def outerColorCtrl(self): return self._outer_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def locationCtrl(self): return self._location_ctrl


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 计算中心点和基础半径
        center = QPointF(self.width()/2, self.height()/2)
        base_radius = min(self.width(), self.height())/2 - 1
        # 绘制外边框
        painter.setPen(QPen(self._border_cc.color, 1))
        border_radius = base_radius * self._inner_scale_ctrl.value
        painter.setBrush(Qt.NoBrush)  # 不填充
        painter.drawEllipse(center, border_radius, border_radius)
        # 绘制外圈(大小可变)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._outer_cc.color)
        outer_radius = base_radius * self._outer_scale_ctrl.value
        painter.drawEllipse(center, outer_radius, outer_radius)
        # 绘制内圈(大小可变)
        inner_radius = base_radius * self._inner_scale_ctrl.value
        painter.setBrush(self._inner_cc.color)
        painter.drawEllipse(center, inner_radius, inner_radius)
        painter.end()

    def enterEvent(self, event):
        super().enterEvent(event)
        self._inner_scale_ctrl.setValueTo(self._inner_scale_hover)
        self._outer_scale_ctrl.setValueTo(self._outer_scale_hover)
        if self.parent().isHorizontal:
            ZGlobal.tooltip.showTip(
                text = self.parent().displayValue,
                target = self,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = TipPos.Top)
        else:
            ZGlobal.tooltip.showTip(
                text = self.parent().displayValue,
                target = self,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = TipPos.Left)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._inner_scale_ctrl.setValueTo(self._inner_scale_normal)
        self._outer_scale_ctrl.setValueTo(self._outer_scale_normal)
        ZGlobal.tooltip.hideTipDelayed(500)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._inner_scale_ctrl.setValueTo(self._inner_scale_pressed)
        self._outer_cc.setAlphaTo(150)
        self._border_cc.setAlphaTo(150)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._inner_scale_ctrl.setValueTo(self._inner_scale_released)
        self._outer_cc.setAlphaTo(255)
        self._border_cc.setAlphaTo(255)


    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        slider = self.parent()
        pos = event.globalPos() - slider.mapToGlobal(QPoint(self._radius, self._radius))
        if slider.isHorizontal:
            delta = max(0, min(pos.x(), slider._track_length))
            slider.setValue(delta / slider._track_length * slider._max)
            ZGlobal.tooltip.showTip(
                text = self.parent().displayValue,
                target = self,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position =TipPos.Top)
        else:
            delta = max(0, min(pos.y(), slider._track_length))
            slider.setValue(slider._max - delta / slider._track_length * slider._max)
            ZGlobal.tooltip.showTip(
                text = self.parent().displayValue,
                target = self,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = TipPos.Left)


    def parent(self) -> 'ZSlider':
        return super().parent()
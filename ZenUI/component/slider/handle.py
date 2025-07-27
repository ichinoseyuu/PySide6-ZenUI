
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorManager,LocationManager
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
        self._inner_scale = 0.4
        self._inner_scale_normal = 0.4      # 正常状态的内圈大小
        self._inner_scale_hover = 0.6       # 悬停状态的内圈大小
        self._inner_scale_pressed = 0.5     # 按下状态的内圈大小
        self._inner_scale_released = 0.6    # 释放状态的内圈大小

        self._outer_scale = 0.8
        self._outer_scale_normal = 0.8      # 正常状态的外圈大小
        self._outer_scale_hover = 1.0       # 悬停状态的外圈大小
        self._outer_scale_pressed = 1.0     # 按下状态的外圈大小
        self._outer_scale_released = 1.0    # 释放状态的外圈大小


        self._inner_color_mgr = ColorManager(self)
        self._outer_color_mgr = ColorManager(self)
        self._border_color_mgr = ColorManager(self)
        self._location_mgr = LocationManager(self)

        # 创建内圈动画
        self._inner_anim = QPropertyAnimation(self, b"innerScale")
        self._inner_anim.setDuration(150)
        # 创建外圈动画
        self._outer_anim = QPropertyAnimation(self, b"outerScale")
        self._outer_anim.setDuration(150)
        # 初始化大小
        self.resize(2*radius, 2*radius)
    @property
    def innerColorMgr(self): return self._inner_color_mgr

    @property
    def outerColorMgr(self): return self._outer_color_mgr

    @property
    def borderColorMgr(self): return self._border_color_mgr

    @property
    def locationMgr(self): return self._location_mgr

    # 添加内圈缩放属性动画支持
    @Property(float)
    def innerScale(self):
        return self._inner_scale

    @innerScale.setter
    def innerScale(self, value):
        self._inner_scale = value
        self.update()

    # 添加外圈缩放属性动画支持
    @Property(float)
    def outerScale(self):
        return self._outer_scale

    @outerScale.setter
    def outerScale(self, value):
        self._outer_scale = value
        self.update()

    def setInnerScaleTo(self, value):
        self._inner_anim.stop()
        self._inner_anim.setStartValue(self._inner_scale)
        self._inner_anim.setEndValue(value)
        self._inner_anim.start()

    def setOuterScaleTo(self, value):
        self._outer_anim.stop()
        self._outer_anim.setStartValue(self._outer_scale)
        self._outer_anim.setEndValue(value)
        self._outer_anim.start()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 计算中心点和基础半径
        center = QPointF(self.width()/2, self.height()/2)
        base_radius = min(self.width(), self.height())/2 - 1
        # 绘制外边框
        painter.setPen(QPen(self._border_color_mgr.color, 1))
        border_radius = base_radius * self._outer_scale
        painter.setBrush(Qt.NoBrush)  # 不填充
        painter.drawEllipse(center, border_radius, border_radius)
        # 绘制外圈(大小可变)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._outer_color_mgr.color)
        outer_radius = base_radius * self._outer_scale
        painter.drawEllipse(center, outer_radius, outer_radius)
        # 绘制内圈(大小可变)
        inner_radius = base_radius * self._inner_scale
        painter.setBrush(self._inner_color_mgr.color)
        painter.drawEllipse(center, inner_radius, inner_radius)
        painter.end()

    def enterEvent(self, event):
        super().enterEvent(event)
        # 悬停时内外圈都放大
        self.setInnerScaleTo(self._inner_scale_hover)
        self.setOuterScaleTo(self._outer_scale_hover)
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
        # 离开时内外圈都恢复原始大小
        self.setInnerScaleTo(self._inner_scale_normal)
        self.setOuterScaleTo(self._outer_scale_normal)
        ZGlobal.tooltip.hideTipDelayed(500)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 按下时内圈缩小,外圈保持放大状态
        self.setInnerScaleTo(self._inner_scale_pressed)
        self._outer_color_mgr.setAlphaTo(150)
        self._border_color_mgr.setAlphaTo(150)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # 释放时内圈恢复放大状态,外圈保持放大
        self.setInnerScaleTo(self._inner_scale_released)
        self._outer_color_mgr.setAlphaTo(255)
        self._border_color_mgr.setAlphaTo(255)


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
                position = TipPos.Top)


    def parent(self) -> 'ZSlider':
        return super().parent()
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.core import Zen,ZColorTool,ZenGlobal
class SliderHandle(QWidget):
    '滑块手柄'
    def __init__(self,
                 parent: ZWidget = None, 
                 radius: int = 6):
        super().__init__(parent)
        self._radius = radius
        self._inner_color_config = '#00000000'
        self._outer_color_config = '#00000000'
        self._border_color_config = '#00000000'
        self._inner_color = QColor(0, 0, 0, 0)
        self._outer_color = QColor(0, 0, 0, 0)
        self._border_color = QColor(0, 0, 0, 0)
        # 添加内外圈大小动画
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
        # 创建内圈动画
        self._inner_anim = QPropertyAnimation(self, b"innerScale")
        self._inner_anim.setDuration(150)
        # 创建外圈动画
        self._outer_anim = QPropertyAnimation(self, b"outerScale")
        self._outer_anim.setDuration(150)
        # 创建背景动画
        self._inner_color_anim = QPropertyAnimation(self, b"innerColor")
        self._inner_color_anim.setDuration(150)
        self._outer_color_anim = QPropertyAnimation(self, b"outerColor")
        self._outer_color_anim.setDuration(150)
        self._border_color_anim = QPropertyAnimation(self, b"borderColor")
        self._border_color_anim.setDuration(150)
        # 初始化大小
        self.resize(2*radius, 2*radius)

    @Property(QColor)
    def innerColor(self):
        return self._inner_color

    @innerColor.setter
    def innerColor(self, value):
        self._inner_color = value
        self.update()

    @Property(QColor)
    def outerColor(self):
        return self._outer_color

    @outerColor.setter
    def outerColor(self, value):
        self._outer_color = value
        self.update()

    @Property(QColor)
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, value):
        self._border_color = value

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
        '内圈缩放动画'
        self._inner_anim.stop()
        self._inner_anim.setStartValue(self._inner_scale)
        self._inner_anim.setEndValue(value)
        self._inner_anim.start()

    def setOuterScaleTo(self, value):
        '外圈缩放动画'
        self._outer_anim.stop()
        self._outer_anim.setStartValue(self._outer_scale)
        self._outer_anim.setEndValue(value)
        self._outer_anim.start()

    def setInnerColorTo(self, value):
        '内圈颜色动画'
        self._inner_color_anim.stop()
        self._inner_color_anim.setStartValue(self._inner_color)
        self._inner_color_anim.setEndValue(value)
        self._inner_color_anim.start()

    def setOuterColorTo(self, value):
        '外圈颜色动画'
        self._outer_color_anim.stop()
        self._outer_color_anim.setStartValue(self._outer_color)
        self._outer_color_anim.setEndValue(value)
        self._outer_color_anim.start()

    def setBorderColorTo(self, value):
        '边框颜色动画'
        self._border_color_anim.stop()
        self._border_color_anim.setStartValue(self._border_color)
        self._border_color_anim.setEndValue(value)
        self._border_color_anim.start()

    def configColor(self, inner_color, outer_color, border_color):
        self._inner_color_config = inner_color
        self._outer_color_config = outer_color
        self._border_color_config = border_color
        self._inner_color = ZColorTool.toQColor(inner_color)
        self._outer_color = ZColorTool.toQColor(outer_color)
        self._border_color = ZColorTool.toQColor(border_color)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 计算中心点和基础半径
        center = QPointF(self.width()/2, self.height()/2)
        base_radius = min(self.width(), self.height())/2 - 1
        # 绘制外边框
        painter.setPen(QPen(self.borderColor, 1))
        border_radius = base_radius * self._outer_scale
        painter.setBrush(Qt.NoBrush)  # 不填充
        painter.drawEllipse(center, border_radius, border_radius)
        # 绘制外圈(大小可变)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.outerColor)
        outer_radius = base_radius * self._outer_scale
        painter.drawEllipse(center, outer_radius, outer_radius)
        # 绘制内圈(大小可变)
        inner_radius = base_radius * self._inner_scale
        painter.setBrush(self.innerColor)
        painter.drawEllipse(center, inner_radius, inner_radius)
        painter.end()

    def enterEvent(self, event):
        super().enterEvent(event)
        if "ToolTip" in ZenGlobal.ui.windows:
            # 获取handle相对于屏幕的全局位置
            ZenGlobal.ui.windows["ToolTip"].setText(str(self.parent().value()))
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(self.parent())
            ZenGlobal.ui.windows["ToolTip"].showTip()
        # 悬停时内外圈都放大
        self.setInnerScaleTo(self._inner_scale_hover) 
        self.setOuterScaleTo(self._outer_scale_hover)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        if "ToolTip" in ZenGlobal.ui.windows:
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(None)
            ZenGlobal.ui.windows["ToolTip"].hideTip()
        # 离开时内外圈都恢复原始大小
        self.setInnerScaleTo(self._inner_scale_normal)
        self.setOuterScaleTo(self._outer_scale_normal)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 按下时内圈缩小,外圈保持放大状态
        self.setInnerScaleTo(self._inner_scale_pressed)
        color = ZColorTool.toQColor(ZColorTool.trans(self._outer_color_config,150))
        self.setOuterColorTo(color)
        border_color = ZColorTool.toQColor(ZColorTool.trans(self._border_color_config,150))
        self.setBorderColorTo(border_color)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # 释放时内圈恢复放大状态,外圈保持放大
        self.setInnerScaleTo(self._inner_scale_released)
        self.setOuterColorTo(ZColorTool.toQColor(self._outer_color_config))
        self.setBorderColorTo(ZColorTool.toQColor(self._border_color_config))


    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 获取父组件(ZSlider)
        slider = self.parent()
        # 获取鼠标相对于slider的位置
        # 这里需要使用handle的半径来调整起始位置
        pos = event.globalPos() - slider.mapToGlobal(QPoint(self._radius, self._radius))
        if slider._direction == Zen.Direction.Horizontal:
            delta = max(0, min(pos.x(), slider._track_length))
            slider.setValue(delta / slider._track_length * slider._max)
        elif slider._direction == Zen.Direction.Vertical:
            delta = max(0, min(pos.y(), slider._track_length))
            slider.setValue(slider._max - delta / slider._track_length * slider._max)
        # 更新位置和样式
        ZenGlobal.ui.windows["ToolTip"].setText(str(slider.value()))

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from ZenUI.component.basewidget import ZWidget
from ZenUI.core import Zen,ZColorTool,ZenGlobal
class Handle(QWidget):
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
        self._inner_scale = 0.4             # 内圈默认为基础半径的0.6倍
        self._inner_scale_normal = 0.4      # 正常状态的内圈大小
        self._inner_scale_hover = 0.6       # 悬停状态的内圈大小
        self._inner_scale_pressed = 0.5     # 按下状态的内圈大小
        self._inner_scale_released = 0.6    # 释放状态的内圈大小
        self._outer_scale = 0.8             # 外圈默认为基础半径的1.0倍
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

    def playInnerScaleAnim(self, inner_value):
        '内圈缩放动画'
        self._inner_anim.stop()
        self._inner_anim.setStartValue(self._inner_scale)
        self._inner_anim.setEndValue(inner_value)
        self._inner_anim.start()

    def playOuterScaleAnim(self, outer_value):
        '外圈缩放动画'
        self._outer_anim.stop()
        self._outer_anim.setStartValue(self._outer_scale)
        self._outer_anim.setEndValue(outer_value)
        self._outer_anim.start()

    def playInnerColorAnim(self, inner_value):
        '内圈颜色动画'
        self._inner_color_anim.stop()
        self._inner_color_anim.setStartValue(self._inner_color)
        self._inner_color_anim.setEndValue(inner_value)
        self._inner_color_anim.start()

    def playOuterColorAnim(self, outer_value):
        '外圈颜色动画'
        self._outer_color_anim.stop()
        self._outer_color_anim.setStartValue(self._outer_color)
        self._outer_color_anim.setEndValue(outer_value)
        self._outer_color_anim.start()

    def playBorderColorAnim(self, border_value):
        '边框颜色动画'
        self._border_color_anim.stop()
        self._border_color_anim.setStartValue(self._border_color)
        self._border_color_anim.setEndValue(border_value)
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

    def enterEvent(self, event):
        super().enterEvent(event)
        if "ToolTip" in ZenGlobal.ui.windows:
            ZenGlobal.ui.windows["ToolTip"].setText(str(self.parent().value()))
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(self.parent())
            ZenGlobal.ui.windows["ToolTip"].showTip()
        # 悬停时内外圈都放大
        self.playInnerScaleAnim(self._inner_scale_hover) 
        self.playOuterScaleAnim(self._outer_scale_hover)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        if "ToolTip" in ZenGlobal.ui.windows:
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(None)
            ZenGlobal.ui.windows["ToolTip"].hideTip()
        # 离开时内外圈都恢复原始大小
        self.playInnerScaleAnim(self._inner_scale_normal)
        self.playOuterScaleAnim(self._outer_scale_normal)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 按下时内圈放大,外圈保持放大状态
        self.playInnerScaleAnim(self._inner_scale_pressed)
        color = ZColorTool.toQColor(ZColorTool.trans(self._outer_color_config,150))
        self.playOuterColorAnim(color)
        border_color = ZColorTool.toQColor(ZColorTool.trans(self._border_color_config,150))
        self.playBorderColorAnim(border_color)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # 释放时内圈恢复放大状态,外圈保持放大
        self.playInnerScaleAnim(self._inner_scale_released)
        color = ZColorTool.toQColor(self._outer_color_config)
        self.playOuterColorAnim(color)
        border_color = ZColorTool.toQColor(self._border_color_config)
        self.playBorderColorAnim(border_color)


    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 获取父组件(ZSlider)
        slider = self.parent()
        # 获取鼠标相对于slider的位置
        # 这里需要使用handle的半径来调整起始位置
        pos = event.globalPos() - slider.mapToGlobal(QPoint(self._radius, self._radius))
        # 根据方向计算新位置
        if slider._direction == Zen.Direction.Horizontal:
            # 水平方向移动，限制x坐标在有效范围内
            new_x = max(0, min(pos.x(), slider.width() - 2 * self._radius))
            self.move(new_x, (slider.height() - 2 * self._radius) / 2)
            slider._fill_track(round(slider._max/slider._track_length*new_x, 2))
        else:
            # 垂直方向移动，限制y坐标在有效范围内
            new_y = max(0, min(pos.y(), slider.height() - 2 * self._radius))
            self.move((slider.width() - 2 * self._radius) / 2, new_y)
            slider._fill_track(slider._max-round(slider._max/slider._track_length*new_y, 2))
        # 更新位置和样式
        ZenGlobal.ui.windows["ToolTip"].setText(str(slider.value()))
        self.update()

    def moveEvent(self, event):
        super().moveEvent(event)
        # 更新数值窗口的位置
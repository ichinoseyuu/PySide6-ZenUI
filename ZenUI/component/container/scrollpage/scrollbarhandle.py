from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from ZenUI.component.basewidget import ZWidget
from ZenUI.core import Zen,ZColorTool,ZenGlobal
class ScrollBarHandle(QWidget):
    '滚动条手柄'
    def __init__(self,
                 parent: ZWidget = None, 
                 radius: int = 6):
        super().__init__(parent)
        self._radius = radius
        self._color_config = '#00000000'
        self._border_color_config = '#00000000'
        self._color = QColor(0, 0, 0, 0)
        self._border_color = QColor(0, 0, 0, 0)
        self._scale = 0.8             # 外圈默认为基础半径的1.0倍
        self._scale_normal = 0.8      # 正常状态的缩放大小
        self._scale_hover = 1.0       # 悬停状态的缩放大小
        self._scale_pressed = 1.0     # 按下状态的缩放大小
        self._scale_released = 1.0    # 释放状态的缩放大小
        # 创建缩放动画
        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(150)
        # 创建背景动画
        self._color_anim = QPropertyAnimation(self, b"color")
        self._color_anim.setDuration(150)
        # 创建边框动画
        self._border_color_anim = QPropertyAnimation(self, b"borderColor")
        self._border_color_anim.setDuration(150)
        # 初始化大小
        self.resize(2*radius, 2*radius)

    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update()

    @Property(QColor)
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, value):
        self._border_color = value

    # 添加缩放属性动画支持
    @Property(float)
    def scale(self):
        return self._outer_scale

    @scale.setter
    def scale(self, value):
        self._outer_scale = value
        self.update()

    def setScaleTo(self, value):
        '缩放动画'
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(value)
        self._scale_anim.start()

    def setColorTo(self, value):
        '颜色动画'
        self._color_anim.stop()
        self._color_anim.setStartValue(self._color)
        self._color_anim.setEndValue(value)
        self._color_anim.start()

    def setBorderColorTo(self, value):
        '边框颜色动画'
        self._border_color_anim.stop()
        self._border_color_anim.setStartValue(self._border_color)
        self._border_color_anim.setEndValue(value)
        self._border_color_anim.start()

    def configColor(self, color, border_color):
        self._color_config = color
        self._border_color_config = border_color
        self._color = ZColorTool.toQColor(color)
        self._border_color = ZColorTool.toQColor(border_color)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 计算圆角半径和矩形区域
        corner_radius = min(self.width(), self.height()) / 2
        rect = QRectF(1, 1, self.width()-2, self.height()-2)  # 留出1px边框的空间
        # 绘制边框
        painter.setPen(QPen(self.borderColor, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, corner_radius, corner_radius)
        # 绘制内部填充
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        # 内部填充区域略小，避免边框被覆盖
        inner_rect = rect.adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(inner_rect, corner_radius, corner_radius)

    def enterEvent(self, event):
        super().enterEvent(event)
        # 悬停时放大
        self.setScaleTo(self._scale_hover)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        # 离开时恢复原始大小
        self.setScaleTo(self._scale_normal)


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 按下时缩小
        self.setScaleTo(self._scale_pressed)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # 释放时放大
        self.setScaleTo(self._scale_released)


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
            slider._fill_track(slider._max/slider._track_length*new_x)
        else:
            # 垂直方向移动，限制y坐标在有效范围内
            new_y = max(0, min(pos.y(), slider.height() - 2 * self._radius))
            self.move((slider.width() - 2 * self._radius) / 2, new_y)
            slider._fill_track(slider._max-slider._max/slider._track_length*new_y)
        # 更新位置和样式
        ZenGlobal.ui.windows["ToolTip"].setText(str(slider.value()))
        self.update()
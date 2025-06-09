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
                 width: int = 6,
                 height: int = 10,
                 radius: int = 4):
        super().__init__(parent)
        self._radius = radius
        self._color_config = '#00000000'
        self._border_color_config = '#00000000'
        self._color = QColor(0, 0, 0, 0)
        self._border_color = QColor(0, 0, 0, 0)
        # 添加缩放比例
        self._scale = 0.8
        self._scale_normal = 0.8      # 正常缩放大小
        self._scale_hover = 1.0       # 悬停缩放大小
        self._scale_pressed = 0.9     # 按下缩放大小
        self._scale_released = 1.0    # 释放缩放大小
        # 创建缩放动画
        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(150)
        # 创建背景动画
        self._color_anim = QPropertyAnimation(self, b"color")
        self._color_anim.setDuration(150)
        self._border_color_anim = QPropertyAnimation(self, b"borderColor")
        self._border_color_anim.setDuration(150)
        # 初始化大小
        self.resize(width, height)

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

    # 添加外圈缩放属性动画支持
    @Property(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    def setColorTo(self, value):
        '背景颜色动画'
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

    def setScaleTo(self, value):
        '缩放动画'
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(value)
        self._scale_anim.start()

    def paintEvent(self, event):
        # painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # # 计算中心点和基础半径
        # center = QPointF(self.width()/2, self.height()/2)
        # base_radius = min(self.width(), self.height())/2 - 1
        # # 绘制外边框
        # painter.setPen(QPen(self.borderColor, 1))
        # border_radius = base_radius * self._outer_scale
        # painter.setBrush(Qt.NoBrush)  # 不填充
        # painter.drawEllipse(center, border_radius, border_radius)
        # # 绘制外圈(大小可变)
        # painter.setPen(Qt.NoPen)
        # painter.setBrush(self.outerColor)
        # outer_radius = base_radius * self._scale
        # painter.drawEllipse(center, outer_radius, outer_radius)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 计算缩放后的尺寸
        original_width = self.width() - 1  # 留出边框空间
        original_height = self.height() - 1
        scaled_width = original_width * self._scale
        scaled_height = original_height * self._scale
        # 计算居中位置
        x = (self.width() - scaled_width) / 2
        y = (self.height() - scaled_height) / 2
        # 创建缩放后的矩形区域
        rect = QRectF(x, y, scaled_width, scaled_height)
        # 绘制外边框
        painter.setPen(QPen(self.borderColor, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, self._radius, self._radius)
        # 绘制内部填充
        inner_rect = rect.adjusted(0, 0, 0, 0)  # 内部区域略小，避免覆盖边框
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRoundedRect(inner_rect, self._radius, self._radius)


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
        color = ZColorTool.toQColor(ZColorTool.trans(self._color_config,150))
        self.setColorTo(color)
        border_color = ZColorTool.toQColor(ZColorTool.trans(self._border_color_config,150))
        self.setBorderColorTo(border_color)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # 释放时恢复
        self.setScaleTo(self._scale_released)
        self.setColorTo(ZColorTool.toQColor(self._color_config))
        self.setBorderColorTo(ZColorTool.toQColor(self._border_color_config))


    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 获取父组件(ZSlider)
        slider = self.parent()
        # 获取鼠标相对于slider的位置
        # 这里需要使用handle的半径来调整起始位置
        
        pos = event.globalPos() - slider.mapToGlobal(QPoint(self.width() / 2, self.height() / 2))
        if slider._direction == Zen.Direction.Horizontal:
            delta = max(0, min(pos.x(), slider._track_length))
            slider.setValue(delta / slider._track_length * slider._max)
        elif slider._direction == Zen.Direction.Vertical:
            delta = max(0, min(pos.y(), slider._track_length))
            slider.setValue(slider._max - delta / slider._track_length * slider._max)

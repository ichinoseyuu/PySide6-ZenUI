from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import Union
from enum import IntEnum
from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.core import Zen

class ScrollBarMode(IntEnum):
    """滚动条显示模式"""
    Auto = 0    # 自动隐藏
    Always = 1  # 始终显示
    Hidden = 2  # 始终隐藏

class ZScrollBar(ZWidget):
    """现代风格滚动条
    特性:
    1. 支持自动隐藏
    2. 平滑滚动动画
    3. 悬停效果
    4. 自适应大小
    5. 圆角风格
    """
    valueChanged = Signal(int)  # 值改变信号
    rangeChanged = Signal(int, int)  # 范围改变信号

    def __init__(self, 
                 parent=None,
                 orientation=Qt.Orientation.Vertical,
                 show_mode=Zen.ScrollBarMode.Auto):
        super().__init__(parent)
        
        # 基础属性
        self._orientation = orientation
        self._show_mode = show_mode
        self._opacity = 0.0  # 用于动画
        
        # 数值相关
        self._value = 0
        self._minimum = 0 
        self._maximum = 100
        self._page_step = 10
        self._single_step = 1
        
        # 样式配置
        self._track_width = 6  # 轨道宽度
        self._handle_min_length = 30  # 滑块最小长度
        self._corner_radius = 3  # 圆角半径
        
        # 状态标志
        self._pressed = False
        self._hover = False
        self._scrolling = False
        
        # 动画
        self._fade_animation = QPropertyAnimation(self, b"opacity")
        self._fade_animation.setDuration(200)
        
        # 定时器(用于自动隐藏)
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._start_fade_out)
        
        # 初始化
        self._init_ui()
        
    @Property(float)
    def opacity(self):
        return self._opacity
        
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
        
    def _init_ui(self):
        """初始化UI"""
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        # 设置大小策略
        if self._orientation == Qt.Orientation.Vertical:
            self.setFixedWidth(self._track_width * 2)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        else:
            self.setFixedHeight(self._track_width * 2)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 计算轨道和滑块区域
        track_rect = self._get_track_rect()
        handle_rect = self._get_handle_rect()
        
        # 绘制轨道
        track_color = self._colors.track.darker(120) if self._hover else self._colors.track
        track_color.setAlpha(int(255 * self._opacity))
        painter.setPen(Qt.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, self._corner_radius, self._corner_radius)
        
        # 绘制滑块
        if self._maximum > self._minimum:
            handle_color = self._colors.handle_inner.lighter(120) if self._pressed else self._colors.handle_inner
            handle_color.setAlpha(int(255 * self._opacity))
            painter.setBrush(handle_color)
            painter.drawRoundedRect(handle_rect, self._corner_radius, self._corner_radius)
            
    def _get_track_rect(self) -> QRect:
        """获取轨道矩形区域"""
        if self._orientation == Qt.Orientation.Vertical:
            return QRectF(
                self.width() / 2 - self._track_width / 2,
                0,
                self._track_width,
                self.height()
            ).toRect()
        else:
            return QRectF(
                0,
                self.height() / 2 - self._track_width / 2,
                self.width(),
                self._track_width
            ).toRect()
            
    def _get_handle_rect(self) -> QRect:
        """获取滑块矩形区域"""
        available = self._maximum - self._minimum
        if available <= 0:
            return QRect()
            
        if self._orientation == Qt.Orientation.Vertical:
            height = max(self._handle_min_length, 
                        self.height() * self._page_step / (available + self._page_step))
            y = self._value * (self.height() - height) / available
            return QRectF(
                self.width() / 2 - self._track_width / 2,
                y,
                self._track_width,
                height
            ).toRect()
        else:
            width = max(self._handle_min_length,
                       self.width() * self._page_step / (available + self._page_step))
            x = self._value * (self.width() - width) / available
            return QRectF(
                x,
                self.height() / 2 - self._track_width / 2,
                width,
                self._track_width
            ).toRect()
            
    def _start_fade_in(self):
        """开始淡入动画"""
        self._fade_animation.stop()
        self._fade_animation.setStartValue(self._opacity)
        self._fade_animation.setEndValue(1.0)
        self._fade_animation.start()
        
    def _start_fade_out(self):
        """开始淡出动画"""
        self._fade_animation.stop()
        self._fade_animation.setStartValue(self._opacity)
        self._fade_animation.setEndValue(0.0)
        self._fade_animation.start()
        
    def enterEvent(self, event):
        self._hover = True
        self._start_fade_in()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._hover = False
        if not self._pressed and self._show_mode == Zen.ScrollBarMode.Auto:
            self._hide_timer.start(500)
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            handle_rect = self._get_handle_rect()
            
            if not handle_rect.contains(event.pos()):
                # 点击轨道,移动到点击位置
                if self._orientation == Qt.Orientation.Vertical:
                    y = event.pos().y()
                    available = self.height() - handle_rect.height()
                    if available > 0:
                        self.setValue(int((y - handle_rect.height()/2) * 
                                       self._maximum / available))
                else:
                    x = event.pos().x()
                    available = self.width() - handle_rect.width()
                    if available > 0:
                        self.setValue(int((x - handle_rect.width()/2) * 
                                       self._maximum / available))
                        
            self._scrolling = True
            self._scroll_start_pos = event.pos()
            self._scroll_start_value = self._value
            
        event.accept()
        
    def mouseMoveEvent(self, event):
        if self._scrolling:
            if self._orientation == Qt.Orientation.Vertical:
                delta = event.pos().y() - self._scroll_start_pos.y()
                available = self.height() - self._get_handle_rect().height()
                if available > 0:
                    delta_value = int(delta * self._maximum / available)
                    self.setValue(self._scroll_start_value + delta_value)
            else:
                delta = event.pos().x() - self._scroll_start_pos.x()
                available = self.width() - self._get_handle_rect().width()
                if available > 0:
                    delta_value = int(delta * self._maximum / available)
                    self.setValue(self._scroll_start_value + delta_value)
        event.accept()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = False
            self._scrolling = False
            if not self._hover and self._show_mode == Zen.ScrollBarMode.Auto:
                self._hide_timer.start(500)
        event.accept()
        
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.setValue(self._value - int(delta * self._single_step))
        event.accept()
        
    # API方法
    def setValue(self, value):
        value = max(self._minimum, min(self._maximum, value))
        if value != self._value:
            self._value = value
            self.update()
            self.valueChanged.emit(value)
            
    def setRange(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = max(minimum, maximum)
        self.setValue(self._value)
        self.rangeChanged.emit(minimum, maximum)
        self.update()
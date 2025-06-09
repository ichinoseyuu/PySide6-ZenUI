from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import Union, Tuple
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.scrollbar.layer import ScrollBarLayer
from ZenUI.component.scrollbar.handle import ScrollBarHandle
from ZenUI.core import Zen,ZColorSheet

class ZScrollBar(ZWidget):
    """滚动条控件"""
    valueChanged = Signal(object) #数值改变信号
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 direction: Zen.Direction = Zen.Direction.Horizontal,
                 track_width: int = 4,
                 track_length: int = 100,
                 value_range: tuple = (0,100),
                 value: int = 0,
                 step: int = 1):
        super().__init__(parent, name)
        self._direction = direction
        '方向'
        self._track_width = track_width
        '轨道宽度'
        self._track_length = track_length
        '轨道长度'
        self._value = 0
        '当前数值'
        self._percentage = 0
        '当前的百分比'
        self._min = value_range[0]
        '最小值'
        self._max = value_range[1]
        '最大值'
        self._step = step
        '滑动步长'
        self._init_style()
        self.setValue(value)


    def _init_style(self):
        self._track = ScrollBarLayer(self)
        '轨道'
        self._handle = ScrollBarHandle(parent=self,
                                       width=10,
                                       height=20)
        '滑块'
        #设置样式
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.ScrollBar)
        self._colors.overwrite(self._color_sheet.getSheet())
        self._track._bg_color_a = self._colors.track
        self._track._stylesheet_fixed =f'border-radius: {int(self._track_width/2)}px;'
        self._handle.configColor(self._colors.handle, self._colors.handle_border)

        #设置大小
        if self._direction == Zen.Direction.Horizontal:
            self._handle.resize(30, 10)
            self.setFixedHeight(self._handle.width())
            self.setFixedWidth(self._track_length + self._handle.width())


        elif self._direction == Zen.Direction.Vertical:
            self._handle.resize(10, 30)
            self.setFixedWidth(self._handle.width())
            self.setFixedHeight(self._track_length + self._handle.width())



    def _normalize_value(self, value: float) -> float:
        """标准化输入值，将输入值调整为合法的步进值,并确保在范围内"""
        # 计算步长小数位
        step_str = str(self._step)
        decimal_places = len(step_str.split('.')[-1]) if '.' in step_str else 0
        # 调整到步进值
        adjusted = round(value / self._step) * self._step
        # 确保在范围内
        clamped = max(self._min, min(adjusted, self._max))
        # 格式化小数位
        return round(clamped, decimal_places)


    def _update_track(self) -> None:
        """更新轨道和填充条位置"""
        if self._direction == Zen.Direction.Horizontal:
            self._update_horizontal_track()
        else:
            self._update_vertical_track()


    def _update_horizontal_track(self):
        """更新水平方向轨道"""
        y = (self.height() - self._track_width) / 2
        # 更新轨道
        self._track.setGeometry(
            self._handle.width()/2,
            y,
            self._track_length,
            self._track_width
            )
        # 计算滑块可移动的最大范围
        handle_width = self._handle.width() * self._handle._scale_normal
        max_x = self._track_length - handle_width
        current_x = self._percentage * max_x
        # 更新滑块位置
        self._handle.move(
            handle_width/2 + current_x,  # 考虑起始位置偏移
            (self.height() - self._handle.height()) / 2
        )

    def _update_vertical_track(self):
        """更新垂直方向轨道"""
        x = (self.width() - self._track_width) / 2
        # 更新轨道
        self._track.setGeometry(
            x,
            self._handle.width()/2,
            self._track_width,
            self._track_length
        )
        # 计算滑块可移动的最大范围
        handle_height = self._handle.height() * self._handle._scale_normal
        height = self._handle.height() * (1-self._handle._scale_normal)
        max_y = self._track_length - handle_height
        current_y = self._percentage * max_y

        # 更新滑块位置
        self._handle.move(
            (self.width() - self._handle.width()) / 2,
            height/2 + (max_y - current_y)  # 垂直方向需要反转
        )


    def setValue(self, value: Union[int, float]) -> None:
        """设置当前值"""
        # 标准化值
        self._value = self._normalize_value(value)
        # 计算百分比
        self._percentage = (self._value - self._min) / (self._max - self._min)
        # 更新UI
        self._update_track()
        # 发送信号
        self.valueChanged.emit(self._value)

    def value(self):
        '获取数值'
        return self._value

    def percentage(self):
        '获取百分比'
        return self._percentage

    def track(self):
        '获取轨道对象'
        return self._track

    def handle(self):
        '获取滑块对象'
        return self._handle

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_track()

    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        # 开启鼠标追踪
        self.setMouseTracking(True)
        # 设置焦点以接收滚轮事件
        self.setFocus()

    def wheelEvent(self, event: QWheelEvent):
        """处理鼠标滚轮事件"""
        # 获取滚轮滚动的角度，通常为 120 或 -120
        delta = event.angleDelta().y()
        # 计算滚动步数（向上为正，向下为负）
        steps = delta / 120
        # 计算值的变化
        new_value = self._value + steps * self._step
        # 更新值（内部会处理方向及范围限制）
        self.setValue(new_value)
        # 阻止事件继续传播
        event.accept()

    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        # 关闭鼠标追踪
        self.setMouseTracking(False)
        # 清除焦点
        self.clearFocus()


    def _theme_changed_handler(self, theme):
        """主题改变处理"""
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self._track.setColor(self._colors.track)
        self._handle.configColor(
            self._colors.handle,
            self._colors.handle_border
        )
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import IntEnum
from ZenUI.core import ZGlobal
from .fill import SliderFill
from .track import SliderTrack
class ZSlider(QWidget):
    class Orientation(IntEnum):
        Horizontal = 0
        Vertical = 1
    valueChanged = Signal(object)
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 orientation: Orientation = Orientation.Horizontal,
                 length: int = 100,
                 scope: tuple = (0, 100),
                 step: int = 1,
                 value: int = 0,):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._orientation = orientation
        self._length = length
        self._scope = scope
        self._max = scope[1]
        self._min = scope[0]
        self._step = step
        self._value = value
        self._percentage = 0
        self._fill = SliderFill(self)
        self._track = SliderTrack(self)
        self._track_width = 4
        self._handle_radius = 10
        if self._orientation == self.Orientation.Horizontal:
            self.setFixedHeight(self._handle_radius*2)
            self.setFixedWidth(self._length + self._handle_radius*2)
        elif self._orientation == self.Orientation.Vertical:
            self.setFixedWidth(self._handle_radius*2)
            self.setFixedHeight(self._length + self._handle_radius*2)
        self.setValue(value)
        # self._style_data: ZSlider = None
        # self.styleData = ZGlobal.styleDataManager.getStyleData('ZScrollPage')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self._normalize_value(value)
        self._percentage = (self._value - self._min) / (self._max - self._min)
        self._update_track()
        self.valueChanged.emit(self._value)

    @property
    def percentage(self):
        return self._percentage

    @property
    def track(self):
        return self._track

    @property
    def fill(self):
        return self._fill

    @property
    def handle(self):
        return self._handle

    def setValue(self,value: int | float):
        self._value = self._normalize_value(value)
        self._percentage = (self._value - self._min) / (self._max - self._min)
        self._update_track()
        self.valueChanged.emit(self._value)


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
        if self._orientation == self.Orientation.Horizontal:
            self._update_horizontal_track()
        else:
            self._update_vertical_track()


    def _update_horizontal_track(self):
        """更新水平方向轨道"""
        y = (self.height() - self._track_width) / 2
        # 更新轨道
        self._track.setGeometry(
            self._handle_radius, 
            y,
            self._length,
            self._track_width
            )
        # 更新填充条
        self._fill.setGeometry(
            self._handle_radius,
            y, 
            self._percentage * self._length,
            self._track_width
            )
        # 更新滑块
        # self._handle.move(
        #     self._percentage * self._track_length,
        #     (self.height() - 2 * self._handle_radius) / 2
        #     )

    def _update_vertical_track(self):
        """更新垂直方向轨道"""
        x = (self.width() - self._track_width) / 2
        # 更新轨道
        self._track.setGeometry(
            x,
            self._handle_radius,
            self._track_width,
            self._length
        )
        # 更新填充条
        fill_height = self._percentage * self._length
        self._fill.setGeometry(
            x,
            self._length - fill_height + self._handle_radius,
            self._track_width,
            fill_height
        )
        # 更新滑块
        # self._handle.move(
        #     (self.width() - 2 * self._handle_radius) / 2,
        #     self._track_length - self._percentage * self._track_length
        # )


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

    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘按键事件"""
        # 显示提示框
        ZGlobal.tooltip.setInsideOf(self)
        ZGlobal.tooltip.showTip()

        # 根据滑块方向处理不同的按键
        if self._orientation == self.Orientation.Horizontal:
            if event.key() == Qt.Key_Left:
                new_value = self._value - self._step
                self.setValue(new_value)
                ZGlobal.tooltip.setText(str(self.value()))
                event.accept()
                return
            elif event.key() == Qt.Key_Right:
                new_value = self._value + self._step
                self.setValue(new_value)
                ZGlobal.tooltip.setText(str(self.value()))
                event.accept()
                return
        else:  # 垂直方向
            if event.key() == Qt.Key_Up:
                new_value = self._value + self._step
                self.setValue(new_value)
                ZGlobal.tooltip.setText(str(self.value()))
                event.accept()
                return
            elif event.key() == Qt.Key_Down:
                new_value = self._value - self._step
                self.setValue(new_value)
                ZGlobal.tooltip.setText(str(self.value()))
                event.accept()
                return
        super().keyPressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        """处理鼠标滚轮事件"""
        # 获取handle相对于屏幕的全局位置
        ZGlobal.tooltip.setInsideOf(self)
        ZGlobal.tooltip.showTip()
        # 获取滚轮滚动的角度，通常为 120 或 -120
        delta = event.angleDelta().y()
        # 计算滚动步数（向上为正，向下为负）
        steps = delta / 120
        # 计算值的变化
        new_value = self._value + steps * self._step
        # 更新值（内部会处理方向及范围限制）
        self.setValue(new_value)
        ZGlobal.tooltip.setText(str(self.value()))
        # 阻止事件继续传播
        event.accept()

    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        ZGlobal.tooltip.setInsideOf(None)
        ZGlobal.tooltip.hideTip()
        # 关闭鼠标追踪
        self.setMouseTracking(False)
        # 清除焦点
        self.clearFocus()

    def _theme_changed_handler(self, theme):
        """主题改变处理"""
    pass
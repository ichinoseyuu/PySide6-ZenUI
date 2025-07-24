from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import IntEnum
from typing import overload
from ZenUI.core import ZGlobal,ZSliderStyleData
from .fill import SliderFill
from .track import SliderTrack
from .handle import SliderHandle
class ZSlider(QWidget):
    class Orientation(IntEnum):
        Horizontal = 0
        Vertical = 1
    valueChanged = Signal(object)
    displayValueChanged = Signal(str)
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 orientation: Orientation = Orientation.Horizontal,
                 scope: tuple = (0, 100),
                 step: int = 1,
                 step_multiplier: int = 1,
                 accuracy: float = 1,
                 value: int = 0,
                 auto_strip_zero: bool = False):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._orientation = orientation
        self._scope = scope
        self._max = scope[1]
        self._min = scope[0]
        self._step = max(step, accuracy)
        self._step_multiplier = step_multiplier
        self._accuracy = accuracy
        self._value: int | float = 0
        self._auto_strip_zero = auto_strip_zero

        self._percentage = 0
        self._track_width = 4
        self._track_length: int = 0
        self._handle_radius = 10
        self._min_length = 200
        self._fixed_length = None

        self._track = SliderTrack(self)
        self._fill = SliderFill(self)
        self._handle = SliderHandle(self,10)

        if self._orientation == self.Orientation.Horizontal:
            self.setFixedHeight(2*self._handle_radius)
        elif self._orientation == self.Orientation.Vertical:
            self._fill.backgroundStyle.reverse = True
            self.setFixedWidth(2*self._handle_radius)

        self._style_data: ZSliderStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)
        ZGlobal.themeManager.themeChanged.connect(self._theme_changed_handler)
        self.setValue(value)

        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet('background:transparent;border:1px solid red;')
    @property
    def autoStripZero(self):
        return self._auto_strip_zero

    @autoStripZero.setter
    def autoStripZero(self, value: bool):
        self._auto_strip_zero = value

    @property
    def value(self):
        if self._accuracy >= 1:
            return int(round(self._value))
        else:
            decimal_places = max(0, len(str(self._accuracy).split('.')[-1]))
            return round(self._value, decimal_places)

    @property
    def displayValue(self):
        if self._accuracy >= 1:
            return str(int(round(self._value)))
        else:
            decimal_places = max(0, len(str(self._accuracy).split('.')[-1]))
            s = f"{self._value:.{decimal_places}f}"
            if self._auto_strip_zero:
                # 去掉多余的0和小数点
                s = s.rstrip('0').rstrip('.') if '.' in s else s
            return s

    @value.setter
    def value(self, value: int | float):
        clamped = max(self._min, min(value, self._max))
        self._value = clamped
        self._percentage = (self._value - self._min) / (self._max - self._min)
        self._update_value()
        self.valueChanged.emit(self._value)



    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope: tuple):
        self._scope = scope
        self._max = scope[1]
        self._min = scope[0]
        self.setValue(self._value)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max: int | float):
        self._max = max 
        self._scope = (self._min, self._max)
        self.setValue(self._value)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, min: int | float):
        self._min = min
        self._scope = (self._min, self._max)
        self.setValue(self._value)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step: int | float):
        self._step = max(step, self._accuracy)

    @property
    def stepMultiplier(self):
        return self._step_multiplier

    @stepMultiplier.setter
    def stepMultiplier(self, step_multiplier: int):
        self._step_multiplier = step_multiplier

    @property
    def accuracy(self):
        return self._accuracy

    @accuracy.setter
    def accuracy(self, accuracy: int | float):
        self._accuracy = accuracy
        self._step = max(self._step, accuracy)
        self.setValue(self._value)


    @property
    def percentage(self):
        return self._percentage

    @property
    def orientation(self):
        return self._orientation

    @property
    def track(self):
        return self._track

    @property
    def fill(self):
        return self._fill

    @property
    def handle(self):
        return self._handle


    @property
    def styleData(self):
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZSliderStyleData):
        self._style_data = style_data
        self._track.backgroundStyle.color = style_data.Track
        self._track.borderStyle.color = style_data.TrackBorder
        self._track.cornerStyle.radius = style_data.Radius
        self._fill.backgroundStyle.colorStart = style_data.TrackFilledStart
        self._fill.backgroundStyle.colorEnd = style_data.TrackFilledEnd
        self._fill.borderStyle.color = style_data.TrackBorder
        self._fill.cornerStyle.radius = style_data.Radius
        self._handle.innerStyle.color = style_data.HandleInner
        self._handle.outerStyle.color = style_data.HandleOuter
        self._handle.borderStyle.color = style_data.HandleBorder
        self.update()


    def _theme_changed_handler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__, theme.name)
        self._track.backgroundStyle.setColorTo(self._style_data.Track)
        self._track.borderStyle.setColorTo(self._style_data.TrackBorder)
        self._track.cornerStyle.radius = self._style_data.Radius
        self._fill.backgroundStyle.setColorTo(self._style_data.TrackFilledStart,self._style_data.TrackFilledEnd)
        self._fill.borderStyle.setColorTo(self._style_data.TrackBorder)
        self._fill.cornerStyle.radius = self._style_data.Radius
        self._handle.innerStyle.setColorTo(self._style_data.HandleInner)
        self._handle.outerStyle.setColorTo(self._style_data.HandleOuter)
        self._handle.borderStyle.setColorTo(self._style_data.HandleBorder)

    @overload
    def stepValue(self, step: int, multiplier: int = 1) -> None:
        "根据步长调整值，使用自定义步进倍数"
        ...

    @overload
    def stepValue(self, step: int) -> None:
        "根据步长调整值，使用默认的步进倍数"
        ...

    def stepValue(self, *args) -> None:
        if len(args) == 1:
            new_value = self._value + args[0] * self._step * self._step_multiplier
            self.setValue(new_value)
        elif len(args) == 2:
            new_value = self._value + args[0] * self._step * args[1]
            self.setValue(new_value)


    def setValue(self, value: int | float):
        clamped = max(self._min, min(value, self._max))
        self._value = clamped
        self._percentage = (self._value - self._min) / (self._max - self._min)
        self._update_value()
        self.valueChanged.emit(self._value)


    def setFixedLength(self, length: int):
        """设置滑块长度为固定值"""
        self._fixed_length = max(length, self._min_length)
        if self._orientation == self.Orientation.Horizontal:
            self.setFixedWidth(self._fixed_length + self._handle_radius * 2)
        else:
            self.setFixedHeight(self._fixed_length + self._handle_radius * 2)
        self._update_track()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 轨道长度不小于最小长度
        if self._fixed_length is None:
            if self._orientation == self.Orientation.Horizontal:
                self._track_length = max(self._min_length, self.width() - self._handle_radius * 2)
            else:
                self._track_length = max(self._min_length, self.height() - self._handle_radius * 2)
        else:
            self._track_length = max(self._min_length, self._fixed_length)
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
                self.stepValue(-1)
                ZGlobal.tooltip.setText(self.displayValue)
                event.accept()
                return
            elif event.key() == Qt.Key_Right:
                self.stepValue(1)
                ZGlobal.tooltip.setText(self.displayValue)
                event.accept()
                return
        else:  # 垂直方向
            if event.key() == Qt.Key_Up:
                self.stepValue(1)
                ZGlobal.tooltip.setText(self.displayValue)
                event.accept()
                return
            elif event.key() == Qt.Key_Down:
                self.stepValue(-1)
                ZGlobal.tooltip.setText(self.displayValue)
                event.accept()
                return
        super().keyPressEvent(event)


    def wheelEvent(self, event: QWheelEvent):
        """处理鼠标滚轮事件"""
        steps = event.angleDelta().y() / 120
        self.stepValue(steps)
        ZGlobal.tooltip.setText(self.displayValue)
        ZGlobal.tooltip.setInsideOf(self)
        ZGlobal.tooltip.showTip()
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

    def sizeHint(self):
        if self._orientation == self.Orientation.Horizontal:
            if self._fixed_length is None:
                return QSize(self._min_length + self._handle_radius * 2, self._track_width)
            else:
                w = max(self._fixed_length, self._min_length)
                return QSize(w + self._handle_radius * 2, self._track_width)
        else:
            if self._fixed_length is None:
                return QSize(self._track_width, self._min_length + self._handle_radius * 2)
            else:
                h = max(self._fixed_length, self._min_length)
                return QSize(self._track_width, h + self._handle_radius * 2)


    def _update_track(self) -> None:
        """更新轨道和填充条"""
        if self._orientation == self.Orientation.Horizontal:
            y = (self.height() - self._track_width) / 2
            # 更新轨道
            geo_track = QRect(self._handle_radius, y, self._track_length, self._track_width)
            self._track.setGeometry(geo_track)
            # 更新填充条
            geo_fill = QRect(self._handle_radius, y, self._percentage * self._track_length, self._track_width)
            self._fill.setGeometry(geo_fill)
            # 更新滑块
            self._handle.move(self._percentage * self._track_length, 0)
            return
        x = (self.width() - self._track_width) / 2
        # 更新轨道
        geo_track = QRect(x, self._handle_radius, self._track_width, self._track_length)
        self._track.setGeometry(geo_track)
        # 更新填充条
        fill_height = self._percentage * self._track_length
        geo_fill = QRect(x, self._track_length - fill_height + self._handle_radius, self._track_width, fill_height)
        self._fill.setGeometry(geo_fill)
        # 更新滑块
        self._handle.move(0, self._track_length - self._percentage * self._track_length)

    def _update_value(self) -> None:
        """更新滑块值"""
        if self._orientation == self.Orientation.Horizontal:
            # 更新填充条
            size_fill = QSize(self._percentage * self._track_length, self._track_width)
            self._fill.resize(size_fill)
            # 更新滑块
            handle_pos = QPoint(self._percentage * self._track_length, 0)
            self._handle.moveAnimation.moveTo(handle_pos)
            return
        x = (self.width() - self._track_width) / 2
        # 更新填充条
        fill_height = self._percentage * self._track_length
        geo_fill = QRect(x, self._track_length - fill_height + self._handle_radius, self._track_width, fill_height)
        self._fill.setGeometry(geo_fill)
        # 更新滑块
        self._handle.moveAnimation.moveTo(0, self._track_length - self._percentage * self._track_length)
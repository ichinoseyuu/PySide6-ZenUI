from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import IntEnum
from typing import overload
from ZenUI.component.base import StyleData
from ZenUI.core import ZGlobal, ZSliderStyleData,TipPos
from .fill import SliderFill
from .track import SliderTrack
from .handle import SliderHandle

class ZSlider(QWidget):
    class Orientation(IntEnum):
        Horizontal = 0
        Vertical = 1

    class Weight(IntEnum):
        Thin = 4
        Normal = 5
        Thick = 6

    valueChanged = Signal(object)
    displayValueChanged = Signal(str)

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 orientation: Orientation = Orientation.Horizontal,
                 weight: Weight = Weight.Normal,
                 scope: tuple[int, int] | tuple[float, float] = (0, 100),
                 step: int = 1,
                 step_multiplier: int = 1,
                 accuracy: float = 1,
                 value: int = 0,
                 auto_strip_zero: bool = False):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._orientation = orientation
        self._weight = weight
        self._scope = scope
        self._min, self._max = scope
        self._step = max(step, accuracy)
        self._step_multiplier = step_multiplier
        self._accuracy = accuracy
        self._auto_strip_zero = auto_strip_zero

        self._value: int | float = 0
        self._percentage: float = 0.0

        self._track_width: int = self._weight.value
        self._track_length: int = 0
        self._track_start: int = 0
        self._track_end: int = 0
        self._handle_radius: int = 10
        self._min_length: int = 200
        self._fixed_track_length = None

        self._track = SliderTrack(self)
        self._fill = SliderFill(self)
        self._handle = SliderHandle(self,10)

        self._style_data = StyleData[ZSliderStyleData](self, 'ZSlider')
        self._style_data.styleChanged.connect(self._styleChangeHandler)

        self._handle.locationCtrl.animation.valueChanged.connect(self._update_fill)
        self._initStyle(value)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet('background:transparent;border:1px solid red;')

    @property
    def percentage(self): return self._percentage

    @property
    def orientation(self): return self._orientation

    @property
    def isHorizontal(self): return self._orientation == self.Orientation.Horizontal

    @property
    def isVertical(self): return self._orientation == self.Orientation.Vertical

    @property
    def track(self): return self._track

    @property
    def fill(self): return self._fill

    @property
    def handle(self): return self._handle

    @property
    def styleData(self): return self._style_data

    @property
    def weight(self): return self._weight
    @weight.setter
    def weight(self, weight: Weight):
        self._weight = weight
        self._track_width = self._weight.value
        self._update_track()

    @property
    def autoStripZero(self): return self._auto_strip_zero
    @autoStripZero.setter
    def autoStripZero(self, value: bool):
        self._auto_strip_zero = value

    @property
    def scope(self): return self._scope
    @scope.setter
    def scope(self, scope: tuple):
        self._scope = scope
        self._max = scope[1]
        self._min = scope[0]
        self.setValue(self._value)

    @property
    def max(self): return self._max
    @max.setter
    def max(self, max: int | float):
        self._max = max 
        self._scope = (self._min, self._max)
        self.setValue(self._value)

    @property
    def min(self): return self._min
    @min.setter
    def min(self, min: int | float):
        self._min = min
        self._scope = (self._min, self._max)
        self.setValue(self._value)

    @property
    def step(self): return self._step
    @step.setter
    def step(self, step: int | float):
        self._step = max(step, self._accuracy)

    @property
    def stepMultiplier(self): return self._step_multiplier
    @stepMultiplier.setter
    def stepMultiplier(self, step_multiplier: int):
        self._step_multiplier = step_multiplier

    @property
    def accuracy(self): return self._accuracy
    @accuracy.setter
    def accuracy(self, accuracy: int | float):
        self._accuracy = accuracy
        self._step = max(self._step, accuracy)
        self.setValue(self._value)

    @property
    def value(self):
        if self._accuracy >= 1:
            return int(round(self._value))
        decimal_places = max(0, len(str(self._accuracy).split('.')[-1]))
        return round(self._value, decimal_places)
    @value.setter
    def value(self, value: float):
        self.setValue(value)

    @property
    def displayValue(self):
        if self._accuracy >= 1:
            s = str(int(round(self._value)))
        else:
            decimal_places = max(0, len(str(self._accuracy).split('.')[-1]))
            s = f"{self._value:.{decimal_places}f}"
            if self._auto_strip_zero:
                s = s.rstrip('0').rstrip('.') if '.' in s else s
        return s

    def _initStyle(self, value):
        if self.isHorizontal:
            self._fill.bodyColorCtrl.direction = 0
            self.setFixedHeight(2 * self._handle_radius)
            self.setMinimumWidth(self._min_length + self._handle_radius * 2)
        else:
            self._fill.bodyColorCtrl.reverse = True
            self._fill.bodyColorCtrl.direction = 1
            self.setFixedWidth(2 * self._handle_radius)
            self.setMinimumHeight(self._min_length + self._handle_radius * 2)
        self._update_track_radius()
        self.setValue(value)
        data = self._style_data.data
        self._track.bodyColorCtrl.color = data.Track
        self._track.borderColorCtrl.color = data.TrackBorder
        self._fill.bodyColorCtrl.colorStart = data.FillAreaStart
        self._fill.bodyColorCtrl.colorEnd = data.FillAreaEnd
        self._fill.borderColorCtrl.color = data.FillAreaBorder
        self._handle.innerColorCtrl.color = data.HandleInner
        self._handle.outerColorCtrl.color = data.HandleOuter
        self._handle.borderColorCtrl.color = data.HandleBorder
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._track.bodyColorCtrl.setColorTo(data.Track)
        self._track.borderColorCtrl.setColorTo(data.TrackBorder)
        self._fill.bodyColorCtrl.setColorTo(data.FillAreaStart, data.FillAreaEnd)
        self._fill.borderColorCtrl.setColorTo(data.FillAreaBorder)
        self._handle.innerColorCtrl.setColorTo(data.HandleInner)
        self._handle.outerColorCtrl.setColorTo(data.HandleOuter)
        self._handle.borderColorCtrl.setColorTo(data.HandleBorder)

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
        self.valueChanged.emit(self.value)
        self.displayValueChanged.emit(self.displayValue)


    def setFixedLength(self, length: int):
        """设置滑块长度为固定值"""
        self._fixed_track_length = length
        self._update_track()


    def keyPressEvent(self, event: QKeyEvent):
        if self.isHorizontal and (event.key() == Qt.Key_Left or event.key() == Qt.Key_Right):
            step = -1 if event.key() == Qt.Key_Left else 1
            self.stepValue(step)
            ZGlobal.tooltip.showTip(
                text=self.displayValue,
                target=self._handle,
                mode=ZGlobal.tooltip.Mode.TrackTarget,
                position=TipPos.Top,
                hide_delay=1000)
        elif self.isVertical and (event.key() == Qt.Key_Up or event.key() == Qt.Key_Down):
            step = 1 if event.key() == Qt.Key_Up else -1
            self.stepValue(step)
            ZGlobal.tooltip.showTip(
                text=self.displayValue,
                target=self._handle,
                mode=ZGlobal.tooltip.Mode.TrackTarget,
                position=TipPos.Left,
                hide_delay=1000)
        event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            start = self._track_start
            end = self._track_end
            length = self._track_length
            if self.isHorizontal:
                # 限制点击范围
                x = min(max(event.x(), start), end)
                percent = (x - start) / length
                value = self._min + percent * (self._max - self._min)
            else:
                y = min(max(event.y(), start), end)
                # 垂直方向是反向
                percent = 1 - (y - start) / length
                value = self._min + percent * (self._max - self._min)
            self.setValue(value)
            self._handle.enterEvent(None)


    def wheelEvent(self, event: QWheelEvent):
        """处理鼠标滚轮事件"""
        steps = event.angleDelta().y() / 120
        self.stepValue(steps)
        if self.isHorizontal:
            ZGlobal.tooltip.showTip(
                text = self.displayValue,
                target = self._handle,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = TipPos.Top,
                hide_delay= 1000)
        else:
            ZGlobal.tooltip.showTip(
                text = self.displayValue,
                target = self._handle,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = TipPos.Left,
                hide_delay= 1000)
        event.accept()

    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        # 开启鼠标追踪
        self.setMouseTracking(True)
        # 设置焦点以接收滚轮事件
        self.setFocus()

    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        self._handle.leaveEvent(None)
        # 关闭鼠标追踪
        self.setMouseTracking(False)
        self.clearFocus()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_track()


    def sizeHint(self):
        if self.isHorizontal:
            w = max(self._fixed_track_length or self._min_length, self._min_length)
            return QSize(w + self._handle_radius * 2, self._track_width)
        else:
            h = max(self._fixed_track_length or self._min_length, self._min_length)
            return QSize(self._track_width, h + self._handle_radius * 2)


    def _calc_track_length(self):
        if self._fixed_track_length is not None:
            return max(self._min_length, self._fixed_track_length)
        if self.isHorizontal:
            return max(self._min_length, self.width() - self._handle_radius * 2)
        else:
            return max(self._min_length, self.height() - self._handle_radius * 2)


    def _update_track_radius(self):
        self._track.radiusCtrl.value = self._track_width / 2
        self._fill.radiusCtrl.value = self._track_width / 2

    def _update_track(self):
        # 更新轨道,resizeEvent时调用
        length = self._track_length = self._calc_track_length()
        start = self._track_start = self._handle_radius
        end = self._track_end = start + length
        width = self._track_width
        percentage = self._percentage
        self._update_track_radius()
        if self.isHorizontal:
            y = (self.height() - width) // 2
            geo_track = QRect(start, y, length, width)
            self._track.setGeometry(geo_track)
            geo_fill = QRect(start, y, length * percentage, width)
            self._fill.setGeometry(geo_fill)
            self._handle.move(length * percentage, 0)
        else:
            x = (self.width() - width) // 2
            geo_track = QRect(x, start, width, length)
            self._track.setGeometry(geo_track)
            fill_height = length * percentage
            geo_fill = QRect(x, end - fill_height, width, fill_height)
            self._fill.setGeometry(geo_fill)
            self._handle.move(0, length - length * percentage)


    def _update_value(self):
        #更新值/更新滑块位置
        if self.isHorizontal:
            handle_pos = QPoint(self._percentage * self._track_length, 0)
            self._handle.locationCtrl.moveTo(handle_pos)
        else:
            self._handle.locationCtrl.moveTo(0, self._track_length - self._percentage * self._track_length)


    def _update_fill(self):
        #handle位置改变时的fill条更新逻辑，让fill始终随着handle移动
        if self.isHorizontal:
            size_fill = QSize(self._handle.x(), self._track_width)
            self._fill.resize(size_fill)
        else:
            x = (self.width() - self._track_width) / 2
            geo_fill = QRect(x, self._handle.y() + self._track_start,
                             self._track_width, self._track_length - self._handle.y())
            self._fill.setGeometry(geo_fill)


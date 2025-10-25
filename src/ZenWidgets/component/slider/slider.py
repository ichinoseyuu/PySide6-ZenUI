from dataclasses import dataclass
from enum import Enum
from typing import overload
from PySide6.QtCore import QPoint,QPointF,QRect,QRectF,QSize,Qt,Signal
from PySide6.QtGui import QPainter,QPen,QLinearGradient,QPainterPath,QKeyEvent,QMouseEvent,QWheelEvent
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.base import (
    QAnimatedColor,
    QAnimatedLinearGradient,
    QAnimatedFloat,
    StyleController,
    ZWidget
)
from ZenWidgets.core import (
    ZGlobal,
    ZSliderStyleData,
    ZDebug,
    ZPosition,
    ZDirection
)
# region SliderFill
class SliderFill(ZWidget):
    bodyColorCtrl: QAnimatedLinearGradient
    borderColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = max(0.0, float(self.radiusCtrl.value))
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        x1, y1, x2, y2 = self.bodyColorCtrl.linearPoints
        gradient = QLinearGradient(
            rect.left() + rect.width() * x1,
            rect.top() + rect.height() * y1,
            rect.left() + rect.width() * x2,
            rect.top() + rect.height() * y2
        )
        if not self.bodyColorCtrl.reverse:
            gradient.setColorAt(0.0, self.bodyColorCtrl.colorStart)
            gradient.setColorAt(1.0, self.bodyColorCtrl.colorEnd)
        else:
            gradient.setColorAt(0.0, self.bodyColorCtrl.colorEnd)
            gradient.setColorAt(1.0, self.bodyColorCtrl.colorStart)

        painter.fillPath(path, gradient)

        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1.0))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()

# region SliderTrack
class SliderTrack(ZWidget):
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = max(0.0, float(self.radiusCtrl.value))

        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1.0))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()

# region SliderHandle
class SliderHandle(ZWidget):
    innerColorCtrl: QAnimatedColor
    outerColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    innerScaleCtrl: QAnimatedFloat
    outerScaleCtrl: QAnimatedFloat

    def __init__(self, parent: QWidget = None, radius: int = 6):
        super().__init__(parent)
        self._radius = radius
        self._inner_scale_normal = 0.4
        self._inner_scale_hover = 0.6
        self._inner_scale_pressed = 0.5
        self._inner_scale_released = 0.6
        self._outer_scale_normal = 0.8
        self._outer_scale_hover = 1.0
        self._outer_scale_pressed = 1.0
        self._outer_scale_released = 1.0
        self.innerScaleCtrl.setValue(self._inner_scale_normal)
        self.outerScaleCtrl.setValue(self._outer_scale_normal)
        self.setFixedSize(2 * radius, 2 * radius)

    def parent(self) -> 'ZSlider':
        return super().parent()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(self.width() * 0.5, self.height() * 0.5)
        base_radius = max(0.0, min(self.width(), self.height()) * 0.5 - 1.0)

        if self.outerColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.outerColorCtrl.color)
            outer_radius = base_radius * float(self.outerScaleCtrl.value)
            painter.drawEllipse(center, outer_radius, outer_radius)

        if self.innerColorCtrl.color.alpha() > 0:
            inner_radius = base_radius * float(self.innerScaleCtrl.value)
            painter.setBrush(self.innerColorCtrl.color)
            painter.drawEllipse(center, inner_radius, inner_radius)

        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1.0))
            border_radius = base_radius * float(self.outerScaleCtrl.value)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(center, border_radius, border_radius)
        painter.end()

    def _show_handle_tooltip(self):
        parent = self.parent()
        pos = ZPosition.Top if parent.isHorizontal() else ZPosition.Left
        ZGlobal.tooltip.showTip(
            text=parent.displayValue,
            target=self,
            mode=ZGlobal.tooltip.Mode.TrackTarget,
            position=pos,
            hide_delay=1000
        )

    def mousePressEvent(self, event):
        self.innerScaleCtrl.setValueTo(self._inner_scale_pressed)
        self.outerColorCtrl.setAlphaTo(150)
        self.borderColorCtrl.setAlphaTo(150)

    def mouseMoveEvent(self, event):
        slider = self.parent()
        global_pos = event.globalPos()
        local_pos = slider.mapFromGlobal(global_pos) - QPoint(self._radius, self._radius)
        if slider.isHorizontal():
            x = int(max(0, min(local_pos.x(), slider._track_length)))
            slider.setValue(x / max(1, slider._track_length) * slider._max_value)
        else:
            y = int(max(0, min(local_pos.y(), slider._track_length)))
            slider.setValue(slider._max_value - y / max(1, slider._track_length) * slider._max_value)
        self._show_handle_tooltip()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.innerScaleCtrl.setValueTo(self._inner_scale_released)
        self.outerColorCtrl.setAlphaTo(255)
        self.borderColorCtrl.setAlphaTo(255)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.innerScaleCtrl.setValueTo(self._inner_scale_hover)
        self.outerScaleCtrl.setValueTo(self._outer_scale_hover)
        self._show_handle_tooltip()

    def leaveEvent(self, event):
        self.innerScaleCtrl.setValueTo(self._inner_scale_normal)
        self.outerScaleCtrl.setValueTo(self._outer_scale_normal)
        ZGlobal.tooltip.hideTipDelayed(500)

@dataclass
class SliderStyle:
    TrackWidth: int
    HandleRadius: int

# region ZSlider
class ZSlider(ZWidget):
    valueChanged = Signal(object)
    displayValueChanged = Signal(str)
    styleDataCtrl: StyleController[ZSliderStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZSlider'}}

    class Style(Enum):
        Thin = SliderStyle(TrackWidth=4, HandleRadius=10)
        Normal = SliderStyle(TrackWidth=6, HandleRadius=12)
        Thick = SliderStyle(TrackWidth=8, HandleRadius=14)

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 direction: ZDirection = ZDirection.Horizontal,
                 style: Style = Style.Normal,
                 scope: tuple[int, int] | tuple[float, float] = (0, 100),
                 step: int|float = 1,
                 step_multiplier: int = 1,
                 accuracy: float = 1,
                 value: int|float = 0,
                 auto_strip_zero: bool = False,
                 length: int = 150
                 ) -> None:
        super().__init__(parent)
        if name: self.setObjectName(name)
        if direction not in (ZDirection.Horizontal, ZDirection.Vertical): raise ValueError('Invalid direction')
        self._dir = direction
        self._style = style
        self._scope = scope
        self._min_value, self._max_value = scope
        self._step = max(step, accuracy)
        self._step_multiplier = step_multiplier
        self._accuracy = accuracy
        self._auto_strip_zero = auto_strip_zero

        self._value: int | float = 0
        self._percentage: float = 0.0

        self._track_width: int = self._style.value.TrackWidth
        self._track_length: int = 0
        self._track_start: int = 0
        self._track_end: int = 0
        self._handle_radius: int = self._style.value.HandleRadius
        self._min_length: int = max(150, length)

        self._track = SliderTrack(self)
        self._fill = SliderFill(self)
        self._handle = SliderHandle(self, self._handle_radius)

        self._handle.widgetPositionCtrl.animation.valueChanged.connect(self._update_fill)
        self._init_style_(value)
        self.resize(self.sizeHint())

    # region public
    @property
    def percentage(self) -> float: return self._percentage

    @property
    def direction(self) -> ZDirection: return self._dir

    def isHorizontal(self) -> bool: return self._dir == ZDirection.Horizontal

    def isVertical(self) -> bool: return self._dir == ZDirection.Vertical

    @property
    def autoStripZero(self) -> bool: return self._auto_strip_zero

    @autoStripZero.setter
    def autoStripZero(self, v: bool):
        self._auto_strip_zero = v

    def setAutoStripZero(self, v: bool):
        self.autoStripZero = v

    @property
    def maxValue(self): return self._max_value

    @maxValue.setter
    def maxValue(self, m: int | float):
        self._max_value = m
        self._scope = (self._min_value, self._max_value)
        self.setValue(self._value)

    def setMaxValue(self, m: int | float):
        self.maxValue = m

    @property
    def minValue(self): return self._min_value

    @minValue.setter
    def minValue(self, m: int | float):
        self._min_value = m
        self._scope = (self._min_value, self._max_value)
        self.setValue(self._value)

    def setMinValue(self, m: int | float):
        self.minValue = m

    @property
    def step(self) -> int | float: return self._step

    @step.setter
    def step(self, s: int | float):
        self._step = max(s, self._accuracy)

    def setStep(self, s: int | float):
        self._step = max(s, self._accuracy)

    @property
    def stepMultiplier(self) -> int: return self._step_multiplier

    @stepMultiplier.setter
    def stepMultiplier(self, step_multiplier: int):
        self._step_multiplier = step_multiplier

    def setStepMultiplier(self, step_multiplier: int):
        self._step_multiplier = step_multiplier

    @property
    def accuracy(self) -> float | int: return self._accuracy

    @accuracy.setter
    def accuracy(self, accuracy: int | float):
        self._accuracy = accuracy
        self._step = max(self._step, accuracy)
        self.setValue(self._value)

    def setAccuracy(self, accuracy: int | float):
        self.accuracy = accuracy

    @property
    def sliderStyle(self) -> Style: return self._style

    @sliderStyle.setter
    def sliderStyle(self, s: Style):
        self._style = s
        self._track_width = self._style.value
        self._update_track()

    def setSliderStyle(self, s: Style):
        self.sliderStyle = s

    @property
    def scope(self): return self._scope

    @scope.setter
    def scope(self, s: tuple):
        self._scope = s
        self._max_value = s[1]
        self._min_value = s[0]
        self.setValue(self._value)

    def setScope(self, s: tuple):
        self.scope = s

    @property
    def displayValue(self) -> str:
        if self._accuracy >= 1:
            s = str(int(round(self._value)))
        else:
            decimal_places = max(0, len(str(self._accuracy).split('.')[-1]))
            s = f"{self._value:.{decimal_places}f}"
            if self._auto_strip_zero:
                s = s.rstrip('0').rstrip('.') if '.' in s else s
        return s

    @property
    def value(self) -> int | float:
        if self._accuracy >= 1:
            return int(round(self._value))
        decimal_places = max(0, len(str(self._accuracy).split('.')[-1]))
        return round(self._value, decimal_places)

    @value.setter
    def value(self, value: float):
        clamped = max(self._min_value, min(value, self._max_value))
        self._value = clamped
        self._percentage = (self._value - self._min_value) / (self._max_value - self._min_value)
        self._update_value()
        self.valueChanged.emit(self.value)
        self.displayValueChanged.emit(self.displayValue)

    def setValue(self, value: int | float):
        self.value = value

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

    def adjustSize(self):
        self.resize(self.sizeHint())


    def sizeHint(self) -> QSize:
        if self.isHorizontal():
            return QSize(self._min_length + self._handle_radius * 2, self._track_width)
        else:
            return QSize(self._track_width, self._min_length + self._handle_radius * 2)

    # region private
    def _init_style_(self, value):
        # orientation-specific defaults
        if self.isHorizontal():
            self._fill.bodyColorCtrl.direction = 0
            self.setFixedHeight(2 * self._handle_radius)
            self.setMinimumWidth(self._min_length + self._handle_radius * 2)
        else:
            self._fill.bodyColorCtrl.reverse = True
            self._fill.bodyColorCtrl.direction = 1
            self.setFixedWidth(2 * self._handle_radius)
            self.setMinimumHeight(self._min_length + self._handle_radius * 2)

        self._update_track_radius()

        clamped = max(self._min_value, min(value, self._max_value))
        self._value = clamped
        self._percentage = (self._value - self._min_value) / (self._max_value - self._min_value)

        if self.isHorizontal():
            handle_pos = QPoint(self._percentage * self._track_length, 0)
            self._handle.widgetPositionCtrl.setPos(handle_pos)
        else:
            handle_pos = QPoint(0, self._track_length - self._percentage * self._track_length)
            self._handle.widgetPositionCtrl.setPos(handle_pos)

        data = self.styleDataCtrl.data
        self._track.bodyColorCtrl.color = data.Track
        self._track.borderColorCtrl.color = data.TrackBorder
        self._fill.bodyColorCtrl.colorStart = data.FillAreaStart
        self._fill.bodyColorCtrl.colorEnd = data.FillAreaEnd
        self._fill.borderColorCtrl.color = data.FillAreaBorder
        self._handle.innerColorCtrl.color = data.HandleInner
        self._handle.outerColorCtrl.color = data.HandleOuter
        self._handle.borderColorCtrl.color = data.HandleBorder
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self._track.bodyColorCtrl.setColorTo(data.Track)
        self._track.borderColorCtrl.setColorTo(data.TrackBorder)
        self._fill.bodyColorCtrl.setColorsTo(data.FillAreaStart, data.FillAreaEnd)
        self._fill.borderColorCtrl.setColorTo(data.FillAreaBorder)
        self._handle.innerColorCtrl.setColorTo(data.HandleInner)
        self._handle.outerColorCtrl.setColorTo(data.HandleOuter)
        self._handle.borderColorCtrl.setColorTo(data.HandleBorder)

    def _calc_track_length(self):
        if self.isHorizontal():
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

        if self.isHorizontal():
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
        # move handle smoothly via position controller
        if self.isHorizontal():
            self._handle.widgetPositionCtrl.moveTo(int(self._percentage * self._track_length), 0)
        else:
            self._handle.widgetPositionCtrl.moveTo(0, int(self._track_length - self._percentage * self._track_length))

    def _update_fill(self):
        # keep fill synchronized with handle
        if self.isHorizontal():
            size_fill = QSize(self._handle.x(), self._track_width)
            self._fill.resize(size_fill)
        else:
            x = (self.width() - self._track_width) / 2
            geo_fill = QRect(x, self._handle.y() + self._track_start,
                             self._track_width, self._track_length - self._handle.y())
            self._fill.setGeometry(geo_fill)

    def _show_tooltip(self):
        pos = ZPosition.Top if self.isHorizontal() else ZPosition.Left
        ZGlobal.tooltip.showTip(
            text=self.displayValue,
            target=self._handle,
            mode=ZGlobal.tooltip.Mode.TrackTarget,
            position=pos,
            hide_delay=1000
        )
    # region event
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_track()
        self.adjustSize()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

    def keyPressEvent(self, event: QKeyEvent):
        if self.isHorizontal() and (event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_Right):
            step = -1 if event.key() == Qt.Key.Key_Left else 1
            self.stepValue(step)
        elif self.isVertical() and (event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down):
            step = 1 if event.key() == Qt.Key.Key_Up else -1
            self.stepValue(step)
        self._show_tooltip()
        event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            start = self._track_start
            end = self._track_end
            length = self._track_length
            if self.isHorizontal():
                x = min(max(event.x(), start), end)
                percent = (x - start) / length
                value = self._min_value + percent * (self._max_value - self._min_value)
            else:
                y = min(max(event.y(), start), end)
                percent = 1 - (y - start) / length
                value = self._min_value + percent * (self._max_value - self._min_value)
            self.setValue(value)
            self._handle.enterEvent(None)

    def wheelEvent(self, event: QWheelEvent):
        steps = event.angleDelta().y() / 120
        self.stepValue(steps)
        self._show_tooltip()
        event.accept()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setMouseTracking(True)
        self.setFocus()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._handle.leaveEvent(None)
        self.setMouseTracking(False)
        self.clearFocus()
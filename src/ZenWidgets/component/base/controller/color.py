from typing import overload,cast
from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject,QPropertyAnimation,QEasingCurve,Property,Signal
from PySide6.QtGui import QColor
from ZenWidgets.core import ZDirection,ZExpPropertyAnimation
from typing import TYPE_CHECKING
if TYPE_CHECKING: from ZenWidgets.component.window.framelesswindow import ZFramelessWindow

# region ABCAnimatedColor
class ABCAnimatedColor(QObject):
    colorChanged = Signal()
    def __init__(self, parent: QWidget, color: QColor = QColor()):
        super().__init__(parent)
        self._anim: ZExpPropertyAnimation|QPropertyAnimation|None = None
        self._color: QColor = color

    @property
    def animation(self): raise NotImplementedError

    def _update_(self): raise NotImplementedError

    def getColor(self) -> QColor: return self._color

    def setColor(self, value: QColor):
        self._color = QColor(value)
        self._update_()

    color: QColor = cast(QColor, Property(QColor, getColor, setColor, notify=colorChanged))

    @overload
    def setColorTo(self, color: QColor,/) -> None: ...

    @overload
    def setColorTo(self, start: QColor, end: QColor,/) -> None: ...

    def setColorTo(self, arg1: QColor, arg2: QColor | None = None,/) -> None:
        self._anim.stop()
        if arg2 is None:
            self._anim.setStartValue(self._color)
            self._anim.setEndValue(QColor(arg1))
        else:
            self._anim.setStartValue(QColor(arg1))
            self._anim.setEndValue(QColor(arg2))
        self._anim.start()

    def transparent(self):
        self.color.setAlpha(0)
        self._update_()

    def toTransparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColorTo(target)

    def opaque(self):
        self.color.setAlpha(255)
        self._update_()

    def toOpaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColorTo(target)

    def setAlpha(self, alpha: int,/) -> None:
        self.color.setAlpha(alpha)
        self._update_()

    def setAlphaTo(self, alpha: int,/) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColorTo(target)

    def setAlphaF(self, alpha: float,/) -> None:
        self.color.setAlphaF(alpha)
        self._update_()

    def setAlphaFTo(self, alpha: float,/) -> None:
        target = QColor(self._color)
        target.setAlphaF(alpha)
        self.setColorTo(target)

    def stopAnimation(self) -> None:
        self._anim.stop()

# region QAnimatedWindowBody
class QAnimatedWindowBody(ABCAnimatedColor):
    '''具有原生属性动画的窗口背景控制器，直接作用于 windows 系统的窗口'''
    def __init__(self, window: 'ZFramelessWindow', color: QColor = QColor('#202020')):
        super().__init__(window, color)
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def _update_(self):
        self.parent().windowEffect().setBackgroundColor(self.parent().winId(), self._color)

    def parent(self) -> 'ZFramelessWindow':
        return super().parent()

# region QAnimatedColor
class QAnimatedColor(ABCAnimatedColor):
    '''具有原生属性动画的颜色控制器'''
    def __init__(self, parent: QWidget, color: QColor = QColor('#202020')):
        super().__init__(parent, color)
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def _update_(self): self.parent().update()

    def parent(self) -> QWidget:
        return super().parent()

# region ZAnimatedColor
class ZAnimatedColor(QObject):
    '''具有原生属性动画的颜色控制器'''
    def __init__(self, parent: QWidget, color: QColor = QColor('#202020')):
        super().__init__(parent, color)
        self._color: QColor = color
        self._anim = ZExpPropertyAnimation(self, 'color')
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def _update_(self): self.parent().update()

    def parent(self) -> QWidget:
        return super().parent()

# region QAnimatedLinearGradient
class QAnimatedLinearGradient(QObject):
    '''具有原生属性动画的线性渐变颜色控制器'''
    def __init__(self, parent: QWidget, startColor: QColor = QColor('#202020'), endColor: QColor = QColor('#202020')):
        super().__init__(parent)
        self._start = QAnimatedColor(parent, startColor)
        self._end = QAnimatedColor(parent, endColor)
        self._direction: ZDirection = ZDirection.Diagonal
        self._reverse: bool = False
        self._linear_points: tuple[float, float, float, float] = (0, 0, 1, 1)

    @property
    def start(self) -> QAnimatedColor: return self._start

    @property
    def end(self) -> QAnimatedColor: return self._end

    @property
    def direction(self) -> ZDirection: return self._direction

    @direction.setter
    def direction(self, value: ZDirection) -> None:
        self._direction = value
        if self._direction is ZDirection.Horizontal:
            self._linear_points = (0, 0, 1, 0)
        elif self._direction is ZDirection.Vertical:
            self._linear_points = (0, 0, 0, 1)
        elif self._direction is ZDirection.Diagonal:
            self._linear_points = (0, 0, 1, 1)
        elif self._direction is ZDirection.DiagonalReverse:
            self._linear_points = (1, 0, 0, 1)
        self.parent().update()


    @property
    def reverse(self) -> bool: return self._reverse

    @reverse.setter
    def reverse(self, value: bool) -> None:
        self._reverse = value
        self.parent().update()


    @property
    def linearPoints(self) -> tuple[float, float, float, float]: return self._linear_points

    @linearPoints.setter
    def linearPoints(self, value: tuple[float, float, float, float]) -> None:
        self._linear_points = value
        self._direction = ZDirection.Custom
        self.parent().update()

    def parent(self) -> QWidget:
        return super().parent()
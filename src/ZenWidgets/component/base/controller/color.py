from typing import overload,cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject,QPropertyAnimation,QEasingCurve,Property,Signal,QRect,QRectF
from PySide6.QtGui import QColor,Qt,QPainter,QPen
from ZenWidgets.core import ZDirection,ZExpPropertyAnimation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ZenWidgets.component.window.framelesswindow import ZFramelessWindow

__All__ = [
    'ABCAnimatedColor',
    'ZAnimatedColor',
    'ZAnimatedLinearGradient',
    'ZWindowBackGround',
]

# region ABCAnimatedColor
class ABCAnimatedColor(QObject):
    """为 QColor 类型封装的动画抽象类，实现了透明度、颜色的动画控制等"""
    colorChanged = Signal()
    alphaFChanged = Signal()
    def __init__(self, parent: QWidget, color: QColor = QColor()):
        super().__init__(parent)
        self._color: QColor = color
        self._anim: ZExpPropertyAnimation|QPropertyAnimation|None = None
        self._anim_alpha: ZExpPropertyAnimation|QPropertyAnimation|None = None

    @property
    def animation(self): raise NotImplementedError

    @property
    def animationAlpha(self): raise NotImplementedError

    def _update_(self) -> None: raise NotImplementedError

    def getColor(self) -> QColor: return self._color

    def setColor(self, v: QColor,/) -> None: self._color = QColor(v); self._update_()

    color: QColor = cast(QColor, Property(QColor, getColor, setColor, notify=colorChanged))

    def getAlphaF(self) -> float: return self._color.alphaF()

    def setAlphaF(self, a: float,/) -> None: self._color.setAlphaF(a); self._update_()

    alphaF: float = cast(float, Property(float, getAlphaF, setAlphaF, notify=alphaFChanged))

    def transparent(self) -> None: self._color.setAlphaF(.0); self._update_()

    def opaque(self) -> None: self._color.setAlphaF(1.0); self._update_()

    def stopAnimation(self) -> None: self._anim.stop()

    def stopAnimationAlpha(self) -> None: self._anim_alpha.stop()

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

    @overload
    def setAlphaTo(self, alpha: int,/) -> None: ...

    @overload
    def setAlphaTo(self, start: int, end: int,/) -> None: ...

    def setAlphaTo(self, arg1: int, arg2: int | None = None,/) -> None:
        self._anim_alpha.stop()
        if arg2 is None:
            self._anim_alpha.setStartValue(self._color.alphaF())
            self._anim_alpha.setEndValue(float(arg1/255))
        else:
            self._anim_alpha.setStartValue(float(arg1/255))
            self._anim_alpha.setEndValue(float(arg1/255))
        self._anim_alpha.start()

    @overload
    def setAlphaFTo(self, alpha: int | float,/) -> None: ...

    @overload
    def setAlphaFTo(self, start: int | float, end: int | float,/) -> None: ...

    def setAlphaFTo(self, arg1: int | float, arg2: int | float | None = None,/) -> None:
        self._anim_alpha.stop()
        if arg2 is None:
            self._anim_alpha.setStartValue(self._color.alphaF())
            self._anim_alpha.setEndValue(float(arg1))
        else:
            self._anim_alpha.setStartValue(float(arg1))
            self._anim_alpha.setEndValue(float(arg1))
        self._anim_alpha.start()

    def toTransparent(self):
        self.setAlphaFTo(0.0)

    def toOpaque(self):
        self.setAlphaFTo(1.0)


# region ZAnimatedColor
class ZAnimatedColor(ABCAnimatedColor):
    '''具有原生属性动画的颜色控制器'''
    def __init__(self, parent: QWidget, color: QColor = QColor('#202020')):
        super().__init__(parent, color)
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)
        self._anim_alpha = QPropertyAnimation(self, b'alphaF')
        self._anim_alpha.setDuration(250)
        self._anim_alpha.setEasingCurve(QEasingCurve.Type.OutExpo)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    @property
    def animationAlpha(self) -> QPropertyAnimation: return self._anim_alpha

    def _update_(self): self.parent().update()

    def parent(self) -> QWidget:
        return super().parent()


# region ZAnimatedLinearGradient
class ZAnimatedLinearGradient(QObject):
    '''具有原生属性动画的线性渐变颜色控制器'''
    def __init__(self, parent: QWidget, startColor: QColor = QColor('#202020'), endColor: QColor = QColor('#202020')):
        super().__init__(parent)
        self._start = ZAnimatedColor(parent, startColor)
        self._end = ZAnimatedColor(parent, endColor)
        self._direction: ZDirection = ZDirection.Diagonal
        self._reverse: bool = False
        self._linear_points: tuple[float, float, float, float] = (0, 0, 1, 1)

    @property
    def start(self) -> ZAnimatedColor: return self._start

    @property
    def end(self) -> ZAnimatedColor: return self._end

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


# region ZWindowBackGround
class ZWindowBackGround(ABCAnimatedColor):
    '''具有原生属性动画的窗口背景控制器，直接作用于 windows 系统的窗口'''
    def __init__(self, window: 'ZFramelessWindow', color: QColor = QColor('#202020')):
        super().__init__(window, color)
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)
        self._anim_alpha = QPropertyAnimation(self, b'alphaF')
        self._anim_alpha.setDuration(250)
        self._anim_alpha.setEasingCurve(QEasingCurve.Type.OutExpo)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    @property
    def animationAlpha(self) -> QPropertyAnimation: return self._anim_alpha

    def _update_(self):
        self.parent().windowEffect().setBackgroundColor(self.parent().winId(), self._color)

    def parent(self) -> 'ZFramelessWindow':
        return super().parent()
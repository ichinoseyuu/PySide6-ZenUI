from typing import overload
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject,QPropertyAnimation,QEasingCurve,Property
from PySide6.QtGui import QColor
from ZenWidgets.core import ZDirection,ZExpPropertyAnimation
from typing import TYPE_CHECKING
if TYPE_CHECKING: from ZenWidgets.component.window.framelesswindow import ZFramelessWindow
# region QAnimatedWindowBody
class QAnimatedWindowBody(QObject):
    '''具有原生属性动画的窗口背景控制器，直接作用于 windows 系统的窗口'''
    def __init__(self, window: 'ZFramelessWindow', color: QColor = QColor('#202020')):
        super().__init__(window)
        self._color: QColor = color
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def getColor(self) -> QColor: return self._color

    def setColor(self, value: QColor):
        self._color = value
        self.parent().windowEffect.setBackgroundColor(self.parent().winId(), value)

    color: QColor = Property(QColor, getColor, setColor)

    @overload
    def setColorTo(self, color: QColor): ...

    @overload
    def setColorTo(self, start: QColor, end: QColor): ...

    def setColorTo(self, *args):
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QColor):
            self._anim.setEndValue(args[0])
        elif len(args) == 2 and all(isinstance(arg, QColor) for arg in args):
            self._anim.setStartValue(args[0])
            self._anim.setEndValue(args[1])
        else:
            raise TypeError('args must be QColor or (QColor, QColor)')
        self._anim.start()


    def transparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColor(target)

    def toTransparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColorTo(target)


    def opaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColor(target)

    def toOpaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColorTo(target)


    def setAlpha(self, alpha: int) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColor(target)

    def setAlphaTo(self, alpha: int) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColorTo(target)

    def stopAnimation(self) -> None:
        self._anim.stop()

    def parent(self) -> 'ZFramelessWindow':
        return super().parent()

# region QAnimatedColor
class QAnimatedColor(QObject):
    '''具有原生属性动画的颜色控制器'''
    def __init__(self, parent: QWidget, color: QColor = QColor('#202020')):
        super().__init__(parent)
        self._color: QColor = color
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.Type.OutExpo)


    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def getColor(self) -> QColor: return self._color

    def setColor(self, value: QColor):
        self._color = value
        self.parent().update()

    color: QColor = Property(QColor, getColor, setColor)


    @overload
    def setColorTo(self, color: QColor): ...

    @overload
    def setColorTo(self, start: QColor, end: QColor): ...

    def setColorTo(self, *args):
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QColor):
            self._anim.setEndValue(args[0])
        elif len(args) == 2 and all(isinstance(arg, QColor) for arg in args):
            self._anim.setStartValue(args[0])
            self._anim.setEndValue(args[1])
        else:
            raise TypeError('args must be QColor or (QColor, QColor)')
        self._anim.start()


    def transparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColor(target)

    def toTransparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColorTo(target)


    def opaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColor(target)

    def toOpaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColorTo(target)


    def setAlpha(self, alpha: int) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColor(target)

    def setAlphaTo(self, alpha: int) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColorTo(target)

    def stopAnimation(self) -> None:
        self._anim.stop()

    def parent(self) -> QWidget:
        return super().parent()

# region ZAnimatedColor
class ZAnimatedColor(QObject):
    '''具有原生属性动画的颜色控制器'''
    def __init__(self, parent: QWidget, color: QColor = QColor('#202020')):
        super().__init__(parent)
        self._color: QColor = color
        self._anim = ZExpPropertyAnimation(self, 'color')
        self._anim.setBias(1)
        self._anim.setFactor(0.2)


    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getColor(self) -> QColor: return self._color

    def setColor(self, value: QColor):
        self._color = value
        self.parent().update()

    color: QColor = Property(QColor, getColor, setColor)


    @overload
    def setColorTo(self, color: QColor): ...

    @overload
    def setColorTo(self, start: QColor, end: QColor): ...

    def setColorTo(self, *args):
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QColor):
            self._anim.setEndValue(args[0])
        elif len(args) == 2 and all(isinstance(arg, QColor) for arg in args):
            self._anim.setStartValue(args[0])
            self._anim.setEndValue(args[1])
        else:
            raise TypeError('args must be QColor or (QColor, QColor)')
        self._anim.start()


    def transparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColor(target)

    def toTransparent(self):
        target = QColor(self._color)
        target.setAlpha(0)
        self.setColorTo(target)


    def opaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColor(target)

    def toOpaque(self):
        target = QColor(self._color)
        target.setAlpha(255)
        self.setColorTo(target)


    def setAlpha(self, alpha: int) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColor(target)

    def setAlphaTo(self, alpha: int) -> None:
        target = QColor(self._color)
        target.setAlpha(alpha)
        self.setColorTo(target)

    def stopAnimation(self) -> None:
        self._anim.stop()

    def parent(self) -> QWidget:
        return super().parent()

# region QAnimatedLinearGradient
class QAnimatedLinearGradient(QObject):
    '''具有原生属性动画的线性渐变颜色控制器'''
    def __init__(self, parent: QWidget, startColor: QColor = QColor('#202020'), endColor: QColor = QColor('#202020')):
        super().__init__(parent)
        self._color1: QColor = startColor
        self._color2: QColor = endColor
        self._direction: ZDirection = ZDirection.Diagonal
        self._reverse: bool = False
        self._linear_points: tuple[float, float, float, float] = (0, 0, 1, 1)
        self._anim1 = QPropertyAnimation(self, b'colorStart')
        self._anim1.setDuration(150)
        self._anim1.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim2 = QPropertyAnimation(self, b'colorEnd')
        self._anim2.setDuration(150)
        self._anim2.setEasingCurve(QEasingCurve.Type.InOutQuad)

    @property
    def animationStart(self) -> QPropertyAnimation: return self._anim1

    @property
    def animationEnd(self) -> QPropertyAnimation: return self._anim2

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


    def getColorStart(self) -> QColor: return self._color1

    def setColorStart(self, value: QColor) -> None:
        self._color1 = value
        self.parent().update()

    colorStart: QColor = Property(QColor, getColorStart, setColorStart)


    def getColorEnd(self) -> QColor: return self._color2

    def setColorEnd(self, value: QColor) -> None:
        self._color2 = value
        self.parent().update()

    colorEnd: QColor = Property(QColor, getColorEnd, setColorEnd)



    def setColorStartTo(self, value: QColor) -> None:
        self._anim1.stop()
        self._anim1.setEndValue(value)
        self._anim1.start()

    def setColorEndTo(self, value: QColor) -> None:
        self._anim2.stop()
        self._anim2.setEndValue(value)
        self._anim2.start()

    def setColors(self, start: QColor, end: QColor) -> None:
        self.setColorStart(start)
        self.setColorEnd(end)

    def setColorsTo(self, start: QColor, end: QColor) -> None:
        self._anim1.stop()
        self._anim2.stop()
        self._anim1.setEndValue(start)
        self._anim2.setEndValue(end)
        self._anim1.start()
        self._anim2.start()


    def transparent(self):
        target1 = QColor(self._color1)
        target2 = QColor(self._color2)
        target1.setAlpha(0)
        target2.setAlpha(0)
        self.setColorStart(target1)
        self.setColorEnd(target2)

    def toTransparent(self):
        target1 = QColor(self._color1)
        target2 = QColor(self._color2)
        target1.setAlpha(0)
        target2.setAlpha(0)
        self.setColorStartTo(target1)
        self.setColorEndTo(target2)


    def opaque(self):
        target1 = QColor(self._color1)
        target2 = QColor(self._color2)
        target1.setAlpha(255)
        target2.setAlpha(255)
        self.setColorStart(target1)
        self.setColorEnd(target2)

    def toOpaque(self):
        target1 = QColor(self._color1)
        target2 = QColor(self._color2)
        target1.setAlpha(255)
        target2.setAlpha(255)
        self.setColorStartTo(target1)
        self.setColorEndTo(target2)

    def stopAnimation(self) -> None:
        self._anim1.stop()
        self._anim2.stop()

    def parent(self) -> QWidget:
        return super().parent()
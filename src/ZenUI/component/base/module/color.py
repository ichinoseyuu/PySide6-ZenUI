from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject,QPropertyAnimation,QEasingCurve,Property
from PySide6.QtGui import QColor
from enum import Enum
import logging

class ColorController(QObject):
    '''颜色控制器，用于控制颜色变化'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._color: QColor = QColor('#dcdcdc')
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

    def setColorTo(self, value: QColor) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._color)
        self._anim.setEndValue(value)
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


class LinearGradientController(QObject):
    '''线性渐变控制器，用于控制线性渐变颜色变化'''
    class Direction(Enum):
        Horizontal = 0
        Vertical = 1
        Diagonal = 2
        DiagonalReverse = 3
        Custom = 4

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._color1: QColor = QColor('#202020')
        self._color2: QColor = QColor('#202020')
        self._direction: LinearGradientController.Direction = self.Direction.Diagonal
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
    def direction(self) -> Direction: return self._direction
    @direction.setter
    def direction(self, value: Direction) -> None:
        self._direction = value
        if self._direction is self.Direction.Horizontal:
            self._linear_points = (0, 0, 1, 0)
        elif self._direction is self.Direction.Vertical:
            self._linear_points = (0, 0, 0, 1)
        elif self._direction is self.Direction.Diagonal:
            self._linear_points = (0, 0, 1, 1)
        elif self._direction is self.Direction.DiagonalReverse:
            self._linear_points = (1, 0, 0, 1)
        elif self._direction is self.Direction.Custom:
            logging.warning('自定义渐变方向请直接设置渐变起点和终点')
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
        self._direction = self.Direction.Custom
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
        self._anim1.setStartValue(self._color1)
        self._anim1.setEndValue(value)
        self._anim1.start()

    def setColorEndTo(self, value: QColor) -> None:
        self._anim2.stop()
        self._anim2.setStartValue(self._color2)
        self._anim2.setEndValue(value)
        self._anim2.start()

    def setColorTo(self, start: QColor, end: QColor) -> None:
        self._anim1.stop()
        self._anim2.stop()
        self._anim1.setStartValue(self._color1)
        self._anim2.setStartValue(self._color2)
        self._anim1.setEndValue(start)
        self._anim2.setEndValue(end)
        self._anim1.start()
        self._anim2.start()

    def stopAnimSatrt(self) -> None:
        self._anim1.stop()

    def stopAnimEnd(self) -> None:
        self._anim2.stop()

    def parent(self) -> QWidget:
        return super().parent()
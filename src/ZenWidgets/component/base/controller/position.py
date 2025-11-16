from typing import overload,cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QPoint, QPointF,Signal
from ZenWidgets.core import ZExpPropertyAnimation

__all__ = [
    'ABCAnimatedPoint',
    'ZWidgetPosition',
    'ZAnimatedPoint',
    'ZAnimatedPointF'
]

# region ABCAnimatedPoint
class ABCAnimatedPoint(QObject):
    '''具有属性动画的坐标控制器的抽象类'''
    positionChanged = Signal(QPoint)
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim: ZExpPropertyAnimation|None = None

    @property
    def animation(self): return self._anim

    def getPos(self) -> QPoint: raise NotImplementedError

    def setPos(self, pos: QPoint) -> None: raise NotImplementedError

    pos: QPoint = cast(QPoint, Property(QPoint, getPos, setPos, notify=positionChanged))

    @overload
    def moveTo(self, pos: QPoint) -> None: ...

    @overload
    def moveTo(self, x:int, y:int) -> None: ...

    def moveTo(self, *args) -> None:
        self._anim.stop()
        self._anim.setEndValue(QPoint(*args))
        self._anim.start()

    def moveFromTo(self, start: QPoint, end: QPoint) -> None:
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def moveBy(self, dx: int, dy: int) -> None:
        self._anim.stop()
        self._anim.setEndValue(self.parent().pos() + QPoint(dx, dy))
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

# region ZWidgetPosition
class ZWidgetPosition(ABCAnimatedPoint):
    '''具有属性动画的位置控制器，直接作用于父 QWidget 的位置'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpPropertyAnimation(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    def getPos(self) -> QPoint: return self.parent().pos()

    def setPos(self, pos: QPoint) -> None: self.parent().move(pos)

    pos: QPoint = cast(QPoint, Property(QPoint, getPos, setPos, notify=ABCAnimatedPoint.positionChanged))

# region ZAnimatedPoint
class ZAnimatedPoint(ABCAnimatedPoint):
    '''具有属性动画的坐标控制器'''
    def __init__(self, parent:QWidget, point: QPoint = QPoint(0, 0)):
        super().__init__(parent)
        self._point = point
        self._anim = ZExpPropertyAnimation(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    def getPos(self) -> QPoint: return self._point

    def setPos(self, pos:QPoint) -> None:
        self._point = pos
        self.parent().update()

    pos: QPoint = cast(QPoint, Property(QPoint, getPos, setPos, notify=ABCAnimatedPoint.positionChanged))


# region ZAnimatedPointF
class ZAnimatedPointF(QObject):
    '''具有属性动画的浮点坐标控制器'''
    positionChanged = Signal(QPointF)

    def __init__(self, parent:QWidget, point: QPointF = QPointF(0, 0)):
        super().__init__(parent)
        self._point = point
        self._anim = ZExpPropertyAnimation(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getPos(self) -> QPointF: return self._point

    def setPos(self, pos:QPointF|QPoint) -> None:
        self._point = QPointF(pos)
        self.parent().update()

    pos: QPointF = cast(QPointF, Property(QPointF, getPos, setPos, notify=ABCAnimatedPoint.positionChanged))

    @overload
    def moveTo(self, pos: QPoint|QPointF) -> None: ...

    @overload
    def moveTo(self, x:int|float, y:int|float) -> None: ...

    def moveTo(self, *args) -> None:
        self._anim.stop()
        self._anim.setEndValue(QPointF(*args))
        self._anim.start()

    def moveFromTo(self, start: QPoint|QPointF, end: QPoint|QPointF) -> None:
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def moveBy(self, dx: int|float, dy: int|float) -> None:
        self._anim.stop()
        self._anim.setEndValue(self._point + QPointF(dx, dy))
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
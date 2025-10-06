from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QPoint, QPointF
from typing import overload
from ZenUI.core import ZExpAnimationRefactor

class PositionController(QObject):
    '''位置控制器，用于控制父控件的位置变化'''
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getPos(self) -> QPoint: return self.parent().pos()

    def setPos(self, pos:QPoint) -> None: self.parent().move(pos)

    pos: QPoint = Property(QPoint, getPos, setPos)


    @overload
    def moveTo(self, pos: QPoint) -> None: ...

    @overload
    def moveTo(self, start: QPoint, end: QPoint) -> None: ...

    @overload
    def moveTo(self, x:int, y:int) -> None: ...

    def moveTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QPoint):
            pos = args[0]
            self._anim.setStartValue(self.parent().pos())
        elif len(args) == 2 and isinstance(args[0], int):
            pos = QPoint(args[0], args[1])
            self._anim.setStartValue(self.parent().pos())
        elif len(args) == 2 and isinstance(args[0], QPoint):
            pos = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(pos)
        self._anim.start()

    def moveBy(self, dx: int, dy: int) -> None:
        """根据偏移量移动控件
        参数:
            dx: x方向偏移量
            dy: y方向偏移量
        """
        self._anim.stop()
        current_pos = self.parent().pos()
        target_pos = QPoint(current_pos.x() + dx, current_pos.y() + dy)
        self._anim.setStartValue(current_pos)
        self._anim.setEndValue(target_pos)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class PointController(QObject):
    '''位置控制器，用于控制位置变化'''
    def __init__(self, parent:QWidget, point: QPoint = QPoint(0, 0)):
        super().__init__(parent)
        self._point = point
        self._anim = ZExpAnimationRefactor(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getPos(self) -> QPoint: return self._point

    def setPos(self, pos:QPoint) -> None:
        self._point = pos
        self.parent().update()

    pos: QPoint = Property(QPoint, getPos, setPos)


    @overload
    def moveTo(self, pos: QPoint) -> None: ...

    @overload
    def moveTo(self, start: QPoint, end: QPoint) -> None: ...

    @overload
    def moveTo(self, x:int, y:int) -> None: ...

    def moveTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QPoint):
            pos = args[0]
            self._anim.setStartValue(self._point)
        elif len(args) == 2 and isinstance(args[0], int):
            pos = QPoint(args[0], args[1])
            self._anim.setStartValue(self._point)
        elif len(args) == 2 and isinstance(args[0], QPoint):
            pos = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(pos)
        self._anim.start()

    def moveBy(self, dx: int, dy: int) -> None:
        """根据偏移量移动控件
        参数:
            dx: x方向偏移量
            dy: y方向偏移量
        """
        self._anim.stop()
        current_pos = self._point
        target_pos = QPoint(current_pos.x() + dx, current_pos.y() + dy)
        self._anim.setStartValue(current_pos)
        self._anim.setEndValue(target_pos)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class PointFController(QObject):
    '''位置控制器，用于控制位置变化'''
    def __init__(self, parent:QWidget, point: QPointF = QPointF(0, 0)):
        super().__init__(parent)
        self._point = point
        self._anim = ZExpAnimationRefactor(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getPos(self) -> QPointF: return self._point

    def setPos(self, pos:QPointF|QPoint) -> None:
        self._point = QPointF(pos)
        self.parent().update()

    pos: QPointF = Property(QPointF, getPos, setPos)


    @overload
    def moveTo(self, pos: QPointF) -> None: ...

    @overload
    def moveTo(self, start: QPointF, end: QPointF) -> None: ...

    @overload
    def moveTo(self, x:int|float, y:int|float) -> None: ...

    def moveTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QPointF):
            pos = args[0]
            self._anim.setStartValue(self._point)
        elif len(args) == 2 and isinstance(args[0], int|float):
            pos = QPointF(args[0], args[1])
            self._anim.setStartValue(self._point)
        elif len(args) == 2 and isinstance(args[0], QPointF):
            pos = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(pos)
        self._anim.start()

    def moveBy(self, dx: int|float, dy: int|float) -> None:
        """根据偏移量移动控件
        参数:
            dx: x方向偏移量
            dy: y方向偏移量
        """
        self._anim.stop()
        current_pos = self._point
        target_pos = QPointF(current_pos.x() + dx, current_pos.y() + dy)
        self._anim.setStartValue(current_pos)
        self._anim.setEndValue(target_pos)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
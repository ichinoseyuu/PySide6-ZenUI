from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QPoint
from typing import overload
from ZenUI.core import ZExpAnimationRefactor

class LocationController(QObject):
    '''位置控制器，用于控制位置变化'''
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "pos")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getPos(self) -> QPoint: return self.parent().pos()
    def setPos(self, pos:QPoint) -> None:
        self.parent().move(pos)

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
        # 计算目标位置 = 当前位置 + 偏移量
        current_pos = self.parent().pos()
        target_pos = QPoint(current_pos.x() + dx, current_pos.y() + dy)
        # 设置动画参数并启动
        self._anim.setStartValue(current_pos)
        self._anim.setEndValue(target_pos)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()
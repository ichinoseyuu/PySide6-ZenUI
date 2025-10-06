from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QRect
from typing import overload
from ZenUI.core import ZExpAnimationRefactor

class GeometryController(QObject):
    '''矩形控制器，用于控制父控件位置和尺寸变化'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "rect")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getRect(self) -> QRect: return self.parent().geometry()

    def setRect(self, rect: QRect) -> None: self.parent().setGeometry(rect)

    rect: QRect = Property(QRect, getRect, setRect)


    @overload
    def moveAndResizeTo(self, rect: QRect) -> None: ...

    @overload
    def moveAndResizeTo(self, start: QRect, end: QRect) -> None: ...

    @overload
    def moveAndResizeTo(self, x: int, y: int, width: int, height: int) -> None: ...

    def moveAndResizeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QRect):
            rect = args[0]
            self._anim.setStartValue(self.parent().geometry())
        elif len(args) == 4 and all(isinstance(arg, int) for arg in args):
            rect = QRect(args[0], args[1], args[2], args[3])
            self._anim.setStartValue(self.parent().geometry())
        elif len(args) == 2 and isinstance(args[0], QRect):
            rect = args[1]
            self._anim.setStartValue(args[0])
        else:
            raise ValueError("Invalid arguments for moveAndResizeTo")
        self._anim.setEndValue(rect)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class RectController(QObject):
    '''QRect 控制器，用于控制 QRect 对象的变化'''
    def __init__(self, parent: QWidget, rect: QRect = QRect(0, 0, 0, 0)):
        super().__init__(parent)
        self._rect = rect
        self._anim = ZExpAnimationRefactor(self, "rect")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getRect(self) -> QRect: return self._rect

    def setRect(self, rect: QRect) -> None:
        self._rect = rect
        self.parent().update()

    rect: QRect = Property(QRect, getRect, setRect)


    @overload
    def moveAndResizeTo(self, rect: QRect) -> None: ...

    @overload
    def moveAndResizeTo(self, start: QRect, end: QRect) -> None: ...

    @overload
    def moveAndResizeTo(self, x: int, y: int, width: int, height: int) -> None: ...

    def moveAndResizeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QRect):
            rect = args[0]
            self._anim.setStartValue(self._rect)
        elif len(args) == 4 and all(isinstance(arg, int) for arg in args):
            rect = QRect(args[0], args[1], args[2], args[3])
            self._anim.setStartValue(self._rect)
        elif len(args) == 2 and isinstance(args[0], QRect):
            rect = args[1]
            self._anim.setStartValue(args[0])
        else:
            raise ValueError("Invalid arguments for moveAndResizeTo")
        self._anim.setEndValue(rect)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QSize
from typing import overload
from ZenUI.core import ZExpAnimationRefactor

class WidgetSizeController(QObject):
    '''尺寸控制器，用于控制父控件尺寸变化'''
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "size")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getSize(self) -> QSize: return self.parent().size()

    def setSize(self, size: QSize) -> None:
        self.parent().resize(size)

    size: QSize = Property(QSize, getSize, setSize)


    @overload
    def resizeTo(self, size:QSize) -> None: ...

    @overload
    def resizeTo(self, start:QSize, end:QSize) -> None: ...

    @overload
    def resizeTo(self, x:int, y:int) -> None: ...

    def resizeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QSize):
            size = args[0]
            self._anim.setStartValue(self.parent().size())
        elif len(args) == 2 and isinstance(args[0], int):
            size = QSize(args[0], args[1])
            self._anim.setStartValue(self.parent().size())
        elif len(args) == 2 and isinstance(args[0], QSize):
            size = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(size)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class SizeController(QObject):
    '''尺寸控制器，用于控制 QSize 的变化'''
    def __init__(self, parent:QWidget, size: QSize = QSize(0, 0)):
        super().__init__(parent)
        self._size = size
        self._anim = ZExpAnimationRefactor(self, "size")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getSize(self) -> QSize: return self._size

    def setSize(self, size: QSize) -> None:
        self._size = size
        self.parent().update()

    size: QSize = Property(QSize, getSize, setSize)


    @overload
    def resizeTo(self, size:QSize) -> None: ...

    @overload
    def resizeTo(self, start:QSize, end:QSize) -> None: ...

    @overload
    def resizeTo(self, x:int, y:int) -> None: ...

    def resizeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QSize):
            size = args[0]
            self._anim.setStartValue(self._size)
        elif len(args) == 2 and isinstance(args[0], int):
            size = QSize(args[0], args[1])
            self._anim.setStartValue(self._size)
        elif len(args) == 2 and isinstance(args[0], QSize):
            size = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(size)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
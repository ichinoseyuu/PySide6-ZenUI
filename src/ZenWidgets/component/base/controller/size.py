from typing import overload,cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QSize, Signal
from ZenWidgets.core import ZExpPropertyAnimation

__all__ = [
    'ABCAnimatedSize',
    'ZWidgetSize',
    'ZAnimatedSize'
]

# region ABCAnimatedSize
class ABCAnimatedSize(QObject):
    sizeChanged = Signal()
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim: ZExpPropertyAnimation|None = None

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getSize(self) -> QSize: raise NotImplementedError

    def setSize(self, s: QSize) -> None: raise NotImplementedError

    size: QSize = cast(QSize, Property(QSize, getSize, setSize, notify=sizeChanged))


    @overload
    def resizeTo(self, size:QSize) -> None: ...

    @overload
    def resizeTo(self, x:int, y:int) -> None: ...

    def resizeTo(self, *args) -> None:
        self._anim.stop()
        self._anim.setEndValue(QSize(*args))
        self._anim.start()

    def resizeFromTo(self, start: QSize, end: QSize) -> None:
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()


# region ZWidgetSize
class ZWidgetSize(ABCAnimatedSize):
    '''具有属性动画的 QWidget 尺寸控制器，直接作用于父 QWidget'''
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = ZExpPropertyAnimation(self, "size")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)


    def getSize(self) -> QSize: return self.parent().size()

    def setSize(self, size: QSize) -> None: self.parent().resize(size)

    size: QSize = cast(QSize, Property(QSize, getSize, setSize, notify=ABCAnimatedSize.sizeChanged))

# region ZAnimatedSize
class ZAnimatedSize(ABCAnimatedSize):
    '''具有属性动画的 QSize 控制器'''
    def __init__(self, parent:QWidget, size: QSize = QSize(0, 0)):
        super().__init__(parent)
        self._size = size
        self._anim = ZExpPropertyAnimation(self, "size")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getSize(self) -> QSize: return self._size

    def setSize(self, size: QSize) -> None:
        self._size = size
        self.parent().update()

    size: QSize = cast(QSize, Property(QSize, getSize, setSize, notify=ABCAnimatedSize.sizeChanged))
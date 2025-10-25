from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, Signal
from typing import overload
from ZenWidgets.core import ZExpPropertyAnimation

class ZAnimatedOpacity(QObject):
    '''具有属性动画的透明度控制器'''
    completelyHide = Signal()
    completelyShow = Signal()
    def __init__(self, parent: QWidget, opacity: float = 1.0):
        super().__init__(parent)
        self._opacity = opacity
        self._anim = ZExpPropertyAnimation(self, "opacity")
        self._anim.finished.connect(self._onFinished)
        self._anim.setBias(0.02)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getOpacity(self) -> float: return self._opacity

    def setOpacity(self, opacity: float) -> None:
        self._opacity = opacity
        self.parent().update()

    opacity: float = Property(float, getOpacity, setOpacity)


    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setEndValue(0)
        self._anim.start()


    @overload
    def fadeTo(self, opacity: float) -> None: ...

    @overload
    def fadeTo(self, start: float, end: float) -> None: ...

    def fadeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], float):
            self._anim.setEndValue(max(min(args[0], 1.0), 0))
        elif len(args) == 2 and all(isinstance(arg, float) for arg in args):
            self._anim.setStartValue(max(min(args[0], 1.0), 0))
            self._anim.setEndValue(max(min(args[0], 1.0), 0))
        else:
            raise TypeError("fadeTo() takes 1 or 2 arguments")
        self._anim.start()

    def _onFinished(self) -> None:
        if self.opacity == 0:
            self.completelyHide.emit()
        elif self.opacity == 1:
            self.completelyShow.emit()

    def parent(self) -> QWidget:
        return super().parent()


class ZAnimatedWindowOpacity(QObject):
    '''具有属性动画的透明度控制器，直接作用于窗口透明度'''
    completelyHide = Signal()
    completelyShow = Signal()
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpPropertyAnimation(self, "opacity")
        self._anim.finished.connect(self._onFinished)
        self._anim.setBias(0.02)
        self._anim.setFactor(0.2)


    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getOpacity(self) -> float: return self.parent().windowOpacity()

    def setOpacity(self, opacity: float) -> None:
        self.parent().setWindowOpacity(opacity)

    opacity: float = Property(float, getOpacity, setOpacity)


    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setEndValue(0)
        self._anim.start()


    @overload
    def fadeTo(self, opacity: float) -> None: ...

    @overload
    def fadeTo(self, start: float, end: float) -> None: ...

    def fadeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], float):
            self._anim.setEndValue(max(min(args[0], 1.0), 0))
        elif len(args) == 2 and all(isinstance(arg, float) for arg in args):
            self._anim.setStartValue(max(min(args[0], 1.0), 0))
            self._anim.setEndValue(max(min(args[0], 1.0), 0))
        else:
            raise TypeError("fadeTo() takes 1 or 2 arguments")
        self._anim.start()

    def _onFinished(self) -> None:
        if self.opacity == 0:
            self.completelyHide.emit()
        elif self.opacity == 1:
            self.completelyShow.emit()

    def parent(self) -> QWidget:
        return super().parent()
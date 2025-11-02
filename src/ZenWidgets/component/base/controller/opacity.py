from typing import overload,cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, Signal
from ZenWidgets.core import ZExpPropertyAnimation

# region ABCAnimatedOpacity
class ABCAnimatedOpacity(QObject):
    opacityChanged = Signal(float)
    completelyHide = Signal()
    completelyShow = Signal()
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim: ZExpPropertyAnimation | None = None

    @property
    def animation(self): raise NotImplementedError

    def getOpacity(self) -> float: raise NotImplementedError

    def setOpacity(self, o: float) -> None: raise NotImplementedError

    opacity: float = cast(float, Property(float, getOpacity, setOpacity, notify=opacityChanged))

    @overload
    def fadeTo(self, opacity: float) -> None: ...

    @overload
    def fadeTo(self, start: float, end: float) -> None: ...

    def fadeTo(self, arg1: float, arg2: float | None = None) -> None:
        self._anim.stop()
        if arg2 is None:
            self._anim.setEndValue(max(min(arg1, 1.0), 0))
        else:
            self._anim.setStartValue(max(min(arg1, 1.0), 0))
            self._anim.setEndValue(max(min(arg2, 1.0), 0))
        self._anim.start()

    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setEndValue(0)
        self._anim.start()

    def _on_finished_(self) -> None:
        if self.opacity == 0:
            self.completelyHide.emit()
        elif self.opacity == 1:
            self.completelyShow.emit()

    def parent(self) -> QWidget:
        return super().parent()

# region ZAnimatedOpacity
class ZAnimatedOpacity(ABCAnimatedOpacity):
    '''具有属性动画的透明度控制器'''
    def __init__(self, parent: QWidget, opacity: float = 1.0):
        super().__init__(parent)
        self._opacity = opacity
        self._anim = ZExpPropertyAnimation(self, "opacity")
        self._anim.finished.connect(self._on_finished_)
        self._anim.setBias(0.02)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getOpacity(self) -> float: return self._opacity

    def setOpacity(self, opacity: float) -> None:
        self._opacity = max(min(opacity, 1.0), 0)
        self.parent().update()

    opacity: float = cast(float, Property(float, getOpacity, setOpacity, notify=ABCAnimatedOpacity.opacityChanged))

# region ZAnimatedWindowOpacity
class ZAnimatedWindowOpacity(ABCAnimatedOpacity):
    '''具有属性动画的透明度控制器，直接作用于窗口透明度'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpPropertyAnimation(self, "opacity")
        self._anim.finished.connect(self._on_finished_)
        self._anim.setBias(0.02)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

    def getOpacity(self) -> float: return self.parent().windowOpacity()

    def setOpacity(self, opacity: float) -> None: self.parent().setWindowOpacity(max(min(opacity, 1.0), 0))

    opacity: float = cast(float, Property(float, getOpacity, setOpacity, notify=ABCAnimatedOpacity.opacityChanged))

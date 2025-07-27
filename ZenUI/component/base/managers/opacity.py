from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property
from typing import overload
from ZenUI.core import ZExpAnimationRefactor

class OpacityManager(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._opacity: float = 1.0
        self._anim = ZExpAnimationRefactor(self, "opacity")
        self._anim.setBias(0.02)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getOpacity(self) -> float: return self._opacity
    def setOpacity(self, opacity: float) -> None:
        self._opacity = opacity
        #logging.info("setOpacity: %s", opacity)
        self.parent().update()

    opacity: float = Property(float, getOpacity, setOpacity)


    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._opacity)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._opacity)
        self._anim.setEndValue(0)
        self._anim.start()


    @overload
    def fadeTo(self, opacity: float) -> None: ...

    @overload
    def fadeTo(self, start: float, end: float) -> None: ...

    def fadeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], float):
            opacity = args[0]
            self._anim.setStartValue(self._opacity)
        elif len(args) == 2 and isinstance(args[0], float):
            opacity = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(opacity)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class WindowOpacityManager(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "opacity")
        self._anim.setBias(0.02)
        self._anim.setFactor(0.2)


    @property
    def animation(self) -> ZExpAnimationRefactor: return self._anim

    def getOpacity(self) -> float: return self.parent().windowOpacity()
    def setOpacity(self, opacity: float) -> None:
        self.parent().setWindowOpacity(opacity)

    opacity: float = Property(float, getOpacity, setOpacity)


    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self.parent().windowOpacity())
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self.parent().windowOpacity())
        self._anim.setEndValue(0)
        self._anim.start()


    @overload
    def fadeTo(self, opacity: float) -> None: ...

    @overload
    def fadeTo(self, start: float, end: float) -> None: ...

    def fadeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], float):
            opacity = args[0]
            self._anim.setStartValue(self.parent().windowOpacity())
        elif len(args) == 2 and isinstance(args[0], float):
            opacity = args[1]
            self._anim.setStartValue(args[0])
        self._anim.setEndValue(opacity)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
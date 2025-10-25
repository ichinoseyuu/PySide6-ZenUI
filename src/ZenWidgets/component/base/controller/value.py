from typing import overload
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QObject, Property, QEasingCurve

class QAnimatedInt(QObject):
    '''具有原生属性动画的整数控制器'''
    def __init__(self, parent: QWidget, value: int = 0):
        super().__init__(parent)
        self._value: int = value
        self._anim = QPropertyAnimation(self, b'value')
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.Linear)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def getValue(self) -> int: return self._value

    def setValue(self, value: int) -> None:
        self._value = value
        self.parent().update()

    value: int = Property(int, getValue, setValue)



    @overload
    def setValueTo(self, value: int) -> None: ...

    @overload
    def setValueTo(self, start: int, end: int) -> None: ...

    def setValueTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1:
            self._anim.setEndValue(args[0])
        elif len(args) == 2:
            self._anim.setStartValue(args[0])
            self._anim.setEndValue(args[1])
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class QAnimatedFloat(QObject):
    '''具有原生属性动画的浮点数控制器'''
    def __init__(self, parent: QWidget, value: int|float = 0.0):
        super().__init__(parent)
        self._value: float = value
        self._anim = QPropertyAnimation(self, b'value')
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.Linear)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def getValue(self) -> float: return self._value

    def setValue(self, value: float) -> None:
        self._value = value
        self.parent().update()

    value: float = Property(float, getValue, setValue)


    @overload
    def setValueTo(self, value: int) -> None: ...

    @overload
    def setValueTo(self, start: int, end: int) -> None: ...

    def setValueTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1:
            self._anim.setEndValue(args[0])
        elif len(args) == 2:
            self._anim.setStartValue(args[0])
            self._anim.setEndValue(args[1])
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
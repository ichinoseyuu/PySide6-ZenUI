from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QObject, Property, QEasingCurve

class IntegerController(QObject):
    '''整数控制器，用于控制整数变化'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._value: int = 0
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


    def setValueTo(self, value: int) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._value)
        self._anim.setEndValue(value)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()


class FloatController(QObject):
    '''浮点数控制器，用于控制浮点数变化'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._value: float = 0.0
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


    def setValueTo(self, value: float) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._value)
        self._anim.setEndValue(value)
        self._anim.start()


    def parent(self) -> QWidget:
        return super().parent()
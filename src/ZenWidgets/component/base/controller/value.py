from typing import overload,cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation,QObject,Property,QEasingCurve,Signal
from ZenWidgets.core import ZExpPropertyAnimation

__All__ = [
    'ABCAnimatedInt',
    'QAnimatedInt',
    'ZAnimatedInt',
    'ABCAnimatedFloat',
    'QAnimatedFloat',
    'ZAnimatedFloat'
]

# region ABCAnimatedInt
class ABCAnimatedInt(QObject):
    valueChanged = Signal()
    def __init__(self, parent: QWidget, value: int = 0):
        super().__init__(parent)
        self._value: int = value
        self._anim: ZExpPropertyAnimation|QPropertyAnimation|None = None

    @property
    def animation(self): return self._anim

    def getValue(self) -> int: return self._value

    def setValue(self, value: int) -> None:
        self._value = max(self._min, min(self._max, value))
        self.parent().update()

    value: int = cast(int, Property(int, getValue, setValue, notify=valueChanged))

    @overload
    def setValueTo(self, value: int) -> None: ...

    @overload
    def setValueTo(self, start: int, end: int) -> None: ...

    def setValueTo(self, arg1: int, arg2: int|None = None) -> None:
        self._anim.stop()
        if arg2 is None:
            self._anim.setStartValue(self._value)
            self._anim.setEndValue(arg1)
        else:
            self._anim.setStartValue(arg1)
            self._anim.setEndValue(arg2)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

# region QAnimatedInt
class QAnimatedInt(ABCAnimatedInt):
    '''具有原生属性动画的整数控制器'''
    def __init__(self, parent: QWidget, value: int = 0):
        super().__init__(parent, value)
        self._anim = QPropertyAnimation(self, b'value')
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.Linear)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

# region ZAnimatedInt
class ZAnimatedInt(ABCAnimatedInt):
    '''具有原生属性动画的整数控制器'''
    def __init__(self, parent: QWidget, value: int = 0):
        super().__init__(parent, value)
        self._anim = ZExpPropertyAnimation(self, 'value')
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim

# region ABCAnimatedFloat
class ABCAnimatedFloat(QObject):
    valueChanged = Signal()
    def __init__(self, parent: QWidget, value: int|float = .0):
        super().__init__(parent)
        self._value: float = value
        self._anim: ZExpPropertyAnimation|QPropertyAnimation|None = None

    @property
    def animation(self): return self._anim

    def getValue(self) -> float: return self._value

    def setValue(self, value: float) -> None:
        self._value = value
        self.parent().update()

    value: float = cast(float, Property(float, getValue, setValue, notify=valueChanged))

    @overload
    def setValueTo(self, value: int|float) -> None: ...

    @overload
    def setValueTo(self, start: int|float, end: int|float) -> None: ...

    def setValueTo(self, arg1: int|float, arg2: int|float|None = None) -> None:
        self._anim.stop()
        if arg2 is None:
            self._anim.setStartValue(self._value)
            self._anim.setEndValue(arg1)
        else:
            self._anim.setStartValue(arg1)
            self._anim.setEndValue(arg2)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

# region QAnimatedFloat
class QAnimatedFloat(ABCAnimatedFloat):
    '''具有原生属性动画的浮点数控制器'''
    def __init__(self, parent: QWidget, value: int|float = .0):
        super().__init__(parent, value)
        self._anim = QPropertyAnimation(self, b'value')
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.Linear)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim
# region ZAnimatedFloat
class ZAnimatedFloat(ABCAnimatedFloat):
    '''具有原生属性动画的浮点数控制器'''
    def __init__(self, parent: QWidget, value: int|float = .0):
        super().__init__(parent, value)
        self._anim = ZExpPropertyAnimation(self,'value')
        self._anim.setBias(0.05)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation: return self._anim
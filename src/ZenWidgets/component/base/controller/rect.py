from typing import overload, cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Property, QRect, Signal,QSize
from ZenWidgets.core import ZExpPropertyAnimation

__All__ = [
    'ABCAnimatedRect',
    'ZWidgetRect',
    'ZAnimatedRect'
]

# region ABCAnimatedRect
class ABCAnimatedRect(QObject):
    rectChanged = Signal()
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim: ZExpPropertyAnimation | None = None

    @property
    def animation(self) -> ZExpPropertyAnimation:
        return self._anim

    def getRect(self) -> QRect:
        raise NotImplementedError

    def setRect(self, r: QRect) -> None:
        raise NotImplementedError

    rect: QRect = cast(QRect, Property(QRect, getRect, setRect, notify=rectChanged))

    @overload
    def moveResizeTo(self, rect: QRect) -> None: ...

    @overload
    def moveResizeTo(self, x: int, y: int, width: int, height: int) -> None: ...

    def moveResizeTo(self, *args) -> None:
        self._anim.stop()
        if len(args) == 1 and isinstance(args[0], QRect):
            self._anim.setEndValue(args[0])
        else:
            self._anim.setEndValue(QRect(*args))
        self._anim.start()

    def moveResizeFromTo(self, start: QRect, end: QRect) -> None:
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def scaleIn(self, target_rect: QRect) -> None:
        self._anim.stop()
        center = target_rect.center()
        start_rect = QRect(center, QSize(0, 0))
        self._anim.setStartValue(start_rect)
        self._anim.setEndValue(target_rect)
        self._anim.start()

    def scaleOut(self) -> None:
        self._anim.stop()
        current_rect = self.getRect()
        center = current_rect.center()
        end_rect = QRect(center, QSize(0, 0))
        self._anim.setStartValue(current_rect)
        self._anim.setEndValue(end_rect)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()


# region ZWidgetRect
class ZWidgetRect(ABCAnimatedRect):
    '''具有属性动画的 QWidget 矩形控制器，直接作用于父 QWidget 的位置和大小'''
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpPropertyAnimation(self, "rect")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    def getRect(self) -> QRect:
        return self.parent().geometry()

    def setRect(self, rect: QRect) -> None:
        self.parent().setGeometry(rect)

    rect: QRect = cast(QRect, Property(QRect, getRect, setRect, notify=ABCAnimatedRect.rectChanged))


# region ZAnimatedRect
class ZAnimatedRect(ABCAnimatedRect):
    '''具有属性动画的 QRect 控制器，维护独立的矩形状态'''
    def __init__(self, parent: QWidget, rect: QRect = QRect(0, 0, 0, 0)):
        super().__init__(parent)
        self._rect = rect
        self._anim = ZExpPropertyAnimation(self, "rect")
        self._anim.setBias(1)
        self._anim.setFactor(0.2)

    @property
    def animation(self) -> ZExpPropertyAnimation:
        return self._anim

    def getRect(self) -> QRect:
        return self._rect

    def setRect(self, rect: QRect) -> None:
        self._rect = rect
        self.parent().update()

    rect: QRect = cast(QRect, Property(QRect, getRect, setRect, notify=ABCAnimatedRect.rectChanged))
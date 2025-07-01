from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import overload
from ZenUI.core import ZExpAnimationRefactor
import logging


__all__ = ["MoveExpAnimation","MovePropertyAnimation",
           "ResizeExpAnimation", "ResizePropertyAnimation",
           "WindowOpacityExpAnimation", "WindowOpacityPropertyAnimation","OpacityExpAnimation",
           "LengthExpAnimation", "WidthExpAnimation"]

# region Move
class MovePropertyAnimation(QObject):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = QPropertyAnimation(self, b"pos")
        self._anim.setDuration(150)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> QPropertyAnimation:
        return self._anim

    def getPos(self) -> QPoint:
        return self.parent().pos()

    def setPos(self, pos:QPoint) -> None:
        self.parent().move(pos)

    pos = Property(QPoint, getPos, setPos)

    @overload
    def moveTo(self, pos:QPoint) -> None:
        ...

    @overload
    def moveTo(self, x:int, y:int) -> None:
        ...

    def moveTo(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], QPoint):
            pos = args[0]
        elif len(args) == 2:
            pos = QPoint(args[0], args[1])
        self._anim.stop()
        self._anim.setStartValue(self.getPos())
        self._anim.setEndValue(pos)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()


class MoveExpAnimation(QObject):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "pos")
        self._anim.setBias(0.5)
        self._anim.setFactor(0.20)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> ZExpAnimationRefactor:
        return self._anim

    def getPos(self) -> QPoint:
        return self.parent().pos()

    def setPos(self, pos:QPoint) -> None:
        self.parent().move(pos)

    pos = Property(QPoint, getPos, setPos)

    @overload
    def moveTo(self, pos:QPoint) -> None:
        ...

    @overload
    def moveTo(self, x:int, y:int) -> None:
        ...

    def moveTo(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], QPoint):
            pos = args[0]
        elif len(args) == 2:
            pos = QPoint(args[0], args[1])
        self._anim.stop()
        self._anim.setCurrentValue(self.getPos())
        self._anim.setEndValue(pos)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

# region Resize
class ResizePropertyAnimation(QObject):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = QPropertyAnimation(self, b"size")
        self._anim.setDuration(150)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> QPropertyAnimation:
        return self._anim

    def getSize(self) -> QSize:
        return self.parent().size()

    def setSize(self, size: QSize) -> None:
        self.parent().resize(size)

    size = Property(QSize, getSize, setSize)

    @overload
    def resizeTo(self, pos:QSize) -> None:
        ...

    @overload
    def resizeTo(self, x:int, y:int) -> None:
        ...

    def resizeTo(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], QSize):
            size = args[0]
        elif len(args) == 2:
            size = QSize(args[0], args[1])
        self._anim.stop()
        self._anim.setStartValue(self.getSize())
        self._anim.setEndValue(size)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

class ResizeExpAnimation(QObject):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "size")
        self._anim.setBias(0.5)
        self._anim.setFactor(0.20)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> ZExpAnimationRefactor:
        return self._anim

    def getSize(self) -> QSize:
        return self.parent().size()

    def setSize(self, size: QSize) -> None:
        self.parent().resize(size)

    size = Property(QSize, getSize, setSize)

    @overload
    def resizeTo(self, pos:QSize) -> None:
        ...

    @overload
    def resizeTo(self, x:int, y:int) -> None:
        ...

    def resizeTo(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], QSize):
            size = args[0]
        elif len(args) == 2:
            size = QSize(args[0], args[1])
        self._anim.stop()
        self._anim.setCurrentValue(self.getSize())
        self._anim.setEndValue(size)
        self._anim.start()
        
    def parent(self) -> QWidget:
        return super().parent()

# region Opacity
class WindowOpacityPropertyAnimation(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = QPropertyAnimation(self, b"opacity")
        self._anim.setDuration(500)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> QPropertyAnimation:
        return self._anim

    def getOpacity(self) -> float:
        return self.parent().windowOpacity()

    def setOpacity(self, opacity: float) -> None:
        self.parent().setWindowOpacity(opacity)

    opacity = Property(float, getOpacity, setOpacity)

    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self.getOpacity())
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self.getOpacity())
        self._anim.setEndValue(0)
        self._anim.start()

    def fadeTo(self, opacity: float) -> None:
        self._anim.stop()
        self._anim.setStartValue(self.getOpacity())
        self._anim.setEndValue(opacity)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

class WindowOpacityExpAnimation(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._anim = ZExpAnimationRefactor(self, "opacity")
        self._anim.setBias(0.05)
        self._anim.setFactor(0.2)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> ZExpAnimationRefactor:
        return self._anim

    def getOpacity(self) -> float:
        return self.parent().windowOpacity()

    def setOpacity(self, opacity: float) -> None:
        self.parent().setWindowOpacity(opacity)

    opacity = Property(float, getOpacity, setOpacity)

    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getOpacity())
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getOpacity())
        self._anim.setEndValue(0)
        self._anim.start()

    def fadeTo(self, opacity: float) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getOpacity())
        self._anim.setEndValue(opacity)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

class OpacityExpAnimation(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._opacity: float = 1.0
        self._anim = ZExpAnimationRefactor(self, "opacity")
        self._anim.setBias(0.05)
        self._anim.setFactor(0.2)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> ZExpAnimationRefactor:
        return self._anim

    def getOpacity(self) -> float:
        return self._opacity

    def setOpacity(self, opacity: float) -> None:
        self._opacity = opacity
        #logging.info("setOpacity: %s", opacity)
        self.parent().update()

    opacity = Property(float, getOpacity, setOpacity)

    def fadeIn(self) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getOpacity())
        self._anim.setEndValue(1.0)
        self._anim.start()

    def fadeOut(self) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getOpacity())
        self._anim.setEndValue(0)
        self._anim.start()

    def fadeTo(self, opacity: float) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getOpacity())
        self._anim.setEndValue(opacity)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

# region Length
class LengthExpAnimation(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._length: int = 0
        self._anim = ZExpAnimationRefactor(self, "length")
        self._anim.setBias(0.05)
        self._anim.setFactor(0.2)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> ZExpAnimationRefactor:
        return self._anim

    def getLength(self) -> int:
        return self._length

    def setLength(self, length: int) -> None:
        self._length = length
        self.parent().update()

    length = Property(int, getLength, setLength)

    def setLengthTo(self, length: int) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getLength())
        self._anim.setEndValue(length)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

# region Width
class WidthExpAnimation(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._width: int = 0
        self._anim = ZExpAnimationRefactor(self, "width")
        self._anim.setBias(0.05)
        self._anim.setFactor(0.2)

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def animation(self) -> ZExpAnimationRefactor:
        return self._anim

    def getWidth(self) -> int:
        return self._width

    def setWidth(self, width: int) -> None:
        self._width = width
        self.parent().update()

    width = Property(int, getWidth, setWidth)

    def setLengthTo(self, width: int) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getWidth())
        self._anim.setEndValue(width)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()


class Panel(QWidget):
    def __init__(self):
        super().__init__()
        self._move_anim = MovePropertyAnimation(self)
        self._resize_anim = ResizePropertyAnimation(self)
        self._opacity_anim = WindowOpacityPropertyAnimation(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet('background-color: #dcdcdc;')


def test1():
    panel._move_anim.moveTo(QPoint(100, 100))

def test2():
    panel._resize_anim.resizeTo(QSize(200, 200))

def test3():
    panel._opacity_anim.fadeOut()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    panel = Panel()
    panel.resize(400, 300)
    btn = QPushButton('ChangePos', panel)
    btn.setFont(QFont('Arial', 10))
    btn.setGeometry(10, 10, 100, 30)
    btn.clicked.connect(test1)
    btn = QPushButton('ChangeSize', panel)
    btn.setFont(QFont('Arial', 10))
    btn.setGeometry(10, 50, 100, 30)
    btn.clicked.connect(test2)
    btn = QPushButton('ChangeOpiacity', panel)
    btn.setFont(QFont('Arial', 10))
    btn.setGeometry(10, 90, 100, 30)
    btn.clicked.connect(test3)
    panel.show()
    app.exec()
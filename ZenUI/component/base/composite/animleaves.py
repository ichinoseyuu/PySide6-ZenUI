from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.core import ZExpAnimationRefactor
import logging

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

    def moveTo(self, pos:QPoint) -> None:
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

    def moveTo(self, pos:QPoint) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getPos())
        self._anim.setEndValue(pos)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()


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

    def resizeTo(self, size: QSize) -> None:
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

    def resizeTo(self, size: QSize) -> None:
        self._anim.stop()
        self._anim.setCurrentValue(self.getSize())
        self._anim.setEndValue(size)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

class OpacityPropertyAnimation(QObject):
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

class OpacityExpAnimation(QObject):
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



class Panel(QWidget):
    def __init__(self):
        super().__init__()
        self._move_anim = MovePropertyAnimation(self)
        self._resize_anim = ResizePropertyAnimation(self)
        self._opacity_anim = OpacityPropertyAnimation(self)
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
from typing import cast
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QPropertyAnimation,Property,QEasingCurve,QObject,QRect
from PySide6.QtGui import QPainter,QColor

__All__ = ['ZFlashLayer', 'ZOpacityLayer']

class ABCAnimatedEffect(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._color: QColor = QColor(130, 130, 130, 0)
        self._anim = QPropertyAnimation(self, b'alphaF')
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    @property
    def animation(self) -> QPropertyAnimation: return self._anim

    def getAlphaF(self) -> float: return self._color.alphaF()

    def setAlphaF(self, opacity: float): self._color.setAlphaF(opacity); self.parent().update()

    alphaF: float = cast(float, Property(float, getAlphaF, setAlphaF))

    def getColor(self) -> QColor: return self._color

    def setColor(self, color: QColor): self._color = QColor(color); self.parent().update()

    color: QColor = cast(QColor, Property(QColor, getColor, setColor))

    def parent(self) -> QWidget: return super().parent()

    def stopAnimation(self) -> None: self._anim.stop()


class ZFlashEffect(ABCAnimatedEffect):
    '''用于控件按下或刷新时的反馈动画'''
    def __init__(self, parent):
        super().__init__(parent)
        self._anim.setDuration(500)

    def flash(self, start: float|int = 0.2,/,duration: int = 500):
        self._anim.stop()
        self._anim.setDuration(duration)
        if type(start) == int: start = start/255
        self._anim.setStartValue(start)
        self._anim.setEndValue(0.0)
        self._anim.start()

    def drawFlashLayer(self, painter: QPainter, rect: QRect, radius: float,/):
        if self._color.alpha() <= 0: return
        painter.save()
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)
        painter.restore()


class ZOpacityEffect(ABCAnimatedEffect):
    '''用于鼠标悬停或按下时控件的透明度反馈动画'''
    def setAlphaTo(self, end: int,/):
        self._anim.stop()
        self._anim.setStartValue(self._color.alphaF())
        self._anim.setEndValue(end/255)
        self._anim.start()

    def setAlphaFTo(self, end: float,/):
        self._anim.stop()
        self._anim.setStartValue(self._color.alphaF())
        self._anim.setEndValue(end)
        self._anim.start()

    def toTransparent(self):
        self._anim.stop()
        self._anim.setStartValue(self._color.alphaF())
        self._anim.setEndValue(0.0)
        self._anim.start()

    def drawOpacityLayer(self, painter: QPainter, rect: QRect, radius: float,/):
        if self._color.alpha() <= 0: return
        painter.save()
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)
        painter.restore()
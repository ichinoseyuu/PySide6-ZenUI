from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QPoint, QEvent, QSize
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.core import ZGlobal,TipPos
class ZABCSwitch(QWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    toggled = Signal(bool)

    class State(IntEnum):
        Idle = 0
        Hover = 1
        Pressed = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        #self.setMouseTracking(True)
        self._state = self.State.Idle
        self._checked: bool = False
        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.toggled.connect(self.toggleHandler)


    # region Property
    @property
    def state(self) -> State: return self._state

    @property
    def isOn(self) -> bool: return self._checked

    # region Slot
    @Slot()
    def hoverHandler(self):
        pass

    @Slot()
    def leaveHandler(self):
        pass

    @Slot()
    def pressHandler(self):
        pass

    @Slot()
    def releaseHandler(self):
        pass

    @Slot(bool)
    def toggleHandler(self, checked: bool):
        pass

    # endregion

    # region Event
    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)
        self._state = self.State.Hover
        self.entered.emit()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self._state = self.State.Idle
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._state = self.State.Pressed
            self.pressed.emit()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.released.emit()
            # if mouse is still in button
            if self.rect().contains(event.position().toPoint()):
                self._checked = not self._checked
                self.toggled.emit(self._checked)

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)
from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QPoint, QEvent, QSize
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.core import ZGlobal
class ZABCNavBarToggleButton(QWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    clicked = Signal()
    toggled = Signal(bool)
    class State(IntEnum):
        Idle = 0
        Hover = 1
        Pressed = 2
    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = self.State.Idle
        self._tool_tip: str = ""
        self._checked: bool = False
        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.clicked.connect(self.clickHandler)
        self.toggled.connect(self.toggleHandler)


    # region Property
    @property
    def state(self) -> State:
        return self._state

    @property
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, checked: bool) -> None:
        self._checked = checked
        self.toggled.emit(checked)
        self.leaved.emit()
        self.update()

    # region Func
    def toolTip(self):
        return self._tool_tip

    def setToolTip(self, tip: str):
        self._tool_tip = tip
        self.update()


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

    @Slot(QPoint)
    def clickHandler(self):
        pass

    @Slot(bool)
    def toggleHandler(self, checked: bool):
        pass

    # endregion

    # region Event
    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)
        if self._tool_tip != "" and ZGlobal.tooltip:
            ZGlobal.tooltip.setInsideOf(self)
            ZGlobal.tooltip.setText(self._tool_tip)
            ZGlobal.tooltip.showTip()
        self._state = self.State.Hover
        self.entered.emit()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        if self._tool_tip != "" and ZGlobal.tooltip:
            ZGlobal.tooltip.setInsideOf(None)
            ZGlobal.tooltip.hideTip()
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
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()
                if not self._checked: self._checked = True
                
                self.toggled.emit(self._checked)

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)
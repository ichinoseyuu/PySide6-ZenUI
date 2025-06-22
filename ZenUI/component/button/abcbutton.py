from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QPoint, QEvent, Property
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.core import ZGlobal

class ZABCButton(QWidget):
    entered = Signal(QPoint)
    leaved = Signal()
    pressed = Signal(QPoint)
    released = Signal(QPoint)
    clicked = Signal(QPoint)
    hoverMove = Signal(QPoint)
    class State(IntEnum):
        Idle = 0
        Hover = 1
        Pressed = 2
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setMouseTracking(True)
        self._state = self.State.Idle
        self._tool_tip: str = ""
        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.clicked.connect(self.clickHandler)
        self.hoverMove.connect(self.hoverMoveHandler)




    # region Property
    @Property(int)
    def state(self):
        return self._state

    @state.setter
    def setState(self, state):
        self._state = state

    # region Func
    def setHoverMoveSignal(self, enabled: bool):
        if enabled: self.setMouseTracking(True)
        else: self.setMouseTracking(False)

    def toolTip(self):
        return self._tool_tip

    def setToolTip(self, tip: str):
        self._tool_tip = tip
        self.update()


    # region Slot
    @Slot(QPoint)
    def hoverHandler(self, pos:QPoint):
        pass

    @Slot()
    def leaveHandler(self):
        pass

    @Slot(QPoint)
    def pressHandler(self, pos:QPoint):
        pass

    @Slot(QPoint)
    def releaseHandler(self, pos:QPoint):
        pass

    @Slot(QPoint)
    def clickHandler(self, pos:QPoint):
        pass

    @Slot(QPoint)
    def hoverMoveHandler(self, pos:QPoint):
        pass

    # endregion

    # region Event
    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)
        if self._tool_tip != "" and ZGlobal.tooltip:
            ZGlobal.tooltip.setInsideOf(self)
            ZGlobal.tooltip.setText(self._tool_tip)
            ZGlobal.tooltip.showTip()
        self.entered.emit(event.position().toPoint())

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        if self._tool_tip != "" and ZGlobal.tooltip:
            ZGlobal.tooltip.setInsideOf(None)
            ZGlobal.tooltip.hideTip()
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.pressed.emit(event.position().toPoint())

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.released.emit(event.position().toPoint())
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit(event.position().toPoint())

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.NoButton:
            self.hoverMove.emit(event.position().toPoint())

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)

    # endregion

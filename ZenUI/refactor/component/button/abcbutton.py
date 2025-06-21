from enum import IntEnum
import logging
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QPoint, QEvent, Property
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.refactor.core import ZGlobal
logging.basicConfig(level=logging.INFO)
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
        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.clicked.connect(self.clickHandler)
        self.hoverMove.connect(self.hoverMoveHandler)


    def setHoverMoveSignal(self, enabled: bool):
        if enabled: self.setMouseTracking(True)
        else: self.setMouseTracking(False)

    @Property(int)
    def state(self):
        return self._state

    @state.setter
    def setState(self, state):
        self._state = state



    # region Slot
    @Slot(QPoint)
    def hoverHandler(self, pos:QPoint):
        logging.info(f"Hovered at {pos}")

    @Slot()
    def leaveHandler(self):
        logging.info("Leaved")

    @Slot(QPoint)
    def pressHandler(self, pos:QPoint):
        logging.info(f"Pressed at {pos}")

    @Slot(QPoint)
    def releaseHandler(self, pos:QPoint):
        logging.info(f"Released at {pos}")

    @Slot(QPoint)
    def clickHandler(self, pos:QPoint):
        logging.info(f"Clicked at {pos}")

    @Slot(QPoint)
    def hoverMoveHandler(self, pos:QPoint):
        logging.info(f"Hover move to {pos}")

    # endregion

    # region Event
    def enterEvent(self, event: QEnterEvent):
        """鼠标进入事件"""
        super().enterEvent(event)
        self.entered.emit(event.position().toPoint())

    def leaveEvent(self, event: QEvent):
        """鼠标离开事件"""
        super().leaveEvent(event)
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.pressed.emit(event.position().toPoint())

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.released.emit(event.position().toPoint())
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit(event.position().toPoint())

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        """鼠标移动事件"""
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.NoButton:
            self.hoverMove.emit(event.position().toPoint())

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)

    # endregion



if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    button = ZABCButton()
    button.show()
    sys.exit(app.exec())
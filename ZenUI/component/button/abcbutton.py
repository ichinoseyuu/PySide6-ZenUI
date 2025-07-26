from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QTimer,QSize,QPoint
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.core import ZGlobal

class ZABCButton(QWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    clicked = Signal()
    class State(IntEnum):
        Idle = 0
        Hover = 1
        Pressed = 2
    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = self.State.Idle
        self._tool_tip: str = ""
        self._repeat_click = False

        self._repeat_click_timer = QTimer(self) # 重复点击计时器
        self._repeat_click_timer.setInterval(50)
        self._repeat_click_timer.timeout.connect(self.clicked.emit)

        self._repeat_click_trigger = QTimer(self) # 重复点击触发器
        self._repeat_click_trigger.setSingleShot(True)
        self._repeat_click_trigger.timeout.connect(self._repeat_click_timer.start)
        self._repeat_click_trigger.setInterval(500)

        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.clicked.connect(self.clickHandler)

    # region Property
    @property
    def state(self) -> State:
        return self._state


    @property
    def repeatClick(self) -> bool:
        return self._repeat_click

    @repeatClick.setter
    def repeatClick(self, enabled: bool) -> None:
        self._repeat_click = enabled


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

    @Slot()
    def clickHandler(self):
        pass

    # endregion

    # region Event
    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)
        if self._tool_tip != "":
            ZGlobal.tooltip.showTip(text=self._tool_tip, target=self)
        self._state = self.State.Hover
        self.entered.emit()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        if self._tool_tip != "": ZGlobal.tooltip.hideTip()
        self._state = self.State.Idle
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._state = self.State.Pressed
            self.pressed.emit()
            if self._repeat_click:
                self._repeat_click_trigger.start()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self._state = self.State.Hover
            self.released.emit()
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()
            self._repeat_click_trigger.stop()
            self._repeat_click_timer.stop()


    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)

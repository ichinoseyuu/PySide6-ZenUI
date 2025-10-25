from enum import Enum
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QMouseEvent, QEnterEvent
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.base import QAnimatedColor

class ZABCTitleBarButton(QWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    clicked = Signal()

    class State(Enum):
        Idle = 0
        Hover = 1
        Pressed = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_NoMousePropagation) # 防止鼠标事件传播到父组件
        self.setFixedSize(46, 32)

        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.clicked.connect(self.clickHandler)

        self._state = self.State.Idle

        self._body_cc = QAnimatedColor(self)
        self._icon_cc = QAnimatedColor(self)

    # region Property
    @property
    def state(self) -> State: return self._state

    # region Func
    def isPressed(self) -> bool: return self._state == self.State.Pressed

    # region Slot
    def hoverHandler(self):
        pass

    def leaveHandler(self):
        pass

    def pressHandler(self):
        pass

    def releaseHandler(self):
        pass

    def clickHandler(self):
        pass

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
            self._state = self.State.Hover
            self.released.emit()
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)
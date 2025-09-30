from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QPoint, QEvent, QTimer
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.component.base import ZState
class ABCButton(QWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    clicked = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        # self.setMouseTracking(True)
        self._state = ZState.Idle
        self._tool_tip: str = ""
        self.entered.connect(self.hoverHandler)
        self.leaved.connect(self.leaveHandler)
        self.pressed.connect(self.pressHandler)
        self.released.connect(self.releaseHandler)
        self.clicked.connect(self.clickHandler)


    # region Slot
    @Slot()
    def hoverHandler(self): ...

    @Slot()
    def leaveHandler(self): ...

    @Slot()
    def pressHandler(self): ...

    @Slot()
    def releaseHandler(self): ...

    @Slot(QPoint)
    def clickHandler(self): ...


    # region Property
    @property
    def state(self) -> ZState: return self._state

    @property
    def toolTip(self): return self._tool_tip

    @toolTip.setter
    def toolTip(self, tip: str):
        self._tool_tip = tip
        self.update()

    # region Public
    def setToolTip(self, tip: str):
        self._tool_tip = tip
        self.update()


    # region Event
    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)
        self._state = ZState.Hover
        self.entered.emit()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self._state = ZState.Idle
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self._state = ZState.Pressed
            self.pressed.emit()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.released.emit()
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)


class ABCToggleButton(ABCButton):
    toggled = Signal(bool)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._checkable: bool = True
        self._checked: bool = False
        self._is_group_member: bool = False  # 标记是否为按钮组成员
        self.toggled.connect(self.toggleHandler)

    # region Slot
    @Slot(bool)
    def toggleHandler(self, c: bool): ...

    # region Property
    @property
    def checked(self) -> bool: return self._checked

    @checked.setter
    def checked(self, c: bool):
        self._checked = c
        self.toggled.emit(self._checked)

    @property
    def checkable(self) -> bool: return self._checkable

    @checkable.setter
    def checkable(self, c: bool): self._checkable = c

    @property
    def isGroupMember(self) -> bool: return self._is_group_member

    @isGroupMember.setter
    def isGroupMember(self, b: bool): self._is_group_member = b

    # region Event
    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self._checkable:
            if self.rect().contains(event.position().toPoint()):
                if not self._is_group_member:
                    self._checked = not self._checked
                    self.toggled.emit(self._checked)
                else:
                    if not self._checked:
                        self._checked = True
                        self.toggled.emit(self._checked)


class ABCRepeatButton(ABCButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repeatable = True
        self._repeat_count = 1

        self._repeat_timer = QTimer(self) # 重复点击计时器
        self._repeat_timer.setInterval(50)
        self._repeat_timer.timeout.connect(self.repeatClickHandler)

        self._delay_timer = QTimer(self) # 延迟启动计时器
        self._delay_timer.setSingleShot(True)
        self._delay_timer.setInterval(500)
        self._delay_timer.timeout.connect(self._repeat_timer.start)


    # region Slot
    @Slot()
    def repeatClickHandler(self):
        self._repeat_count += 1
        self.clicked.emit()

    # region Property
    @property
    def repeatable(self) -> bool: return self._repeatable

    @repeatable.setter
    def repeatable(self, r: bool): self._repeatable = r

    @property
    def repeatCount(self) -> int: return self._repeat_count

    @property
    def delayTime(self) -> int: return self._delay_timer.interval()

    @delayTime.setter
    def delayTime(self, delay: int): self._delay_timer.setInterval(delay)

    @property
    def repeatTime(self) -> int: return self._repeat_timer.interval()

    @repeatTime.setter
    def repeatTime(self, repeat: int): self._repeat_timer.setInterval(repeat)


    # region Event
    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self._repeatable:
            #self.setMouseTracking(True)
            self._delay_timer.start()

    # def mouseMoveEvent(self, event: QMouseEvent):
    #     super().mouseMoveEvent(event)
    #     if self._repeatable and self._repeat_timer.isActive():
    #         if self.rect().contains(event.position().toPoint()):
    #             # 鼠标回到按钮内，重启计时器
    #             if not self._repeat_timer.isActive():
    #                 self._repeat_timer.start()
    #         else:
    #             # 鼠标移出按钮，停止计时器
    #             self._repeat_timer.stop()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self._repeatable:
            self._delay_timer.stop()
            self._repeat_timer.stop()
            self._repeat_count = 1
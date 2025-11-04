from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QTimer
from PySide6.QtGui import QMouseEvent, QEnterEvent, QFont
from ZenWidgets.core import ZState
from ZenWidgets.component.base.widget import ZWidget
# region ABCButton
class ABCButton(ZWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    clicked = Signal()
    def __init__(self,
                 parent: QWidget | ZWidget | None = None,
                 *args,
                 objectName: str | None = None,
                 toolTip: str | None = None,
                 **kwargs
                 ):
        super().__init__(parent,
                         *args,
                         objectName=objectName,
                         toolTip=toolTip,
                         **kwargs
                         )
        self.entered.connect(self._hover_handler_)
        self.leaved.connect(self._leave_handler_)
        self.pressed.connect(self._press_handler_)
        self.released.connect(self._release_handler_)
        self.clicked.connect(self._click_handler_)


    # region slot
    @Slot()
    def _hover_handler_(self):
        '''鼠标进入时的槽函数'''

    @Slot()
    def _leave_handler_(self):
        '''鼠标离开时的槽函数'''

    @Slot()
    def _press_handler_(self):
        '''鼠标按下时的槽函数'''

    @Slot()
    def _release_handler_(self):
        '''鼠标释放时的槽函数'''

    @Slot()
    def _click_handler_(self):
        '''鼠标成功点击时的槽函数'''

    # region event
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

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if self.rect().contains(event.position().toPoint()):
            self._state = ZState.Hover
            self.entered.emit()
        else:
            self._state = ZState.Idle
            self.leaved.emit()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.released.emit()
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()



# region ABCToggleButton
class ABCToggleButton(ABCButton):
    toggled = Signal(bool)
    def __init__(self,
                 parent: QWidget | ZWidget | None = None,
                 *args,
                 checked: bool = False,
                 checkable: bool = True,
                 is_group_member: bool = False,
                 objectName: str | None = None,
                 toolTip: str | None = None,
                 **kwargs
                 ):
        super().__init__(parent,
                         *args,
                         objectName=objectName,
                         toolTip=toolTip,
                         **kwargs
                         )
        self.toggled.connect(self._toggle_handler_)
        self._checkable: bool = checkable
        self._checked: bool = checked
        self._is_group_member: bool = is_group_member

    # region Slot
    @Slot(bool)
    def _toggle_handler_(self, c: bool):
        '''按钮状态改变时的槽函数'''

    # region public method
    def isChecked(self) -> bool: return self._checked

    def setChecked(self, c: bool):
        self._checked = c
        self.toggled.emit(self._checked)

    def isCheckable(self) -> bool: return self._checkable

    def setCheckable(self, c: bool): self._checkable = c

    def isGroupMember(self) -> bool: return self._is_group_member

    def setGroupMember(self, b: bool): self._is_group_member = b

    # region event
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

# region ABCRepeatButton
class ABCRepeatButton(ABCButton):
    def __init__(self,
                 parent: QWidget | ZWidget | None = None,
                 *args,
                 repeatable: bool = True,
                 interval: int = 50,
                 delay: int = 500,
                 objectName: str | None = None,
                 toolTip: str | None = None,
                 **kwargs
                 ):
        super().__init__(parent,
                         *args,
                         objectName=objectName,
                         toolTip=toolTip,
                         **kwargs
                         )
        self._repeatable = repeatable
        self._repeat_count = 0

        self._trigger_interval = QTimer(self) # 触发间隔
        self._trigger_interval.setInterval(interval)
        self._trigger_interval.timeout.connect(self._repeat_click_handler_)

        self._trigger_delay = QTimer(self) # 触发延迟
        self._trigger_delay.setSingleShot(True)
        self._trigger_delay.setInterval(delay)
        self._trigger_delay.timeout.connect(self._trigger_interval.start)


    # region slot
    @Slot()
    def _repeat_click_handler_(self):
        '''重复点击时的槽函数'''
        self._repeat_count += 1
        self.clicked.emit()

    # region Property
    def isRepeatable(self) -> bool: return self._repeatable

    def setRepeatable(self, r: bool): self._repeatable = r

    def repeatCount(self) -> int: return self._repeat_count

    def triggerInterval(self) -> int: return self._trigger_interval.interval()

    def setTriggerInterval(self, t: int): self._trigger_interval.setInterval(t)

    def triggerDelay(self) -> int: return self._trigger_delay.interval()

    def setTriggerDelay(self, d: int): self._trigger_delay.setInterval(d)

    # region event
    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self._repeatable:
            #self.setMouseTracking(True)
            self._trigger_delay.start()

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
            self._trigger_delay.stop()
            self._trigger_interval.stop()
            self._repeat_count = 0
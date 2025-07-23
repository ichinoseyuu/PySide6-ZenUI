from enum import Enum
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QMouseEvent, QEnterEvent
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import BackGroundStyle,IconStyle
from ZenUI.core import ZGlobal, ZTitleBarButtonData

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
        # 属性
        self._state = self.State.Idle
        self._style_data: ZTitleBarButtonData = None
        # 样式属性
        self._background_style = BackGroundStyle(self)
        self._icon_style = IconStyle(self)
        # 主题管理
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

    # region Property
    @property
    def state(self) -> State:
        return self._state

    @property
    def styleData(self) -> ZTitleBarButtonData:
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZTitleBarButtonData):
        self._style_data = style_data
        self._background_style.color = style_data.Body
        self._icon_style.color = style_data.Icon
        self.update()

    # region Func
    def isPressed(self) -> bool:
        """判断按钮是否被按下"""
        return self._state == self.State.Pressed

    # region Slot
    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__, theme.name)
        self._background_style.setColorTo(self._style_data.Body)
        self._icon_style.setColorTo(self._style_data.Icon)

    def hoverHandler(self):
        self._background_style.setColorTo(self._style_data.BodyHover)
        self._icon_style.setColorTo(self._style_data.IconHover)

    def leaveHandler(self):
        self._background_style.setColorTo(self._style_data.Body)
        self._icon_style.setColorTo(self._style_data.Icon)

    def pressHandler(self):
        self._background_style.setColorTo(self._style_data.BodyPressed)
        self._icon_style.setColorTo(self._style_data.IconPressed)

    def releaseHandler(self):
        self._background_style.setColorTo(self._style_data.Body)
        self._icon_style.setColorTo(self._style_data.Icon)

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
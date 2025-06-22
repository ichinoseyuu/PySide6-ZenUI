from enum import IntEnum
from PySide6.QtCore import Qt, Property, Signal, QEvent,QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QMouseEvent, QEnterEvent
from PySide6.QtWidgets import QWidget
from ZenUI.core import ZGlobal
class State(IntEnum):
    Idle = 0
    Hover = 1
    Pressed = 2

class ZABCTitleBarButton(QWidget):
    entered = Signal()
    leaved = Signal()
    pressed = Signal()
    released = Signal()
    clicked = Signal()
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
        self._state = State.Idle
        self._color_bg = QColor(0, 0, 0)
        self._color_icon = QColor(0, 0, 0)
        self._style_data = None
        # 属性动画
        self._anim_bg = QPropertyAnimation(self, b"backgroundColor")
        self._anim_bg.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim_bg.setDuration(150)
        self._anim_icon = QPropertyAnimation(self, b"iconColor")
        self._anim_icon.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim_icon.setDuration(150)
        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

    # region Property
    @property
    def state(self) -> State:
        return self._state

    @Property(QColor)
    def backgroundColor(self) -> QColor:
        """获取按钮背景颜色"""
        return self._color_bg

    @backgroundColor.setter
    def backgroundColor(self, color: QColor) -> None:
        """设置按钮背景颜色"""
        self._color_bg = color
        self.update()

    @Property(QColor)
    def iconColor(self) -> QColor:
        """获取图标颜色"""
        return self._color_icon

    @iconColor.setter
    def iconColor(self, color: QColor) -> None:
        """设置图标颜色"""
        self._color_icon = color
        self.update()

    # region Func

    def isPressed(self) -> bool:
        """判断按钮是否被按下"""
        return self._state == State.Pressed

    def setStyleData(self, style_data):
        self._style_data = style_data
        self._color_bg = QColor(self._style_data.body)
        self._color_icon = QColor(self._style_data.icon)
        self.update()

    def setBackgroundColorTo(self, color: QColor):
        self._anim_bg.stop()
        self._anim_bg.setStartValue(self._color_bg)
        self._anim_bg.setEndValue(color)
        self._anim_bg.start()

    def setIconColorTo(self, color: QColor):
        self._anim_icon.stop()
        self._anim_icon.setStartValue(self._color_icon)
        self._anim_icon.setEndValue(color)
        self._anim_icon.start()

    # region Slot
    def themeChangeHandler(self, theme):
        pass

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

    def hoverMoveHandler(self):
        pass


    # region Event
    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)
        self._state = State.Hover
        self.entered.emit()

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)
        self._state = State.Idle
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._state = State.Pressed
            self.pressed.emit()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self._state = State.Hover
            self.released.emit()
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)
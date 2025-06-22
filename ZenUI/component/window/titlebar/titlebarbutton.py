# coding:utf-8
from enum import IntEnum
from PySide6.QtCore import QPointF, Qt, Property, Signal, Slot, QEvent,QPropertyAnimation, QEasingCurve,QLineF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QMouseEvent, QEnterEvent
from PySide6.QtWidgets import QWidget
from ZenUI.core import ZGlobal
class State(IntEnum):
    Idle = 0
    Hover = 1
    Press = 2
# region TitleBarButton
class ZTitleBarButton(QWidget):
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
    @Property(State)
    def state(self):
        """获取按钮状态"""
        return self._state

    @state.setter
    def state(self, state: State):
        """设置按钮状态"""
        self._state = state

    @Property(QColor)
    def backgroundColor(self):
        """获取按钮背景颜色"""
        return self._color_bg

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        """设置按钮背景颜色"""
        self._color_bg = color
        self.update()

    @Property(QColor)
    def iconColor(self):
        """获取图标颜色"""
        return self._color_icon

    @iconColor.setter
    def iconColor(self, color: QColor):
        """设置图标颜色"""
        self._color_icon = color
        self.update()

    # region Public Func

    def isPressed(self):
        """判断按钮是否被按下"""
        return self._state == State.Press

    def setStyleData(self, style_data):
        """设置按钮样式数据"""
        self._style_data = style_data
        self._color_bg = QColor(self._style_data.body)
        self._color_icon = QColor(self._style_data.icon)
        self.update()

    def setBackgroundColorTo(self, color: QColor):
        """设置按钮背景颜色"""
        self._anim_bg.stop()
        self._anim_bg.setStartValue(self._color_bg)
        self._anim_bg.setEndValue(color)
        self._anim_bg.start()

    def setIconColorTo(self, color: QColor):
        """设置图标颜色"""
        self._anim_icon.stop()
        self._anim_icon.setStartValue(self._color_icon)
        self._anim_icon.setEndValue(color)
        self._anim_icon.start()

    # region Slot
    def themeChangeHandler(self, theme):
        ...

    @Slot()
    def hoverHandler(self):
        ...

    @Slot()
    def leaveHandler(self):
        ...

    @Slot()
    def pressHandler(self):
        ...

    @Slot()
    def releaseHandler(self):
        ...

    @Slot()
    def clickHandler(self):
        ...

    @Slot()
    def hoverMoveHandler(self):
        ...

    # endregion

    # region Event
    def enterEvent(self, event: QEnterEvent):
        """鼠标进入事件"""
        super().enterEvent(event)
        self.state = State.Hover
        self.entered.emit()

    def leaveEvent(self, event: QEvent):
        """鼠标离开事件"""
        super().leaveEvent(event)
        self.state = State.Idle
        self.leaved.emit()

    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.state = State.Press
            self.pressed.emit()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.state = State.Hover
            self.released.emit()
            # 如果鼠标在按钮区域内释放，触发clicked信号
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)


class ZMinimizeButton(ZTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZMinimizeButton"))

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZMinimizeButton", theme.name)
        self.setIconColorTo(QColor(self._style_data.icon))
        self.setBackgroundColorTo(QColor(self._style_data.body))

    def hoverHandler(self):
        self.setBackgroundColorTo(self._style_data.bodyhover)
        self.setIconColorTo(QColor(self._style_data.iconhover))

    def leaveHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def pressHandler(self):
        self.setBackgroundColorTo(self._style_data.bodypressed)
        self.setIconColorTo(QColor(self._style_data.iconpressed))

    def releaseHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def paintEvent(self, e):
        painter = QPainter(self)
        # draw background
        painter.setBrush(self._color_bg)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._color_icon, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class ZMaximizeButton(ZTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZMaximizeButton"))

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZMaximizeButton", theme.name)
        self.setIconColorTo(QColor(self._style_data.icon))
        self.setBackgroundColorTo(QColor(self._style_data.body))

    def hoverHandler(self):
        self.setBackgroundColorTo(self._style_data.bodyhover)
        self.setIconColorTo(QColor(self._style_data.iconhover))

    def leaveHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def pressHandler(self):
        self.setBackgroundColorTo(self._style_data.bodypressed)
        self.setIconColorTo(QColor(self._style_data.iconpressed))

    def releaseHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def setMaxState(self, isMax):
        if self._isMax == isMax: return
        self._isMax = isMax
        self.update()

    def toggleMaxState(self):
        self._isMax = not self._isMax
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        # draw background
        painter.setBrush(self._color_bg)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))

        # draw icon
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._color_icon, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self._isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)


class ZCloseButton(ZTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZCloseButton"))

    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZCloseButton", theme.name)
        self.setIconColorTo(QColor(self._style_data.icon))
        self.setBackgroundColorTo(QColor(self._style_data.body))

    def hoverHandler(self):
        self.setBackgroundColorTo(self._style_data.bodyhover)
        self.setIconColorTo(QColor(self._style_data.iconhover))

    def leaveHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def pressHandler(self):
        self.setBackgroundColorTo(self._style_data.bodypressed)
        self.setIconColorTo(QColor(self._style_data.iconpressed))

    def releaseHandler(self):
        self.setBackgroundColorTo(self._style_data.body)
        self.setIconColorTo(QColor(self._style_data.icon))

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        r = self.devicePixelRatioF()
        painter.setBrush(self._color_bg)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))

        pen = QPen(self._color_icon, 1.1 * r)  # 增加线宽
        pen.setCapStyle(Qt.RoundCap)  # 设置线段端点为圆形
        pen.setJoinStyle(Qt.RoundJoin)  # 设置线段连接处为圆形
        pen.setCosmetic(True)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        w, h = self.width(), self.height()
        iw = ih = 9
        x = w/2 - iw/2
        y = h/2 - ih/2
        lines = [
            QLineF(x, y, x + iw, y + ih),        # 左上到右下
            QLineF(x + iw, y, x, y + ih)         # 右上到左下
        ]
        painter.drawLines(lines)
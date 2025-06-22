# coding:utf-8
from PySide6.QtCore import QEvent, Qt, QPoint, Signal
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from .abctitlebarbutton import ZABCTitleBarButton
from .closebutton import ZCloseButton
from .maximizebutton import ZMaximizeButton
from .minimizebutton import ZMinimizeButton


class TitleBarBase(QWidget):
    moved = Signal(QPoint)
    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = ZMinimizeButton(parent=self)
        self.closeBtn = ZCloseButton(parent=self)
        self.maxBtn = ZMaximizeButton(parent=self)
        self._isDoubleClickEnabled = True
        self._moved = False
        self.dragPosition: QPoint = None
        self.setFixedHeight(32)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton or not self._isDoubleClickEnabled:
            return

        self.__toggleMaxState()

    def mousePressEvent(self, event: QMouseEvent):
        window = self.window()._resize_grip
        if self.window().isMaximized():
            # 计算还原时的窗口位置和大小
            normalGeo = self.window().normalGeometry()
            pos = event.globalPosition().toPoint()
            ratio = pos.x() / self.width()
            x = int(pos.x() - normalGeo.width() * ratio)
            y = pos.y()
            window.setGeometry(x, y, normalGeo.width(), normalGeo.height())
        self.dragPosition = event.globalPosition().toPoint() - window.pos()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.dragPosition: return 
        window = self.window()._resize_grip
        newPos = event.globalPosition().toPoint() - self.dragPosition
        window.move(newPos)
        self._moved = True
        event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self._moved:
            self.moved.emit(event.globalPos())
            self._moved = False

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
        self._releaseMouseLeftButton()


    def _releaseMouseLeftButton(self):
        from ..win32utils import releaseMouseLeftButton
        releaseMouseLeftButton(self.window().winId())

    def _isDragRegion(self, pos):
        width = 0
        for button in self.findChildren(ZABCTitleBarButton):
            if button.isVisible():
                width += button.width()

        return 0 < pos.x() < self.width() - width

    def _hasButtonPressed(self):
        return any(btn.isPressed() for btn in self.findChildren(ZABCTitleBarButton))

    def canDrag(self, pos):
        return self._isDragRegion(pos) and not self._hasButtonPressed()

    def setDoubleClickEnabled(self, isEnabled):
        self._isDoubleClickEnabled = isEnabled

class AcrylicTitleBar(TitleBarBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)


class StandardAcrylicTitleBar(AcrylicTitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft)
        self.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                padding: 0 4px
            }
        """)
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(20, 20))

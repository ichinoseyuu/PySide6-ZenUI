# coding:utf-8
from PySide6.QtCore import QEvent, Qt, QPoint, Signal
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from ..win32utils import startSystemMove
from .abctitlebarbutton import ZABCTitleBarButton
from .closebutton import ZCloseButton
from .maximizebutton import ZMaximizeButton
from .minimizebutton import ZMinimizeButton


class ZTitleBarBase(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = ZMinimizeButton(parent=self)
        self.closeBtn = ZCloseButton(parent=self)
        self.maxBtn = ZMaximizeButton(parent=self)
        self._isDoubleClickEnabled = True
        self._moved = False
        self.dragPosition: QPoint = None
        self.setFixedHeight(32)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        #self.setStyleSheet("background-color: transparent;border: 1px solid red;")

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.window():
            if event.type() == QEvent.WindowStateChange:
                self.maxBtn.toggleMaxState()
                return False

        return super().eventFilter(obj, event)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton or not self._isDoubleClickEnabled:
            return
        self.__toggleMaxState()

    def mouseMoveEvent(self, event):
        if not self.canDrag(event.pos()): return
        startSystemMove(self.window())

    def mousePressEvent(self, event):
        if not self.canDrag(event.pos()): return

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

class ZTitleBar(ZTitleBarBase):
    """ Title bar with minimize, maximum and close button """

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


class ZStandardTitleBar(ZTitleBar):
    """ Title bar with icon and title """

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

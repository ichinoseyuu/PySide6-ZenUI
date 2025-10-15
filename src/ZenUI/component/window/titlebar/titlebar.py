# coding:utf-8
from PySide6.QtCore import QEvent, Qt, QPoint,QMargins
from PySide6.QtGui import QIcon,QPainter
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from ZenUI.component.headline import ZHeadLine
from ZenUI.core import ZGlobal,ZDebug
from ..win32utils import startSystemMove, toggleWindowState
from .abctitlebarbutton import ZABCTitleBarButton
from .closebutton import ZCloseButton
from .maximizebutton import ZMaximizeButton
from .minimizebutton import ZMinimizeButton
from .themebutton import ZThemeButton


class ZTitleBarBase(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.themeBtn = ZThemeButton(parent=self)
        self.minBtn = ZMinimizeButton(parent=self)
        self.maxBtn = ZMaximizeButton(parent=self)
        self.closeBtn = ZCloseButton(parent=self)
        self._isDoubleClickEnabled = True
        self._moved = False
        self.dragPosition: QPoint = None
        self.setFixedHeight(32)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet("background-color: transparent;border: 1px solid red;")

        # connect signal to slot
        self.themeBtn.clicked.connect(ZGlobal.themeManager.toggleThemeForce)
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
        toggleWindowState(self.window())
        self._releaseMouseLeftButton()


    def _releaseMouseLeftButton(self):
        from ..win32utils import releaseMouseLeftButton
        releaseMouseLeftButton(self.window().winId())

    # def _isDragRegion(self, pos):
    #     # 如果鼠标在任何按钮区域内，则不可拖动
    #     for button in self.findChildren(ZABCTitleBarButton):
    #         if button.isVisible() and button.geometry().contains(pos):
    #             return False
    #     return True

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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()


class ZTitleBar(ZTitleBarBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft|
                                    Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.themeBtn, 0, Qt.AlignRight|Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight|Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight|Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight|Qt.AlignVCenter)

        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft|Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        self.title = ZHeadLine(self)
        self.hBoxLayout.insertWidget(2, self.title, 0, Qt.AlignLeft|Qt.AlignVCenter)
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.title.text = title

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(20, 20))

    def setIconVisible(self, isVisible: bool):
        self.iconLabel.setVisible(isVisible)

    def setThemeBtnVisible(self, isVisible: bool):
        self.themeBtn.setVisible(isVisible)

    def setMaxBtnVisible(self, isVisible: bool):
        self.maxBtn.setVisible(isVisible)
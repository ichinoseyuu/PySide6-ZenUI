from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG
import win32con
import win32gui
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.window.utils.win32_utils import Taskbar, isMaximized, isFullScreen, getResizeBorderThickness
from ZenUI.component.window.utils.c_structures import LPNCCALCSIZE_PARAMS
from ZenUI.component.window.utils.window_effect import WindowEffect
from ZenUI.component.window.titlebar import ZTitlebar
class ZWindow(ZWidget):
    """窗口"""
    border_width = 5
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint) # 无边框
        self._isResizeEnabled = True # 是否允许调整窗口大小
        # 添加DWM阴影和最大化动画
        self._windowEffect = WindowEffect(self)
        self._windowEffect.addWindowAnimation(self.winId())
        self._windowEffect.addShadowEffect(self.winId())
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)
        self.setObjectName("zenMainWindow")
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self._titlebar_container = QHBoxLayout()
        self._titlebar_container.setContentsMargins(0, 0, 0, 0)
        self._titlebar_container.setSpacing(0)
        self._layout.addLayout(self._titlebar_container)
        self._container = QVBoxLayout()
        self._container.setContentsMargins(0, 0, 0, 0)
        self._container.setSpacing(0)
        self._layout.addLayout(self._container)
        self.setTitlebar(ZTitlebar(self))

    def addWidget(self, widget):
        self._container.addWidget(widget)

    def addLayout(self, layout):
        self._container.addLayout(layout)

    def insertWidget(self, index, widget):
        self._container.insertWidget(index, widget)

    def setTitlebar(self, titleBar):
        """ 设置标题栏 """
        self._titlebar_container.addWidget(titleBar)
        self._titlebar = titleBar
        # self.titleBar.setParent(self)
        # self.titleBar.raise_() #将标题显示在最上层

    def setWindowTitle(self, arg__1):
        self._titlebar.setTitle(arg__1)


    def setCenter(self):
        ''' 将窗口放在屏幕中心 '''
        # 获取当前屏幕的尺寸
        screen = QApplication.primaryScreen()
        # 计算窗口应该放置的位置，使其位于屏幕中央
        x = (screen.geometry().width() - self.geometry().width()) // 2
        y = (screen.geometry().height() - self.geometry().height()) // 2
        # 设置窗口位置为屏幕中心
        self.move(x, y)


    def setResizeEnabled(self, isEnabled: bool):
        """设置是否允许调整窗口大小"""
        self._isResizeEnabled = isEnabled


    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        #self.titleBar.resize(self.width(), self.titleBar.height())
        #self._board.resize(self.width(), self.height()-self.titleBar.height())
        #self._board.resize(event.size())

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(eventType, message)

        if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w = self.frameGeometry().width()
            h = self.frameGeometry().height()

            bw = 0 if isMaximized(msg.hWnd) or isFullScreen(msg.hWnd) else self.border_width
            lx = xPos < bw
            rx = xPos > w - bw
            ty = yPos < bw
            by = yPos > h - bw
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = isMaximized(msg.hWnd)
            isFull = isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                ty = getResizeBorderThickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty

                tx = getResizeBorderThickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.isAutoHide():
                position = Taskbar.getPosition(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result

        return super().nativeEvent(eventType, message)

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                            win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

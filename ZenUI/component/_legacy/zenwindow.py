# coding:utf-8

from ctypes import cast,windll
from ctypes.wintypes import LPRECT, MSG
import win32api
import win32con
import win32gui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from .utils import win32_utils as win_utils
from .utils.win32_utils import Taskbar
from .utils.c_structures import LPNCCALCSIZE_PARAMS
from .utils.window_effect import WindowEffect
from ..board.zenboard import ZenBoard


class ZenWindow(QWidget):
    """ZenUI窗口"""
    border_width = 5
    def __init__(self, parent=None,titlebar=None):
        super().__init__(parent=parent)
        if titlebar is not None:
            self.setTitleBar(titlebar)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet('background-color: transparent;')
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self._isResizeEnabled = True # 是否允许调整窗口大小
        self.windowEffect = WindowEffect(self)
        # 添加DWM阴影和最大化动画
        self.windowEffect.addWindowAnimation(self.winId())
        # self.windowEffect.addShadowEffect(self.winId())
        #self.windowHandle().screenChanged.connect(self.__onScreenChanged)
        self.resize(400, 300)

        self._board = ZenBoard(self,'board')
        
        # self.Layout = QVBoxLayout(self)
        # self.Layout.setContentsMargins(0, 0, 0, 0)
        # self.Layout.setSpacing(0)
        # self.setLayout(self.Layout)
        # self._titlebar_container = QVBoxLayout()
        # self._titlebar_container.setContentsMargins(0, 0, 0, 0)
        # self._titlebar_container.setSpacing(0)
        # self.Layout.addLayout(self._titlebar_container)
        # #self._titlebar_container.addWidget(QLabel('标题栏', self))
        # self._container = QVBoxLayout()
        # self._container.setContentsMargins(0, 0, 0, 0)
        # self._container.setSpacing(0)
        # self.Layout.addLayout(self._container)
        # #self._container.addWidget(QLabel('main board', self))
        


    def addWidget(self, widget):
        self._container.addWidget(widget)

    def setTitleBar(self, titleBar):
        """ 设置标题栏 """
        self._titlebar_container.addWidget(titleBar)
        # self.titleBar = titleBar
        # self.titleBar.setParent(self)
        # self.titleBar.raise_() #将标题显示在最上层


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
        self._board.resize(event.size())
    def nativeEvent(self, eventType, message):
        pass
    # def nativeEvent(self, eventType, message):
    #     """ Handle the Windows message """
    #     msg = MSG.from_address(message.__int__())
    #     # if not msg.hWnd:
    #     #     return super().nativeEvent(eventType, message)

    #     if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
    #         pos = QCursor.pos()
    #         xPos = pos.x() - self.x()
    #         yPos = pos.y() - self.y()
    #         w = self.frameGeometry().width()
    #         h = self.frameGeometry().height()

    #         bw = 0 if win_utils.isMaximized(msg.hWnd) or win_utils.isFullScreen(msg.hWnd) else self.border_width
    #         lx = xPos < bw
    #         rx = xPos > w - bw
    #         ty = yPos < bw
    #         by = yPos > h - bw
    #         if lx and ty:
    #             return True, win32con.HTTOPLEFT
    #         elif rx and by:
    #             return True, win32con.HTBOTTOMRIGHT
    #         elif rx and ty:
    #             return True, win32con.HTTOPRIGHT
    #         elif lx and by:
    #             return True, win32con.HTBOTTOMLEFT
    #         elif ty:
    #             return True, win32con.HTTOP
    #         elif by:
    #             return True, win32con.HTBOTTOM
    #         elif lx:
    #             return True, win32con.HTLEFT
    #         elif rx:
    #             return True, win32con.HTRIGHT
    #     elif msg.message == win32con.WM_NCCALCSIZE:
    #         if msg.wParam:
    #             rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
    #         else:
    #             rect = cast(msg.lParam, LPRECT).contents

    #         isMax = win_utils.isMaximized(msg.hWnd)
    #         isFull = win_utils.isFullScreen(msg.hWnd)

    #         # adjust the size of client rect
    #         if isMax and not isFull:
    #             ty = win_utils.getResizeBorderThickness(msg.hWnd, False)
    #             rect.top += ty
    #             rect.bottom -= ty

    #             tx = win_utils.getResizeBorderThickness(msg.hWnd, True)
    #             rect.left += tx
    #             rect.right -= tx

    #         # handle the situation that an auto-hide taskbar is enabled
    #         if (isMax or isFull) and Taskbar.isAutoHide():
    #             position = Taskbar.getPosition(msg.hWnd)
    #             if position == Taskbar.LEFT:
    #                 rect.top += Taskbar.AUTO_HIDE_THICKNESS
    #             elif position == Taskbar.BOTTOM:
    #                 rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
    #             elif position == Taskbar.LEFT:
    #                 rect.left += Taskbar.AUTO_HIDE_THICKNESS
    #             elif position == Taskbar.RIGHT:
    #                 rect.right -= Taskbar.AUTO_HIDE_THICKNESS

    #         result = 0 if not msg.wParam else win32con.WVR_REDRAW
    #         return True, result

    #     return super().nativeEvent(eventType, message)

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                            win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    # def winEvent(self, event):
    #     if event.type() == 14:  # 系统事件
    #         hwnd = self.winId()  # 获取窗口句柄
    #         windll.user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
    #         windll.user32.SetLayeredWindowAttributes(hwnd, 2, 128, 2)  # 设置透明度（128为50%）
    #     return super().winEvent(event)

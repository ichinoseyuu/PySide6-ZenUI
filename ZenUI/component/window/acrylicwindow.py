import win32api
import win32con
import win32gui
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRect,Property,QPoint
from PySide6.QtGui import QResizeEvent,QColor
from ZenUI.core import ZGlobal,ZTheme
from .titlebar.acrylictitlebar import AcrylicTitleBar
from .resizewidget import ResizeWindow
from .utils import (WindowsWindowEffect,LPNCCALCSIZE_PARAMS,WinTaskbar,
                    isSystemBorderAccentEnabled, getSystemAccentColor,
                    isMaximized, isFullScreen, getResizeBorderThickness)

class AcrylicWindow(QWidget):
    """亚克力窗口"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._isResizeEnabled = True
        self._titlebar = AcrylicTitleBar(self)
        self._resize_grip = ResizeWindow(self)
        self._resize_grip.resized.connect(self.resizedHandler)
        self._resize_grip.setGeometry(self.geometry())
        self._resize_grip.show()
        self._resize_grip.moved.connect(self.movedHandler)
        self._windowEffect = WindowsWindowEffect(self)
        self._windowEffect.addWindowAnimation(self.winId())
        self.setStyleSheet("background-color: transparent;")
        color = "202020b4" if ZGlobal.themeManager.getTheme() == ZTheme.Dark else "f2f2f2b4"
        self._windowEffect.setAcrylicEffect(self.winId(), color, True, 0)
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @Property(QColor)
    def borderColor(self):
        return self._color_border

    @borderColor.setter
    def borderColor(self, color: QColor):
        self._color_border = color
        self.update()

    @Property(QColor)
    def backgroundColor(self):
        return self._color_bg

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        self._color_bg = color

    # region Public Func
    def setResizeEnabled(self, enabled: bool):
        """ 设置是否允许调整窗口大小 """
        self._isResizeEnabled = enabled

    def showNormal(self):
        super().showNormal()
        self._resize_grip.move(self.geometry().topLeft())
        self._titlebar.maxBtn.releaseHandler()

    def showMaximized(self):
        super().showMaximized()
        self._resize_grip.move(self.geometry().topLeft())

    # region Slot
    def themeChangeHandler(self, theme):
        color = "202020b4" if theme == ZTheme.Dark else "f2f2f2b4"
        self._windowEffect.setAcrylicEffect(self.winId(), color, True, 0)

    def resizedHandler(self, rect: QRect):
        self.move(rect.x(), rect.y())
        self.resize(rect.width(), rect.height())

    def movedHandler(self, pos: QPoint):
        if self.isMaximized():
            self.showNormal()
        else:
            self.move(pos)

    # region Event
    def resizeEvent(self, event: QResizeEvent):
        """ 调整窗口大小 """
        super().resizeEvent(event)
        self._titlebar.resize(self.width(), self._titlebar.height())
        #self._resize_grip.resize(self.width(), self.height())
        self._resize_grip.setGeometry(self.geometry())

    def moveEvent(self, event):
        super().moveEvent(event)
        self._resize_grip.move(self.geometry().topLeft())


    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(eventType, message)
        if msg.message == win32con.WM_NCCALCSIZE:
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
            if (isMax or isFull) and WinTaskbar.isAutoHide():
                position = WinTaskbar.getPosition(msg.hWnd)
                if position == WinTaskbar.LEFT:
                    rect.top += WinTaskbar.AUTO_HIDE_THICKNESS
                elif position == WinTaskbar.BOTTOM:
                    rect.bottom -= WinTaskbar.AUTO_HIDE_THICKNESS
                elif position == WinTaskbar.LEFT:
                    rect.left += WinTaskbar.AUTO_HIDE_THICKNESS
                elif position == WinTaskbar.RIGHT:
                    rect.right -= WinTaskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result
        elif msg.message == win32con.WM_SETFOCUS and isSystemBorderAccentEnabled():
            self._windowEffect.setBorderAccentColor(self.winId(), getSystemAccentColor())
            return True, 0
        elif msg.message == win32con.WM_KILLFOCUS:
            self._windowEffect.removeBorderAccentColor(self.winId())
            return True, 0

        return super().nativeEvent(eventType, message)

    # region Private Func
    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
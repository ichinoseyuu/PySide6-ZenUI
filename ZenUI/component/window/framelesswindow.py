import win32api
import win32con
import win32gui
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QPropertyAnimation,Property,QEasingCurve
from PySide6.QtGui import QResizeEvent,QColor
from ZenUI.core import ZGlobal,ZFramelessWindowStyleData
from ZenUI.component.tooltip import ZToolTip
from ZenUI._legacy.core import ZenGlobal
from ZenUI._legacy.component import ZToolTip as ZToolTipLegacy
from .titlebar.titlebar import ZTitleBar
from .win32utils import (WindowsWindowEffect,LPNCCALCSIZE_PARAMS,WinTaskbar,
                    isSystemBorderAccentEnabled, getSystemAccentColor,
                    isMaximized, isFullScreen, getResizeBorderThickness)

class ZFramelessWindow(QWidget):
    BORDER_WIDTH = 6
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # create tooltip
        tooltip = ZToolTip()
        tooltip.show()
        tooltip.setWindowOpacity(0)
        ZGlobal.tooltip = tooltip

        tooltiplegacy = ZToolTipLegacy()
        tooltiplegacy.show()
        tooltiplegacy.setWindowOpacity(0)
        ZenGlobal.ui.windows['ToolTip'] = tooltiplegacy

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet('background-color: transparent;')
        self._titlebar = ZTitleBar(self)
        self._centerWidget = QWidget(self)
        self._resizable = True
        self._windowEffect = WindowsWindowEffect(self)
        self._windowEffect.addWindowAnimation(self.winId())
        self._windowEffect.addShadowEffect(self.winId())
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)

        self._color_bg = QColor('#000000')
        self._anim_bg_color = QPropertyAnimation(self, b'backgroundColor')
        self._anim_bg_color.setDuration(150)
        self._anim_bg_color.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self._style_data: ZFramelessWindowStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZFramelessWindow")

        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

    # region Property
    @property
    def resizable(self) -> bool:
        return self._resizable

    @resizable.setter
    def resizable(self, enabled: bool) -> None:
        self._resizable = enabled

    @property
    def styleData(self) -> ZFramelessWindowStyleData:
        return self._style_data

    @styleData.setter
    def styleData(self, data: ZFramelessWindowStyleData) -> None:
        self._style_data = data
        self.backgroundColor = data.body

    @property
    def centerWidget(self):
        return self._centerWidget

    @Property(QColor)
    def backgroundColor(self) -> QColor:
        return self._color_bg

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        self._color_bg = color
        self._windowEffect.setBackgroundColor(self.winId(), color)

    # region Func
    def setBackgroundColorTo(self, color: QColor):
        self._anim_bg_color.setStartValue(self._color_bg)
        self._anim_bg_color.setEndValue(color)
        self._anim_bg_color.start()

    def moveCenter(self):
        screen = self.windowHandle().screen()
        if screen:
            rect = screen.availableGeometry()
            self.move(rect.center().x() - self.width() / 2, rect.center().y() - self.height() / 2)
        else:
            self.move(self.x() + self.width() / 2, self.y() + self.height() / 2)


    # region Slot
    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData('ZFramelessWindow', theme.name)
        self.setBackgroundColorTo(QColor(self._style_data.body))

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    # region Event
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self._titlebar.setGeometry(0,0,event.size().width(), self._titlebar.height())
        self._centerWidget.setGeometry(0, self._titlebar.height(), event.size().width(), event.size().height() - self._titlebar.height())


    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(eventType, message)

        if msg.message == win32con.WM_NCHITTEST and self._resizable:
            xPos, yPos = win32gui.ScreenToClient(msg.hWnd, win32api.GetCursorPos())
            clientRect = win32gui.GetClientRect(msg.hWnd)

            w = clientRect[2] - clientRect[0]
            h = clientRect[3] - clientRect[1]

            bw = 0 if isMaximized(msg.hWnd) or isFullScreen(msg.hWnd) else self.BORDER_WIDTH
            lx = xPos < bw  # left
            rx = xPos > w - bw  # right
            ty = yPos < bw  # top
            by = yPos > h - bw  # bottom
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
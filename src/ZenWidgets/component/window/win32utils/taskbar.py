import win32api
import win32con
import win32gui
from ctypes import byref, sizeof, windll
from ctypes.wintypes import RECT
from win32comext.shell import shellcon
from .c_structures import APPBARDATA
from .win32_func import isGreaterEqualWin8_1, getMonitorInfo
class WinTaskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def isAutoHide():
        """ 检测任务栏是否自动隐藏 """
        appbarData = APPBARDATA(
            sizeof(APPBARDATA),
            0, 0, 0,
            RECT(0, 0, 0, 0), 0
            )
        taskbarState = windll.shell32.SHAppBarMessage(
            shellcon.ABM_GETSTATE,
            byref(appbarData)
            )

        return taskbarState == shellcon.ABS_AUTOHIDE

    @classmethod
    def getPosition(cls, hWnd):
        """ 获取自动隐藏任务栏的位置

        Args:
            hWnd (int or `sip.voidptr`): 窗口句柄
        """
        if isGreaterEqualWin8_1():
            monitorInfo = getMonitorInfo(
                hWnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not monitorInfo:
                return cls.NO_POSITION

            monitor = RECT(*monitorInfo['Monitor'])
            appbarData = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
            positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
            for position in positions:
                appbarData.uEdge = position
                if windll.shell32.SHAppBarMessage(11, byref(appbarData)):
                    return position

            return cls.NO_POSITION

        appbarData = APPBARDATA(sizeof(APPBARDATA), win32gui.FindWindow(
            "Shell_TrayWnd", None), 0, 0, RECT(0, 0, 0, 0), 0)
        if appbarData.hWnd:
            windowMonitor = win32api.MonitorFromWindow(
                hWnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not windowMonitor:
                return cls.NO_POSITION

            taskbarMonitor = win32api.MonitorFromWindow(
                appbarData.hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
            if not taskbarMonitor:
                return cls.NO_POSITION

            if taskbarMonitor == windowMonitor:
                windll.shell32.SHAppBarMessage(
                    shellcon.ABM_GETTASKBARPOS, byref(appbarData))
                return appbarData.uEdge

        return cls.NO_POSITION

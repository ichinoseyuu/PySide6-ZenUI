import sys
import logging
import win32api
import win32con
import win32gui
import win32print
from ctypes import byref, windll, c_int, c_ulong, c_bool, POINTER
from ctypes.wintypes import HWND, UINT
from platform import platform
from winreg import OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx, CloseKey
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtGui import QGuiApplication, QColor

def getSystemAccentColor() -> QColor:
    """ 获取系统强调色"""
    DwmGetColorizationColor = windll.dwmapi.DwmGetColorizationColor
    DwmGetColorizationColor.restype = c_ulong
    DwmGetColorizationColor.argtypes = [POINTER(c_ulong), POINTER(c_bool)]

    color = c_ulong()
    code = DwmGetColorizationColor(byref(color), byref(c_bool()))

    if code != 0:
        logging.warning("Unable to obtain system accent color.")
        return QColor()

    return QColor(color.value)


def isSystemBorderAccentEnabled() -> bool:
    """ 检查是否启用了边框强调色 """
    if not isGreaterEqualWin11(): return False

    try:
        key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM", 0, KEY_READ)
        value, _ = QueryValueEx(key, "ColorPrevalence")
        CloseKey(key)
        return bool(value)
    except:
        return False


def isMaximized(hWnd) -> bool:
    """ 判断窗口是否最大化"""
    windowPlacement = win32gui.GetWindowPlacement(hWnd)

    if not windowPlacement: return False
    return windowPlacement[1] == win32con.SW_MAXIMIZE


def isFullScreen(hWnd):
    """ 判断窗口是否全屏"""
    if not hWnd: return False

    hWnd = int(hWnd)
    winRect = win32gui.GetWindowRect(hWnd)
    if not winRect: return False

    monitorInfo = getMonitorInfo(hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitorInfo: return False

    monitorRect = monitorInfo["Monitor"]
    return all(i == j for i, j in zip(winRect, monitorRect))


def isCompositionEnabled() -> bool:
    """ 检测是否启用了DWM合成 """
    bResult = c_int(0)
    windll.dwmapi.DwmIsCompositionEnabled(byref(bResult))
    return bool(bResult.value)


def getMonitorInfo(hWnd, dwFlags):
    """ 获取显示器信息,如果失败则返回 None

    Args:
        hWnd (int or `sip.voidptr`): 窗口句柄
        dwFlags (int): 查询标志
    """
    monitor = win32api.MonitorFromWindow(hWnd, dwFlags)
    if not monitor: return

    return win32api.GetMonitorInfo(monitor)


def getResizeBorderThickness(hWnd, horizontal=True):
    """ 获取窗口边框厚度
    
    Args:
        hWnd (int or `sip.voidptr`): 窗口句柄
        horizontal (bool, optional): 是否水平边框. Defaults to True.
    """
    window = findWindow(hWnd)
    if not window:
        return 0

    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    result = getSystemMetrics(hWnd, frame, horizontal) + getSystemMetrics(hWnd, 92, horizontal)

    if result > 0:
        return result

    thickness = 8 if isCompositionEnabled() else 4
    return round(thickness*window.devicePixelRatio())


def getSystemMetrics(hWnd, index, horizontal):
    """ 获取系统度量值 """
    if not hasattr(windll.user32, 'GetSystemMetricsForDpi'):
        return win32api.GetSystemMetrics(index)

    dpi = getDpiForWindow(hWnd, horizontal)
    return windll.user32.GetSystemMetricsForDpi(index, dpi)


def getDpiForWindow(hWnd, horizontal=True):
    """ 获取窗口DPI

    Args:
        hWnd (int or `sip.voidptr`): 窗口句柄
        horizontal (bool, optional): 是否水平边框. Defaults to True.
    """
    if hasattr(windll.user32, 'GetDpiForWindow'):
        windll.user32.GetDpiForWindow.argtypes = [HWND]
        windll.user32.GetDpiForWindow.restype = UINT
        return windll.user32.GetDpiForWindow(hWnd)

    hdc = win32gui.GetDC(hWnd)
    if not hdc:
        return 96

    dpiX = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    dpiY = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSY)
    win32gui.ReleaseDC(hWnd, hdc)
    if dpiX > 0 and horizontal:
        return dpiX
    elif dpiY > 0 and not horizontal:
        return dpiY
    return 96


def findWindow(hWnd):
    """ 根据句柄查找窗口，如果未找到则返回 None
    
    Args:
        hWnd (int or `sip.voidptr`): 窗口句柄
    """
    if not hWnd: return

    windows = QGuiApplication.topLevelWindows()
    if not windows: return

    hWnd = int(hWnd)
    for window in windows:
        if window and int(window.winId()) == hWnd: return window


def isGreaterEqualVersion(version):
    """判断Windows版本是否大于或等于指定版本"""
    return QOperatingSystemVersion.current() >= version


def isGreaterEqualWin8_1():
    """ 判断Windows版本是否大于或等于Win8.1 """
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows8_1)


def isGreaterEqualWin10():
    """ 判断Windows版本是否大于或等于Win10 """
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows10)


def isGreaterEqualWin11():
    """ 判断Windows版本是否大于或等于Win11 """
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows10) and sys.getwindowsversion().build >= 22000


def isWin7():
    """ 判断Windows版本是否为Win7 """
    return "Windows-7" in platform()


def releaseMouseLeftButton(hWnd, x=0, y=0):
    """在指定位置(x, y)释放鼠标左键

    Args:
        hWnd (int or `sip.voidptr`): 窗口句柄
        x (int, optional): x坐标. Defaults to 0.
        y (int, optional): y坐标. Defaults to 0.
    """
    lp = (y & 0xFFFF) << 16 | (x & 0xFFFF)
    win32api.SendMessage(int(hWnd), win32con.WM_LBUTTONUP, 0, lp)



def startSystemMove(window):
    """ 移动窗口

    Args:
        window (QWidget): 窗口
        globalPos (QPoint): 鼠标按下时的全局位置
    """
    win32gui.ReleaseCapture()
    win32api.SendMessage(
        int(window.winId()),
        win32con.WM_SYSCOMMAND,
        win32con.SC_MOVE | win32con.HTCAPTION,
        0
    )


def starSystemResize(window, globalPos, edges):
    """ 调整窗口大小

    Args:
        window (QWidget): 窗口
        globalPos (QPoint): 鼠标按下时的全局位置
        edges (int): 窗口边缘
    """
    pass
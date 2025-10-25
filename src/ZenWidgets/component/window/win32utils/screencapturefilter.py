from ctypes import WinDLL, wintypes
from PySide6.QtCore import QObject, QEvent
from PySide6.QtWidgets import QWidget

class WindowsScreenCaptureFilter(QObject):
    """ 屏幕捕获过滤器 """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setScreenCaptureEnabled(False)

    def eventFilter(self, watched, event):
        if watched == self.parent():
            if event.type() == QEvent.Type.WinIdChange:
                self.setScreenCaptureEnabled(self.isScreenCaptureEnabled)

        return super().eventFilter(watched, event)

    def setScreenCaptureEnabled(self, enabled: bool):
        """ 设置是否允许屏幕捕获 """
        self.isScreenCaptureEnabled = enabled
        WDA_NONE = 0x00000000
        WDA_EXCLUDEFROMCAPTURE = 0x00000011

        user32 = WinDLL('user32', use_last_error=True)
        SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
        SetWindowDisplayAffinity.argtypes = (wintypes.HWND, wintypes.DWORD)
        SetWindowDisplayAffinity.restype = wintypes.BOOL

        SetWindowDisplayAffinity(int(self.parent().winId()), WDA_NONE if enabled else WDA_EXCLUDEFROMCAPTURE)
from PySide6.QtCore import QObject,Signal,Property
from enum import IntEnum
from ..utils import singleton
class ZTheme(IntEnum):
    Dark = 0
    Light = 1

@singleton
class ZThemeManager(QObject):
    themeChanged = Signal(ZTheme)
    _instance = None
    def __init__(self):
        super().__init__()
        # # 防止重复初始化
        # if hasattr(self, '_initialized'):
        #     return
        self._theme = ZTheme.Dark

    def getTheme(self) -> ZTheme:
        return self._theme

    def setTheme(self, value: ZTheme) -> None:
        if self._theme != value:
            self._theme = value
            self.themeChanged.emit(value)

    theme = Property(ZTheme, getTheme, setTheme, notify=themeChanged)

    def toggleTheme(self) -> None:
        self.setTheme(ZTheme.Light if self._theme == ZTheme.Dark else ZTheme.Dark)
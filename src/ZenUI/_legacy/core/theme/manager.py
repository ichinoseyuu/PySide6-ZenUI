from PySide6.QtCore import QObject,Signal
from ZenUI._legacy.core.enumrates import Zen

class ZThemeManager(QObject):
    '''主题管理器'''
    themeChanged = Signal(object)
    _instance = None
    def __init__(self):
        super().__init__()
        self._theme = Zen.Theme.Dark

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ZThemeManager, cls).__new__(cls)
        return cls._instance

    def theme(self):
        "获取当前主题"
        return self._theme

    def setTheme(self, theme:Zen.Theme):
        "设置主题"
        if self._theme == theme: return
        self._theme = theme
        # 发出主题切换信号，通知所有组件
        self.themeChanged.emit(theme)


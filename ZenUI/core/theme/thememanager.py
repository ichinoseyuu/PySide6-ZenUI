from PySide6.QtCore import QObject,Signal
from ZenUI.core.enumrates.zen import Zen

class ThemeManager(QObject):
    themeChanged = Signal(object)
    _instance = None
    def __init__(self):
        super().__init__()
        self._theme = Zen.Theme.Dark

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
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


import winreg
import logging
import threading
from PySide6.QtCore import QObject, Signal, Property
from PySide6.QtWidgets import QApplication
from enum import IntEnum
from ZenWidgets.core.utils import Singleton

__All__ = [
    'ZTheme',
    'ZThemeMode',
    'ZThemeManager'
]

class ZTheme(IntEnum):
    Light = 0
    Dark = 1

class ZThemeMode(IntEnum):
    FollowSystem = 0
    Preset = 1

@Singleton
class ZThemeManager(QObject):
    themeChanged = Signal(str)
    def __init__(self):
        super().__init__()
        self._theme = ZTheme.Dark
        self._mode = ZThemeMode.FollowSystem
        self._monitor_thread = None
        self._stop_event = threading.Event()
        if self._mode == ZThemeMode.FollowSystem:
            self._theme = self.getSystemTheme()
            self._start_monitoring()

    def _start_monitoring(self):
        """启动主题监控"""
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            self._stop_event.set()
            self._monitor_thread.join()

        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_theme, daemon=True)
        self._monitor_thread.start()

    def _stop_monitoring_internal(self):
        """停止主题监控"""
        if self._stop_event:
            self._stop_event.set()
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join()

    def _monitor_theme(self):
        """监控主题变化"""
        while not self._stop_event.is_set():
            if self._mode == ZThemeMode.FollowSystem:
                current_system_theme = self.getSystemTheme()
                if current_system_theme != self._theme:
                    self._theme = current_system_theme
                    # 在主线程中触发信号
                    self.themeChanged.emit(self._theme.name)
                    # 触发UI重绘
                    app = QApplication.instance()
                    if app:
                        app.processEvents()
            # 等待1秒或直到停止事件被设置
            self._stop_event.wait(0.5)

    def isDarkTheme(self): return True if self._theme == ZTheme.Dark else False

    def isLightTheme(self): return True if self._theme == ZTheme.Light else False

    def getTheme(self): return self._theme

    def getThemeName(self): return self._theme.name

    def setTheme(self, value: ZTheme):
        if self._theme == value: return
        if self._mode == ZThemeMode.FollowSystem:
            self._mode = ZThemeMode.Preset
            self._stop_monitoring_internal()
        self._theme = value
        self.themeChanged.emit(value.name)

    theme = Property(ZTheme, getTheme, setTheme, notify=themeChanged)

    def toggleTheme(self):
        new_theme = ZTheme.Light if self._theme == ZTheme.Dark else ZTheme.Dark
        self.setTheme(new_theme)

    def updateStyle(self): self.themeChanged.emit(self._theme.name)

    def setThemeMode(self, value: ZThemeMode):
        if self._mode == value: return
        self._mode = value
        if self._mode == ZThemeMode.FollowSystem:
            self._start_monitoring()
            current_system_theme = self.getSystemTheme()
            if current_system_theme != self._theme:
                self._theme = current_system_theme
                self.themeChanged.emit(self._theme.name)
        else:
            self._stop_monitoring_internal()

    @staticmethod
    def getSystemTheme():
        """获取Windows系统主题"""
        try:
            key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as registry_key:
                theme = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")[0]
                return ZTheme.Light if theme == 1 else ZTheme.Dark
        except WindowsError:
            return ZTheme.Light  # 默认使用浅色主题

    def cleanup(self):
        """清理资源"""
        self._stop_monitoring_internal()

import winreg
import logging
import threading
from PySide6.QtCore import QObject, Signal, Property
from PySide6.QtWidgets import QApplication
from enum import IntEnum
from ZenUI.core.utils import singleton

class ZTheme(IntEnum):
    Light = 0
    Dark = 1

class ZThemeMode(IntEnum):
    FollowSystem = 0
    Preset = 1

@singleton
class ZThemeManager(QObject):
    themeChanged = Signal(ZTheme)
    
    def __init__(self):
        super().__init__()
        self._theme = ZTheme.Dark
        self._mode = ZThemeMode.FollowSystem
        self._monitor_thread = None
        self._stop_event = threading.Event()
        
        # 初始化时获取当前系统主题
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
                    self.themeChanged.emit(self._theme)
                    # 触发UI重绘
                    app = QApplication.instance()
                    if app:
                        app.processEvents()
            # 等待1秒或直到停止事件被设置
            self._stop_event.wait(0.5)

    def getTheme(self) -> ZTheme:
        return self._theme

    def setTheme(self, value: ZTheme) -> None:
        if self._theme == value: 
            return
        if self._mode == ZThemeMode.Preset:
            self._theme = value
            self.themeChanged.emit(value)
            # 触发UI重绘
            app = QApplication.instance()
            if app:
                app.processEvents()
        else:
            logging.info("Theme mode is FollowSystem, can't set theme.")

    theme: ZTheme = Property(ZTheme, getTheme, setTheme, notify=themeChanged)

    def setThemeForce(self, value: ZTheme) -> None:
        if self._theme == value: 
            return
        if self._mode == ZThemeMode.FollowSystem:
            self._mode = ZThemeMode.Preset
            self._stop_monitoring_internal()
        self._theme = value
        self.themeChanged.emit(value)
        # 触发UI重绘
        app = QApplication.instance()
        if app:
            app.processEvents()

    def toggleTheme(self) -> None:
        current_theme = self.getTheme()
        new_theme = ZTheme.Light if current_theme == ZTheme.Dark else ZTheme.Dark
        self.setTheme(new_theme)

    def toggleThemeForce(self) -> None:
        current_theme = self.getTheme()
        new_theme = ZTheme.Light if current_theme == ZTheme.Dark else ZTheme.Dark
        self.setThemeForce(new_theme)

    def setThemeMode(self, value: ZThemeMode) -> None:
        if self._mode == value: 
            return
        self._mode = value
        if self._mode == ZThemeMode.FollowSystem:
            # 启动监控
            self._start_monitoring()
            # 立即同步当前系统主题
            current_system_theme = self.getSystemTheme()
            if current_system_theme != self._theme:
                self._theme = current_system_theme
                self.themeChanged.emit(self._theme)
                # 触发UI重绘
                app = QApplication.instance()
                if app:
                    app.processEvents()
        else:
            # 停止监控
            self._stop_monitoring_internal()

    @staticmethod
    def getSystemTheme() -> ZTheme:
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

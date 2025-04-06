from enum import Enum
from PySide6.QtCore import QObject,Signal
from ..color.colorgroup import ColorGroup
from ..enum.zen import Zen

class Light(ColorGroup):
    def __init__(self):
        super().__init__()
        self.assign(Zen.ColorRole.Board_BG_A, "#ffffffff")
        self.assign(Zen.ColorRole.Board_BG_B, "#ffefeff0")
        self.assign(Zen.ColorRole.Board_Border, "#ffe0e0e0")

        self.assign(Zen.ColorRole.ZenText, "#ff000000")

        self.assign(Zen.ColorRole.Button_Text, "#ff000000")
        self.assign(Zen.ColorRole.Button_BG_A, "#ffbfbfbf")
        self.assign(Zen.ColorRole.Button_BG_B, "#ffbfbfbf")
        self.assign(Zen.ColorRole.Button_Hover, "#10000000")
        self.assign(Zen.ColorRole.Button_Flash, "#30000000")
        self.assign(Zen.ColorRole.Button_OFF, "#ff4f4f4f")
        self.assign(Zen.ColorRole.Button_ON, "#ff4f4f4f")


class Dark(ColorGroup):
    def __init__(self):
        super().__init__()
        self.assign(Zen.ColorRole.Board_BG_A, "#ff202022")
        self.assign(Zen.ColorRole.Board_BG_B, "#ff363636")
        self.assign(Zen.ColorRole.Board_Border, "#ff4a4a4a")

        self.assign(Zen.ColorRole.ZenText, "#ffffffff")

        self.assign(Zen.ColorRole.Button_Text, "#ffffffff")
        self.assign(Zen.ColorRole.Button_BG_A, "#ff464646")
        self.assign(Zen.ColorRole.Button_BG_B, "#ff464646")
        self.assign(Zen.ColorRole.Button_Hover, "#10ffffff")
        self.assign(Zen.ColorRole.Button_Flash, "#30ffffff")
        self.assign(Zen.ColorRole.Button_OFF, "#ff4f4f4f")
        self.assign(Zen.ColorRole.Button_ON, "#ff4f4f4f")

class Theme(Enum):
    Light = Light()
    Dark = Dark()

class ThemeManager(QObject):
    themeChanged = Signal(object)
    _instance = None
    def __init__(self):
        super().__init__()
        self._theme = Theme.Dark

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance


    def setTheme(self, theme:Theme):
        "设置主题"
        if self._theme == theme: return
        self._theme = theme
        # 发出主题切换信号，通知所有组件
        self.themeChanged.emit(theme.value)

    def theme(self):
        "获取当前主题"
        return self._theme
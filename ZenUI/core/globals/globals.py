from ZenUI.core.theme.theme import ThemeManager
from ZenUI.core.color.colormanager import ZenColorConfig
from ZenUI.core.metaclass.metaclass import ImmutableMeta,NoInstanceClass,Singleton
class UIGlobal(Singleton):
    windows ={}
    theme_manager = ThemeManager()
    color_config = ZenColorConfig()

class Config(NoInstanceClass):
    TITLEBAR_HEIGHT = 36


class ZenGlobal(NoInstanceClass, metaclass=ImmutableMeta):
    ui = UIGlobal()
    config = Config

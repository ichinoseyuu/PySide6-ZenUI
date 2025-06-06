from ZenUI.core.theme import ZThemeManager
from ZenUI.core.color import ZThemeColorConfig
from ZenUI.core.metaclass import ImmutableMeta,NoInstanceClass,Singleton
class UIGlobal(Singleton):
    '''全局UI配置'''
    windows ={}
    theme_manager = ZThemeManager()
    color_config = ZThemeColorConfig()

class Config(NoInstanceClass):
    '''全局配置'''
    TITLEBAR_HEIGHT = 37
    '标题栏高度'



class ZenGlobal(NoInstanceClass, metaclass=ImmutableMeta):
    '''全局配置'''
    ui = UIGlobal()
    config = Config



def tooltip():
    '获取提示窗口'
    return ZenGlobal.ui.windows.get("ToolTip")

def mainWindow():
    '获取主窗口'
    return ZenGlobal.ui.windows.get("main")
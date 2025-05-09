from ZenUI.core.theme.theme_manager import ZThemeManager
from ZenUI.core.color.color_manager import ZThemeColorConfig
from ZenUI.core.metaclass.metaclass import ImmutableMeta,NoInstanceClass,Singleton
class UIGlobal(Singleton):
    '''全局UI配置'''
    windows ={}
    theme_manager = ZThemeManager()
    color_config = ZThemeColorConfig()

class Config(NoInstanceClass):
    '''全局变量配置'''
    TITLEBAR_HEIGHT = 37
    '标题栏高度'


class ZenGlobal(NoInstanceClass, metaclass=ImmutableMeta):
    '''全局配置'''
    ui = UIGlobal()
    config = Config



def toolTipWindow():
    return ZenGlobal.ui.windows.get("tooltip")


def raiseToolTipWindow():
    window = toolTipWindow()
    if window is not None:
        window.raise_()


def showToolTip(widget, flash: bool = True) -> None:
    """ Show tool tip of specified widget """
    if widget.toolTip() == "":
        return
    window = toolTipWindow()
    if window is None:
        return
    window.setText(widget.toolTip(), flash=flash)
    window.setNowInsideOf(widget)
    window.show()


def hideToolTip(widget) -> None:
    window = toolTipWindow()
    if window is None:
        return
    window.setNowInsideOf(None)
    window.hide()


def updateToolTip(widget, flash: bool = True) -> None:
    window = toolTipWindow()
    if window is None:
        return
    if widget.toolTip() == "":
        return
    window.setText(widget.toolTip(), flash=flash)


def isTooltipShown() -> bool:
    return toolTipWindow().is_shown


def isToolTipInsideOf(widget) -> bool:
    return widget == toolTipWindow().nowInsideOf()
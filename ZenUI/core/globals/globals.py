from ZenUI.core.theme.thememanager import ThemeManager
from ZenUI.core.color.colormanager import ZenColorConfig
from ZenUI.core.metaclass.metaclass import ImmutableMeta,NoInstanceClass,Singleton
class UIGlobal(Singleton):
    windows ={}
    theme_manager = ThemeManager()
    color_config = ZenColorConfig()

class Config(NoInstanceClass):
    TITLEBAR_HEIGHT = 37


class ZenGlobal(NoInstanceClass, metaclass=ImmutableMeta):
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
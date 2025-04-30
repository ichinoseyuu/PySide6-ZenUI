from ZenUI.component.window.window import ZWindow
from ZenUI.component.tooltip.tooltip import ZToolTip
from ZenUI.core import ZenGlobal
class ZMainWindow(ZWindow):
    '''主窗口'''
    def __init__(self):
        super().__init__()
        ZenGlobal.ui.windows['ToolTip'] = ZToolTip()
        ZenGlobal.ui.windows['ToolTip'].show()
        ZenGlobal.ui.windows['ToolTip'].setOpacity(0)
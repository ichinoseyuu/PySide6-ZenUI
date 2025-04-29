from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ZenUI.component.window.window import ZenWindow
from ZenUI.component.tooltip.tooltip import ZenToolTip
from ZenUI.core import ZenGlobal
class ZenMainWindow(ZenWindow):
    '''主窗口'''
    def __init__(self):
        super().__init__()
        ZenGlobal.ui.windows['ToolTip'] = ZenToolTip()
        ZenGlobal.ui.windows['ToolTip'].show()
        ZenGlobal.ui.windows['ToolTip'].setOpacity(0)
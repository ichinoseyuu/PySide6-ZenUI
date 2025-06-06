from ZenUI.component.window.abstract import ABCWindow
from ZenUI.component.tooltip import ZToolTip
from ZenUI.core import ZenGlobal

class ZMainWindow(ABCWindow):
    '主窗口'
    def __init__(self,
                 parent = None,
                 name: str = None,
                 shadow_width: int= 8,
                 border_radius: int = 4,
                 grip_width:int = 5 ,
                 can_resize:bool = True):
        super().__init__(parent=parent,
                         name=name,
                         shadow_width=shadow_width,
                         border_radius=border_radius,
                         grip_width=grip_width,
                         can_resize=can_resize)
        ZenGlobal.ui.windows['MainWindow'] = self
        ZenGlobal.ui.windows['ToolTip'] = ZToolTip()
        ZenGlobal.ui.windows['ToolTip'].show()
        ZenGlobal.ui.windows['ToolTip'].setOpacity(0)
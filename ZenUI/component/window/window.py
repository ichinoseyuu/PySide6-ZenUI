from ZenUI.component.window.abcwindow import ABCWindow
class ZWindow(ABCWindow):
    def __init__(self,
                 parent = None,
                 name: str = None,
                 shadow_width: int= 12,
                 border_radius: int = 4,
                 grip_width:int = 5 ,
                 can_resize:bool = True):
        super().__init__(parent=parent,
                         name=name,
                         shadow_width=shadow_width,
                         border_radius=border_radius,
                         grip_width=grip_width,
                         can_resize=can_resize)
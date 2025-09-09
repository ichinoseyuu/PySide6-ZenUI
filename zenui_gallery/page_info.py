from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PageInfo(ZScrollPage):
    def __init__(self,parent = None,name ='PageInfo'):
        super().__init__(parent = parent,
                         name=name,
                         margins=QMargins(9, 9, 9, 9),
                         spacing=12,
                         alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        #self.setMaximumWidth(600)
        self._setup_ui()

    def _setup_ui(self):
        pass



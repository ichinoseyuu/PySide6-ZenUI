from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.core import ZenMargins,Zen

class ZenGridLayout(QGridLayout):
    '''网格布局'''
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 margins: ZenMargins = ZenMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Zen.Alignment = None
                 ):
        super().__init__(parent)
        if name:
            self.setObjectName(name)
        self.setContentsMargins(margins.toQmargins())
        self.setSpacing(spacing)
        if alignment:
            self.setAlignment(alignment.value)
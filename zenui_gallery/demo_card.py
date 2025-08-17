from PySide6.QtWidgets import QWidget,QSizePolicy
from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *

class DemoCard(ZCard):
    def __init__(self,parent = None,name ='DemoCard'):
        super().__init__(parent, name)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(100)
        self._setup_ui()

    def _setup_ui(self):
        self.title = ZTextBlock(parent=self,
                                 name='title',
                                 text='title')
        self.title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        self.title.margins = QMargins(6, 0, 6, 0)
        self.title.move(10, 10)

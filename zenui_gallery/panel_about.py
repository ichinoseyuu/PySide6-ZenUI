from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *

class PanelAbout(ZPanel):
    def __init__(self,parent = None,name ='PanelAbout'):
        super().__init__(parent = parent, name=name)
        self.setLayout(ZVBoxLayout(self, margins = QMargins(10, 10, 10, 10),spacing=10))
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZTextBlock(parent=self,
                                 name='text',
                                 text='关于')
        self.text.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))
        self.text.margins = QMargins(6, 0, 6, 0)
        self.layout().addWidget(self.text)
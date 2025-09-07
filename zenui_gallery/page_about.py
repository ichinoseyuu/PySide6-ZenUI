from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard
class PageAbout(ZPage):
    def __init__(self,parent = None,name ='PageAbout'):
        super().__init__(parent = parent,
                         name=name,
                         layout=self.Layout.Column,
                         margins=QMargins(6, 6, 6, 6),
                         spacing=12,
                         alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZTextBlock(parent=self,
                                 name='text',
                                 text='关于')
        self.text.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))
        self.text.margins = QMargins(6, 0, 6, 0)
        self.layout().addWidget(self.text)
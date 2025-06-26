from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *

class PageWidget(ZPage):
    def __init__(self,parent = None,name ='pageWidget'):
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
                                 text='控件')
        self.text.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        self.layout().addWidget(self.text)
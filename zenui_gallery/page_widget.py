from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *

class PageWidget(ZScrollPanel):
    def __init__(self,parent = None,name ='pageWidget'):
        super().__init__(parent = parent,
                         name=name,
                         layout=ZPage.Layout.Column,
                         margins=QMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZTextBlock(parent=self,
                                 name='text',
                                 text='控件')
        self.text.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        self.text.setFixedSize(400,800)
        self.content.layout().addWidget(self.text)

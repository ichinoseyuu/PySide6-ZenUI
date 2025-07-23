from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *

class PageWidget(ZScrollPage):
    def __init__(self,parent = None,name ='pageWidget'):
        super().__init__(parent = parent,
                         name=name,
                         margins=QMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZTextBlock(parent=self,
                                 name='text',
                                 text='控件')
        self.text.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        #self.text.setFixedSize(800,800)
        self.content.layout().addWidget(self.text)

        self.btn_box = QHBoxLayout()
        self.btn_box.setContentsMargins(0, 0, 0, 0)
        self.btn_box.setSpacing(6)
        self.content.layout().addLayout(self.btn_box)

        self.btn = ZButton(parent=self,
                      name='btn',
                      text='普通按钮')
        self.btn.setToolTip('这是一个按钮')
        self.btn_box.addWidget(self.btn)

        self.toggle_btn = ZToggleButton(parent=self,
                      name='toggle_btn',
                      text='切换按钮')
        self.toggle_btn.setToolTip('这是一个切换按钮')
        self.btn_box.addWidget(self.toggle_btn)
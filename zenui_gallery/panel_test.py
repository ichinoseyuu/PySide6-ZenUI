from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint,QMarginsF
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PanelTest(ZScrollPanel):
    def __init__(self, parent = None, name ='PanelTest'):
        super().__init__(parent = parent, name=name)
        self.setLayout(ZVBoxLayout(self, margins = QMargins(40, 30, 40, 30),spacing=30, alignment=Qt.AlignmentFlag.AlignTop))
        self._setup_ui()


    def _setup_ui(self):
        self.title = ZTextBlock(self, 'title', '测试组件')
        self.title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        self.title.margins = QMargins(6, 0, 6, 6)
        self.content.layout().addWidget(self.title)

        card = DemoCard(self)
        self.content.layout().addWidget(card)

        title = ZTextBlock(self, text= '测试')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.combobox = ZComboBox(
            parent=container,
            name='combobox',
            text='combobox',
            options=['选项1', '选项2', '选项3'],
            )
        self.combobox.addItem('选项4')
        self.combobox.addItem('选项5')
        self.combobox.removeItem('选项3')
        container.addWidget(self.combobox)
        self.test_btn = ZButton(
            parent=container,
            name='test_btn',
            text='测试按钮'
            )
        container.addWidget(self.test_btn)
        self.test_btn.clicked.connect(self.test_btn_clicked)

    def test_btn_clicked(self):
        self.combobox.removeItem('选项3')
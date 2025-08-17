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

        self.test_card = DemoCard(self, 'test_card')
        #self.test_card.setMaximumWidth(400)
        self.test_card.title.hide()
        self.test_card.resize(400, 400)
        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        self.test_card.setLayout(layout)
        self.layout().addWidget(self.test_card)

        self.text_block_111 = ZTextBlock(self.test_card, name='text_block_111',selectable=True)
        self.text_block_111.margins = QMargins(6, 6, 6, 6)
        #self.text_block_111.setMaximumWidth(120)
        self.text_block_111.wrapMode = ZTextBlock.WrapMode.NoWrap
        self.text_block_111.text = '简单说：做 Hello VaM 时经验不足，早期设计的数据结构限制了后期功能的扩展。与其在老架构上修修补补，不如用新思路重写一个。所以，VaM Box 是在 Hello VaM 经验基础上完全重写的新软件，用了更扎实的架构，目标是能持续更新和运营。'
        #self.text_block_111.text = 'H'
        self.test_card.layout().addWidget(self.text_block_111)

        self.text_block_222 = ZTextBlock(self.test_card, name='text_block_222',selectable=True)
        #self.text_block_222.setMaximumWidth(300)
        self.text_block_222.margins = QMargins(6, 6, 6, 6)
        self.text_block_222.text = '简单说：做 Hello VaM 时经验不足，早期设计的数据结构限制了后期功能的扩展。与其在老架构上修修补补，不如用新思路重写一个。所以，VaM Box 是在 Hello VaM 经验基础上完全重写的新软件，用了更扎实的架构，目标是能持续更新和运营。'
        self.text_block_222.wrapMode = ZTextBlock.WrapMode.WordWrap
        self.test_card.layout().addWidget(self.text_block_222)
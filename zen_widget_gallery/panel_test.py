from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint,QMarginsF,QSize
from PySide6.QtGui import QFont, QIcon, QColor
from ZenWidgets import *

class PanelTest(ZScrollPanel):
    def __init__(self, parent = None):
        super().__init__(parent, objectName ='PanelTest')
        self.setLayout(ZVBoxLayout(self, QMargins(40, 30, 40, 30), 30, Qt.AlignmentFlag.AlignTop))
        self._setup_ui()


    def _setup_ui(self):
        self.title = ZHeadLine(self, text='测试组件', display_indicator=True)
        self.title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        self.title.setPadding(ZPadding(6, 0, 6, 6))
        self.content().layout().addWidget(self.title)

        card = ZCard(self)
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.content().layout().addWidget(card)

        title = ZHeadLine(card, text= '测试')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        # container = ZHContainer(card)
        # card.layout().addWidget(container)

        # self.progress_btn = ZProgressButton(card, text="随机进度")
        # import random
        # self.progress_btn.clicked.connect(lambda: self.progress_btn.setProgress(random.random()))
        # self.progress_btn.progressChanged.connect(lambda x: print(f"progress: {x}"))
        # self.progress_btn.progressFinished.connect(lambda: print("finished"))
        # container.addWidget(self.progress_btn)

        container = ZFlowContainer(card)
        card.layout().addWidget(container)
        # container.setColumns(3)
        # container.setColumnWidth(100)
        # container.setAutoAdjustColumnAmount(True)
        container.setLineHeight(64)
        i = 0
        for icon_name, pixmap in ZGlobal.iconPack.icons(size=QSize(64, 64)):
            if i > 10: break
            #print(f"图标名称: {icon_name}")
            m = ZImage(container)
            m.resize(pixmap.size())
            m.setPixmap(pixmap)
            container.addWidget(m)
            container.regDraggableWidget(m)
            i += 1
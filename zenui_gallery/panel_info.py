from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PanelInfo(ZScrollPanel):
    def __init__(self, parent = None, name ='PanelInfo'):
        super().__init__(parent = parent, name=name)
        self.setLayout(ZVBoxLayout(self, QMargins(40, 30, 40, 30), 30, Qt.AlignmentFlag.AlignTop))
        self._setup_ui()


    def _setup_ui(self):
        self.title = ZHeadLine(self, 'title', '状态与信息', display_indicator=True)
        self.title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        self.title.padding = ZPadding(6, 0, 6, 6)
        self.content.layout().addWidget(self.title)

        # region ToolTip
        self.tooltipdemo = ZToolTipDemo(self)
        self.content.layout().addWidget(self.tooltipdemo)
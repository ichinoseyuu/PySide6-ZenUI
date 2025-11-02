from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenWidgets import *

class PanelAbout(ZPanel):
    def __init__(self, parent = None):
        super().__init__(parent, objectName ='PanelAbout')
        self.setLayout(ZVBoxLayout(self, QMargins(40, 30, 40, 30), 30, Qt.AlignmentFlag.AlignTop))
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZHeadLine(parent=self, text='关于', display_indicator=True)
        self.text.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))
        self.text.setPadding(ZPadding(6, 0, 6, 6))
        self.layout().addWidget(self.text)
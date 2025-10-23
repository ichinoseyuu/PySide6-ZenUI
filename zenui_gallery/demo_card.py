from PySide6.QtWidgets import QWidget,QSizePolicy
from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont,QColor
from ZenUI import *

class DemoCard(ZPanel):
    def __init__(self,parent:QWidget = None,name ='DemoCard'):
        light_data = ZPanelStyleData(Body=QColor('#f3f3f3'), Border=QColor('#e5e5e5'), Radius=5.0)
        dark_data = ZPanelStyleData(Body=QColor('#202020'), Border=QColor('#1d1d1d'), Radius=5.0)
        super().__init__(parent, name, light_data, dark_data)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(ZVBoxLayout(self,margins=QMargins(16,16,16,16),spacing=16))

    def layout(self)-> ZVBoxLayout | ZHBoxLayout:
        return super().layout()
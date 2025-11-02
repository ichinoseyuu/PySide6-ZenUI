from PySide6.QtWidgets import QWidget,QSizePolicy
from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont,QColor
from ZenWidgets import *

class DemoCard(ZPanel):
    def __init__(self,parent:QWidget = None,name ='DemoCard'):
        super().__init__(parent, name)
        # self.styleDataCtrl.setCustomData("Light",ZStyleDataKey.Body, QColor('#F9F9F9'))
        # self.styleDataCtrl.setCustomData("Dark",ZStyleDataKey.Body, QColor('#1D1D1D'))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(ZVBoxLayout(self,margins=QMargins(16,16,16,16),spacing=16))

    def layout(self)-> ZVBoxLayout | ZHBoxLayout:
        return super().layout()
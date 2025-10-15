from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint,QMarginsF
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PanelTest(ZScrollPanel):
    def __init__(self, parent = None, name ='PanelTest'):
        super().__init__(parent = parent, name=name)
        self.setLayout(ZVBoxLayout(self, QMargins(40, 30, 40, 30), 30, Qt.AlignmentFlag.AlignTop))
        self._setup_ui()


    def _setup_ui(self):
        self.title = ZHeadLine(self, 'title', '测试组件', display_indicator=True)
        self.title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        self.title.padding = ZPadding(6, 0, 6, 6)
        self.content.layout().addWidget(self.title)

        card = DemoCard(self)
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.content.layout().addWidget(card)

        title = ZHeadLine(self, text= '测试')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)


        self.headline = ZHeadLine(container, 'headline', 'headline',True)
        container.addWidget(self.headline)

        self.lineedit = ZLineEdit(container, 'textbox')
        container.addWidget(self.lineedit)

        self.logbtn = ZButton(container, 'logbtn', '关闭/打开日志')
        self.logbtn.clicked.connect(ZDebug.toggleLogging)
        container.addWidget(self.logbtn)

        self.btn_frame_wind = ZButton(container, 'btn_frame_wind', 'FramelessWindow',style=ZButtonStyle.Flat)
        container.addWidget(self.btn_frame_wind)

        self.btn_areo_wind = ZRepeatButton(container, 'btn_areo_wind', 'AreoEffectWindow',style=ZButtonStyle.Flat)
        container.addWidget(self.btn_areo_wind)

        self.btn_areo_wind_2 = ZToggleButton(container, 'btn_areo_wind_2', 'AreoEffectWindow',style=ZButtonStyle.Flat)
        container.addWidget(self.btn_areo_wind_2)
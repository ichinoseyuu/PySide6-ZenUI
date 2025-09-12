from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *
from demo_card import DemoCard

class PanelSettings(ZPanel):
    def __init__(self, parent = None, name ='PanelSettings'):
        super().__init__(parent = parent, name=name)
        self.setLayout(ZVBoxLayout(self, margins = QMargins(10, 10, 10, 10),spacing=10, alignment=Qt.AlignmentFlag.AlignTop))
        self._setup_ui()

    def layout(self) -> ZVBoxLayout:
        return super().layout()

    def _setup_ui(self):
        self.text = ZTextBlock(self, 'text', '设置')
        self.text.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))
        self.text.margins = QMargins(6, 0, 6, 0)
        self.layout().addWidget(self.text)

        self.hcontainer = ZHContainer(self)
        self.hcontainer.margins = QMargins(10, 10, 10, 10)
        self.hcontainer.alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        self.layout().addWidget(self.hcontainer)

        self.text_theme_set = ZTextBlock(self.hcontainer, 'theme_setting_label', '主题：')
        self.text_theme_set.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Normal))
        self.hcontainer.addWidget(self.text_theme_set)

        self.btn_theme_set_1 = ZButton(
            parent=self.hcontainer,
            name='btn_theme_set_1',
            text='浅色')
        self.btn_theme_set_1.clicked.connect(lambda: ZGlobal.themeManager.setThemeForce(ZTheme.Light))
        self.hcontainer.addWidget(self.btn_theme_set_1)

        self.btn_theme_set_2 = ZButton(
            parent=self.hcontainer,
            name='btn_theme_set_2',
            text='深色')
        self.btn_theme_set_2.clicked.connect(lambda: ZGlobal.themeManager.setThemeForce(ZTheme.Dark))
        self.hcontainer.addWidget(self.btn_theme_set_2)

        self.btn_theme_set_3 = ZButton(
            parent=self.hcontainer,
            name='btn_theme_set_3',
            text='跟随系统')
        self.btn_theme_set_3.clicked.connect(lambda: ZGlobal.themeManager.setThemeMode(ZThemeMode.FollowSystem))
        self.hcontainer.addWidget(self.btn_theme_set_3)






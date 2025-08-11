from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *

class PageSettings(ZPage):
    def __init__(self,parent = None,name ='pageSettings'):
        super().__init__(parent = parent,
                        name=name,
                        layout=self.Layout.Column,
                        margins=QMargins(6, 6, 6, 6),
                        spacing=12,
                        alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZTextBlock(self, 'text', '设置')
        self.text.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        self.text.margins = QMargins(12, 0, 6, 0)
        self.layout().addWidget(self.text)

        # region Button
        self.theme_set_box = QHBoxLayout()
        self.theme_set_box.setContentsMargins(6, 6, 6, 6)
        self.theme_set_box.setSpacing(12)
        self.theme_set_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout().addLayout(self.theme_set_box)

        self.text_theme_set = ZTextBlock(self, 'theme_setting_label', '主题颜色')
        self.text_theme_set.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Normal))
        self.theme_set_box.addWidget(self.text_theme_set)

        self.btn_theme_set_1 = ZToggleButton(
            parent=self,
            name='btn_theme_set_1',
            text='浅色')
        self.btn_theme_set_1.clicked.connect(lambda: ZGlobal.themeManager.setThemeForce(ZTheme.Light))
        self.theme_set_box.addWidget(self.btn_theme_set_1)

        self.btn_theme_set_2 = ZToggleButton(
            parent=self,
            name='btn_theme_set_1',
            text='深色')
        self.btn_theme_set_2.clicked.connect(lambda: ZGlobal.themeManager.setThemeForce(ZTheme.Dark))
        self.theme_set_box.addWidget(self.btn_theme_set_2)

        self.btn_theme_set_3 = ZToggleButton(
            parent=self,
            name='btn_theme_set_3',
            text='跟随系统')
        self.btn_theme_set_3.clicked.connect(lambda: ZGlobal.themeManager.setThemeMode(ZThemeMode.FollowSystem))
        self.theme_set_box.addWidget(self.btn_theme_set_3)


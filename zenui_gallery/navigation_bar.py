from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class NavigationBar(ZNavigationBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setup_ui()

    def _setup_ui(self):
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/fluent/regular/ic_fluent_home_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/svg/fluent/filled/ic_fluent_home_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnHome = ZNavBarToggleButton("btnHome", self, icon1)
        self.btnHome.setToolTip("主页")
        self.addToggleButton(self.panel, self.btnHome)

        icon2 = QIcon()
        icon2.addFile(u":/icons/svg/fluent/regular/ic_fluent_cube_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/svg/fluent/filled/ic_fluent_cube_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnWidget = ZNavBarToggleButton("btnWidget", self, icon2)
        self.btnWidget.setToolTip("控件演示")
        self.addToggleButton(self.panel, self.btnWidget)

        icon3 = QIcon()
        icon3.addFile(u":/icons/svg/fluent/regular/ic_fluent_info_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/svg/fluent/filled/ic_fluent_info_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnAbout = ZNavBarToggleButton("btnAbout", self, icon3)
        self.btnAbout.setToolTip("关于")
        self.addToggleButton(self.footerPanel, self.btnAbout)

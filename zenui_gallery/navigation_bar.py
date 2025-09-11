from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class NavigationBar(ZNavigationBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setup_ui()
        self.resize(self.sizeHint())
    def _setup_ui(self):
        icon1 = QIcon()
        icon1.addFile(u":/icons/fluent/regular/ic_fluent_home_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/fluent/filled/ic_fluent_home_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnHome = ZNavBarToggleButton(self, "btnHome", icon1)
        self.btnHome.setToolTip("主页")
        self.addToggleButton(self.panel, self.btnHome)

        icon2 = QIcon()
        icon2.addFile(u":/icons/fluent/regular/ic_fluent_cube_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/fluent/filled/ic_fluent_cube_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnWidget = ZNavBarToggleButton(self, "btnWidget", icon2)
        self.btnWidget.setToolTip("基础组件")
        self.addToggleButton(self.panel, self.btnWidget)

        icon3 = QIcon()
        icon3.addFile(u":/icons/fluent/regular/ic_fluent_comment_multiple_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/fluent/filled/ic_fluent_comment_multiple_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnInfo = ZNavBarToggleButton(self, "btnInfo", icon3)
        self.btnInfo.setToolTip("状态与信息")
        self.addToggleButton(self.panel, self.btnInfo)

        icon4 = QIcon()
        icon4.addFile(u":/icons/fluent/regular/ic_fluent_info_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addFile(u":/icons/fluent/filled/ic_fluent_info_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnAbout = ZNavBarToggleButton(self, "btnAbout", icon4)
        self.btnAbout.setToolTip("关于")
        self.addToggleButton(self.panel, self.btnAbout)

        icon5 = QIcon()
        icon5.addFile(u":/icons/fluent/regular/ic_fluent_settings_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon5.addFile(u":/icons/fluent/filled/ic_fluent_settings_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnSettings = ZNavBarToggleButton(self, "btnSettings", icon5)
        self.btnSettings.setToolTip("设置")
        self.addToggleButton(self.footerPanel, self.btnSettings)

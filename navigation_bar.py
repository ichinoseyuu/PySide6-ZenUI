from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class LeftNavigationBar(ZNavigationBar):
    def _setup_ui(self):
        super()._setup_ui()
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/fluent/regular/ic_fluent_home_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/svg/fluent/filled/ic_fluent_home_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnHome = ZQuickButton.navbarToggleButton(parent=self,
                                  name="btnHome",
                                  text="        主页",
                                  icon=icon1,
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnHome)
        icon2 = QIcon()
        icon2.addFile(u":/icons/svg/fluent/regular/ic_fluent_cube_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/svg/fluent/filled/ic_fluent_cube_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnWidget = ZQuickButton.navbarToggleButton(parent=self,
                                  name="btnWidget",
                                  text="        控件",
                                  icon=icon2,
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnWidget)

        icon3 = QIcon()
        icon3.addFile(u":/icons/svg/fluent/regular/ic_fluent_info_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/svg/fluent/filled/ic_fluent_info_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnAbout = ZQuickButton.navbarToggleButton(parent=self,
                                  name="btnAbout",
                                  text="        关于",
                                  icon=icon3,
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnAbout)

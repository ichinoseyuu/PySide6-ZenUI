from ZenUI import *

class LeftMenuBar(ZLeftSideMenu):
    def _setup_ui(self):
        super()._setup_ui()
        self.btnHome = ZTabButton(parent=self,
                                  name="btnHome",
                                  text="\t\t\t\t主页",
                                  icon=ZIcon(u":/icons/fluent_ui_filled/home.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnHome)

        self.btnBox = ZTabButton(parent=self,
                                  name="btnBox",
                                  text="\t\t\t\t控件",
                                  icon=ZIcon(u":/icons/fluent_ui_filled/box.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnBox)

        self.btnAbout = ZTabButton(parent=self,
                                  name="btnAbout",
                                  text="\t\t\t\t关于",
                                  icon=ZIcon(u":/icons/fluent_ui_filled/info.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnAbout)

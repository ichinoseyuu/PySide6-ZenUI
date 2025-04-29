from ZenUI import *

class LeftMenuBar(ZenLeftSideMenu):
    def _setup_ui(self):
        super()._setup_ui()
        self.btnHome = ZenTabButton(parent=self,
                                  name="btnHome",
                                  text="\t\t\t\t主页",
                                  icon=ZenIcon(u":/icons/fluent_ui_filled/home.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnHome)

        self.btnAbout = ZenTabButton(parent=self,
                                  name="btnAbout",
                                  text="\t\t\t\t关于",
                                  icon=ZenIcon(u":/icons/fluent_ui_filled/info.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnAbout)

        self.btnSettings = ZenTabButton(parent=self,
                                  name="btnSettings",
                                  text="\t\t\t\t设置",
                                  icon=ZenIcon(u":/icons/fluent_ui_filled/wrench_settings.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnSettings)

        self.btnTest = ZenTransButton(parent=self,
                                  name="btnTest",
                                  text="\t\t\t\t测试",
                                  icon=ZenIcon(u":/icons/fluent_ui_filled/wrench_settings.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.addButton(self.btnTest)

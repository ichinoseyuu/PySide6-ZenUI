from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.sidebar.sidebar import ZenSidebar
from ZenUI.component.button.transbutton import ZenTransButton
from ZenUI.component.button.tabbutton import ZenTabButton
from ZenUI.component.layout.spacer import ZenSpacer
from ZenUI.core import Zen,ZenSize
class ZenLeftSideMenu(ZenSidebar):
    '''可折叠左侧菜单栏类'''
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 layout: Zen.Layout = Zen.Layout.Column,
                 can_expand: bool = True,
                 state = Zen.State.Collapsed,
                 dir = Zen.Direction.Vertical,
                 collapse_width = 52,
                 expand_width = 150,
                 btn_height: int = 48,
                 btn_icon_size: ZenSize = ZenSize(36, 36)
                 ):
        super().__init__(parent, name, layout, can_expand, state, dir, collapse_width, expand_width)
        self._btn_height = btn_height
        self._btn_icon_size = btn_icon_size
        self._toggled_btn = None
        self._last_toggled_btn = None
        self._btns = {}
        self._setup_ui()
        self._btn_connect()

    def _setup_ui(self):
        '''设置UI'''
        icon = QIcon(u":/leftsidemenu/icon/menu.svg")
        self.btnMenu = ZenTransButton(self,
                                      name="btnMenu",
                                      text="\t\t\t\t收起",
                                      icon=icon,
                                      min_height=self._btn_height,
                                      icon_size=self._btn_icon_size)
        self.btnMenu.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;\nborder-radius: 2px;\nborder: 1px solid transparent;')
        self.layout().addWidget(self.btnMenu)


        icon = QIcon(u":/leftsidemenu/icon/home.svg")
        self.btnHome = ZenTabButton(self,
                                  name="btnHome",
                                  text="\t\t\t\t主页",
                                  icon=icon,
                                  checked=True,
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.layout().addWidget(self.btnHome)
        self._btns["btnHome"] = self.btnHome

        icon = QIcon(u":/leftsidemenu/icon/about.svg")
        self.btnAbout = ZenTabButton(parent=self,
                                  name="btnAbout",
                                  text="\t\t\t\t关于",
                                  icon=icon,
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.layout().addWidget(self.btnAbout)
        self._btns["btnAbout"] = self.btnAbout

        icon = QIcon(u":/leftsidemenu/icon/settings.svg")
        self.btnSettings = ZenTabButton(parent=self,
                                  name="btnSettings",
                                  text="\t\t\t\t设置",
                                  icon=icon,
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.layout().addWidget(self.btnSettings)
        self._btns["btnSettings"] = self.btnSettings

        self.leftSideMenuSpacer = ZenSpacer()
        self.layout().addItem(self.leftSideMenuSpacer)


    def _btn_connect(self):
        self.btnMenu.clicked.connect(self.toggleState)
        self.btnHome.clicked.connect(lambda: self._switch_btn_state(self.btnHome))
        self.btnAbout.clicked.connect(lambda: self._switch_btn_state(self.btnAbout))
        self.btnSettings.clicked.connect(lambda: self._switch_btn_state(self.btnSettings))

    def _switch_btn_state(self, btn: ZenTabButton):
        for k, v in self._btns.items():
            if v != btn:
                v.setChecked(False)

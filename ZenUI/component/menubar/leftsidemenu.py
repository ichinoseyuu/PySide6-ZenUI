from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.sidebar.sidebar import ZenSidebar
from ZenUI.component.button.transbutton import ZenTransButton
from ZenUI.component.button.tabbutton import ZenTabButton
from ZenUI.core import Zen, ZenExpAnim,ColorSheet
class ZenLeftSideMenu(ZenSidebar):
    '''可折叠左侧菜单栏类'''
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 btn_height: int = 48,
                 btn_icon_size: int = 36,
                 can_expand: bool = True,
                 state = Zen.State.Collapsed,
                 dir = Zen.Direction.Vertical,
                 size: tuple[int, int] = (50, 150),
                 layout = Zen.Layout.Vertical):
        super().__init__(parent, name, state, dir, size, layout)
        self._can_expand = can_expand
        self._btn_height = btn_height
        self._btn_icon_size = btn_icon_size
        self._btns = {}
        self._setup_ui()
        self._btn_connect()

    def _setup_ui(self):
        icon = QIcon(u":/leftsidemenu/icon/menu.svg")
        self.btnMenu = ZenTransButton(self,
                                      name="btnMenu",
                                      text="\t\t\t收起",
                                      icon=icon,)
        self.btnMenu.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;\nborder-radius: 2px;\nborder: 1px solid transparent;')
        self.btnMenu.setMinimumHeight(self._btn_height)
        self.btnMenu.setIconSize(QSize(self._btn_icon_size, self._btn_icon_size))
        self.addWidget(self.btnMenu)


        icon = QIcon(u":/leftsidemenu/icon/home.svg")
        self.btnHome = ZenTabButton(self,
                                  name="btnHome",
                                  text="\t\t\t主页",
                                  icon=icon,
                                  checked=True)
        self.btnHome.setMinimumHeight(self._btn_height)
        self.btnHome.setIconSize(QSize(self._btn_icon_size, self._btn_icon_size))
        self.addWidget(self.btnHome)
        self._btns["btnHome"] = self.btnHome

        icon = QIcon(u":/leftsidemenu/icon/about.svg")
        self.btnAbout = ZenTabButton(self,
                                  name="btnAbout",
                                  text="\t\t\t关于",
                                  icon=icon)
        self.btnAbout.setMinimumHeight(self._btn_height)
        self.btnAbout.setIconSize(QSize(self._btn_icon_size, self._btn_icon_size))
        self.addWidget(self.btnAbout)
        self._btns["btnAbout"] = self.btnAbout

        icon = QIcon(u":/leftsidemenu/icon/settings.svg")
        self.btnSettings = ZenTabButton(self,
                                  name="btnSettings",
                                  text="\t\t\t设置",
                                  icon=icon)
        self.btnSettings.setMinimumHeight(self._btn_height)
        self.btnSettings.setIconSize(QSize(self._btn_icon_size, self._btn_icon_size))
        self.addWidget(self.btnSettings)
        self._btns["btnSettings"] = self.btnSettings

        self.leftSideMenuSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.addItem(self.leftSideMenuSpacer)


    def _btn_connect(self):
        self.btnMenu.clicked.connect(self.toggleState)
        self.btnHome.clicked.connect(lambda: self._switch_btn_state(self.btnHome))
        self.btnAbout.clicked.connect(lambda: self._switch_btn_state(self.btnAbout))
        self.btnSettings.clicked.connect(lambda: self._switch_btn_state(self.btnSettings))

    def _switch_btn_state(self, btn: ZenTabButton):
        for k, v in self._btns.items():
            if v != btn:
                v.setChecked(False)

    def toggleState(self):
        if self._can_expand:
            super().toggleState()

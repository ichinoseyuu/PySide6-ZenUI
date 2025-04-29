from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.container.collapsiblecontainer import ZenCollapsibleContainer
from ZenUI.component.button.transbutton import ZenTransButton
from ZenUI.component.button.tabbutton import ZenTabButton
from ZenUI.component.layout.spacer import ZenSpacer
from ZenUI.core import Zen,ZenSize
class ZenLeftSideMenu(ZenCollapsibleContainer):
    '''可折叠左侧菜单栏
    - 继承这个类重写`_setup_ui`方法，通过`addButton`方法添加按钮
    '''
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
                 btn_icon_size: ZenSize = ZenSize(32, 32)
                 ):
        super().__init__(parent, name, layout, can_expand, state, dir, collapse_width, expand_width)
        self._btn_height = btn_height
        self._btn_icon_size = btn_icon_size
        self._toggled_btn = None
        self._last_toggled_btn = None
        self._btns = {}
        self._btn_count = 0
        self._setup_ui()

    def _setup_ui(self):
        '''设置UI'''
        icon = QIcon(u":/icons/fluent_ui_filled/list.svg")
        self.btnMenu = ZenTransButton(self,
                                      name="btnMenu",
                                      text="\t\t\t\t收起",
                                      icon=icon,
                                      min_height=self._btn_height,
                                      icon_size=self._btn_icon_size)
        self.btnMenu.setFixedStyleSheet(f'text-align: left;\npadding-left: 10px;\nborder-radius: 4px;\nborder: 1px solid transparent;')
        self.btnMenu.clicked.connect(self.toggleState)
        self.layout().addWidget(self.btnMenu)

        self.leftSideMenuSpacer = ZenSpacer()
        self.layout().addItem(self.leftSideMenuSpacer)


    def addButton(self, btn: ZenTabButton|ZenTransButton):
        '''添加按钮'''
        if isinstance(btn, ZenTabButton):
            if self._toggled_btn is None:
                btn.setChecked(True)
                self._toggled_btn = btn
            btn.pressed.connect(lambda: self._btn_pressed_handler(btn))
            self.layout().insertWidget(self._btn_count + 1, btn)
            self._btns[f"{btn.objectName()}"] = btn
            self._btn_count += 1
        elif isinstance(btn, ZenTransButton):
            btn.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;\nborder-radius: 2px;\nborder: 1px solid transparent;')
            self.layout().insertWidget(self._btn_count + 1, btn)


    def _btn_pressed_handler(self, btn: ZenTabButton):
        if self._toggled_btn == btn:
            btn.setChecked(False)
            return
        self._last_toggled_btn = self._toggled_btn
        self._last_toggled_btn.setChecked(False)
        self._toggled_btn = btn
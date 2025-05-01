from PySide6.QtGui import QIcon
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.container.collapsible_container import ZCollapsibleContainer
from ZenUI.component.button.transbutton import ZTransButton
from ZenUI.component.button.tabbutton import ZTabButton
from ZenUI.component.layout.spacer import ZSpacer
from ZenUI.core import Zen,ZSize,ZMargins
class ZNavigationBar(ZCollapsibleContainer):
    '''可折叠左侧菜单栏
    - 继承这个类重写`_setup_ui`方法，通过`addButton`方法添加按钮
    '''
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 layout: Zen.Layout = Zen.Layout.Column,
                 margins: ZMargins = ZMargins(6, 6, 6, 6),
                 spacing: int = 6,
                 alignment: Zen.Alignment = Zen.Alignment.Left,
                 can_expand: bool = True,
                 state = Zen.State.Collapsed,
                 dir = Zen.Direction.Vertical,
                 collapse_width = 56,
                 expand_width = 150,
                 btn_height: int = 42,
                 btn_icon_size: ZSize = ZSize(26, 26)):
        super().__init__(parent=parent,
                         name= name,
                         layout=layout,
                         margins=margins,
                         spacing=spacing,
                         alignment=alignment,
                         can_expand=can_expand,
                         state=state,
                         dir=dir,
                         collapse_width=collapse_width,
                         expand_width=expand_width)
        self._btn_height = btn_height
        self._btn_icon_size = btn_icon_size
        self._toggled_btn = None
        self._last_toggled_btn = None
        self._btns = {}
        self._btn_count = 0
        self._setup_ui()

    def _setup_ui(self):
        '''设置UI'''
        self.btnCollapse = ZTransButton(parent=self,
                                  name="btnCollapse",
                                  text="\t\t\t\t收起",
                                  icon=QIcon(u":/icons/svg/fluent/filled/ic_fluent_navigation_filled.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size)
        self.btnCollapse.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;\nborder-radius: 4px;\nborder: 1px solid transparent;')
        self.btnCollapse.clicked.connect(self.toggleState)
        self.layout().addWidget(self.btnCollapse)

        self.spacer = ZSpacer()
        self.layout().addItem(self.spacer)


    def addButton(self, btn: ZTabButton|ZTransButton):
        '''添加按钮'''
        if isinstance(btn, ZTabButton):
            if self._toggled_btn is None:
                btn.setChecked(True)
                self._toggled_btn = btn
            btn.pressed.connect(lambda: self._btn_pressed_handler(btn))
            self.layout().insertWidget(self._btn_count + 1, btn)
            self._btns[f"{btn.objectName()}"] = btn
            self._btn_count += 1
        elif isinstance(btn, ZTransButton):
            btn.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;\nborder-radius: 2px;\nborder: 1px solid transparent;')
            self.layout().insertWidget(self._btn_count + 1, btn)


    def _btn_pressed_handler(self, btn: ZTabButton):
        if self._toggled_btn == btn:
            btn.setChecked(False)
            return
        self._last_toggled_btn = self._toggled_btn
        self._last_toggled_btn.setChecked(False)
        self._toggled_btn = btn

from PySide6.QtGui import QIcon
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.container.collapsible_container import ZCollapsibleContainer
from ZenUI.component.button.togglebutton import ZToggleButton
from ZenUI.component.button.pushbutton import ZPushButton
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
                 expand_width = 128,
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
        self.btnCollapse = ZPushButton(parent=self,
                                  name="btnCollapse",
                                  text="\t\t\t\t收起",
                                  icon=QIcon(u":/icons/svg/fluent/filled/ic_fluent_navigation_filled.svg"),
                                  min_height=self._btn_height,
                                  icon_size=self._btn_icon_size,
                                  border_radius=4,
                                  idle_style= ZPushButton.IdleStyle.Transparent,
                                  hover_style=ZPushButton.HoverStyle.ColorChange,
                                  pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.btnCollapse.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;')
        self.btnCollapse.clicked.connect(self.toggleState)
        self.layout().addWidget(self.btnCollapse)

        self.spacer = ZSpacer()
        self.layout().addItem(self.spacer)


    def addButton(self, btn: ZToggleButton|ZPushButton):
        '''添加按钮'''
        if isinstance(btn, ZToggleButton):
            if self._toggled_btn is None:
                btn.setChecked(True)
                self._toggled_btn = btn
            btn._fixed_stylesheet = f'text-align: left;\npadding-left: 8px;'
            print(btn.styleSheet())
            btn.pressed.connect(lambda: self._btn_pressed_handler(btn))
            self.layout().insertWidget(self._btn_count + 1, btn)
            self._btns[f"{btn.objectName()}"] = btn
            self._btn_count += 1
        elif isinstance(btn, ZPushButton):
            btn.setFixedStyleSheet(f'text-align: left;\npadding-left: 8px;')
            self.layout().insertWidget(self._btn_count + 1, btn)


    def _btn_pressed_handler(self, btn: ZToggleButton):
        '''按钮点击事件处理'''
        btn.setChecked(False)
        if self._toggled_btn == btn: return
        self._last_toggled_btn = self._toggled_btn
        self._last_toggled_btn.setChecked(False)
        self._last_toggled_btn.leaved.emit()
        self._toggled_btn = btn

    def toggleToNextButton(self):
        '''切换到下一个按钮'''
        if self._toggled_btn:
            self._toggled_btn.click()
        index = self.layout().indexOf(self._toggled_btn)
        widget = self.layout().itemAt(index + 1).widget()
        if isinstance(widget, ZToggleButton):
            widget.click()

    def toggleToLastButton(self):
        '''切换到上一个按钮'''
        if self._toggled_btn:
            self._toggled_btn.click()
        index = self.layout().indexOf(self._toggled_btn)
        widget = self.layout().itemAt(index - 1).widget()
        if isinstance(widget, ZToggleButton):
            widget.click()
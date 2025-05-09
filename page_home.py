from PySide6.QtGui import QIcon
from ZenUI import *

class PageHome(ZBox):
    def __init__(self,parent = None,name ='pageHome'):
        super().__init__(parent = parent,
                         name=name,
                         style= ZBox.Style.MonochromeWithBorder,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        self.label_title = ZTextLabel(parent=self,
                                 name='text',
                                 text="Hello, ZenUI!")
        self.label_title.setFixedStyleSheet("padding-top:200px;\nfont-size: 42px;\nfont-weight: bold;\ncolor: pink;")
        self.layout().addWidget(self.label_title)

        self.spacer = ZSpacer(minH=40,
                              minW=20,
                              row=Zen.SizePolicy.Minimum,
                              columns=Zen.SizePolicy.Expanding)
        self.layout().addItem(self.spacer)

        self.contain_button = ZBox(parent=self,
                                 name='contain_zpush',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=6)
        self.layout().addWidget(self.contain_button)

        self.btn_ztrans_spacer = ZSpacer(minH=20,
                              minW=40,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_button.layout().addItem(self.btn_ztrans_spacer)

        self.btn_nextpage = ZPushButton(parent=self.contain_button,
                                 name='btn_nextpage',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_arrow_right_filled.svg'),
                                 min_height=40,
                                 min_width=60,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum),
                                 idle_style=ZPushButton.IdleStyle.Transparent,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.Flash)
        self.contain_button.layout().addWidget(self.btn_nextpage)
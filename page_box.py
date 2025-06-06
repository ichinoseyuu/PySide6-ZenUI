from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class PageBox(ZStackPage):
    def __init__(self,parent = None,name ='pageBox'):
        super().__init__(parent = parent,
                         name=name,
                         fixed_stylesheet="border-width: 1px;\nborder-style: solid;\nborder-radius:4px;",
                         style= ZStackPage.Style.Monochrome|ZStackPage.Style.Border,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        text = """控件"""
        self.label_title = ZTextLabel(parent=self,
                                 name='text',
                                 text=text,
                                 alignment=Zen.Alignment.Left)
        self.label_title.setFixedStyleSheet('padding:5px;\nfont-size: 24px;\nfont-family: "微软雅黑";\nfont-weight: bold;')
        self.layout().addWidget(self.label_title)


        self.label_btn = ZTextLabel(parent=self,
                                 name='label_btn',
                                 text='按钮',
                                 alignment=Zen.Alignment.Left)
        self.label_btn.setFixedStyleSheet('''padding:10px;\npadding-left:20px;\nfont-size: 14px;\nfont-family: "微软雅黑";''')
        self.layout().addWidget(self.label_btn)

        # region ZPushButton
        self.contain_zpush = ZBox(parent=self,
                                 name='contain_zpush',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_zpush)

        self.label_zpush = ZTextLabel(parent=self.contain_zpush,
                                 name='label_zpush',
                                 text='ZPushButton',
                                 alignment=Zen.Alignment.Center)
        self.label_zpush.setFixedStyleSheet('''padding:10px;\npadding-left:20px;\nfont-size: 12px;\nfont-family: "微软雅黑";''')
        self.contain_zpush.layout().addWidget(self.label_zpush)


        self.btn_push1 = ZQuickButton.ghostButton(parent=self.contain_zpush,
                                 name='btn_push1',
                                 text='幽灵按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_push1)

        self.btn_push2 = ZQuickButton.transButton(parent=self.contain_zpush,
                                 name='btn_push2',
                                 text='透明按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_push2)

        self.btn_push3 = ZQuickButton.gradientButton(parent=self.contain_zpush,
                                 name='btn_push3',
                                 text='渐变按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_push3)

        self.btn_push4 = ZQuickButton.textButton(parent=self.contain_zpush,
                                 name='btn_push4',
                                 text='文本按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_push4)

        self.btn_push5 = ZQuickButton.iconButton(parent=self.contain_zpush,
                                 name='btn_push5',
                                 icon=QIcon(':/icons/svg/fluent/regular/ic_fluent_sparkle_regular.svg'),
                                 fixed_size=ZSize(32, 32))
        self.contain_zpush.layout().addWidget(self.btn_push5)

        self.btn_zpush_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_zpush.layout().addItem(self.btn_zpush_spacer)


        # region ZToggleButton
        self.contain_ztoggle = ZBox(parent=self,
                                 name='contain_ztoggle',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_ztoggle)

        self.label_ztoggle = ZTextLabel(parent=self.contain_ztoggle,
                                 name='label_ztab',
                                 text='ZToggleButton',
                                 alignment=Zen.Alignment.Center)
        self.label_ztoggle.setFixedStyleSheet('padding:10px;\npadding-left:20px;\nfont-size: 12px;\nfont-family: "微软雅黑";')
        self.contain_ztoggle.layout().addWidget(self.label_ztoggle)


        icon_toggle = QIcon()
        icon_toggle.addFile(':/icons/svg/fluent/regular/ic_fluent_sparkle_regular.svg', QSize(32, 32), QIcon.Mode.Normal, QIcon.State.Off)
        icon_toggle.addFile(':/icons/svg/fluent/filled/ic_fluent_sparkle_filled.svg', QSize(32, 32), QIcon.Mode.Normal, QIcon.State.On)
        self.btn_toggle1 = ZQuickButton.toggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle1',
                                 text='收藏',
                                 icon=icon_toggle,
                                 fixed_size=ZSize(56, 32))
        self.contain_ztoggle.layout().addWidget(self.btn_toggle1)


        self.contain_ztoggle_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_ztoggle.layout().addItem(self.contain_ztoggle_spacer)

        self.btn_push7 = ZGhostButton(parent=self,
                                 name='btn_push7',
                                 text='幽灵按钮',
                                 fixed_size=ZSize(100, 40),
                                 fixed_stylesheet='border-radius: 4px;\nborder-style: solid;\nborder-width: 1px;',
                                 hover_stylesheet='border-radius: 4px;',
                                 pressed_stylesheet='border-radius: 4px;')
        self.layout().addWidget(self.btn_push7)

        self.btn_push8 = ZFillButton(parent=self,
                                 name='btn_push8',
                                 text='填充按钮',
                                 fixed_size=ZSize(100, 40),
                                 fixed_stylesheet='border-radius: 4px;\nborder-style: solid;\nborder-width: 1px;',
                                 hover_stylesheet='border-radius: 4px;',
                                 pressed_stylesheet='border-radius: 4px;')
        self.layout().addWidget(self.btn_push8)

        self.btn_push9 = ZGradientButton(parent=self,
                                 name='btn_push9',
                                 text='渐变按钮',
                                 fixed_size=ZSize(100, 40),
                                 fixed_stylesheet='border-radius: 4px;',
                                 hover_stylesheet='border-radius: 4px;',
                                 pressed_stylesheet='border-radius: 4px;')
        self.layout().addWidget(self.btn_push9)


        self.btn_push10 = ZTransparentButton(parent=self,
                                 name='btn_push10',
                                 text='透明按钮',
                                 fixed_size=ZSize(100, 40),
                                 fixed_stylesheet='border-radius: 4px;',
                                 hover_stylesheet='border-radius: 4px;')
        self.layout().addWidget(self.btn_push10)

        self.btn_push11 = ZNoBackgroundButton(parent=self,
                                 name='btn_push11',
                                 text='无背景按钮',
                                 fixed_size=ZSize(100, 40))
        self.layout().addWidget(self.btn_push11)

        self.spacer = ZSpacer(minH=40,
                              minW=20,
                              row=Zen.SizePolicy.Minimum,
                              columns=Zen.SizePolicy.Expanding)
        self.layout().addItem(self.spacer)



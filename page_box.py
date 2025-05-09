from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class PageBox(ZBox):
    def __init__(self,parent = None,name ='pageBox'):
        super().__init__(parent = parent,
                         name=name,
                         style= ZBox.Style.MonochromeWithBorder,
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
        self.label_title.setFixedStyleSheet('padding:5px;\nfont-size: 24px;\nfont-family: "幼圆";\nfont-weight: bold;')
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


        self.btn_push1 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push1',
                                 text='点赞',
                                 fixed_size=ZSize(56, 32),
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum),
                                 idle_style=ZPushButton.IdleStyle.Transparent,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push1)

        self.btn_push2 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push2',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_thumb_like_filled.svg'),
                                 tooltip='点赞',
                                 fixed_size=ZSize(32, 32),
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum),
                                 idle_style=ZPushButton.IdleStyle.Transparent,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push2)

        self.btn_push3 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push3',
                                 text='点赞',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_thumb_like_filled.svg'),
                                 fixed_size=ZSize(72, 32),
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum),
                                 idle_style=ZPushButton.IdleStyle.Monochrome,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push3)

        self.btn_push4 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push4',
                                 text='点赞',
                                 fixed_size=ZSize(56, 32),
                                 idle_style=ZPushButton.IdleStyle.Gradient,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push4)

        self.btn_push5 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push5',
                                 text='点赞',
                                 fixed_size=ZSize(56, 32),
                                 border_radius=0,
                                 idle_style=ZPushButton.IdleStyle.Border,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push5)

        self.btn_push6 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push6',
                                 text='点赞',
                                 fixed_size=ZSize(56, 32),
                                 idle_style=ZPushButton.IdleStyle.MonochromeWithBorder,
                                 hover_style=ZPushButton.HoverStyle.ColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push6)

        self.btn_push7 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push7',
                                 text='点赞',
                                 fixed_size=ZSize(56, 32),
                                 border_radius=0,
                                 idle_style=ZPushButton.IdleStyle.Transparent,
                                 hover_style=ZPushButton.HoverStyle.AddBorder,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push7)

        self.btn_push8 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push8',
                                 text='点赞',
                                 fixed_size=ZSize(56, 32),
                                 idle_style=ZPushButton.IdleStyle.Gradient,
                                 hover_style=ZPushButton.HoverStyle.IconTextColorChange,
                                 pressed_style=ZPushButton.PressedStyle.ColorChange)
        self.contain_zpush.layout().addWidget(self.btn_push8)

        self.btn_zpush_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_zpush.layout().addItem(self.btn_zpush_spacer)


        # region ZTabButton
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

        self.btn_toggle1 = ZToggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle1',
                                 text='收藏',
                                 icon=icon_toggle,
                                 fixed_size=ZSize(56, 32),
                                 have_tab=True,
                                 tab_pos=Zen.Position.Left,
                                 tab_width=2,
                                 tab_offset=2,
                                 tab_border_radius=1,
                                 tab_len_offset=8,
                                 checked_style=ZToggleButton.CheckedStyle.IconTextColorChange,
                                 hover_style=ZToggleButton.HoverStyle.ColorChange,
                                 pressed_style=ZToggleButton.PressedStyle.Transparent)
        self.contain_ztoggle.layout().addWidget(self.btn_toggle1)

        self.btn_toggle2 = ZToggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle2',
                                 icon=icon_toggle,
                                 tooltip='收藏',
                                 fixed_size=ZSize(32, 32),
                                 checked_style=ZToggleButton.CheckedStyle.IconTextColorChange,
                                 hover_style=ZToggleButton.HoverStyle.ColorChange,
                                 pressed_style=ZToggleButton.PressedStyle.Transparent)
        self.contain_ztoggle.layout().addWidget(self.btn_toggle2)

        self.btn_toggle3 = ZToggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle3',
                                 text='收藏',
                                 icon=icon_toggle,
                                 fixed_size=ZSize(56, 32),
                                 checked_style=ZToggleButton.CheckedStyle.IconTextColorChange,
                                 hover_style=ZToggleButton.HoverStyle.ColorChange,
                                 pressed_style=ZToggleButton.PressedStyle.Transparent)
        self.contain_ztoggle.layout().addWidget(self.btn_toggle3)

        self.btn_toggle4 = ZToggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle4',
                                 text='收藏',
                                 icon=icon_toggle,
                                 fixed_size=ZSize(56, 32),
                                 checked_style=ZToggleButton.CheckedStyle.AddBorder,
                                 hover_style=ZToggleButton.HoverStyle.ColorChange,
                                 pressed_style=ZToggleButton.PressedStyle.Transparent)
        self.contain_ztoggle.layout().addWidget(self.btn_toggle4)

        self.btn_toggle5 = ZToggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle5',
                                 text='收藏',
                                 icon=icon_toggle,
                                 fixed_size=ZSize(56, 32),
                                 checked_style=ZToggleButton.CheckedStyle.Monochrome,
                                 hover_style=ZToggleButton.HoverStyle.ColorChange,
                                 pressed_style=ZToggleButton.PressedStyle.Transparent)
        self.contain_ztoggle.layout().addWidget(self.btn_toggle5)

        self.btn_toggle6 = ZToggleButton(parent=self.contain_ztoggle,
                                 name='btn_toggle6',
                                 text='收藏',
                                 icon=icon_toggle,
                                 fixed_size=ZSize(56, 32),
                                 checked_style=ZToggleButton.CheckedStyle.Gradient,
                                 hover_style=ZToggleButton.HoverStyle.ColorChange,
                                 pressed_style=ZToggleButton.PressedStyle.Transparent)
        self.contain_ztoggle.layout().addWidget(self.btn_toggle6)

        self.contain_ztoggle_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_ztoggle.layout().addItem(self.contain_ztoggle_spacer)


        self.spacer = ZSpacer(minH=40,
                              minW=20,
                              row=Zen.SizePolicy.Minimum,
                              columns=Zen.SizePolicy.Expanding)
        self.layout().addItem(self.spacer)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class PageWidget(ZScrollPage):
    def __init__(self,parent = None,name ='pageWidget'):
        super().__init__(parent=parent,
                         name=name,
                         fixed_stylesheet="border-width: 1px;\nborder-style: solid;\nborder-radius:4px;",
                         style= ZScrollPage.Style.Monochrome|ZScrollPage.Style.Border,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        # region title
        self.label_title = ZTextLabel(parent=self,
                                 name='title',
                                 text='控件',
                                 alignment=Zen.Alignment.Left)
        self.label_title.setFixedStyleSheet('padding:5px;\nfont-size: 24px;\nfont-family: "微软雅黑";\nfont-weight: bold;')
        self.layout().addWidget(self.label_title)

        # region btn
        self.label_btn = ZTextLabel(parent=self,
                                 name='label_btn',
                                 text='按钮',
                                 alignment=Zen.Alignment.Left)
        self.label_btn.setFixedStyleSheet('''padding:10px;\npadding-left:20px;\nfont-size: 14px;\nfont-family: "微软雅黑";''')
        self.layout().addWidget(self.label_btn)


        self.contain_zpush = ZBox(parent=self,
                                 name='contain_zpush',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_zpush)

        self.label_zpush = ZTextLabel(parent=self.contain_zpush,
                                 name='label_zpush',
                                 text='基础按钮',
                                 alignment=Zen.Alignment.Center)
        self.label_zpush.setFixedStyleSheet('''padding:10px;\npadding-left:20px;\nfont-size: 12px;\nfont-family: "微软雅黑";''')
        self.contain_zpush.layout().addWidget(self.label_zpush)


        self.btn_trans = ZQuickButton.transButton(parent=self.contain_zpush,
                                 name='btn_trans',
                                 text='透明按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_trans)

        self.btn_fill = ZQuickButton.fillButton(parent=self.contain_zpush,
                                 name='btn_fill',
                                 text='填充按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_fill)

        self.btn_gradient = ZQuickButton.gradientButton(parent=self.contain_zpush,
                                 name='btn_gradient',
                                 text='渐变按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_gradient)

        self.btn_text = ZQuickButton.textButton(parent=self.contain_zpush,
                                 name='btn_text',
                                 text='文本按钮',
                                 tooltip='文本按钮',
                                 fixed_size=ZSize(78, 32))
        self.contain_zpush.layout().addWidget(self.btn_text)

        self.btn_icon = ZQuickButton.iconButton(parent=self.contain_zpush,
                                 name='btn_icon',
                                 icon=QIcon(':/icons/svg/fluent/regular/ic_fluent_sparkle_regular.svg'),
                                 tooltip='图标按钮',
                                 fixed_size=ZSize(32, 32))
        self.contain_zpush.layout().addWidget(self.btn_icon)

        self.btn_zpush_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_zpush.layout().addItem(self.btn_zpush_spacer)


        # region toggle_btn
        self.contain_ztoggle = ZBox(parent=self,
                                 name='contain_ztoggle',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_ztoggle)

        self.label_ztoggle = ZTextLabel(parent=self.contain_ztoggle,
                                 name='label_ztab',
                                 text='切换按钮',
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

        # region slider,scrollbar
        self.contain_zslider = ZBox(parent=self,
                                 name='contain_zslider',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_zslider)

        self.label_zslider = ZTextLabel(parent=self.contain_zslider,
                                 name='label_ztab',
                                 text='ZSlider',
                                 alignment=Zen.Alignment.Center)
        self.label_zslider.setFixedStyleSheet('padding:10px;\npadding-left:20px;\nfont-size: 12px;\nfont-family: "微软雅黑";')
        self.contain_zslider.layout().addWidget(self.label_zslider)

        self.slider_h = ZSlider(parent=self.contain_zslider,
                                 direction=Zen.Direction.Horizontal,
                                 track_length=200,
                                 value_range=(0,100),
                                 step=0.1,
                                 value=20)
        self.contain_zslider.layout().addWidget(self.slider_h)

        self.slider_v = ZSlider(parent=self.contain_zslider,
                                 direction=Zen.Direction.Vertical,
                                 track_length=200,
                                 value_range=(0,100),
                                 step=1,
                                 value=50)
        self.contain_zslider.layout().addWidget(self.slider_v)

        self.scrollbar_h = ZScrollBar(parent=self.contain_zslider,
                                 direction=Zen.Direction.Horizontal,
                                 track_length=200,
                                 value_range=(0,100),
                                 step=1,
                                 value=50)
        self.contain_zslider.layout().addWidget(self.scrollbar_h)

        self.scrollbar_v = ZScrollBar(parent=self.contain_zslider,
                                 direction=Zen.Direction.Vertical,
                                 track_length=200,
                                 value_range=(0,100),
                                 step=1,
                                 value=50)
        self.contain_zslider.layout().addWidget(self.scrollbar_v)

        self.contain_zslider_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_zslider.layout().addItem(self.contain_zslider_spacer)

        self.spacer = ZSpacer(minH=40,
                              minW=20,
                              row=Zen.SizePolicy.Minimum,
                              columns=Zen.SizePolicy.Expanding)
        self.layout().addItem(self.spacer)

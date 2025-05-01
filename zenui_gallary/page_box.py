from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from ZenUI import *

class PageBox(ZContainer):
    def __init__(self,parent = None,name ='pageBox'):
        super().__init__(parent = parent,
                         name=name,
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


        # region ZPushButton
        self.contain_zpush = ZContainer(parent=self,
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


        self.btn_push1 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push1',
                                 text='点赞',
                                 min_height=32,
                                 min_width=64,
                                 max_height=32,
                                 max_width=64,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_zpush.layout().addWidget(self.btn_push1)

        self.btn_push2 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push2',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_thumb_like_filled.svg'),
                                 tooltip='点赞',
                                 min_height=32,
                                 min_width=32,
                                 max_height=32,
                                 max_width=32,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_zpush.layout().addWidget(self.btn_push2)

        self.btn_push3 = ZPushButton(parent=self.contain_zpush,
                                 name='btn_push3',
                                 text='点赞',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_thumb_like_filled.svg'),
                                 min_height=32,
                                 min_width=96,
                                 max_height=32,
                                 max_width=96,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_zpush.layout().addWidget(self.btn_push3)

        self.btn_zpush_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_zpush.layout().addItem(self.btn_zpush_spacer)



        # region ZTransButton
        self.contain_ztrans = ZContainer(parent=self,
                                 name='contain_ztrans',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_ztrans)

        self.label_ztrans = ZTextLabel(parent=self.contain_ztrans,
                                 name='label_zpush',
                                 text='透明按钮',
                                 alignment=Zen.Alignment.Center)
        self.label_ztrans.setFixedStyleSheet('padding:10px;\npadding-left:20px;\nfont-size: 12px;\nfont-family: "微软雅黑";')
        self.contain_ztrans.layout().addWidget(self.label_ztrans)


        self.btn_trans1 = ZTransButton(parent=self.contain_ztrans,
                                 name='btn_trans1',
                                 text='点赞',
                                 min_height=32,
                                 min_width=64,
                                 max_height=32,
                                 max_width=64,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_ztrans.layout().addWidget(self.btn_trans1)

        self.btn_trans2 = ZTransButton(parent=self.contain_ztrans,
                                 name='btn_trans2',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_thumb_like_filled.svg'),
                                 tooltip='点赞',
                                 min_height=32,
                                 min_width=32,
                                 max_height=32,
                                 max_width=32,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_ztrans.layout().addWidget(self.btn_trans2)

        self.btn_trans3 = ZTransButton(parent=self.contain_ztrans,
                                 name='btn_trans3',
                                 text='点赞',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_thumb_like_filled.svg'),
                                 min_height=32,
                                 min_width=96,
                                 max_height=32,
                                 max_width=96,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_ztrans.layout().addWidget(self.btn_trans3)

        self.btn_ztrans_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_ztrans.layout().addItem(self.btn_ztrans_spacer)


        # region ZTabButton
        self.contain_ztab = ZContainer(parent=self,
                                 name='contain_ztab',
                                 layout=Zen.Layout.Row,
                                 margins=ZMargins(6, 6, 6, 6),
                                 spacing=12)
        self.layout().addWidget(self.contain_ztab)

        self.label_ztab = ZTextLabel(parent=self.contain_ztab,
                                 name='label_ztab',
                                 text='标签按钮',
                                 alignment=Zen.Alignment.Center)
        self.label_ztab.setFixedStyleSheet('padding:10px;\npadding-left:20px;\nfont-size: 12px;\nfont-family: "微软雅黑";')
        self.contain_ztab.layout().addWidget(self.label_ztab)


        icon_tab = QIcon()
        icon_tab.addFile(':/icons/svg/fluent/regular/ic_fluent_sparkle_regular.svg', QSize(32, 32), QIcon.Mode.Normal, QIcon.State.Off)
        icon_tab.addFile(':/icons/svg/fluent/filled/ic_fluent_sparkle_filled.svg', QSize(32, 32), QIcon.Mode.Normal, QIcon.State.On)
        self.btn_tab1 = ZTabButton(parent=self.contain_ztab,
                                 name='btn_tab1',
                                 text='收藏',
                                 tab_length_offset=8,
                                 min_height=32,
                                 min_width=64,
                                 max_height=32,
                                 max_width=64,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_ztab.layout().addWidget(self.btn_tab1)

        self.btn_tab2 = ZTabButton(parent=self.contain_ztab,
                                 name='btn_tab2',
                                 icon=icon_tab,
                                 tooltip='收藏',
                                 tab_length_offset=8,
                                 min_height=32,
                                 min_width=32,
                                 max_height=32,
                                 max_width=32,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_ztab.layout().addWidget(self.btn_tab2)

        self.btn_tab3 = ZTabButton(parent=self.contain_ztab,
                                 name='btn_tab3',
                                 text='收藏',
                                 icon=icon_tab,
                                 tab_length_offset=8,
                                 min_height=32,
                                 min_width=96,
                                 max_height=32,
                                 max_width=96,
                                 sizepolicy=(Zen.SizePolicy.Minimum, Zen.SizePolicy.Minimum))
        self.contain_ztab.layout().addWidget(self.btn_tab3)

        self.contain_ztab_spacer = ZSpacer(minH=20,
                              minW=32,
                              row=Zen.SizePolicy.Expanding,
                              columns=Zen.SizePolicy.Minimum)
        self.contain_ztab.layout().addItem(self.contain_ztab_spacer)


        self.spacer = ZSpacer(minH=40,
                              minW=20,
                              row=Zen.SizePolicy.Minimum,
                              columns=Zen.SizePolicy.Expanding)
        self.layout().addItem(self.spacer)
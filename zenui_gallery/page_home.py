from PySide6.QtGui import QIcon,QColor
from textwrap import dedent
from ZenUI._legacy import *
from zenui_gallery.rc_rc import *
class PageHome(ZPage):
    def __init__(self,parent = None,name ='pageHome'):
        super().__init__(parent = parent,
                         name=name,
                         fixed_stylesheet="border-width: 1px;\nborder-style: solid;\nborder-radius:4px;",
                         style=ZPage.Style.Border,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(6, 6, 6, 6),
                         spacing=12)
        self.image_bg = ZImageLayer(parent=self,
                                  scale_type=Zen.ScaleType.Fill,
                                  corner_radius=4)
        self.image_bg_mask = ZImageLayer(parent=self,
                                  scale_type=Zen.ScaleType.Stretch,
                                  corner_radius=4)
        self._load_bg_image()

        self._setup_ui()

    def _load_bg_image(self):
        if getTheme() == Zen.Theme.Light:
            self.image_bg.setImage(":/image/home_bg_light.png")
            self.image_bg_mask.setImage(":/image/home_bg_mask_light.png")
        else:
            self.image_bg.setImage(":/image/home_bg_dark.png")
            self.image_bg_mask.setImage(":/image/home_bg_mask_dark.png")

    def _theme_changed_handler(self, theme):
        super()._theme_changed_handler(theme)
        self._load_bg_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.image_bg.setGeometry(1, 1, self.width()-2, self.height()-2)
        self.image_bg_mask.setGeometry(1, 1, self.width()-2, self.height()-2)


    def _setup_ui(self):
        self.label_title = ZTextLabel(parent=self,
                                 name='text',
                                 text="ZenUI Gallary",
                                 alignment=Zen.Alignment.Left)
        sheet = dedent('''\
                padding-top:30px;
                padding-left:20px;
                padding-bottom:30px;
                font-family: 'Microsoft YaHei';
                font-size: 30px;
                font-weight: bold;
                border-radius: 4px;''')
        self.label_title.setFixedStyleSheet(sheet)
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

        self.btn_nextpage = ZQuickButton.transButton(parent=self.contain_button,
                                 name='btn_nextpage',
                                 icon=QIcon(':/icons/svg/fluent/filled/ic_fluent_arrow_right_filled.svg'),
                                 fixed_size=ZSize(60,40),
                                 tooltip='下一页'
                                 )
        self.contain_button.layout().addWidget(self.btn_nextpage)
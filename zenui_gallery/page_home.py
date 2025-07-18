from PySide6.QtCore import Qt,QMargins
from PySide6.QtGui import QFont
from ZenUI import *
from zenui_gallery.rc_rc import *
class PageHome(ZPage):
    def __init__(self,parent = None,name ='pageHome'):
        super().__init__(parent = parent,
                         name=name,
                         layout=self.Layout.Column,
                         margins=QMargins(6, 6, 6, 6),
                         spacing=12,
                         alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        self.image_bg = ZImage(parent=self,
                                  scale_type=ZImage.ScaleType.Fill,
                                  corner_radius=4)
        self.image_bg_mask = ZImage(parent=self,
                                  scale_type=ZImage.ScaleType.Stretch,
                                  corner_radius=4)
        ZGlobal.themeManager.themeChanged.connect(self._theme_changed_handler)
        self._load_bg_image()
        self._setup_ui()

    def _load_bg_image(self):
        if ZGlobal.themeManager.getTheme() == ZTheme.Light:
            self.image_bg.setImage(":/image/home_bg_light.svg")
            self.image_bg_mask.setImage(":/image/home_bg_mask_light.svg")
        else:
            self.image_bg.setImage(":/image/home_bg_dark.svg")
            self.image_bg_mask.setImage(":/image/home_bg_mask_dark.svg")

    def _theme_changed_handler(self, theme):
        self._load_bg_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.image_bg.setGeometry(1, 1, self.width()-2, self.height()-2)
        self.image_bg_mask.setGeometry(1, 1, self.width()-2, self.height()-2)

    def _setup_ui(self):
        self.text = ZTextBlock(parent=self,
                                 name='text',
                                 text='ZenUI Gallery')
        self.text.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        self.text.margins = QMargins(50,50,50,50)
        self.layout().addWidget(self.text)
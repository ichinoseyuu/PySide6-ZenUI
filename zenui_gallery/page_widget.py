from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QFont, QIcon
from ZenUI import *

class PageWidget(ZScrollPage):
    def __init__(self,parent = None,name ='pageWidget'):
        super().__init__(parent = parent,
                         name=name,
                         margins=QMargins(6, 6, 6, 6),
                         spacing=12,
                         alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        self._setup_ui()

    def _setup_ui(self):
        self.text = ZTextBlock(parent=self,
                                 name='text',
                                 text='控件')
        self.text.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        #self.text.setFixedSize(800,800)
        self.content.layout().addWidget(self.text)

        # region Button
        self.btn_box = QHBoxLayout()
        self.btn_box.setContentsMargins(6, 6, 6, 6)
        self.btn_box.setSpacing(12)
        self.btn_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.content.layout().addLayout(self.btn_box)


        btn_icon  = QIcon(u":/icons/fluent/regular/ic_fluent_save_regular.svg")

        self.btn_1 = ZButton(
            parent=self,
            name='btn_1',
            icon=btn_icon)
        self.btn_1.setToolTip('保存')
        self.btn_box.addWidget(self.btn_1)

        self.btn_2 = ZButton(
            parent=self,
            name='btn_2',
            icon=btn_icon,
            text='保存')
        self.btn_box.addWidget(self.btn_2)

        self.btn_3 = ZButton(
            parent=self,
            name='btn_3',
            text='保存')
        self.btn_box.addWidget(self.btn_3)

        self.btn_4 = ZButton(
            parent=self,
            name='btn_4',
            text='连点按钮')
        self.btn_4.repeatClick = True
        self.btn_box.addWidget(self.btn_4)

        self.toggle_btn_box = QHBoxLayout()
        self.toggle_btn_box.setContentsMargins(6, 6, 6, 6)
        self.toggle_btn_box.setSpacing(12)
        self.toggle_btn_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.content.layout().addLayout(self.toggle_btn_box)

        self.toggle_btn = ZToggleButton(
            parent=self,
            name='toggle_btn',
            text='切换按钮')
        self.toggle_btn.setToolTip('这是一个切换按钮')
        self.toggle_btn.setFixedSize(100, 30)
        self.toggle_btn_box.addWidget(self.toggle_btn)

        self.hslider_box = QVBoxLayout()
        self.hslider_box.setContentsMargins(6, 6, 6, 6)
        self.hslider_box.setSpacing(12)
        self.hslider_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.content.layout().addLayout(self.hslider_box)

        self.hslider_1 = ZSlider(
            parent=self,
            name='hslider_1',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=8)
        self.hslider_box.addWidget(self.hslider_1)

        self.hslider_2 = ZSlider(
            parent=self,
            name='hslider_2',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=30)
        self.hslider_box.addWidget(self.hslider_2)

        self.hslider_3 = ZSlider(
            parent=self,
            name='hslider_3',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50,
            auto_strip_zero=True)
        self.hslider_box.addWidget(self.hslider_3)

        self.vslider_box = QHBoxLayout()
        self.vslider_box.setContentsMargins(6, 6, 6, 6)
        self.vslider_box.setSpacing(12)
        #self.vslider_box.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.content.layout().addLayout(self.vslider_box)

        self.vslider_1 = ZSlider(
            parent=self,
            name='vslider_1',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=8)

        self.vslider_box.addWidget(self.vslider_1)

        self.vslider_2 = ZSlider(
            parent=self,
            name='vslider_2',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=30)

        self.vslider_box.addWidget(self.vslider_2)

        self.vslider_3 = ZSlider(
            parent=self,
            name='vslider_3',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50)

        self.vslider_box.addWidget(self.vslider_3)

        self.card = ZCard(parent=self,
                          name='card',)
        self.card.setFixedSize(200, 200)
        self.vslider_box.addWidget(self.card)
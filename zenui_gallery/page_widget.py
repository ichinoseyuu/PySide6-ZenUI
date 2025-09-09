from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PageWidget(ZScrollPage):
    def __init__(self,parent = None,name ='PageWidget'):
        super().__init__(parent = parent,
                         name=name,
                         margins=QMargins(9, 9, 9, 9),
                         spacing=12,
                         alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        #self.setMaximumWidth(600)
        self._setup_ui()

    def _setup_ui(self):
        self.title = ZTextBlock(self, 'title', '基础组件')
        self.title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        self.title.margins = QMargins(6, 0, 6, 0)
        self.content.layout().addWidget(self.title)

        # region Text
        self.text_block_card = DemoCard(self, 'text_block_card')
        self.text_block_card.title.text = 'ZTextBlock'
        self.text_block_card.setFixedHeight(260)
        self.content.layout().addWidget(self.text_block_card)

        self.text_block_1 = ZTextBlock(self.text_block_card, name='text_block_1')
        self.text_block_1.margins = QMargins(6, 0, 6, 0)
        self.text_block_1.wrapMode = ZTextBlock.WrapMode.NoWrap
        self.text_block_1.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        self.text_block_1.move(16, 50)

        self.text_block_2 = ZTextBlock(self.text_block_card, name='text_block_2',selectable=True)
        self.text_block_2.margins = QMargins(6, 6, 6, 6)
        self.text_block_2.wrapMode = ZTextBlock.WrapMode.NoWrap
        self.text_block_2.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        self.text_block_2.move(16, 90)

        self.text_block_3 = ZTextBlock(self.text_block_card, name='text_block_3',selectable=True)
        self.text_block_3.setMaximumWidth(400)
        self.text_block_3.margins = QMargins(6, 6, 6, 6)
        self.text_block_3.wrapMode = ZTextBlock.WrapMode.WordWrap
        self.text_block_3.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        self.text_block_3.move(16, 130)

        self.text_block_4 = ZTextBlock(self.text_block_card, name='text_block_4',selectable=True)
        self.text_block_4.setMaximumWidth(400)
        self.text_block_4.margins = QMargins(6, 6, 6, 6)
        self.text_block_4.wrapMode = ZTextBlock.WrapMode.WrapAnywhere
        self.text_block_4.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        self.text_block_4.move(16, 190)

        self.rich_text_card = DemoCard(self, 'rich_text_card')
        self.rich_text_card.title.text = 'ZRichTextBlock'
        self.rich_text_card.setFixedHeight(130)
        self.content.layout().addWidget(self.rich_text_card)

        self.rich_text_1 = ZRichTextBlock(self.rich_text_card, name='rich_text_1')
        self.rich_text_1.html = '''
        <p>
        欢迎使用
        <span style="color: #ff6b6b; font-weight: bold;">ZenUI</span> 
        组件库！这个组件库基于
        <span style="color: #4ecdc4; font-style: bold;">PySide6</span>
        开发。
        </p>
        '''
        self.rich_text_1.move(16, 50)

        self.rich_text_2 = ZRichTextBlock(self.rich_text_card, name='rich_text_2',selectable=True)
        self.rich_text_2.html = '''
        <p>
        欢迎使用
        <span style="color: #ff6b6b; font-weight: bold;">ZenUI</span> 
        组件库！这个组件库基于
        <span style="color: #4ecdc4; font-style: bold;">PySide6</span>
        开发。
        </p>
        '''
        self.rich_text_2.move(16, 90)

        self.text_box_card = DemoCard(self, 'text_box_card')
        self.text_box_card.title.text = 'ZTextBox'
        self.text_box_card.setFixedHeight(240)
        self.content.layout().addWidget(self.text_box_card)

        self.text_box_1 = ZTextBox(self.text_box_card, name='text_box_1',read_only=True)
        self.text_box_1.setMinimumWidth(300)
        #self.text_box_1.setMaximumWidth(500)
        self.text_box_1.setText('Hello ZenUI!')
        #self.text_box_1.setFixedSize(300, 30)
        self.text_box_1.move(16, 50)

        self.text_box_2 = ZTextBox(self.text_box_card, name='text_box_2')
        self.text_box_2.setMinimumWidth(300)
        #self.text_box_2.setFixedSize(300, 30)
        self.text_box_2.move(16, 100)

        self.text_box_3 = ZTextBox(self.text_box_card, name='text_box_3',mask='请输入内容')
        self.text_box_3.setMinimumWidth(300)
        self.text_box_3.wrapMode = ZTextBox.WrapMode.WrapAnywhere
        self.text_box_3.setMaximumWidth(300)
        #self.text_box_3.setFixedSize(300, 30)
        self.text_box_3.move(16, 150)

        # region Button
        self.btn_card = DemoCard(self, 'btn_card')
        self.btn_card.title.text = 'ZButton'
        self.btn_card.setFixedHeight(100)
        self.content.layout().addWidget(self.btn_card)

        btn_icon  = QIcon(u":/icons/fluent/regular/ic_fluent_save_regular.svg")

        self.btn_1 = ZButton(
            parent=self.btn_card,
            name='btn_1',
            icon=btn_icon)
        self.btn_1.setToolTip('保存')
        self.btn_1.move(16, 50)
        self.btn_1.clicked.connect(lambda: ZGlobal.tooltip.showTip(text='保存成功',
                                                                   target=self.btn_1,
                                                                   position=TipPos.TopRight,
                                                                   offset=QPoint(6, 6)
                                                                   ))

        self.btn_2 = ZButton(
            parent=self.btn_card,
            name='btn_2',
            icon=btn_icon,
            text='保存')
        self.btn_2.move(56, 50)
        self.btn_2.clicked.connect(lambda: ZGlobal.tooltip.showTip(text='保存成功',
                                                                   target=self.btn_2,
                                                                   mode=ZToolTip.Mode.TrackTarget,
                                                                   position=TipPos.Top,
                                                                   offset=QPoint(0, 6),
                                                                   hide_delay=800
                                                                   ))
        self.btn_3 = ZButton(
            parent=self.btn_card,
            name='btn_3',
            text='保存')
        self.btn_3.move(150, 50)
        self.btn_3.clicked.connect(lambda: ZGlobal.tooltip.showTip(text='保存成功',
                                                                   target=self.btn_3,
                                                                   mode=ZToolTip.Mode.TrackTarget,
                                                                   position=TipPos.Top,
                                                                   offset=QPoint(0, 6),
                                                                   hide_delay=800
                                                                   ))

        self.btn_4 = ZButton(
            parent=self.btn_card,
            name='btn_4',
            text='连点按钮')
        self.btn_4.repeatClick = True
        self.btn_4.move(222, 50)
        self.btn_4.clicked.connect(lambda: ZGlobal.tooltip.showTip(text=f'你连续点击了{self.btn_4.repeatClickCount}次',
                                                                   target=self.btn_4,
                                                                   position=TipPos.Top,
                                                                   mode=ZToolTip.Mode.TrackTarget,
                                                                   offset=QPoint(0, 6),
                                                                   hide_delay=800
                                                                   ))

        self.toggle_btn_card = DemoCard(self, 'toggle_btn_card')
        self.toggle_btn_card.title.text = 'ZToggleButton'
        self.toggle_btn_card.setFixedHeight(100)
        self.content.layout().addWidget(self.toggle_btn_card)

        self.toggle_btn_1 = ZToggleButton(
            parent=self.toggle_btn_card,
            name='toggle_btn_1',
            icon=btn_icon)
        self.toggle_btn_1.setToolTip('自动保存')
        self.toggle_btn_1.move(16, 50)

        self.toggle_btn_2 = ZToggleButton(
            parent=self.toggle_btn_card,
            name='toggle_btn_2',
            text='自动保存')
        self.toggle_btn_2.move(56, 50)

        self.toggle_btn_3 = ZToggleButton(
            parent=self.toggle_btn_card,
            name='toggle_btn_3',
            icon=btn_icon,
            text='自动保存')
        self.toggle_btn_3.move(166, 50)

        # region Slider
        self.slider_card = DemoCard(self, 'slider_card')
        self.slider_card.title.text = 'ZSlider'
        self.slider_card.setFixedHeight(250)
        self.content.layout().addWidget(self.slider_card)

        self.hslider_1 = ZSlider(
            parent=self.slider_card,
            name='hslider_1',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=8)
        self.hslider_1.setFixedLength(200)
        self.hslider_1.move(16, 72)

        self.hslider_2 = ZSlider(
            parent=self.slider_card,
            name='hslider_2',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=30)
        self.hslider_2.setFixedLength(250)
        self.hslider_2.move(16, 126)

        self.hslider_3 = ZSlider(
            parent=self.slider_card,
            name='hslider_3',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50,
            auto_strip_zero=True)
        self.hslider_3.setFixedLength(300)
        self.hslider_3.move(16, 180)

        self.vslider_1 = ZSlider(
            parent=self.slider_card,
            name='vslider_1',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=8)
        self.vslider_1.setFixedLength(150)
        self.vslider_1.move(380, 70)

        self.vslider_2 = ZSlider(
            parent=self.slider_card,
            name='vslider_2',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=30)
        self.vslider_2.setFixedLength(180)
        self.vslider_2.move(440, 40)

        self.vslider_3 = ZSlider(
            parent=self.slider_card,
            name='vslider_3',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50)
        self.vslider_3.setFixedLength(200)
        self.vslider_3.move(500, 20)



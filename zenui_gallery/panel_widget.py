from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PanelWidget(ZScrollPanel):
    def __init__(self,parent = None,name ='PanelWidget'):
        super().__init__(parent = parent, name=name)
        self.setLayout(ZVBoxLayout(self, margins = QMargins(40, 30, 40, 30),spacing=30, alignment=Qt.AlignmentFlag.AlignTop))
        self._setup_ui()

    def _setup_ui(self):
        title = ZTextBlock(self, 'title', '基础组件')
        title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        title.margins = QMargins(6, 0, 6, 6)
        self.layout().addWidget(title)

        # region Text
        title = ZTextBlock(self, text= '文本')
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.margins = QMargins(6, 6, 6, 6)
        self.layout().addWidget(title)

        card = DemoCard(self)
        self.layout().addWidget(card)

        title = ZTextBlock(self, text= 'ZTextBlock')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.text_block_1 = ZTextBlock(container, name='text_block_1')
        self.text_block_1.margins = QMargins(6, 0, 6, 0)
        self.text_block_1.wrapMode = ZTextBlock.WrapMode.NoWrap
        self.text_block_1.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        container.addWidget(self.text_block_1)

        self.text_block_2 = ZTextBlock(container, name='text_block_2',selectable=True)
        self.text_block_2.margins = QMargins(6, 6, 6, 6)
        self.text_block_2.wrapMode = ZTextBlock.WrapMode.NoWrap
        self.text_block_2.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        container.addWidget(self.text_block_2)

        self.text_block_3 = ZTextBlock(container, name='text_block_3',selectable=True)
        self.text_block_3.setMaximumWidth(400)
        self.text_block_3.margins = QMargins(6, 6, 6, 6)
        self.text_block_3.wrapMode = ZTextBlock.WrapMode.WordWrap
        self.text_block_3.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        container.addWidget(self.text_block_3)

        self.text_block_4 = ZTextBlock(container, name='text_block_4',selectable=True)
        self.text_block_4.setMaximumWidth(400)
        self.text_block_4.margins = QMargins(6, 6, 6, 6)
        self.text_block_4.wrapMode = ZTextBlock.WrapMode.WrapAnywhere
        self.text_block_4.text = 'PySide6 是 Qt 官方提供的 Python 模块，它允许开发者使用 Python 编写跨平台 GUI 应用程序，并提供了完整的 Qt 6.0+ 框架支持。'
        container.addWidget(self.text_block_4)

        title = ZTextBlock(self, text= 'ZRichTextBlock')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.rich_text_1 = ZRichTextBlock(container, name='rich_text_1')
        self.rich_text_1.html = '''
        <p>
        欢迎使用
        <span style="color: #ff6b6b; font-weight: bold;">ZenUI</span> 
        组件库！这个组件库基于
        <span style="color: #4ecdc4; font-style: bold;">PySide6</span>
        开发。
        </p>
        '''
        container.addWidget(self.rich_text_1)

        self.rich_text_2 = ZRichTextBlock(container, name='rich_text_2',selectable=True)
        self.rich_text_2.html = '''
        <p>
        欢迎使用
        <span style="color: #ff6b6b; font-weight: bold;">ZenUI</span> 
        组件库！这个组件库基于
        <span style="color: #4ecdc4; font-style: bold;">PySide6</span>
        开发。
        </p>
        '''
        container.addWidget(self.rich_text_2)

        # region Input
        title = ZTextBlock(self, text= '输入')
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.margins = QMargins(6, 6, 6, 6)
        self.layout().addWidget(title)

        card = DemoCard(self)
        self.layout().addWidget(card)

        title = ZTextBlock(self, text= 'ZTextBox')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.text_box_1 = ZTextBox(container, name='text_box_1',read_only=True)
        self.text_box_1.setMinimumWidth(300)
        #self.text_box_1.setMaximumWidth(500)
        self.text_box_1.setText('Hello ZenUI!')
        container.addWidget(self.text_box_1)

        self.text_box_2 = ZTextBox(container, name='text_box_2')
        self.text_box_2.setMinimumWidth(300)
        container.addWidget(self.text_box_2)

        self.text_box_3 = ZTextBox(container, name='text_box_3',mask='请输入内容')
        self.text_box_3.setMinimumWidth(300)
        self.text_box_3.wrapMode = ZTextBox.WrapMode.WrapAnywhere
        self.text_box_3.setMaximumWidth(300)
        def test():
            print('test')
            container.adjustSize()
            # 2. 触发card的布局重新计算
            card.layout().update()
            # 3. 强制card根据新布局调整自身大小
            card.adjustSize()
            # 4. 如果card所在的父布局也需要更新，可进一步触发
            self.layout().update()
        self.text_box_3.heightChangedByWrapping.connect(test)
        container.addWidget(self.text_box_3)


        # region Button
        title = ZTextBlock(self, text= '按钮')
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.margins = QMargins(6, 6, 6, 6)
        self.layout().addWidget(title)

        card = DemoCard(self)
        self.layout().addWidget(card)

        title = ZTextBlock(self, text= 'ZButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        btn_icon  = QIcon(u":/icons/fluent/regular/ic_fluent_save_regular.svg")

        self.btn_1 = ZButton(
            parent=container,
            name='btn_1',
            icon=btn_icon)
        self.btn_1.setToolTip('保存')
        container.addWidget(self.btn_1)
        self.btn_1.clicked.connect(lambda: ZGlobal.tooltip.showTip(text='保存成功',
                                                                   target=self.btn_1,
                                                                   position=TipPos.TopRight,
                                                                   offset=QPoint(6, 6)
                                                                   ))

        self.btn_2 = ZButton(
            parent=container,
            name='btn_2',
            icon=btn_icon,
            text='保存')
        container.addWidget(self.btn_2)
        self.btn_2.clicked.connect(lambda: ZGlobal.tooltip.showTip(text='保存成功',
                                                                   target=self.btn_2,
                                                                   mode=ZToolTip.Mode.TrackTarget,
                                                                   position=TipPos.Top,
                                                                   offset=QPoint(0, 6),
                                                                   hide_delay=800
                                                                   ))
        self.btn_3 = ZButton(
            parent=container,
            name='btn_3',
            text='保存')
        container.addWidget(self.btn_3)
        self.btn_3.clicked.connect(lambda: ZGlobal.tooltip.showTip(text='保存成功',
                                                                   target=self.btn_3,
                                                                   mode=ZToolTip.Mode.TrackTarget,
                                                                   position=TipPos.Top,
                                                                   offset=QPoint(0, 6),
                                                                   hide_delay=800
                                                                   ))

        self.btn_4 = ZButton(
            parent=container,
            name='btn_4',
            text='连点按钮')
        self.btn_4.repeatClick = True
        container.addWidget(self.btn_4)
        self.btn_4.clicked.connect(lambda: ZGlobal.tooltip.showTip(text=f'你连续点击了{self.btn_4.repeatClickCount}次',
                                                                   target=self.btn_4,
                                                                   position=TipPos.Top,
                                                                   mode=ZToolTip.Mode.TrackTarget,
                                                                   offset=QPoint(0, 6),
                                                                   hide_delay=800
                                                                   ))


        title = ZTextBlock(self, text= 'ZToggleButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        self.toggle_btn_1 = ZToggleButton(
            parent=container,
            name='toggle_btn_1',
            icon=btn_icon)
        self.toggle_btn_1.setToolTip('自动保存')
        container.addWidget(self.toggle_btn_1)

        self.toggle_btn_2 = ZToggleButton(
            parent=container,
            name='toggle_btn_2',
            text='自动保存')
        container.addWidget(self.toggle_btn_2)

        self.toggle_btn_3 = ZToggleButton(
            parent=container,
            name='toggle_btn_3',
            icon=btn_icon,
            text='自动保存')
        container.addWidget(self.toggle_btn_3)

        title = ZTextBlock(self, text= 'ZSwitch')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        container.alignment = Qt.AlignmentFlag.AlignBottom
        card.layout().addWidget(container)

        self.switch_1 = ZSwitch(container, name='switch_1', weight= ZSwitch.Style.Compact)
        container.addWidget(self.switch_1)

        self.switch_2 = ZSwitch(container, name='switch_2', weight= ZSwitch.Style.Standard)
        container.addWidget(self.switch_2)

        self.switch_3 = ZSwitch(container, name='switch_3', weight= ZSwitch.Style.Comfortable)
        container.addWidget(self.switch_3)


        # region Slider
        title = ZTextBlock(self, text= '滑块')
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.margins = QMargins(6, 6, 6, 6)
        self.layout().addWidget(title)

        card = DemoCard(self)
        self.layout().addWidget(card)

        title = ZTextBlock(self, text= 'ZSlider')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        hlayout = ZHBoxLayout(margins=QMargins(0, 0, 0, 0),spacing=16,alignment=Qt.AlignLeft|Qt.AlignTop)
        card.layout().addLayout(hlayout)

        container1 = ZVContainer(card)
        container1.alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter
        container1.defaultSpacing = 16
        hlayout.layout().addWidget(container1)

        self.hslider_1 = ZSlider(
            parent=container1,
            name='hslider_1',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=5)
        self.hslider_1.setFixedLength(230)
        container1.addWidget(self.hslider_1)

        self.hslider_2 = ZSlider(
            parent=container1,
            name='hslider_2',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=50)
        self.hslider_2.setFixedLength(250)
        container1.addWidget(self.hslider_2)

        self.hslider_3 = ZSlider(
            parent=container1,
            name='hslider_3',
            orientation=ZSlider.Orientation.Horizontal,
            weight=ZSlider.Weight.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50,
            auto_strip_zero=True)
        self.hslider_3.setFixedLength(200)
        container1.addWidget(self.hslider_3)
        container1.arrangeWidgets()

        container2 = ZHContainer(card)
        container2.alignment = Qt.AlignmentFlag.AlignBottom
        container2.defaultSpacing = 16
        hlayout.layout().addWidget(container2)

        self.vslider_1 = ZSlider(
            parent=container2,
            name='vslider_1',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=5)
        self.vslider_1.setFixedLength(150)
        container2.addWidget(self.vslider_1)

        self.vslider_2 = ZSlider(
            parent=container2,
            name='vslider_2',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=50)
        self.vslider_2.setFixedLength(180)
        container2.addWidget(self.vslider_2)

        self.vslider_3 = ZSlider(
            parent=container2,
            name='vslider_3',
            orientation=ZSlider.Orientation.Vertical,
            weight=ZSlider.Weight.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50)
        self.vslider_3.setFixedLength(170)
        container2.addWidget(self.vslider_3)
        container2.arrangeWidgets()



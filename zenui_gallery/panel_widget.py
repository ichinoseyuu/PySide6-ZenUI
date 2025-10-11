from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint,QSize
from PySide6.QtGui import QFont, QIcon, QColor
from ZenUI import *
from demo_card import DemoCard

class PanelWidget(ZScrollPanel):
    def __init__(self,parent = None,name ='PanelWidget'):
        super().__init__(parent, name)
        self.setLayout(
            ZVBoxLayout(
                self,
                margins = QMargins(40, 30, 40, 30),
                spacing=30,
                alignment=Qt.AlignmentFlag.AlignTop
                )
            )
        self._setup_ui()

    def _setup_ui(self):
        title = ZTextBlock(self, 'title', '基础组件')
        title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        title.margins = QMargins(6, 0, 6, 6)
        self.layout().addWidget(title)

        # region ZButton
        title = ZTextBlock(self, text= '基本输入组件')
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.margins = QMargins(6, 6, 6, 6)
        self.layout().addWidget(title)

        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        self.layout().addLayout(layout)

        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        btn_icon = ZGlobal.iconPack.toIcon('ic_fluent_save_regular')

        self.btn_1 = ZButton(
            parent=container,
            name='btn_1',
            icon=btn_icon
            )
        self.btn_1.setToolTip('保存')
        container.addWidget(self.btn_1, spacing=16)
        self.btn_1.clicked.connect(
            lambda: ZGlobal.tooltip.showTip(
                text='保存成功',
                target=self.btn_1,
                position=ZPosition.TopRight,
                offset=QPoint(6, 6)
                )
            )

        self.btn_2 = ZButton(
            parent=container,
            name='btn_2',
            icon=btn_icon,
            text='保存'
            )
        container.addWidget(self.btn_2, spacing=16)
        self.btn_2.clicked.connect(
            lambda: ZGlobal.tooltip.showTip(
                text='保存成功',
                target=self.btn_2,
                mode=ZToolTip.Mode.TrackTarget,
                position=ZPosition.Top,
                offset=QPoint(0, 6),
                hide_delay=800
                )
            )
        self.btn_3 = ZButton(
            parent=container,
            name='btn_3',
            text='保存'
            )
        container.addWidget(self.btn_3, spacing=16)
        self.btn_3.clicked.connect(
            lambda: ZGlobal.tooltip.showTip(
                text='保存成功',
                target=self.btn_3,
                mode=ZToolTip.Mode.TrackTarget,
                position=ZPosition.Top,
                offset=QPoint(0, 6),
                hide_delay=800
                )
            )

        # region ZToggleButton
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZToggleButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        self.toggle_btn_1 = ZToggleButton(
            parent=container,
            name='toggle_btn_1',
            icon=btn_icon
            )
        self.toggle_btn_1.setToolTip('自动保存')
        container.addWidget(self.toggle_btn_1, spacing=16)

        self.toggle_btn_2 = ZToggleButton(
            parent=container,
            name='toggle_btn_2',
            icon=btn_icon,
            text='自动保存'
            )
        container.addWidget(self.toggle_btn_2, spacing=16)

        self.toggle_btn_3 = ZToggleButton(
            parent=container,
            name='toggle_btn_3',
            text='自动保存'
            )
        container.addWidget(self.toggle_btn_3, spacing=16)

        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        self.layout().addLayout(layout)

        # region ZSwitch
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZSwitch')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        container.setAlignment(Qt.AlignmentFlag.AlignBottom)
        card.layout().addWidget(container)

        self.switch_1 = ZSwitch(container, name='switch_1', style= ZSwitch.Style.Compact)
        container.addWidget(self.switch_1, spacing=16)

        self.switch_2 = ZSwitch(container, name='switch_2', style= ZSwitch.Style.Standard)
        container.addWidget(self.switch_2, spacing=16)

        self.switch_3 = ZSwitch(container, name='switch_3', style= ZSwitch.Style.Comfortable)
        container.addWidget(self.switch_3, spacing=16)

        # region ZReapeatButton
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZReapeatButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        info = ZTextBlock(container, text= '点击次数: 0')
        container.addWidget(info)

        self.repeat_btn = ZRepeatButton(
            parent=container,
            name='repeat_btn_1',
            text='连点按钮'
            )

        container.addWidget(self.repeat_btn)
        self.repeat_btn.clicked.connect(
            lambda: info.setText(f'点击次数: {self.repeat_btn.repeatCount()}')
            )

        # region ZComboBox
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZComboBox')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.combo_box_1 = ZComboBox(
            text='请选择你的英雄',
            options=['牢大', '坤坤', '凡凡'],
            parent=container,
            name='combo_box_1')
        self.combo_box_1.addItem('马嘉祺')
        self.combo_box_1.addItem('丁程鑫')
        container.addWidget(self.combo_box_1)

        # region ZLineEdit
        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        self.layout().addLayout(layout)

        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZLineEdit')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.lineedit_1 = ZLineEdit(
            parent=container,
            name='lineedit_1',
            text='唱、跳、rap、篮球',
            read_only=True,
            selectable=False,
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_1)

        self.lineedit_2 = ZLineEdit(
            parent=container,
            name='lineedit_2',
             text='孩子，这并不好笑',
            read_only=True,
            selectable=True,
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_2)

        self.lineedit_3 = ZLineEdit(
            parent=container,
            name='lineedit_3',
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_3)

        self.lineedit_4 = ZLineEdit(
            parent=container,
            name='lineedit_4',
            placeholder='请输入你的名字',
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_4)

        # region Slider
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZTextBlock(card, text= 'ZSlider')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        hlayout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=16,
            alignment=Qt.AlignLeft|Qt.AlignTop
            )
        card.layout().addLayout(hlayout)

        container1 = ZVContainer(card)
        container1.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter)
        container1.setDefaultSpacing(16)
        hlayout.layout().addWidget(container1)

        self.hslider_1 = ZSlider(
            parent=container1,
            name='hslider_1',
            direction=ZDirection.Horizontal,
            style=ZSlider.Style.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=5
            )
        self.hslider_1.setFixedLength(200)
        container1.addWidget(self.hslider_1)

        self.hslider_2 = ZSlider(
            parent=container1,
            name='hslider_2',
            direction=ZDirection.Horizontal,
            style=ZSlider.Style.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=50
            )
        self.hslider_2.setFixedLength(200)
        container1.addWidget(self.hslider_2)

        self.hslider_3 = ZSlider(
            parent=container1,
            name='hslider_3',
            direction=ZDirection.Horizontal,
            style=ZSlider.Style.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50,
            auto_strip_zero=True
            )
        self.hslider_3.setFixedLength(200)
        container1.addWidget(self.hslider_3)
        container1.arrangeWidgets()

        container2 = ZHContainer(card)
        container2.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter)
        container2.setDefaultSpacing(16)
        hlayout.layout().addWidget(container2)

        self.vslider_1 = ZSlider(
            parent=container2,
            name='vslider_1',
            direction=ZDirection.Vertical,
            style=ZSlider.Style.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=5
            )
        self.vslider_1.setFixedLength(150)
        container2.addWidget(self.vslider_1)

        self.vslider_2 = ZSlider(
            parent=container2,
            name='vslider_2',
            direction=ZDirection.Vertical,
            style=ZSlider.Style.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=50
            )
        self.vslider_2.setFixedLength(150)
        container2.addWidget(self.vslider_2)

        self.vslider_3 = ZSlider(
            parent=container2,
            name='vslider_3',
            direction=ZDirection.Vertical,
            style=ZSlider.Style.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50
            )
        self.vslider_3.setFixedLength(150)
        container2.addWidget(self.vslider_3)
        container2.arrangeWidgets()


        # region Text
        title = ZTextBlock(self, text= '文本显示组件')
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.margins = QMargins(6, 6, 6, 6)
        self.layout().addWidget(title)

        card = DemoCard(self)
        self.layout().addWidget(card)

        title = ZTextBlock(card, text= 'ZTextBlock')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.text_block_1 = ZTextBlock(container, name='text_block_1')
        self.text_block_1.margins = QMargins(6, 0, 6, 0)
        self.text_block_1.wrapMode = ZWrapMode.NoWrap
        self.text_block_1.text = (
            "PySide6 是 Qt 官方提供的 Python 模块，"
            "它允许开发者使用 Python 编写跨平台 GUI 应用程序，"
            "并提供了完整的 Qt 6.0+ 框架支持。"
        )
        container.addWidget(self.text_block_1)

        self.text_block_2 = ZTextBlock(container, name='text_block_2',selectable=True)
        self.text_block_2.margins = QMargins(6, 6, 6, 6)
        self.text_block_2.wrapMode = ZWrapMode.NoWrap
        self.text_block_2.text = (
            "PySide6 是 Qt 官方提供的 Python 模块，"
            "它允许开发者使用 Python 编写跨平台 GUI 应用程序，"
            "并提供了完整的 Qt 6.0+ 框架支持。"
        )
        container.addWidget(self.text_block_2)

        self.text_block_3 = ZTextBlock(container, name='text_block_3',selectable=True)
        self.text_block_3.setMaximumWidth(400)
        self.text_block_3.margins = QMargins(6, 6, 6, 6)
        self.text_block_3.wrapMode = ZWrapMode.WordWrap
        self.text_block_3.text = (
            "PySide6 是 Qt 官方提供的 Python 模块，"
            "它允许开发者使用 Python 编写跨平台 GUI 应用程序，"
            "并提供了完整的 Qt 6.0+ 框架支持。"
        )
        container.addWidget(self.text_block_3)

        self.text_block_4 = ZTextBlock(container, name='text_block_4',selectable=True)
        self.text_block_4.setMaximumWidth(400)
        self.text_block_4.margins = QMargins(6, 6, 6, 6)
        self.text_block_4.wrapMode = ZWrapMode.WrapAnywhere
        self.text_block_4.text = (
            "PySide6 是 Qt 官方提供的 Python 模块，"
            "它允许开发者使用 Python 编写跨平台 GUI 应用程序，"
            "并提供了完整的 Qt 6.0+ 框架支持。"
        )
        container.addWidget(self.text_block_4)


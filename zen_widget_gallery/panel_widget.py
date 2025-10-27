from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt, QMargins,QPoint,QSize
from PySide6.QtGui import QFont, QIcon, QColor
from ZenWidgets import *
from demo_card import DemoCard

class PanelWidget(ZScrollPanel):
    def __init__(self,parent = None,name ='PanelWidget'):
        super().__init__(parent, name)
        self.setLayout(ZVBoxLayout(self, QMargins(40, 30, 40, 30), 30, Qt.AlignmentFlag.AlignTop))
        self._setup_ui()

    def _setup_ui(self):
        title = ZHeadLine(self, text='基础组件', display_indicator=True)
        title.setFont(QFont('Microsoft YaHei', 20, QFont.Weight.Bold))
        title.setPadding(ZPadding(6, 6, 6, 6))
        self.layout().addWidget(title)

        # region ZButton
        title = ZHeadLine(self, text= '基本输入组件', display_indicator=True)
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.setPadding(ZPadding(6, 6, 6, 6))
        self.layout().addWidget(title)

        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        self.layout().addLayout(layout)

        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        btn_icon = ZGlobal.iconPack.toIcon('ic_fluent_save_regular')
        self.btn_1 = ZButton(container, icon=btn_icon)
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

        self.btn_2 = ZButton(container, icon=btn_icon, text='保存')
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
        self.btn_3 = ZButton(container, text='保存')
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

        self.btn_4 = ZButton(container, text='保存', style=ZButton.Style.Flat)
        container.addWidget(self.btn_4, spacing=16)
        self.btn_4.clicked.connect(
            lambda: ZGlobal.tooltip.showTip(
                text='保存成功',
                target=self.btn_4,
                mode=ZToolTip.Mode.TrackTarget,
                position=ZPosition.Top,
                offset=QPoint(0, 6),
                hide_delay=800
                )
            )
        # region ZToggleButton
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZToggleButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        self.toggle_btn_1 = ZToggleButton(container, icon=btn_icon)
        self.toggle_btn_1.setToolTip('自动保存')
        container.addWidget(self.toggle_btn_1, spacing=16)

        self.toggle_btn_2 = ZToggleButton(container, icon=btn_icon, text='自动保存')
        container.addWidget(self.toggle_btn_2, spacing=16)

        self.toggle_btn_3 = ZToggleButton(container, text='自动保存')
        container.addWidget(self.toggle_btn_3, spacing=16)

        self.toggle_btn_4 = ZToggleButton(container, text='自动保存', style=ZToggleButton.Style.Flat)
        container.addWidget(self.toggle_btn_4, spacing=16)


        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        self.layout().addLayout(layout)

        # region ZSwitch
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZSwitch')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        container.setAlignment(Qt.AlignmentFlag.AlignBottom)
        card.layout().addWidget(container)

        self.switch_1 = ZSwitch(container, style= ZSwitch.Style.Compact)
        container.addWidget(self.switch_1, spacing=16)

        self.switch_2 = ZSwitch(container, style= ZSwitch.Style.Standard)
        container.addWidget(self.switch_2, spacing=16)

        self.switch_3 = ZSwitch(container, style= ZSwitch.Style.Comfortable)
        container.addWidget(self.switch_3, spacing=16)

        # region ZReapeatButton
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZReapeatButton')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        info = ZHeadLine(container, text= '点击次数: 0')
        container.addWidget(info)

        self.repeat_btn = ZRepeatButton(container, text='连点按钮')

        container.addWidget(self.repeat_btn)
        self.repeat_btn.clicked.connect(
            lambda: info.setText(f'点击次数: {self.repeat_btn.repeatCount()}')
            )

        # region ZComboBox
        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZComboBox')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        options = ['坤坤', '凡凡', '祺祺', '鑫鑫']
        self.combo_box_1 = ZComboBox(self, text='请选择')
        for option in options:
            self.combo_box_1.addOption(option)
        container.addWidget(self.combo_box_1)

        # region ZLineEdit
        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )

        self.layout().addLayout(layout)

        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        card.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        title = ZHeadLine(card, text= 'ZLineEdit')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.lineedit_1 = ZLineEdit(
            parent=container,
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_1)

        self.lineedit_2 = ZLineEdit(
            parent=container,
            placeholder='带有提示文字的编辑框',
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_2)

        self.lineedit_3 = ZLineEdit(
            parent=container,
            text='不能修改的编辑框',
            read_only=True,
            selectable=False,
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_3)

        self.lineedit_4 = ZLineEdit(
            parent=container,
            text='不能修改但可以选中编辑框',
            read_only=True,
            selectable=True,
            minimumSize=QSize(300, 30)
        )
        container.addWidget(self.lineedit_4)

        # region ZLoginEdit
        vlayout = ZVBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        layout.addLayout(vlayout)

        card = DemoCard(self)
        vlayout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZLoginEdit')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)

        self.login_edit_1 = ZLoginEdit(card, allow_characters=False)
        container.addWidget(self.login_edit_1)

        self.login_edit_2 = ZLoginEdit(card, is_masked=True)
        container.addWidget(self.login_edit_2)
        # region ZNumberEdit
        card = DemoCard(self)
        vlayout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZNumberEdit')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZVContainer(card)
        card.layout().addWidget(container)
        self.number_edit_1 = ZNumberEdit(card)
        container.addWidget(self.number_edit_1)

        self.number_edit_2 = ZNumberEdit(card, allow_negative=True, allow_decimal=True)
        container.addWidget(self.number_edit_2)

        # region ZSlider
        layout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=30
            )
        self.layout().addLayout(layout)

        card = DemoCard(self)
        layout.addWidget(card, stretch=0)

        title = ZHeadLine(card, text= 'ZSlider')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        hlayout = ZHBoxLayout(
            margins=QMargins(0, 0, 0, 0),
            spacing=16,
            alignment=Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter
            )
        card.layout().addLayout(hlayout)

        container1 = ZVContainer(card)
        container1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container1.setDefaultSpacing(16)
        hlayout.layout().addWidget(container1)

        self.hslider_1 = ZSlider(
            parent=container1,
            direction=ZDirection.Horizontal,
            style=ZSlider.Style.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=5,
            length=300
            )
        container1.addWidget(self.hslider_1)

        self.hslider_2 = ZSlider(
            parent=container1,
            direction=ZDirection.Horizontal,
            style=ZSlider.Style.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=50,
            length=300
            )
        container1.addWidget(self.hslider_2)

        self.hslider_3 = ZSlider(
            parent=container1,
            direction=ZDirection.Horizontal,
            style=ZSlider.Style.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50,
            auto_strip_zero=True,
            length=300
            )
        container1.addWidget(self.hslider_3)

        container2 = ZHContainer(card)
        container2.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter)
        container2.setDefaultSpacing(16)
        hlayout.layout().addWidget(container2)

        self.vslider_1 = ZSlider(
            parent=container2,
            direction=ZDirection.Vertical,
            style=ZSlider.Style.Thin,
            scope=(0, 10),
            step=0.5,
            accuracy=0.1,
            value=5
            )
        container2.addWidget(self.vslider_1)

        self.vslider_2 = ZSlider(
            parent=container2,
            direction=ZDirection.Vertical,
            style=ZSlider.Style.Normal,
            scope=(0, 100),
            step=1,
            accuracy=1,
            value=50
            )
        container2.addWidget(self.vslider_2)

        self.vslider_3 = ZSlider(
            parent=container2,
            direction=ZDirection.Vertical,
            style=ZSlider.Style.Thick,
            scope=(0, 100),
            step=0.5,
            accuracy=0.1,
            value=50
            )
        container2.addWidget(self.vslider_3)


        # region Text
        title = ZHeadLine(self, text= '文本显示组件', display_indicator=True)
        title.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        title.setPadding(ZPadding(6, 6, 6, 6))
        self.layout().addWidget(title)

        card = DemoCard(self)
        self.layout().addWidget(card)

        title = ZHeadLine(card, text= 'ZHeadLine')
        title.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        card.layout().addWidget(title)

        container = ZHContainer(card)
        card.layout().addWidget(container)

        self.headline_1 = ZHeadLine(container)
        self.headline_1.setText('标题')
        container.addWidget(self.headline_1)

        self.headline_2 = ZHeadLine(container, display_indicator=True)
        self.headline_2.setText('带指示器的标题')
        container.addWidget(self.headline_2)

        self.headline_3 = ZHeadLine(container, selectable=True)
        self.headline_3.setText('可选中的标题')
        container.addWidget(self.headline_3)


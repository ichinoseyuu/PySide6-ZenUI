from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.button.pushbutton import ZPushButton
from ZenUI.component.label.text_label import ZTextLabel
from ZenUI.component.layout.spacer import ZSpacer
from ZenUI.component.layout.row import ZRowLayout
from ZenUI.core import Zen,ZenGlobal,ZSize


class ThemeButton(ZPushButton):
    def _init_style(self):
        super()._init_style()
        self.setCheckable(True)
        icon = QIcon()
        if ZenGlobal.ui.theme_manager.theme() == Zen.Theme.Dark:
            icon.addFile(u":/icons/svg/fluent/filled/ic_fluent_weather_sunny_filled.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            icon.addFile(u":/icons/svg/fluent/filled/ic_fluent_weather_moon_filled.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
            self._tooltip = '切换到浅色模式'
        else:
            icon.addFile(u":/icons/svg/fluent/filled/ic_fluent_weather_sunny_filled.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            icon.addFile(u":/icons/svg/fluent/filled/ic_fluent_weather_moon_filled.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
            self._tooltip = '切换到深色模式'
        self.setIcon(icon)

    def _theme_changed_handler(self, theme):
        super()._theme_changed_handler(theme)
        self.hovered.emit()
        if theme == Zen.Theme.Dark:
            self._tooltip = '切换到浅色模式'
            ZenGlobal.ui.windows['ToolTip'].setText(self._tooltip)
        else:
            self._tooltip = '切换到深色模式'
            ZenGlobal.ui.windows['ToolTip'].setText(self._tooltip)


class ZTitlebar(QWidget):
    '''标题栏'''
    def __init__(self, parent, window_shadow:int):
        super().__init__(parent)
        self.setObjectName("Titlebar")
        self._btn_size = ZSize(48, 36)
        self._window_shadow = window_shadow
        self._setup_ui()
        self._btnConnect()

    def _setup_ui(self):
        """创建ui"""
        self.setMinimumHeight(ZenGlobal.config.TITLEBAR_HEIGHT)
        self.setMaximumHeight(ZenGlobal.config.TITLEBAR_HEIGHT)
        self._layout = ZRowLayout(self)
        self.setLayout(self._layout)

        self.icon = ZTextLabel(parent=self,
                                 name="icon")
        self._layout.addWidget(self.icon)

        self.title = ZTextLabel(parent=self,
                                  name="title") # 标题
        self._layout.addWidget(self.title)

        self.spacer = ZSpacer()
        self._layout.addItem(self.spacer)

        self.btnTheme = ThemeButton(parent=self,
                                    name="btnTheme",
                                    fixed_size=self._btn_size,
                                    idle_style=ZPushButton.IdleStyle.None_,
                                    hover_style=ZPushButton.HoverStyle.Icon,
                                    pressed_style=ZPushButton.PressedStyle.None_)
        self._layout.addWidget(self.btnTheme)

        self.btnMin = ZPushButton(parent=self,
                                    name="btnMin",
                                    icon=QIcon(u":/icons/svg/zen_ui/minimize.svg"),
                                    fixed_size=self._btn_size,
                                    idle_style=ZPushButton.IdleStyle.None_,
                                    hover_style=ZPushButton.HoverStyle.Icon,
                                    pressed_style=ZPushButton.PressedStyle.None_)
        self._layout.addWidget(self.btnMin)

        icon2 = QIcon()
        icon2.addFile(u":/icons/svg/zen_ui/maximize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/svg/zen_ui/windowed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.btnMax = ZPushButton(parent=self,
                                    name="btnMin",
                                    icon=icon2,
                                    fixed_size=self._btn_size,
                                    idle_style=ZPushButton.IdleStyle.None_,
                                    hover_style=ZPushButton.HoverStyle.Icon,
                                    pressed_style=ZPushButton.PressedStyle.None_)
        self.btnMax.setCheckable(True)
        self._layout.addWidget(self.btnMax)

        self.btnExit = ZPushButton(parent=self,
                                    name="btnMin",
                                    icon=QIcon(u":/icons/svg/zen_ui/close.svg"),
                                    fixed_size=self._btn_size,
                                    idle_style=ZPushButton.IdleStyle.None_,
                                    hover_style=ZPushButton.HoverStyle.Icon,
                                    pressed_style=ZPushButton.PressedStyle.None_)
        self._layout.addWidget(self.btnExit)


    def _btnConnect(self):
        '''按钮连接'''
        self.btnTheme.clicked.connect(self._changeTheme)
        self.btnMin.clicked.connect(self.window().showMinimized)
        self.btnMax.clicked.connect(self._maxWindow)
        self.btnExit.clicked.connect(self.window().close)

    def _changeTheme(self):
        '切换主题'
        if ZenGlobal.ui.theme_manager.theme() == Zen.Theme.Dark:
            ZenGlobal.ui.theme_manager.setTheme(Zen.Theme.Light)
        else:
            ZenGlobal.ui.theme_manager.setTheme(Zen.Theme.Dark)

    def _maxWindow(self):
        '''最大化窗口'''
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
        self.btnMax.leaved.emit()


    def setTitle(self, title: str):
        '''设置标题'''
        self.title.setText(title)


    def setTitleIcon(self, icon: QPixmap|str):
        '''设置标题栏图标'''
        if isinstance(icon, str):
            self.icon.setPixmap(QPixmap(icon))
        else:
            self.icon.setPixmap(QPixmap(u":/images/icon/icon.png"))


    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() != Qt.LeftButton:
            return
        self.btnMax.click()


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and not self.window().isMaximized():
            # 直接使用窗口位置计算偏移
            window = self.window()
            offset = QPoint(self._window_shadow, self._window_shadow)
            self.dragPosition = event.globalPosition().toPoint() - window.pos() - offset
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and not self.window().isMaximized():
            window = self.window()
            # 使用相同的参考点计算新位置
            window.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()
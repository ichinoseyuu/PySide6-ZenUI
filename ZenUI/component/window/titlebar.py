from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ZenUI.core import ZenGlobal
from ZenUI.component.window.abctitlebar import ABCTitlebar
class ZenTitlebar(ABCTitlebar):
    '''ZenUI标题栏'''
    # region Override
    def _setup_ui(self):
        super()._setup_ui()
        # 设置标题栏高度
        self.setMinimumHeight(ZenGlobal.config.TITLEBAR_HEIGHT)
        self.setMaximumHeight(ZenGlobal.config.TITLEBAR_HEIGHT)

        # 设置图标
        self.icon.setMinimumSize(QSize(24, 24))
        self.icon.setMaximumSize(QSize(24, 24))
        self.icon.setScaledContents(True)

        # 切换主题按钮
        self.btnTheme.setMinimumSize(QSize(36, 36))
        self.btnTheme.setMaximumSize(QSize(36, 36))
        icon = QIcon(u":/titlebar/icon/theme.svg")
        self.btnTheme.setIcon(icon)
        self.btnTheme.setIconSize(QSize(36,36))

        # 最小化按钮
        self.btnMin.setMinimumSize(QSize(36, 36))
        self.btnMin.setMaximumSize(QSize(36, 36))
        icon = QIcon(u":/titlebar/icon/minimize.svg")
        self.btnMin.setIcon(icon)
        self.btnMin.setIconSize(QSize(36,36))

        # 最大化按钮
        self.btnMax.setMinimumSize(QSize(36, 36))
        self.btnMax.setMaximumSize(QSize(36, 36))
        icon1 = QIcon()
        icon1.addFile(u":/titlebar/icon/maximize.svg", QSize(24, 24), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/titlebar/icon/windowed.svg", QSize(24, 24), QIcon.Mode.Normal, QIcon.State.On)
        self.btnMax.setIcon(icon1)
        self.btnMax.setIconSize(QSize(36, 36))


        # 关闭按钮
        self.btnExit.setMinimumSize(QSize(36, 36))
        self.btnExit.setMaximumSize(QSize(36, 36))
        icon = QIcon(u":/titlebar/icon/close.svg",)
        self.btnExit.setIcon(icon)
        self.btnExit.setIconSize(QSize(36,36))

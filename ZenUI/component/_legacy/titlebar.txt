from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ZenUI.core import ZenGlobal
from ZenUI.component.window.abctitlebar import ABCTitlebar
class ZenTitlebar(ABCTitlebar):
    '''标题栏'''
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
        icon1 = QIcon()
        icon1.addFile(u":/icons/zen_ui/light.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/zen_ui/dark.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        #icon = QIcon(u":/titlebar/icon/theme.svg")
        self.btnTheme.setIcon(icon1)

        # 最小化按钮
        self.btnMin.setMinimumSize(QSize(36, 36))
        self.btnMin.setMaximumSize(QSize(36, 36))
        icon = QIcon(u":/icons/zen_ui/minimize.svg")
        self.btnMin.setIcon(icon)

        # 最大化按钮
        self.btnMax.setMinimumSize(QSize(36, 36))
        self.btnMax.setMaximumSize(QSize(36, 36))
        icon2 = QIcon()
        icon2.addFile(u":/icons/zen_ui/maximize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/zen_ui/windowed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.btnMax.setIcon(icon2)


        # 关闭按钮
        self.btnExit.setMinimumSize(QSize(36, 36))
        self.btnExit.setMaximumSize(QSize(36, 36))
        icon = QIcon(u":/icons/zen_ui/close.svg")
        self.btnExit.setIcon(icon)

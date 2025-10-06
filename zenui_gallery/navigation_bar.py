from PySide6.QtCore import Qt,QSize,QPoint
from PySide6.QtGui import QIcon
from ZenUI import *

class NavigationBar(ZNavigationBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setup_ui()
        self.resize(self.sizeHint())
    def _setup_ui(self):
        iconPack = ZGlobal.iconPack
        icon1 = QIcon()
        icon1.addPixmap(iconPack.toPixmap("ic_fluent_home_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addPixmap(iconPack.toPixmap("ic_fluent_home_filled"), QIcon.Mode.Normal, QIcon.State.On)
        # icon1.addFile(u":/icons/fluent/regular/ic_fluent_home_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        # icon1.addFile(u":/icons/fluent/filled/ic_fluent_home_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnHome = ZNavBarToggleButton(icon1, self, "btnHome")
        self.btnHome.setToolTip("主页")
        self.addToggleButton(self.panel, self.btnHome)

        icon2 = QIcon()
        icon2.addPixmap(iconPack.toPixmap("ic_fluent_cube_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addPixmap(iconPack.toPixmap("ic_fluent_cube_filled"), QIcon.Mode.Normal, QIcon.State.On)
        # icon2.addFile(u":/icons/fluent/regular/ic_fluent_cube_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        # icon2.addFile(u":/icons/fluent/filled/ic_fluent_cube_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnWidget = ZNavBarToggleButton(icon2, self, "btnWidget", )
        self.btnWidget.setToolTip("基础组件")
        self.addToggleButton(self.panel, self.btnWidget)

        icon3 = QIcon()
        icon3.addPixmap(iconPack.toPixmap("ic_fluent_window_edit_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addPixmap(iconPack.toPixmap("ic_fluent_window_edit_filled"), QIcon.Mode.Normal, QIcon.State.On)
        # icon3.addFile(u":/icons/fluent/regular/ic_fluent_window_edit_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        # icon3.addFile(u":/icons/fluent/filled/ic_fluent_window_edit_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnTest = ZNavBarToggleButton(icon3, self, "btnTest")
        self.btnTest.setToolTip("测试组件")
        self.addToggleButton(self.panel, self.btnTest)

        icon4 = QIcon()
        icon4.addPixmap(iconPack.toPixmap("ic_fluent_comment_multiple_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addPixmap(iconPack.toPixmap("ic_fluent_comment_multiple_filled"), QIcon.Mode.Normal, QIcon.State.On)
        # icon4.addFile(u":/icons/fluent/regular/ic_fluent_comment_multiple_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        # icon4.addFile(u":/icons/fluent/filled/ic_fluent_comment_multiple_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnInfo = ZNavBarToggleButton(icon4, self, "btnInfo")
        self.btnInfo.setToolTip("状态与信息")
        self.addToggleButton(self.panel, self.btnInfo)

        icon5 = QIcon()
        icon5.addPixmap(iconPack.toPixmap("ic_fluent_info_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon5.addPixmap(iconPack.toPixmap("ic_fluent_info_filled"), QIcon.Mode.Normal, QIcon.State.On)
        # icon5.addFile(u":/icons/fluent/regular/ic_fluent_info_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        # icon5.addFile(u":/icons/fluent/filled/ic_fluent_info_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnAbout = ZNavBarToggleButton(icon5, self, "btnAbout")
        self.btnAbout.setToolTip("关于")
        self.addToggleButton(self.panel, self.btnAbout)

        icon6 = QIcon()
        icon6.addPixmap(iconPack.toPixmap("ic_fluent_settings_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon6.addPixmap(iconPack.toPixmap("ic_fluent_settings_filled"), QIcon.Mode.Normal, QIcon.State.On)
        # icon6.addFile(u":/icons/fluent/regular/ic_fluent_settings_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        # icon6.addFile(u":/icons/fluent/filled/ic_fluent_settings_filled.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.On)
        self.btnSettings = ZNavBarToggleButton(icon6, self, "btnSettings")
        self.btnSettings.setToolTip("设置")
        self.addToggleButton(self.footerPanel, self.btnSettings)

        #icon7 = QIcon()
        #icon6.addFile(u":/icons/fluent/regular/ic_fluent_bug_regular.svg", QSize(26,26), QIcon.Mode.Normal, QIcon.State.Off)
        icon7 = iconPack.toIcon("ic_fluent_bug_regular")
        self.btnDebug = ZNavBarButton(icon7, self, "btnDebug")
        self.btnDebug.setToolTip("调试模式")
        self.insertButton(self.footerPanel, 0, self.btnDebug)
        def _debug():
            ZDebug.draw_rect = not ZDebug.draw_rect
            self.window().repaint()
            ZGlobal.themeManager.updateStyle()
            ZGlobal.tooltip.showTip(text=f"调试模式{'已打开'if ZDebug.draw_rect else '已关闭'}",
                                    mode=ZToolTip.Mode.TrackTarget,
                                    target=self.btnDebug,
                                    position=ZPosition.Right,
                                    offset = QPoint(10, 0)
                                    )
        self.btnDebug.clicked.connect(_debug)

from PySide6.QtCore import Qt,QSize,QPoint
from PySide6.QtGui import QIcon
from ZenWidgets import *

class NavigationBar(ZNavigationBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setup_ui()

    def _setup_ui(self):
        iconPack = ZGlobal.iconPack
        icon1 = QIcon()
        icon1.addPixmap(iconPack.toPixmap("ic_fluent_home_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addPixmap(iconPack.toPixmap("ic_fluent_home_filled"), QIcon.Mode.Normal, QIcon.State.On)
        self.addToggleButton(name="btnHome", icon=icon1, tooltip="主页", panel=self.panel)


        icon2 = QIcon()
        icon2.addPixmap(iconPack.toPixmap("ic_fluent_cube_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addPixmap(iconPack.toPixmap("ic_fluent_cube_filled"), QIcon.Mode.Normal, QIcon.State.On)
        self.addToggleButton(name="btnWidget", icon=icon2, tooltip="组件", panel=self.panel)

        icon3 = QIcon()
        icon3.addPixmap(iconPack.toPixmap("ic_fluent_window_edit_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addPixmap(iconPack.toPixmap("ic_fluent_window_edit_filled"), QIcon.Mode.Normal, QIcon.State.On)
        self.addToggleButton(name="btnTest", icon=icon3, tooltip="测试", panel=self.panel)

        icon4 = QIcon()
        icon4.addPixmap(iconPack.toPixmap("ic_fluent_comment_multiple_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addPixmap(iconPack.toPixmap("ic_fluent_comment_multiple_filled"), QIcon.Mode.Normal, QIcon.State.On)
        self.addToggleButton(name="btnInfo", icon=icon4, tooltip="状态与信息", panel=self.panel)


        icon5 = QIcon()
        icon5.addPixmap(iconPack.toPixmap("ic_fluent_info_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon5.addPixmap(iconPack.toPixmap("ic_fluent_info_filled"), QIcon.Mode.Normal, QIcon.State.On)
        self.addToggleButton(name="btnAbout", icon=icon5, tooltip="关于", panel=self.panel)

        icon6 = QIcon()
        icon6.addPixmap(iconPack.toPixmap("ic_fluent_settings_regular"), QIcon.Mode.Normal, QIcon.State.Off)
        icon6.addPixmap(iconPack.toPixmap("ic_fluent_settings_filled"), QIcon.Mode.Normal, QIcon.State.On)
        self.addToggleButton(name="btnSettings", icon=icon6, tooltip="设置", panel=self.footerPanel)

        icon7 = iconPack.toIcon("ic_fluent_bug_regular")
        self.insertButton(name="btnDebug", icon=icon7, index=0, tooltip="调试模式", panel=self.footerPanel)
        btn = self.getButton("btnDebug")
        def _debug():
            ZDebug.draw_rect = not ZDebug.draw_rect
            self.window().repaint()
            ZGlobal.themeManager.updateStyle()
            ZGlobal.tooltip.showTip(text=f"调试模式{'已打开'if ZDebug.draw_rect else '已关闭'}",
                                    mode=ZToolTip.Mode.TrackTarget,
                                    target=btn,
                                    position=ZPosition.Right,
                                    offset = QPoint(10, 0)
                                    )
        btn.clicked.connect(_debug)


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ZenUI.component.tooltip import ZToolTip
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from ZenUI.core.debug import ZDebug
from ZenUI.core.enumrate import ZWindowType
from ZenUI.core.resource import GlobalIconPack
from ZenUI.core.theme import ZThemeManager
from ZenUI.core.styledata import ZStyleDataManager

class ZGlobal:
    ZDebug._init_logging_()
    tooltip: 'ZToolTip' = None
    themeManager = ZThemeManager()
    styleDataManager = ZStyleDataManager()
    iconPack = GlobalIconPack()

    @staticmethod
    def getBuiltinIcon(icon_path: str) -> QIcon:
        """获取内置资源中的图标"""
        return QIcon(icon_path)

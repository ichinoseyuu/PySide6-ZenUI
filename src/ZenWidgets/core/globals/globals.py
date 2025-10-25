from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ZenWidgets.component.tooltip import ZToolTip
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from ZenWidgets.core.debug import ZDebug
from ZenWidgets.core.enumrate import ZWindowType
from ZenWidgets.core.resource import GlobalIconPack
from ZenWidgets.core.theme import ZThemeManager
from ZenWidgets.core.styledata import ZStyleDataManager

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

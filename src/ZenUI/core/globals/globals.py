import logging
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ZenUI.component.tooltip import ZToolTip
from PySide6.QtGui import QPainter, QPen,QIcon
from PySide6.QtCore import Qt, QRect
from ..theme import ZThemeManager
from ..styledata import ZStyleDataManager
from ..resource import *

def configureLogging():
    """
    同时将日志输出到终端和文件。
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "- %(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])",
        "%Y-%m-%d %H:%M:%S"
    )

    # 文件日志
    file_handler = logging.FileHandler("zenui.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 终端日志
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

class ZGlobal:
    configureLogging()
    tooltip: 'ZToolTip' = None
    themeManager = ZThemeManager()
    styleDataManager = ZStyleDataManager()
    iconPack = GlobalIconPack()

    @staticmethod
    def getBuiltinIcon(icon_path: str) -> QIcon:
        """获取内置资源中的图标"""
        return QIcon(icon_path)

class ZDebug:
    draw_rect = False

    @staticmethod
    def drawRect(painter:QPainter, rect: QRect):
        painter.setOpacity(0.8)
        painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect)
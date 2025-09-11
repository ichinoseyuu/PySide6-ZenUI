import logging
from enum import Enum,IntEnum,Flag,IntFlag,auto
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ZenUI.component.tooltip import ZToolTip
from PySide6.QtGui import QPainter, QPen, QResizeEvent,QColor
from PySide6.QtCore import Qt, QRect 
from PySide6.QtWidgets import QWidget
from ..theme import ZThemeManager
from ..styledata import ZStyleDataManager
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

class TipPos(IntEnum):
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3
    TopLeft = 4
    TopRight = 5
    BottomLeft = 6
    BottomRight = 7

class ZGlobal:
    configureLogging()
    tooltip: 'ZToolTip' = None
    themeManager = ZThemeManager()
    styleDataManager = ZStyleDataManager()

class ZDebug:
    draw_rect = False

    @staticmethod
    def drawRect(painter:QPainter, rect: QRect):
        painter.setOpacity(0.8)
        painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect)
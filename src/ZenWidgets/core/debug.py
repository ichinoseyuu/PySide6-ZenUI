import logging
from PySide6.QtGui import QPainter, QPen,QIcon,QColor
from PySide6.QtCore import Qt, QRect

__All__ = ['ZDebug']

class ZDebug:
    draw_rect = False

    @staticmethod
    def drawRect(painter:QPainter,
                 rect: QRect,
                 color: QColor | Qt.GlobalColor = Qt.GlobalColor.red,
                 alpha: float = 0.8,
                 width: float = 1.0,
                 penStyle: Qt.PenStyle = Qt.PenStyle.SolidLine,
                 penCapStyle: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap,
                 penJoinStyle: Qt.PenJoinStyle = Qt.PenJoinStyle.RoundJoin
                 ):
        painter.save()
        painter.setOpacity(alpha)
        painter.setPen(QPen(color, width, penStyle, penCapStyle, penJoinStyle))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(rect)
        painter.restore()

    @staticmethod
    def disableLogging():
        """禁用所有日志输出"""
        logger = logging.getLogger()
        logger.setLevel(logging.CRITICAL + 1)

    @staticmethod
    def enableLogging():
        """启用所有日志输出"""
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    @staticmethod
    def toggleLogging():
        """启用或禁用所有日志输出"""
        logger = logging.getLogger()
        if logger.level == logging.CRITICAL + 1:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.CRITICAL + 1)

    @staticmethod
    def enableLogging():
        """启用所有日志输出"""
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    @staticmethod
    def _init_logging_():
        log_formatter = logging.Formatter(
            "-%(asctime)s [%(filename)s:%(lineno)d]-%(levelname)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
            )
        logging.basicConfig(
            level=logging.INFO,
            format=log_formatter._fmt,
            datefmt=log_formatter.datefmt,
            filemode="w",
            encoding="utf-8",
            filename='zen.log'
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        logging.getLogger().addHandler(stream_handler)

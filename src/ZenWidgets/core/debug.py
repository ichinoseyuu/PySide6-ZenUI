import logging
from PySide6.QtGui import QPainter, QPen,QIcon
from PySide6.QtCore import Qt, QRect

__All__ = ['ZDebug']

class ZDebug:
    draw_rect = False

    @staticmethod
    def drawRect(painter:QPainter, rect: QRect):
        painter.setOpacity(0.8)
        painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect)

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

import logging
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

class ZGlobal:
    configureLogging()
    tooltip = None
    themeManager = ZThemeManager()
    styleDataManager = ZStyleDataManager()





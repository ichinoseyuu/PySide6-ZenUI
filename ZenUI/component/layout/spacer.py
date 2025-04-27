from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.core import Zen

class ZenSpacer(QSpacerItem):
    '''布局中的空白区域，占位用'''
    def __init__(self,
                 minW: int = 0,
                 minH: int = 0,
                 row: Zen.SizePolicy = Zen.SizePolicy.Expanding,
                 columns: Zen.SizePolicy = Zen.SizePolicy.Expanding):
        super().__init__(minW, minH, row.value, columns.value)
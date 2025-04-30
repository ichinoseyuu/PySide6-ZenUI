from PySide6.QtWidgets import QSpacerItem
from ZenUI.core import Zen

class ZSpacer(QSpacerItem):
    '''占位布局'''
    def __init__(self,
                 minW: int = 0,
                 minH: int = 0,
                 row: Zen.SizePolicy = Zen.SizePolicy.Expanding,
                 columns: Zen.SizePolicy = Zen.SizePolicy.Expanding):
        super().__init__(minW, minH, row.value, columns.value)
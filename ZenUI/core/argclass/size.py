from PySide6.QtCore import QSize
from dataclasses import dataclass

@dataclass
class ZenSize:
    '''尺寸'''
    width: int = 0
    height: int = 0

    def toQsize(self):
        '''转换成QSize'''
        return QSize(self.width, self.height)
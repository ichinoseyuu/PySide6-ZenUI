from PySide6.QtCore import QSize
from dataclasses import dataclass

@dataclass
class ZenSize:
    '''内边距
    Attributes:
        width: int = 0
        height: int = 0
    '''
    width: int = 0
    height: int = 0

    def toQSize(self):
        '''转换成QSize'''
        return QSize(self.width, self.height)
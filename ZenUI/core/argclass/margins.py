from PySide6.QtCore import QMargins
from dataclasses import dataclass

@dataclass
class ZenMargins:
    '''内边距'''
    top: int = 0
    left: int = 0
    right: int = 0
    bottom: int = 0

    def toQmargins(self):
        '''转换为QMargins'''
        return QMargins(self.left, self.top, self.right, self.bottom)
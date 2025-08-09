from PySide6.QtCore import QPoint,QPointF
from dataclasses import dataclass

@dataclass
class ZPoint:
    '''点坐标'''
    x: int = 0
    y: int = 0

    def toQpoint(self):
        '''转换成QPoint'''
        return QPoint(self.x, self.y)

    def toQpointF(self):
        '''转换成QPointF'''
        return QPointF(float(self.x), float(self.y))

@dataclass
class ZPointF:
    '''点坐标'''
    x: float = 0.0
    y: float = 0.0

    def toQpoint(self):
        '''转换成QPoint'''
        return QPoint(int(self.x), int(self.y))

    def toQpointF(self):
        '''转换成QPointF'''
        return QPointF(self.x, self.y)
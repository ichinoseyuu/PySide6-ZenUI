from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QRect, QPoint

class CoordConverter:
    '''坐标转换器，实现局部坐标和全局坐标之间的转换'''
    @staticmethod
    def rectToGlobal(widget:QWidget):
        return QRect(
            widget.mapToGlobal(widget.rect().topLeft()),
            widget.mapToGlobal(widget.rect().bottomRight())
            )

    @staticmethod
    def rectToLocal(widget:QWidget):
        return QRect(
            widget.mapFromGlobal(widget.rect().topLeft()),
            widget.mapFromGlobal(widget.rect().bottomRight())
            )

    @staticmethod
    def pointToGlobal(widget:QWidget, pos:QPoint):
        return widget.mapToGlobal(pos)

    @staticmethod
    def pointToLocal(widget:QWidget, pos:QPoint):
        return widget.mapFromGlobal(pos)
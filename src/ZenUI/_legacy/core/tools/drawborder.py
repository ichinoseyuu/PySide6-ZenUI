from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

def drawBorder(widget: QWidget, color: QColor = QColor(255, 0, 0)):
    """绘制边框"""
    painter = QPainter(widget)
    painter.setRenderHint(QPainter.Antialiasing)
    # 设置边框样式
    pen = QPen(color)
    pen.setWidth(1)# 1px宽度
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)# 不填充
    # 绘制边框矩形
    # 由于 QPen 的宽度是向内外两侧扩展的，所以需要调整绘制区域
    rect = widget.rect().adjusted(0, 0, -1, -1)
    painter.drawRect(rect)
    painter.end()
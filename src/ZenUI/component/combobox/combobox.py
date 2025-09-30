from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QTimer,QSize,QPoint
from PySide6.QtGui import QMouseEvent, QEnterEvent
from ZenUI.core import ZGlobal

class ZComboBox(QWidget):
    def __init__(self, parent: QWidget = None, name: str = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import MoveExpAnimation

class ZScrollContent(QWidget):
    resized = Signal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._move_animation = MoveExpAnimation(self)

    @property
    def moveAnimation(self):
        return self._move_animation

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resized.emit()
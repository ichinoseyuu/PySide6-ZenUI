from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import LocationController

class ZScrollContent(QWidget):
    resized = Signal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._location_ctrl = LocationController(self)
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        #self.setStyleSheet('background:transparent;border:1px solid red;')
    @property
    def locationCtrl(self):
        return self._location_ctrl

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resized.emit()

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from ZenUI.component.base import ColorController,LocationController

class SwitchHandle(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._body_cc = ColorController(self)
        self._location_ctrl = LocationController(self)

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def locationCtrl(self): return self._location_ctrl

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        radius = self.height()/2
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QPointF
from PySide6.QtGui import QPainter
from ZenUI.component.base import ColorController,LocationController,FloatController

class SwitchHandle(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.scale_nomal = 0.8
        self.scale_hover = 1.0
        self._body_cc = ColorController(self)
        self._location_ctrl = LocationController(self)
        self._scale_ctrl = FloatController(self)
        self._scale_ctrl.setValue(self.scale_nomal)

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def locationCtrl(self): return self._location_ctrl

    @property
    def scaleCtrl(self): return self._scale_ctrl

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(self.width()/2, self.height()/2)
        radius = self.height()/2
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            scaled_radius = radius * self._scale_ctrl.value
            painter.drawEllipse(center, scaled_radius, scaled_radius)
        painter.end()
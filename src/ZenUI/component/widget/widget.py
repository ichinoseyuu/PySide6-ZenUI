from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRectF,Signal,Qt
from PySide6.QtGui import QPainter,QPen,QPainterPath
from ZenUI.component.base import ColorController,FloatController,LocationController,SizeController,OpacityController

class ZWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._location_ctrl = LocationController(self)
        self._size_ctrl = SizeController(self)
        self._opacity_ctrl = OpacityController(self)

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def locationCtrl(self): return self._location_ctrl

    @property
    def sizeCtrl(self): return self._size_ctrl

    @property
    def opacityCtrl(self): return self._opacity_ctrl
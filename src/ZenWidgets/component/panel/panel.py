from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRectF,Signal
from PySide6.QtGui import QPainter,QPen
from ZenWidgets.component.base import QAnimatedColor,QAnimatedFloat,StyleController,ZWidget
from ZenWidgets.core import ZPanelStyleData, ZDebug

class ZPanel(ZWidget):
    resized = Signal()
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    styleDataCtrl: StyleController[ZPanelStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZPanel'}}

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 style_data_light: ZPanelStyleData = None,
                 style_data_dark: ZPanelStyleData = None
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        if style_data_light: self.styleDataCtrl.setData('Light',style_data_light)
        if style_data_dark: self.styleDataCtrl.setData('Dark',style_data_dark)
        self._init_style_()

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius, radius
                )
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()

    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = data.Radius
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)

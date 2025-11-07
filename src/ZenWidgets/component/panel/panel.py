from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRectF
from PySide6.QtGui import QPainter,QPen,QColor
from ZenWidgets.component.base import ZAnimatedColor,QAnimatedFloat,ZStyleController,ZWidget
from ZenWidgets.core import ZDebug
from ZenWidgets.gui import ZPanelStyleData

class ZPanel(ZWidget):
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: QAnimatedFloat
    styleDataCtrl: ZStyleController[ZPanelStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{'key': 'ZPanel'},
        'radiusCtrl': {'value': 5.0},
    }
    def __init__(self,
                 parent: ZWidget | QWidget | None = None,
                 objectName: str | None = None,
                 ):
        super().__init__(parent=parent, objectName=objectName)
        self._init_style_()

    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)

    # region event
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        border_rect = QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = self.radiusCtrl.value

        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(border_rect, radius, radius)

        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()
        event.accept()


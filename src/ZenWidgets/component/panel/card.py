from PySide6.QtWidgets import QWidget,QSizePolicy
from PySide6.QtCore import Qt,QRectF,QMargins
from PySide6.QtGui import QPainter,QPen,QPainterPath
from ZenWidgets.component.base import ZAnimatedColor,QAnimatedFloat,ZStyleController,ZWidget
from ZenWidgets.component.layout import ZVBoxLayout,ZHBoxLayout
from ZenWidgets.core import ZDebug
from ZenWidgets.gui import ZCardStyleData

class ZCard(ZWidget):
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: QAnimatedFloat
    shadowColorCtrl: ZAnimatedColor
    shadowWidthCtrl: QAnimatedFloat
    styleDataCtrl: ZStyleController[ZCardStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{'key': 'ZCard'},
        'radiusCtrl': {'value': 8.0},
        'shadowWidthCtrl': {'value': 1.5},
    }
    def __init__(self,
                 parent: ZWidget | QWidget | None = None,
                 display_border: bool = True,
                 display_shadow: bool = True,
                 objectName: str | None = None,
                 ):
        super().__init__(parent=parent, objectName=objectName)
        self._display_border = display_border
        self._display_shadow = display_shadow
        self._init_style_()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(ZVBoxLayout(self,margins=QMargins(16,16,16,16),spacing=16))

    def layout(self)-> ZVBoxLayout | ZHBoxLayout:
        return super().layout()

    def setShadowDisplay(self, display: bool,/):
        self._display_shadow = display
        self.update()

    def setBorderDisplay(self, display: bool,/):
        self._display_border = display
        self.update()

    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.shadowColorCtrl.color = data.Shadow

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)
        self.shadowColorCtrl.setColorTo(data.Shadow)

    # region event
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        clip = QPainterPath()
        clip.addRoundedRect(rect, radius, radius)
        painter.setClipPath(clip)

        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.fillRect(rect, self.bodyColorCtrl.color)

        if self._display_border and self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)

        if self._display_shadow and self.shadowColorCtrl.color.alpha() > 0:
            shadow_w = self.shadowWidthCtrl.value
            painter.fillRect(QRectF(rect.left(), rect.bottom() - shadow_w, rect.width(), shadow_w),
                             self.shadowColorCtrl.color)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()
        event.accept()


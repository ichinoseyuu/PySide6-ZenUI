import random
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenWidgets import *
from typing import TYPE_CHECKING
if TYPE_CHECKING: from main import ZenBieGanMao

class PopupMessage(ZWidget):
    bodyColorCtrl: ZAnimatedColor
    textColorCtrl: ZAnimatedColor
    radiusCtrl: ZAnimatedFloat
    def __init__(self,
                 backgroundColor: QColor,
                 text: str,
                 parent: ZWidget | None = None):
        super().__init__(parent=parent)
        self.bodyColorCtrl.color = backgroundColor
        self.bodyColorCtrl.animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.radiusCtrl.value = 4.0
        self._text = ZHeadLine(self, text=text,font=QFont('Microsoft YaHei', 16, QFont.Weight.Normal))
        self._text.move(12, 8)
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.change_color)
        self.color_timer.start(1000)
        ZWidgetEffect.applyGraphicsShadow(self)

    def change_color(self):
        colors = self.parent().light_bg_color if ZGlobal.themeManager.getThemeName() == 'Light' else self.parent().dark_bg_color
        new_color = QColor(random.choice(colors))
        while new_color.name() == self.bodyColorCtrl.color.name():
            new_color = QColor(random.choice(colors))
        self.bodyColorCtrl.setColorTo(new_color)

    def parent(self) -> 'ZenBieGanMao':
        return super().parent()

    def sizeHint(self):
        return self._text.sizeHint()+ QSize(24, 16)

    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()
        event.accept()

    def mousePressEvent(self, event):
        self.close()
        self.parent().popupstack.remove(self)
        self.parent().popup_count -= 1
        self.setParent(None)
        self.deleteLater()
        event.accept()
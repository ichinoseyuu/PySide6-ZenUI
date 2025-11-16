from PySide6.QtWidgets import QWidget,QPushButton
from PySide6.QtCore import Qt,QRectF,QSize,QRect
from PySide6.QtGui import QPainter,QPen
from ZenWidgets.component.input import ZButton,ZLongPressButton
from ZenWidgets.component.layout import ZVBoxLayout
from ZenWidgets.component.base import(
    ZWidget,
    ZAnimatedColor,
    ZAnimatedFloat
)
from ZenWidgets.core import ZMargin,ZDebug
from ZenWidgets.gui import ZWidgetEffect

class DialogContent(ZWidget):
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: ZAnimatedFloat
    __controllers_kwargs__ = {
        'radiusCtrl': {'value': 5.0}
    }
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setLayout(ZVBoxLayout(self))
        # self.btn_ok = ZButton(self, text='确定')
        # self.layout().addWidget(self.btn_ok)
        # self.btn_cancel = ZButton(self, text='取消')
        # self.layout().addWidget(self.btn_cancel)


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

        painter.end()
        event.accept()

class ZDialog(ZWidget):
    def __init__(self, target: ZWidget | QWidget | None = None):
        super().__init__(f=Qt.WindowType.FramelessWindowHint|Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._target: ZWidget | QWidget | None = target
        self._content = DialogContent(self)
        self._margin = ZMargin(8, 8, 8, 8)
        self.windowOpacityCtrl.completelyHide.connect(self.hide)
        ZWidgetEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)

    def target(self): return self._target

    def sizeHint(self):
        return self._content.sizeHint() + QSize(self._margin.horizontal, self._margin.vertical)

    def show(self):
        self.raise_()
        super().show()
        self.widgetRectCtrl.scaleIn(QRect(860,465,200,150))
        self.windowOpacityCtrl.fadeIn()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.setGeometry(self._margin.left, self._margin.top, self.width() - self._margin.horizontal, self.height() - self._margin.vertical)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        event.accept()

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ZDialog()
    w.show()
    sys.exit(app.exec())

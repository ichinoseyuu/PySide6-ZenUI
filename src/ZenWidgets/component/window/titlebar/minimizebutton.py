from PySide6.QtCore import Qt,Slot
from PySide6.QtGui import QPainter,QPen,QColor
from ZenWidgets.core import ZGlobal,ZDebug
from ZenWidgets.gui import ZPalette
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton

class ZMinimizeButton(ZABCTitleBarButton):
    styledata = {
        'Light':  QColor('#333333'),
        'Dark': QColor('#dcdcdc')
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        ZGlobal.themeManager.themeChanged.connect(self._style_change_handler_)
        self._init_style_()

    def _init_style_(self):
        self._iconColorCtrl.setColor(self.styledata[ZGlobal.themeManager.getThemeName()])
        self._layerColorCtrl.setColor(ZGlobal.palette.Transparent_reverse())

    @Slot(str)
    def _style_change_handler_(self, theme: str):
        self._layerColorCtrl.setColor(ZGlobal.palette.Transparent_reverse())
        self._iconColorCtrl.setColorTo(self.styledata[theme])

    def hoverHandler(self):
        self._layerColorCtrl.setAlphaTo(26)

    def leaveHandler(self):
        self._layerColorCtrl.setAlphaTo(0)

    def pressHandler(self):
        self._layerColorCtrl.setAlphaTo(18)

    def releaseHandler(self):
        self._layerColorCtrl.setAlphaTo(26)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(self._layerColorCtrl.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        painter.setBrush(Qt.NoBrush)
        pen = QPen(self._iconColorCtrl.color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        e.accept()
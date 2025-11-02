from PySide6.QtCore import Qt,QLineF,Slot
from PySide6.QtGui import QPainter, QPen,QColor
from ZenWidgets.core import ZGlobal,ZDebug
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton

class ZCloseButton(ZABCTitleBarButton):
    styledata = {
        'Light': {
            'Icon': QColor('#333333'),
            'IconHover': QColor('#333333'),
            'Body': QColor('#00e81b23'),
            'BodyHover': QColor('#ffe81b23'),
            'BodyPressed': QColor('#fff1707a')
        },
        'Dark': {
            'Icon': QColor('#dcdcdc'),
            'IconHover': QColor('#ffffff'),
            'Body': QColor('#00e81b23'),
            'BodyHover': QColor('#ffe81b23'),
            'BodyPressed': QColor('#fff1707a')
        }
    }
    def __init__(self, parent=None):
        super().__init__(parent)
        ZGlobal.themeManager.themeChanged.connect(self._style_change_handler_)
        self._theme = ZGlobal.themeManager.getThemeName()
        self._init_style_()

    def _init_style_(self):
        self._layerColorCtrl.setColor(self.styledata[self._theme]['Body'])
        self._iconColorCtrl.setColor(self.styledata[self._theme]['Icon'])

    @Slot(str)
    def _style_change_handler_(self, theme: str):
        self._theme = theme
        self._layerColorCtrl.setColorTo(self.styledata[theme]['Body'])
        self._iconColorCtrl.setColorTo(self.styledata[theme]['Icon'])

    def hoverHandler(self):
        self._layerColorCtrl.setColorTo(self.styledata[self._theme]['BodyHover'])
        self._iconColorCtrl.setColorTo(self.styledata[self._theme]['IconHover'])

    def leaveHandler(self):
        self._layerColorCtrl.setColorTo(self.styledata[self._theme]['Body'])
        self._iconColorCtrl.setColorTo(self.styledata[self._theme]['Icon'])

    def pressHandler(self):
        self._layerColorCtrl.setColorTo(self.styledata[self._theme]['BodyPressed'])

    def releaseHandler(self):
        self._layerColorCtrl.setColorTo(self.styledata[self._theme]['BodyHover'])

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setBrush(self._layerColorCtrl.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, -1, 0))
        r =self.devicePixelRatioF()
        pen = QPen(self._iconColorCtrl.color, 1.2 * 1/r)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        w, h = self.width(), self.height()
        iw = ih = 10
        x = w/2 - iw/2
        y = h/2 - ih/2
        lines = [
            QLineF(x, y, x + iw, y + ih),
            QLineF(x + iw, y, x, y + ih)
        ]
        painter.drawLines(lines)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        e.accept()
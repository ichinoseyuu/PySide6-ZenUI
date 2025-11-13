from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QPainter,QIcon,QPixmap
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton
from ZenWidgets.core import ZDebug,ZGlobal
from ZenWidgets.gui import ZTheme

class ZChangeThemeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon = QIcon()
        icon.addPixmap(
            ZGlobal.iconPack.toPixmap("ic_fluent_weather_moon_filled"),
            state=QIcon.State.Off
        )
        icon.addPixmap(
            ZGlobal.iconPack.toPixmap("ic_fluent_weather_sunny_filled"),
            state=QIcon.State.On
        )
        self._icon: QIcon = icon
        self._init_style_()

    def hoverHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.2)

    def leaveHandler(self):
        self._layerColorCtrl.toTransparent()

    def pressHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.4)

    def releaseHandler(self):
        self._layerColorCtrl.setAlphaFTo(0.2)

    def clickHandler(self):
        ZGlobal.themeManager.toggleTheme()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setBrush(self._layerColorCtrl.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))
        if ZGlobal.themeManager.getTheme() is ZTheme.Dark:
            pixmap = self._icon.pixmap(QSize(16, 16), state=QIcon.State.On)
        else:
            pixmap = self._icon.pixmap(QSize(16, 16), state=QIcon.State.Off)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF()) # 适配高DPI
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self._iconColorCtrl.color)
        painter_pix.end()
        painter.drawPixmap(
            (46 - 16) // 2,
            (32 - 16) // 2,
            colored_pixmap
        )
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        e.accept()
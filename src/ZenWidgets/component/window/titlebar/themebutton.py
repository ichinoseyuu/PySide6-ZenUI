from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QPainter,QIcon,QPixmap
from ZenWidgets.component.window.titlebar.abctitlebarbutton import ZABCTitleBarButton
from ZenWidgets.component.base import ZStyleController
from ZenWidgets.core import ZDebug,ZGlobal
from ZenWidgets.gui import ZTitleBarButtonStyleData,ZTheme

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
        self._styleCtrl = ZStyleController[ZTitleBarButtonStyleData](self, 'ZTitleBarButton')
        self._styleCtrl.styleChanged.connect(self._style_change_handler_)
        self._init_style_()

    def _init_style_(self):
        data = self._styleCtrl.data
        self._iconColorCtrl.color = data.Icon
        self._layerColorCtrl.color = data.Layer

    def _style_change_handler_(self):
        data = self._styleCtrl.data
        self._layerColorCtrl.setColor(data.Layer)
        self._iconColorCtrl.setColorTo(data.Icon)

    def hoverHandler(self):
        self._layerColorCtrl.color = self._styleCtrl.data.Layer
        self._layerColorCtrl.setAlphaTo(26)

    def leaveHandler(self):
        self._layerColorCtrl.setAlphaTo(0)

    def pressHandler(self):
        self._layerColorCtrl.setAlphaTo(18)

    def releaseHandler(self):
        ZGlobal.themeManager.toggleTheme()
        self._layerColorCtrl.setAlphaTo(26)

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
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QIcon, QPixmap
from ZenUI.component.base import StyleData
from ZenUI.core import ZGlobal,ZTheme,ZTitleBarButtonStyleData
from .abctitlebarbutton import ZABCTitleBarButton

class ZThemeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon = QIcon()
        icon.addFile(u":/icons/fluent/filled/ic_fluent_weather_moon_filled.svg",
                    QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/fluent/filled/ic_fluent_weather_sunny_filled.svg",
                    QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self._icon: QIcon = icon
        self._theme: ZTheme = ZGlobal.themeManager.getTheme()
        self._style_data = StyleData[ZTitleBarButtonStyleData](self, 'ZThemeButton')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

    @property
    def styleData(self): return self._style_data

    def _initStyle(self):
        data = self._style_data.data
        self._body_cc.color = data.Body
        self._icon_cc.color = data.Icon
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._body_cc.setColorTo(data.Body)
        self._icon_cc.setColorTo(data.Icon)

    def hoverHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)

    def leaveHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)

    def pressHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyPressed)

    def releaseHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)
        # draw background
        painter.setBrush(self._body_cc.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))

        # draw icon
        # 1. 获取原始 QPixmap

        if self._theme is ZTheme.Dark:
            pixmap = self._icon.pixmap(QSize(16, 16), QIcon.Normal, QIcon.On)
        else:
            pixmap = self._icon.pixmap(QSize(16, 16), QIcon.Normal, QIcon.Off)
        # 2. 创建一个新的 QPixmap 用于着色
        colored_pixmap = QPixmap(pixmap.size())
        # 适配高DPI
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self._icon_cc.color)
        painter_pix.end()
        # 3. 绘制到按钮中心
        painter.drawPixmap(
            (46 - 16) // 2,
            (32 - 16) // 2,
            colored_pixmap
        )
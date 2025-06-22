from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QIcon, QPixmap
from ZenUI.core import ZGlobal,ZTheme
from .abctitlebarbutton import ZABCTitleBarButton

class ZThemeButton(ZABCTitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        icon = QIcon()
        icon.addFile(u":/icons/svg/fluent/filled/ic_fluent_weather_moon_filled.svg",
                    QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/svg/fluent/filled/ic_fluent_weather_sunny_filled.svg",
                    QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self._icon: QIcon = icon
        self._theme: ZTheme = ZGlobal.themeManager.getTheme()
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZThemeButton")

    def themeChangeHandler(self, theme):
        self._theme = theme
        self._style_data = ZGlobal.styleDataManager.getStyleData("ZThemeButton", theme.name)
        self._background_style.setColorTo(self._style_data.body)
        self._icon_style.setColorTo(self._style_data.icon)

    def hoverHandler(self):
        self._background_style.setColorTo(self._style_data.bodyhover)
        self._icon_style.setColorTo(self._style_data.iconhover)

    def leaveHandler(self):
        self._background_style.setColorTo(self._style_data.body)
        self._icon_style.setColorTo(self._style_data.icon)

    def pressHandler(self):
        self._background_style.setColorTo(self._style_data.bodypressed)
        self._icon_style.setColorTo(self._style_data.iconpressed)

    def releaseHandler(self):
        self._background_style.setColorTo(self._style_data.body)
        self._icon_style.setColorTo(self._style_data.icon)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)
        # draw background
        painter.setBrush(self._background_style.color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect().adjusted(0, 1, 0, 0))

        # draw icon
        # 1. 获取原始 QPixmap
        if self._theme is ZTheme.Dark:
            pixmap = self._icon.pixmap(QSize(16,16), QIcon.Normal, QIcon.On)
        else:
            pixmap = self._icon.pixmap(QSize(16,16), QIcon.Normal, QIcon.Off)
        # 2. 创建一个新的 QPixmap 用于着色
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self._icon_style.color)
        painter_pix.end()
        # 3. 绘制到按钮中心
        painter.drawPixmap(
            (46 - 16) // 2,
            (32 - 16) // 2,
            colored_pixmap
        )
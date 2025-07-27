
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import ColorManager,FloatManager,OpacityManager
from ZenUI.core import ZGlobal, ZToggleButtonStyleData
from .abctogglebutton import ZABCToggleButton
import logging
class ZToggleButton(ZABCToggleButton):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        # property
        self._text: str = None
        self._icon: QIcon = None
        self._icon_size = QSize(16, 16)
        self._font = QFont("Microsoft YaHei", 9)
        self._spacing = 4
        if text : self.text = text
        if icon : self.icon = icon
        # style property
        self._border_width = 1
        self._body_color_mgr = ColorManager(self)
        self._border_color_mgr = ColorManager(self)
        self._text_color_mgr = ColorManager(self)
        self._icon_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)
        # animation property
        self._opacity_mgr = OpacityManager(self)
        # style data
        self._style_data: ZToggleButtonStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @property
    def bodyColorMgr(self) -> ColorManager: return self._body_color_mgr

    @property
    def borderColorMgr(self) -> ColorManager: return self._border_color_mgr

    @property
    def textColorMgr(self) -> ColorManager: return self._text_color_mgr

    @property
    def iconColorMgr(self) -> ColorManager: return self._icon_color_mgr

    @property
    def radiusMgr(self) -> FloatManager: return self._radius_mgr

    @property
    def borderWidth(self) -> int: return self._border_width
    @borderWidth.setter
    def borderWidth(self, width: int) -> None:
        self._border_width = width
        self.update()

    @property
    def opacityMgr(self) -> OpacityManager: return self._opacity_mgr

    @property
    def text(self) -> str: return self._text
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()

    @property
    def icon(self) -> QIcon: return self._icon
    @icon.setter
    def icon(self, icon: QIcon) -> None:
        self._icon = icon
        self.update()

    @property
    def iconSize(self) -> QSize: return self._icon_size
    @iconSize.setter
    def iconSize(self, size: QSize) -> None:
        self._icon_size = size
        self.update()

    @property
    def spacing(self) -> int: return self._spacing
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._spacing = spacing
        self.update()

    @property
    def font(self) -> QFont: return self._font
    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()

    @property
    def styleData(self) -> ZToggleButtonStyleData: return self._style_data
    @styleData.setter
    def styleData(self, style_data: ZToggleButtonStyleData) -> None:
        self._style_data = style_data
        self._radius_mgr.radius = style_data.Radius
        if self._checked:
            self._body_color_mgr.color = style_data.BodyToggled
            self._text_color_mgr.color = style_data.TextToggled
            self._icon_color_mgr.color = style_data.IconToggled
            self._border_color_mgr.color = style_data.BorderToggled
        else:
            self._body_color_mgr.color = style_data.Body
            self._text_color_mgr.color = style_data.Text
            self._icon_color_mgr.color = style_data.Icon
            self._border_color_mgr.color = style_data.Border
        self.update()


    # region Slot
    def themeChangeHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__,theme.name)
        self._style_data = data
        self._radius_mgr.radius = data.Radius
        if self._checked:
            self._body_color_mgr.setColorTo(data.BodyToggled)
            self._border_color_mgr.setColorTo(data.BorderToggled)
            self._icon_color_mgr.setColorTo(data.IconToggled)
            self._text_color_mgr.setColorTo(data.TextToggled)
        else:
            self._body_color_mgr.setColorTo(data.Body)
            self._border_color_mgr.setColorTo(data.Border)
            self._icon_color_mgr.setColorTo(data.Icon)
            self._text_color_mgr.setColorTo(data.Text)

    def hoverHandler(self):
        if self._checked:
            self._body_color_mgr.setColorTo(self._style_data.BodyToggledHover)
        else:
            self._body_color_mgr.setColorTo(self._style_data.BodyHover)

    def leaveHandler(self):
        if self._checked:
            self._body_color_mgr.setColorTo(self._style_data.BodyToggled)
        else:
            self._body_color_mgr.setColorTo(self._style_data.Body)

    def pressHandler(self):
        if self._checked:
            self._body_color_mgr.setColorTo(self._style_data.BodyToggledPressed)
        else:
            self._body_color_mgr.setColorTo(self._style_data.BodyPressed)


    def toggleHandler(self, checked):
        if checked:
            self._body_color_mgr.setColorTo(self._style_data.BodyToggledHover)
            self._border_color_mgr.setColorTo(self._style_data.BorderToggled)
            self._icon_color_mgr.setColorTo(self._style_data.IconToggled)
            self._text_color_mgr.setColorTo(self._style_data.TextToggled)
        else:
            self._body_color_mgr.setColorTo(self._style_data.BodyHover)
            self._border_color_mgr.setColorTo(self._style_data.Border)
            self._icon_color_mgr.setColorTo(self._style_data.Icon)
            self._text_color_mgr.setColorTo(self._style_data.Text)

    # region Override
    # Method
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self._opacity_mgr.fadeTo(1.0)
        else: self._opacity_mgr.fadeTo(0.3)
        super().setEnabled(enable)

    # Event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|
                             QPainter.RenderHint.TextAntialiasing|
                             QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(self._opacity_mgr.opacity)
        # draw background
        rect = self.rect()
        radius = self._radius_mgr.radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_color_mgr.color)
        painter.drawRoundedRect(rect, radius, radius)
        # draw border
        painter.setPen(QPen(self._border_color_mgr.color, 1))
        painter.setBrush(Qt.NoBrush)
        # adjust border width
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # use QRectF to get more accurate result
            radius,
            radius
        )
        if self._icon and self._text:
            total_width = self._icon_size.width() + self._spacing + \
                         self.fontMetrics().boundingRect(self._text).width()
            start_x = (self.width() - total_width) // 2

            pixmap = self._icon.pixmap(self._icon_size)

            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_color_mgr.color)
            painter_pix.end()

            painter.drawPixmap(
                start_x,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )
            # draw text
            painter.setFont(self.font)
            painter.setPen(self._text_color_mgr.color)
            text_rect = QRect(
                start_x + self._icon_size.width() + self._spacing,
                0,
                rect.width(),
                rect.height()
            )
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self._text)
        # only icon
        elif self._icon:
            # get icon
            pixmap = self._icon.pixmap(self._icon_size)
            # create a new QPixmap for coloring
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_color_mgr.color)
            painter_pix.end()
            # draw icon to center
            painter.drawPixmap(
                (self.width() - self._icon_size.width()) // 2,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )
        # only text
        elif self._text:
            painter.setFont(self._font)
            painter.setPen(self._text_color_mgr.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)

    def sizeHint(self):
        if self._icon and not self._text:
            return QSize(30, 30)
        else:
            return QSize(100, 30)
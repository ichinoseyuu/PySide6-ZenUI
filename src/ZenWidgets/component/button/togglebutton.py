
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.base import (
    QAnimatedColor,
    QAnimatedFloat,
    ZAnimatedOpacity,
    StyleController,
    ABCToggleButton
)
from ZenWidgets.core import (
    ZDebug,
    ZToggleButtonStyleData,
    ZGlobal,
    ZPosition,
    ZButtonStyle
)

class ZToggleButton(ABCToggleButton):
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    textColorCtrl: QAnimatedColor
    iconColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: StyleController[ZToggleButtonStyleData]

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None,
                 style: ZButtonStyle = ZButtonStyle.Normal
                 ):
        super().__init__(parent=parent, font=QFont("Microsoft YaHei", 9))
        if name: self.setObjectName(name)
        self._style = style
        self._text: str = None
        self._icon: QIcon = None
        self._icon_size = QSize(16, 16)
        self._spacing = 4
        if text : self._text = text
        if icon : self._icon = icon
        self._init_style_()
        self.resize(self.sizeHint())


    # region public method
    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, t: str) -> None:
        self._text = t
        self.update()

    def setText(self, t: str) -> None:
        self.text = t

    @property
    def icon(self) -> QIcon: return self._icon

    @icon.setter
    def icon(self, i: QIcon) -> None:
        self._icon = i
        self.update()

    def setIcon(self, i: QIcon) -> None:
        self.icon = i

    @property
    def iconSize(self) -> QSize: return self._icon_size

    @iconSize.setter
    def iconSize(self, s: QSize) -> None:
        self._icon_size = s
        self.update()

    def setIconSize(self, s: QSize) -> None:
        self.iconSize = s

    @property
    def spacing(self) -> int: return self._spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._spacing = spacing
        self.update()

    def setSpacing(self, spacing: int) -> None:
        self.spacing = spacing

    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(enable)


    def sizeHint(self):
        if self._icon and not self._text:
            size = QSize(30, 30)
            self.setMinimumSize(size)
            return size
        elif not self._icon and self._text:
            size = QSize(self.fontMetrics().boundingRect(self._text).width() + 40, 30)
            self.setMinimumSize(size)
            return size
        else:
            size = QSize(self.fontMetrics().boundingRect(self._text).width() + 60, 30)
            self.setMinimumSize(size)
            return size

    # region private method
    def _init_style_(self):
        if self._style == ZButtonStyle.Normal:
            self.styleDataCtrl.setKey('ZToggleButton')
        elif self._style == ZButtonStyle.Flat:
            self.styleDataCtrl.setKey('ZFlatToggleButton')
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        if self._checked:
            self.bodyColorCtrl.color = data.BodyToggled
            self.textColorCtrl.color = data.TextToggled
            self.iconColorCtrl.color = data.IconToggled
            self.borderColorCtrl.color = data.BorderToggled
        else:
            self.bodyColorCtrl.color = data.Body
            self.textColorCtrl.color = data.Text
            self.iconColorCtrl.color = data.Icon
            self.borderColorCtrl.color = data.Border
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        if self._checked:
            self.bodyColorCtrl.setColorTo(data.BodyToggled)
            self.borderColorCtrl.setColorTo(data.BorderToggled)
            self.iconColorCtrl.setColorTo(data.IconToggled)
            self.textColorCtrl.setColorTo(data.TextToggled)
        else:
            self.bodyColorCtrl.setColorTo(data.Body)
            self.borderColorCtrl.setColorTo(data.Border)
            self.iconColorCtrl.setColorTo(data.Icon)
            self.textColorCtrl.setColorTo(data.Text)

    # region slot
    def _hover_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggledHover)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)
        if self.toolTip() != '':
            ZGlobal.tooltip.showTip(text=self.toolTip(),
                                    target=self,
                                    position=ZPosition.TopRight,
                                    offset=QPoint(6, 6))
    def _leave_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggled)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)
        if self.toolTip() != '': ZGlobal.tooltip.hideTip()

    def _press_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggledPressed)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)


    def _toggle_handler_(self, checked):
        data = self.styleDataCtrl.data
        if checked:
            self.bodyColorCtrl.setColorTo(data.BodyToggledHover)
            self.borderColorCtrl.setColorTo(data.BorderToggled)
            self.iconColorCtrl.setColorTo(data.IconToggled)
            self.textColorCtrl.setColorTo(data.TextToggled)
        else:
            self.bodyColorCtrl.setColorTo(data.BodyHover)
            self.borderColorCtrl.setColorTo(data.Border)
            self.iconColorCtrl.setColorTo(data.Icon)
            self.textColorCtrl.setColorTo(data.Text)

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)
        rect = self.rect()
        radius = self.radiusCtrl.value

        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)

        if self._icon:
            pixmap = self._icon.pixmap(self._icon_size)
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            with QPainter(colored_pixmap) as painter_pix:
                painter_pix.drawPixmap(0, 0, pixmap)
                painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
                painter_pix.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
            if self._text:
                total_width = self._icon_size.width() + self._spacing + self.fontMetrics().boundingRect(self._text).width()
                start_x = (self.width() - total_width) / 2
                painter.drawPixmap(
                    start_x,
                    (self.height() - self._icon_size.height()) / 2,
                    colored_pixmap
                )
                painter.setFont(self.font())
                painter.setPen(self.textColorCtrl.color)
                painter.drawText(
                    QRect(start_x + self._icon_size.width() + self._spacing, 0, rect.width(), rect.height()),
                    Qt.AlignLeft | Qt.AlignVCenter,
                    self._text
                )
            else:
                painter.drawPixmap(
                    (self.width() - self._icon_size.width()) / 2,
                    (self.height() - self._icon_size.height()) / 2,
                    colored_pixmap
                )
        elif self._text:
            painter.setFont(self.font())
            painter.setPen(self.textColorCtrl.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)


        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


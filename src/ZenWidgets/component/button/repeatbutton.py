from enum import Enum
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.base import (
    QAnimatedColor,
    QAnimatedFloat,
    StyleController,
    ZWidget,
    ABCRepeatButton
)
from ZenWidgets.core import (
    ZButtonStyleData,
    ZDebug,
    ZGlobal,
    ZPosition
)

class ZRepeatButton(ABCRepeatButton):
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    textColorCtrl: QAnimatedColor
    iconColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    styleDataCtrl: StyleController[ZButtonStyleData]

    class Style(Enum):
        Normal = 'ZButton'
        Flat = 'ZFlatButton'

    def __init__(self,
                 parent: ZWidget | QWidget | None = None,
                 text: str | None = None,
                 font: QFont = QFont('Microsoft YaHei', 9),
                 icon: QIcon | None = None,
                 style: Style = Style.Normal,
                 icon_size: QSize = QSize(16, 16),
                 spacing: int = 4,
                 repeatable: bool = True,
                 interval: int = 50,
                 delay: int = 500,
                 objectName: str | None = None,
                 toolTip: str | None = None,
                 ):
        super().__init__(parent=parent,
                         repeatable=repeatable,
                         interval=interval,
                         delay=delay,
                         objectName=objectName,
                         toolTip=toolTip,
                         font=font,
                         )
        self._style: ZRepeatButton.Style = style
        self._text: str | None = text
        self._icon: QIcon | None = icon
        self._icon_size = icon_size
        self._spacing = spacing
        self._init_style_()
        self.resize(self.sizeHint())

    # region public method
    def text(self) -> str: return self._text

    def setText(self, t: str) -> None:
        self._text = t
        self.update()

    def icon(self) -> QIcon: return self._icon

    def setIcon(self, i: QIcon) -> None:
        self._icon = i
        self.update()

    def iconSize(self) -> QSize: return self._icon_size

    def setIconSize(self, s: QSize) -> None:
        self._icon_size = s
        self.update()

    def spacing(self) -> int: return self._spacing

    def setSpacing(self, spacing: int) -> None:
        self._spacing = spacing
        self.update()

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
        if self._style == self.Style.Normal:
            self.styleDataCtrl.setKey(self._style.value)
        elif self._style == self.Style.Flat:
            self.styleDataCtrl.setKey(self._style.value)

        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.textColorCtrl.color = data.Text
        self.iconColorCtrl.color = data.Icon
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = data.Radius
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)
        self.iconColorCtrl.setColorTo(data.Icon)
        self.textColorCtrl.setColorTo(data.Text)

    # region slot
    def _hover_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)
        if self.toolTip() != '':
            ZGlobal.tooltip.showTip(text=self.toolTip(),
                        target=self,
                        position=ZPosition.TopRight,
                        offset=QPoint(6, 6))
    def _leave_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)
        if self.toolTip() != '': ZGlobal.tooltip.hideTip()

    def _press_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)

    def _release_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)



    # region paintEvent
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
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
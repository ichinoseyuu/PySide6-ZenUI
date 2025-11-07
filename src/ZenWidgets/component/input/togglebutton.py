from enum import Enum
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.base import (
    ZAnimatedColor,
    QAnimatedFloat,
    ZStyleController,
    ZOpacityEffect,
    ZWidget,
    ABCToggleButton
)
from ZenWidgets.core import (
    ZDebug,
    ZGlobal,
    ZPosition,
    ZStyle
)
from ZenWidgets.gui import ZToggleButtonStyleData

class ZToggleButton(ABCToggleButton):
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: QAnimatedFloat
    layerCtrl: ZOpacityEffect
    textColorCtrl: ZAnimatedColor
    iconColorCtrl: ZAnimatedColor
    styleDataCtrl: ZStyleController[ZToggleButtonStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{'key': 'ZToggleButton'},
        'radiusCtrl': {'value': 5.0},
    }
    def __init__(self,
                 parent: ZWidget | QWidget | None = None,
                 text: str | None = None,
                 font: QFont = QFont('Microsoft YaHei', 9),
                 icon: QIcon | None = None,
                 icon_size: QSize = QSize(16, 16),
                 spacing: int = 4,
                 checked: bool = False,
                 checkable: bool = True,
                 is_group_member: bool = False,
                 style: ZStyle = ZStyle.Default,
                 objectName: str | None = None,
                 toolTip: str | None = None,
                 ):
        super().__init__(parent=parent,
                         checked=checked,
                         checkable=checkable,
                         is_group_member=is_group_member,
                         style=style,
                         objectName=objectName,
                         toolTip=toolTip,
                         font=font,
                         )
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
        data = self.styleDataCtrl.data
        color_map = self._get_color_mapping(data, self._checked)
        self._apply_color_mapping(color_map)

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        color_map = self._get_color_mapping(data, self._checked)
        self._apply_color_mapping(color_map, anim=True)

    def _get_color_mapping(self, data, is_checked):
        data = self.styleDataCtrl.data
        if is_checked:
            return {
                'body': data.BodyToggled,
                'border': data.BodyToggled,
                'text': data.TextToggled,
                'icon': data.IconToggled
            }
        else:
            return {
                'body': data.Body,
                'border': data.Border,
                'text': data.Text,
                'icon': data.Icon
            }

    def _apply_color_mapping(self, color_map, anim=False):
        if anim:
            self.bodyColorCtrl.setColorTo(color_map['body'])
            self.borderColorCtrl.setColorTo(color_map['border'])
            self.textColorCtrl.setColorTo(color_map['text'])
            self.iconColorCtrl.setColorTo(color_map['icon'])
        else:
            self.bodyColorCtrl.color = color_map['body']
            self.borderColorCtrl.color = color_map['border']
            self.textColorCtrl.color = color_map['text']
            self.iconColorCtrl.color = color_map['icon']

    # region slot
    def _hover_handler_(self):
        self.layerCtrl.setAlphaFTo(0.11 if self.isFlat() else 0.06)
        if self.toolTip() != '':
            ZGlobal.tooltip.showTip(text=self.toolTip(),
                                    target=self,
                                    position=ZPosition.TopRight,
                                    offset=QPoint(6, 6))
    def _leave_handler_(self):
        self.layerCtrl.toTransparent()
        if self.toolTip() != '': ZGlobal.tooltip.hideTip()

    def _press_handler_(self):
        self.layerCtrl.setAlphaFTo(0.15 if self.isFlat() else 0.11)

    def _toggle_handler_(self, checked):
        self.layerCtrl.setAlphaFTo(0.11 if self.isFlat() else 0.06)
        data = self.styleDataCtrl.data
        color_map = self._get_color_mapping(data, checked)
        self._apply_color_mapping(color_map, anim=True)

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
        if self._style != ZStyle.Flat or self._checked:
            if self.bodyColorCtrl.color.alpha() > 0:
                painter.setPen(Qt.NoPen)
                painter.setBrush(self.bodyColorCtrl.color)
                painter.drawRoundedRect(rect, radius, radius)
            if self.borderColorCtrl.color.alpha() > 0:
                painter.setPen(QPen(self.borderColorCtrl.color, 1))
                painter.setBrush(Qt.NoBrush)
                painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),radius, radius)
        self.layerCtrl.drawOpacityLayer(painter, rect, radius)

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
        event.accept()


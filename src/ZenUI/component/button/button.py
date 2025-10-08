from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenUI.component.abstract import ABCButton
from ZenUI.component.base import (
    ColorController,
    FloatController,
    OpacityController,
    StyleController
    )
from ZenUI.core import (
    ZButtonStyleData,
    ZDebug,
    ZGlobal,
    ZPosition
)

class ZButton(ABCButton):
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    textColorCtrl: ColorController
    iconColorCtrl: ColorController
    radiusCtrl: FloatController
    opacityCtrl: OpacityController
    styleDataCtrl: StyleController[ZButtonStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{
            'key': 'ZButton'
        },
    }
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)

        self._text: str = None
        self._icon: QIcon = None
        self._icon_size = QSize(16, 16)
        self._font = QFont("Microsoft YaHei", 9)
        self._spacing = 4
        if text : self.text = text
        if icon : self.icon = icon

        self._init_style_()
        self.resize(self.sizeHint())

    # region Property
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

    # region public
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


    # region private
    def _init_style_(self):
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
        if self._tool_tip != "":
            ZGlobal.tooltip.showTip(text=self._tool_tip,
                        target=self,
                        position=ZPosition.TopRight,
                        offset=QPoint(6, 6))
    def _leave_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)
        if self._tool_tip != "" or ZGlobal.tooltip.isShowing: ZGlobal.tooltip.hideTip()

    def _press_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)

    def _release_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)



    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)

        # 绘制背景和边框
        rect = self.rect()
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius,
                radius
            )

        # 如果同时有图标和文本，绘制在一起
        if self._icon and self._text:
            total_width = self._icon_size.width() + self._spacing + \
                         self.fontMetrics().boundingRect(self._text).width()
            start_x = (self.width() - total_width) // 2

            # 绘制图标
            pixmap = self._icon.pixmap(self._icon_size)
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
            painter_pix.end()

            painter.drawPixmap(
                start_x,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )

            painter.setFont(self._font)
            painter.setPen(self.textColorCtrl.color)
            text_rect = QRect(
                start_x + self._icon_size.width() + self._spacing,
                0,
                rect.width(),
                rect.height()
            )
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self._text)

        # 只有图标
        elif self._icon:

            pixmap = self._icon.pixmap(self._icon_size)

            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
            painter_pix.end()

            painter.drawPixmap(
                (self.width() - self._icon_size.width()) // 2,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )

        # 只有文本
        elif self._text:
            painter.setFont(self._font)
            painter.setPen(self.textColorCtrl.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)

        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


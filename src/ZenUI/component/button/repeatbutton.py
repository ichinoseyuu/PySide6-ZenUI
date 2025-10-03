from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import (
    ColorController,
    FloatController,
    OpacityController,
    StyleData,
    ABCRepeatButton,
    ZPosition)
from ZenUI.core import (
    ZButtonStyleData,
    ZDebug,
    ZGlobal
)

class ZRepeatButton(ABCRepeatButton):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)

        self._text: str = ''
        self._icon: QIcon = QIcon()
        self._icon_size = QSize(16, 16)
        self._font = QFont("Microsoft YaHei", 9)
        self._spacing = 4
        if text : self.text = text
        if icon : self.icon = icon

        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._text_cc = ColorController(self)
        self._icon_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._opacity_ctrl = OpacityController(self)
        self._style_data = StyleData[ZButtonStyleData](self, 'ZButton')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()
        self.resize(self.sizeHint())

    # region Property
    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def textColorCtrl(self): return self._text_cc

    @property
    def iconColorCtrl(self): return self._icon_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def styleData(self): return self._style_data

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
        if enable: self._opacity_ctrl.fadeTo(1.0)
        else: self._opacity_ctrl.fadeTo(0.3)
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
    def _initStyle(self):
        data = self._style_data.data
        self._body_cc.color = data.Body
        self._text_cc.color = data.Text
        self._icon_cc.color = data.Icon
        self._border_cc.color = data.Border
        self._radius_ctrl.value = data.Radius
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._border_cc.setColorTo(data.Border)
        self._icon_cc.setColorTo(data.Icon)
        self._text_cc.setColorTo(data.Text)

    # region slot
    def hoverHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)
        if self._tool_tip != "":
            ZGlobal.tooltip.showTip(text=self._tool_tip,
                        target=self,
                        position=ZPosition.TopRight,
                        offset=QPoint(6, 6))
    def leaveHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)
        if self._tool_tip != "" or ZGlobal.tooltip.isShowing: ZGlobal.tooltip.hideTip()

    def pressHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyPressed)

    def releaseHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)



    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self._opacity_ctrl.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self._radius_ctrl.value
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self._border_cc.color.alpha() > 0:
            # 绘制边框
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            # 调整矩形以避免边框模糊
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
                radius,
                radius
            )
        # 计算内容区域
        # 如果同时有图标和文本，绘制在一起
        if self._icon and self._text:
            # 计算总宽度
            total_width = self._icon_size.width() + self._spacing + \
                         self.fontMetrics().boundingRect(self._text).width()
            # 计算起始x坐标使内容居中
            start_x = (self.width() - total_width) // 2
            # 绘制图标
            # 1. 获取原始 QPixmap
            pixmap = self._icon.pixmap(self._icon_size)
            # 2. 创建一个新的 QPixmap 用于着色
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_cc.color)
            painter_pix.end()
            # 3. 绘制到按钮中心
            painter.drawPixmap(
                start_x,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )
            # 绘制文本
            painter.setFont(self._font)
            painter.setPen(self._text_cc.color)
            text_rect = QRect(
                start_x + self._icon_size.width() + self._spacing,
                0,
                rect.width(),
                rect.height()
            )
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self._text)
        # 只有图标
        elif self._icon:
            # 1. 获取原始 QPixmap
            pixmap = self._icon.pixmap(self._icon_size)
            # 2. 创建一个新的 QPixmap 用于着色
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_cc.color)
            painter_pix.end()
            # 3. 绘制到按钮中心
            painter.drawPixmap(
                (self.width() - self._icon_size.width()) // 2,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )
        # 只有文本
        elif self._text:
            painter.setFont(self._font)
            painter.setPen(self._text_cc.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


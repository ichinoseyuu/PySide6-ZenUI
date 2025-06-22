
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import BackGroundStyle,BorderStyle,CornerStyle,TextStyle,IconStyle,OpacityExpAnimation
from ZenUI.core import ZGlobal, ZToggleButtonStyleData
from .abctogglebutton import ZABCToggleButton
import logging
class ZToggleButton(ZABCToggleButton):
    def __init__(self,
                 name: str,
                 parent: QWidget = None,
                 text: str = None,
                 icon: QIcon = None):
        super().__init__(parent)
        self.setObjectName(name)
        # 基本属性
        self._text: str = None
        self._icon: QIcon = None
        self._icon_size = QSize(16, 16)
        self._font = QFont("Microsoft YaHei", 9)
        self._spacing = 4
        if text : self.text = text
        if icon : self.icon = icon
        # 样式属性
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._text_style = TextStyle(self)
        self._icon_style = IconStyle(self)
        self._corner_style = CornerStyle(self)
        # 动画属性
        self._opacity_anim = OpacityExpAnimation(self)
        # 样式数据
        self._style_data: ZToggleButtonStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZToggleButton")

        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @property
    def backgroundStyle(self) -> BackGroundStyle:
        return self._background_style

    @property
    def borderStyle(self) -> BorderStyle:
        return self._border_style

    @property
    def textStyle(self) -> TextStyle:
        return self._text_style

    @property
    def iconStyle(self) -> IconStyle:
        return self._icon_style

    @property
    def cornerStyle(self) -> CornerStyle:
        return self._corner_style

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()

    @property
    def icon(self) -> QIcon:
        return self._icon

    @icon.setter
    def icon(self, icon: QIcon) -> None:
        self._icon = icon
        self.update()

    @property
    def iconSize(self) -> QSize:
        return self._icon_size

    @iconSize.setter
    def iconSize(self, size: QSize) -> None:
        self._icon_size = size
        self.update()

    @property
    def spacing(self) -> int:
        return self._spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._spacing = spacing
        self.update()

    @property
    def font(self) -> QFont:
        return self._font

    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()

    @property
    def styleData(self) -> ZToggleButtonStyleData:
        """获取按钮样式数据"""
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZToggleButtonStyleData) -> None:
        """设置按钮样式数据"""
        self._style_data = style_data
        self._corner_style.radius = style_data.radius
        if self._checked:
            self._background_style.color = style_data.bodytoggled
            self._text_style.color = style_data.texttoggled
            self._icon_style.color = style_data.icontoggled
            self._border_style.color = style_data.bordertoggled
        else:
            self._background_style.color = style_data.body
            self._text_style.color = style_data.text
            self._icon_style.color = style_data.icon
            self._border_style.color = style_data.border
        self.update()


    # region Slot
    def themeChangeHandler(self, theme):
        """主题改变事件处理"""
        data = ZGlobal.styleDataManager.getStyleData('ZToggleButton',theme.name)
        self._style_data = data
        self._corner_style.radius = data.radius
        if self._checked:
            self._background_style.setColorTo(data.bodytoggled)
            self._border_style.setColorTo(data.bordertoggled)
            self._icon_style.setColorTo(data.icontoggled)
            self._text_style.setColorTo(data.texttoggled)
        else:
            self._background_style.setColorTo(data.body)
            self._border_style.setColorTo(data.border)
            self._icon_style.setColorTo(data.icon)
            self._text_style.setColorTo(data.text)

    def hoverHandler(self, pos):
        if self._checked:
            self._background_style.setColorTo(self._style_data.bodytoggledhover)
        else:
            self._background_style.setColorTo(self._style_data.bodyhover)

    def leaveHandler(self):
        if self._checked:
            self._background_style.setColorTo(self._style_data.bodytoggled)
        else:
            self._background_style.setColorTo(self._style_data.body)

    def pressHandler(self, pos):
        if self._checked:
            self._background_style.setColorTo(self._style_data.bodytoggledpressed)
        else:
            self._background_style.setColorTo(self._style_data.bodypressed)


    def toggleHandler(self, checked):
        if checked:
            self._background_style.setColorTo(self._style_data.bodytoggledhover)
            self._border_style.setColorTo(self._style_data.bordertoggled)
            self._icon_style.setColorTo(self._style_data.icontoggled)
            self._text_style.setColorTo(self._style_data.texttoggled)
        else:
            self._background_style.setColorTo(self._style_data.bodyhover)
            self._border_style.setColorTo(self._style_data.border)
            self._icon_style.setColorTo(self._style_data.icon)
            self._text_style.setColorTo(self._style_data.text)

    # region Override
    # Method
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self._opacity_anim.fadeTo(1.0)
        else: self._opacity_anim.fadeTo(0.3)
        super().setEnabled(enable)

    # Event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|
                             QPainter.RenderHint.TextAntialiasing|
                             QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(self._opacity_anim.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self._corner_style.radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._border_style.color, self._border_style.width))
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
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_style.color)
            painter_pix.end()
            # 3. 绘制到按钮中心
            painter.drawPixmap(
                start_x,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )
            # 绘制文本
            painter.setFont(self.font)
            painter.setPen(self._text_style.color)
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
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_style.color)
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
            painter.setPen(self._text_style.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import ColorManager,FloatManager,OpacityManager
from ZenUI.core import ZGlobal, ZButtonStyleData
from .abcbutton import ZABCButton

class ZButton(ZABCButton):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
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
        self._body_color_mgr = ColorManager(self)
        self._border_color_mgr = ColorManager(self)
        self._text_color_mgr = ColorManager(self)
        self._icon_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)
        # 动画属性
        self._opacity_mgr = OpacityManager(self)
        # 样式数据
        self._style_data: ZButtonStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZButton")

        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @property
    def bodyColorMgr(self): return self._body_color_mgr

    @property
    def borderColorMgr(self): return self._border_color_mgr

    @property
    def textColorMgr(self): return self._text_color_mgr

    @property
    def iconColorMgr(self): return self._icon_color_mgr

    @property
    def radiusMgr(self): return self._radius_mgr

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
    def styleData(self) -> ZButtonStyleData: return self._style_data
    @styleData.setter
    def styleData(self, style_data: ZButtonStyleData) -> None:
        self._style_data = style_data
        self._body_color_mgr.color = style_data.Body
        self._text_color_mgr.color = style_data.Text
        self._icon_color_mgr.color = style_data.Icon
        self._border_color_mgr.color = style_data.Border
        self._radius_mgr.value = style_data.Radius
        self.update()



    # region Slot
    def themeChangeHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__,theme.name)
        self._style_data = data
        self._radius_mgr.value = data.Radius
        self._body_color_mgr.setColorTo(data.Body)
        self._border_color_mgr.setColorTo(data.Border)
        self._icon_color_mgr.setColorTo(data.Icon)
        self._text_color_mgr.setColorTo(data.Text)

    def hoverHandler(self):
        self._body_color_mgr.setColorTo(self.styleData.BodyHover)

    def leaveHandler(self):
        self._body_color_mgr.setColorTo(self.styleData.Body)

    def pressHandler(self):
        self._body_color_mgr.setColorTo(self.styleData.BodyPressed)

    def releaseHandler(self):
        self._body_color_mgr.setColorTo(self.styleData.BodyHover)

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
        # 绘制背景
        rect = self.rect()
        radius = self._radius_mgr.value
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_color_mgr.color)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._border_color_mgr.color, 1))
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
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_color_mgr.color)
            painter_pix.end()
            # 3. 绘制到按钮中心
            painter.drawPixmap(
                start_x,
                (self.height() - self._icon_size.height()) // 2,
                colored_pixmap
            )
            # 绘制文本
            painter.setFont(self._font)
            painter.setPen(self._text_color_mgr.color)
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
            painter_pix.fillRect(colored_pixmap.rect(), self._icon_color_mgr.color)
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
            painter.setPen(self._text_color_mgr.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)


    def sizeHint(self):
        if self._icon and not self._text:
            return QSize(30, 30)
        elif not self._icon and self._text:
            return QSize(self.fontMetrics().boundingRect(self._text).width() + 40, 30)
        else:
            return QSize(self.fontMetrics().boundingRect(self._text).width() + 60, 30)
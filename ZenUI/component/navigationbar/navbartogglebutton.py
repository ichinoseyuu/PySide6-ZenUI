from PySide6.QtGui import QPainter, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import BackGroundStyle,CornerStyle,IconStyle,OpacityExpAnimation
from ZenUI.core import ZGlobal, ZNavBarToggleButtonStyleData
from .abcnavbartogglebutton import ZABCNavBarToggleButton
import logging
class ZNavBarToggleButton(ZABCNavBarToggleButton):
    def __init__(self,
                 name: str = None,
                 parent: QWidget = None,
                 icon: QIcon = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        # 基本属性
        self._icon: QIcon = None
        self._pixmap_off: QPixmap = None
        self._pixmap_on: QPixmap = None
        self._icon_size = QSize(20, 20)
        if icon : self.icon = icon
        # 样式属性
        self._background_style = BackGroundStyle(self)
        self._icon_style = IconStyle(self)
        self._corner_style = CornerStyle(self)
        # 动画属性
        self._opacity_anim = OpacityExpAnimation(self)
        self._indicator_anim = OpacityExpAnimation(self)
        self._indicator_anim.setOpacity(0)
        # 样式数据
        self._style_data: ZNavBarToggleButtonStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZNavBarToggleButton")

        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @property
    def backgroundStyle(self) -> BackGroundStyle:
        return self._background_style

    @property
    def iconStyle(self) -> IconStyle:
        return self._icon_style

    @property
    def cornerStyle(self) -> CornerStyle:
        return self._corner_style

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
    def styleData(self) -> ZNavBarToggleButtonStyleData:
        """获取按钮样式数据"""
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZNavBarToggleButtonStyleData) -> None:
        """设置按钮样式数据"""
        self._style_data = style_data
        self._corner_style.radius = style_data.radius
        if self._checked:
            self._background_style.color = style_data.bodytoggled
            self._icon_style.color = style_data.icontoggled
        else:
            self._background_style.color = style_data.body
            self._icon_style.color = style_data.icon
        self.update()


    # region Slot
    def themeChangeHandler(self, theme):
        """主题改变事件处理"""
        data = ZGlobal.styleDataManager.getStyleData('ZNavBarToggleButton',theme.name)
        self._style_data = data
        self._corner_style.radius = data.radius
        if self._checked:
            self._background_style.setColorTo(data.bodytoggled)
            self._icon_style.setColorTo(data.icontoggled)
        else:
            self._background_style.setColorTo(data.body)
            self._icon_style.setColorTo(data.icon)

    def hoverHandler(self):
        if self._checked:
            self._background_style.setColorTo(self._style_data.bodytoggledhover)
        else:
            self._background_style.setColorTo(self._style_data.bodyhover)

    def leaveHandler(self):
        if self._checked:
            self._background_style.setColorTo(self._style_data.bodytoggled)
        else:
            self._background_style.setColorTo(self._style_data.body)

    def pressHandler(self):
        if self._checked:
            self._background_style.setColorTo(self._style_data.bodytoggledpressed)
        else:
            self._background_style.setColorTo(self._style_data.bodypressed)


    def toggleHandler(self, checked):
        if ZGlobal.themeManager.getTheme().name == "Dark":
            self._icon_style.color = QColor('#202020')
        else:
            self._icon_style.color = QColor('#ffffff')

        if checked:
            self._background_style.setColorTo(self._style_data.bodytoggledhover)
            self._icon_style.setColorTo(self._style_data.icontoggled)
            self._indicator_anim.fadeIn()
        else:
            self._background_style.setColorTo(self._style_data.bodyhover)
            self._icon_style.setColorTo(self._style_data.icon)
            self._indicator_anim.fadeOut()

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
                             QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(self._opacity_anim.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self._corner_style.radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(rect, radius, radius)



        # 1. 获取原始 QPixmap
        if self._checked:
            pixmap = self._icon.pixmap(self._icon_size, QIcon.Mode.Normal, QIcon.State.On)
        else:
            pixmap = self._icon.pixmap(self._icon_size, QIcon.Mode.Normal, QIcon.State.Off)
        # 2. 创建一个新的 QPixmap 用于着色
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self._icon_style.color)
        painter_pix.end()
        # 3. 绘制到按钮中心
        icon_x = (self.width() - self._icon_size.width()) // 2
        icon_y = (self.height() - self._icon_size.height()) // 2
        painter.drawPixmap(icon_x, icon_y, colored_pixmap)
        # draw indicator
        painter.setOpacity(self._indicator_anim.opacity)
        indicator_width = 3
        indicator_height = self._icon_size.height()
        indicator_radius = indicator_width / 2  # 保证半径不超过宽/高一半
        indicator_rect = QRectF(
            0,
            (rect.height() - indicator_height) / 2,
            indicator_width,
            indicator_height
        )
        painter.setBrush(self._icon_style.color)
        painter.drawRoundedRect(indicator_rect, indicator_radius, indicator_radius)

    def sizeHint(self):
        return QSize(40, 40)
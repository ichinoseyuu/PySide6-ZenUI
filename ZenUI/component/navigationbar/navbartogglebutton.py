from PySide6.QtGui import QPainter, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import ColorManager,FloatManager,OpacityManager
from ZenUI.core import ZGlobal, ZNavBarToggleButtonStyleData
from .abcnavbartogglebutton import ZABCNavBarToggleButton
import logging
class ZNavBarToggleButton(ZABCNavBarToggleButton):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 icon: QIcon = None):
        super().__init__(parent)
        self.setMaximumSize(40, 40)
        if name: self.setObjectName(name)
        # 基本属性
        self._icon: QIcon = None
        self._pixmap_off: QPixmap = None
        self._pixmap_on: QPixmap = None
        self._icon_size = QSize(20, 20)
        if icon : self.icon = icon
        # 样式属性
        self._body_color_mgr = ColorManager(self)
        self._icon_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)
        # 动画属性
        self._opacity_mgr = OpacityManager(self)
        self._indicator_opa_mgr = OpacityManager(self)
        self._indicator_opa_mgr.setOpacity(0)
        # 样式数据
        self._style_data: ZNavBarToggleButtonStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @property
    def bodyColorMgr(self): return self._body_color_mgr

    @property
    def iconColorMgr(self): return self._icon_color_mgr

    @property
    def radiusMgr(self): return self._radius_mgr

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
    def styleData(self) -> ZNavBarToggleButtonStyleData: return self._style_data
    @styleData.setter
    def styleData(self, style_data: ZNavBarToggleButtonStyleData) -> None:
        self._style_data = style_data
        self._radius_mgr.value = style_data.Radius
        if self._checked:
            self._body_color_mgr.color = style_data.BodyToggled
            self._icon_color_mgr.color = style_data.IconToggled
        else:
            self._body_color_mgr.color = style_data.Body
            self._icon_color_mgr.color = style_data.Icon
        self.update()

    # region Slot
    def themeChangeHandler(self, theme):
        """主题改变事件处理"""
        data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__,theme.name)
        self._style_data = data
        self._radius_mgr.value = data.Radius
        if self._checked:
            self._body_color_mgr.setColorTo(data.BodyToggled)
            self._icon_color_mgr.setColorTo(data.IconToggled)
        else:
            self._body_color_mgr.setColorTo(data.Body)
            self._icon_color_mgr.setColorTo(data.Icon)

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
            if ZGlobal.themeManager.getTheme().name == "Dark":
                self._icon_color_mgr.color = QColor('#202020')
            else:
                self._icon_color_mgr.color = QColor('#f3f3f3')
            self._body_color_mgr.setColorTo(self._style_data.BodyToggledHover)
            self._icon_color_mgr.setColorTo(self._style_data.IconToggled)
            self._indicator_opa_mgr.fadeIn()
        else:
            self._body_color_mgr.setColorTo(self._style_data.BodyHover)
            self._icon_color_mgr.setColorTo(self._style_data.Icon)
            self._indicator_opa_mgr.fadeOut()

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
                             QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(self._opacity_mgr.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self._radius_mgr.value
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_color_mgr.color)
        painter.drawRoundedRect(rect, radius, radius)

        # 1. 获取原始 QPixmap
        if self._checked:
            pixmap = self._icon.pixmap(self._icon_size, QIcon.Mode.Normal, QIcon.State.On)
        else:
            pixmap = self._icon.pixmap(self._icon_size, QIcon.Mode.Normal, QIcon.State.Off)

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
        icon_x = (self.width() - self._icon_size.width()) // 2
        icon_y = (self.height() - self._icon_size.height()) // 2
        painter.drawPixmap(icon_x, icon_y, colored_pixmap)

        # draw indicator
        painter.setOpacity(self._indicator_opa_mgr.opacity)
        indicator_width = 3
        indicator_height = self._icon_size.height()
        indicator_radius = indicator_width / 2  # 保证半径不超过宽/高一半
        indicator_rect = QRectF(
            0,
            (rect.height() - indicator_height) / 2,
            indicator_width,
            indicator_height
        )
        painter.setBrush(self._icon_color_mgr.color)
        painter.drawRoundedRect(indicator_rect, indicator_radius, indicator_radius)

    def sizeHint(self):
        return QSize(40, 40)
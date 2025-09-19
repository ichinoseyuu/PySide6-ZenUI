
from PySide6.QtGui import QPainter, QIcon, QPixmap, QPen
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import ColorController,FloatController,OpacityController,StyleData
from ZenUI.core import ZNavBarButtonStyleData,ZDebug
from .abcnavbarbutton import ZABCNavBarButton

class ZNavBarButton(ZABCNavBarButton):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 icon: QIcon = None):
        super().__init__(parent)
        self.setMaximumSize(40, 40)
        if name : self.setObjectName(name)

        self._icon: QIcon = QIcon()
        self._icon_size = QSize(20, 20)
        if icon : self.icon = icon

        self._body_cc = ColorController(self)
        self._icon_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._opacity_ctrl = OpacityController(self)

        self._style_data = StyleData[ZNavBarButtonStyleData](self, 'ZNavBarButton')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()
        self.resize(self.sizeHint())


    # region Property
    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def iconColorCtrl(self): return self._icon_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def styleData(self): return self._style_data

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


    def _initStyle(self):
        data = self._style_data.data
        self._body_cc.color = data.Body
        self._icon_cc.color = data.Icon
        self._radius_ctrl.value = data.Radius
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._icon_cc.setColorTo(data.Icon)

    def hoverHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)

    def leaveHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)

    def pressHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyPressed)

    def releaseHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)

    # region Override
    # Method
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self._opacity_ctrl.fadeTo(1.0)
        else: self._opacity_ctrl.fadeTo(0.3)
        super().setEnabled(enable)

    # Event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(self._opacity_ctrl.opacity)
        rect = self.rect()
        radius = self._radius_ctrl.value
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)

        pixmap = self._icon.pixmap(self._icon_size)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self._icon_cc.color)
        painter_pix.end()
        icon_x = (self.width() - self._icon_size.width()) // 2
        icon_y = (self.height() - self._icon_size.height()) // 2
        painter.drawPixmap(icon_x, icon_y, colored_pixmap)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


    def sizeHint(self):
        return QSize(40, 40)
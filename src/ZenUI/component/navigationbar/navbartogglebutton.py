from PySide6.QtGui import QPainter, QIcon, QPixmap, QPen, QMouseEvent
from PySide6.QtCore import Qt, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenUI.component.abstract import ABCToggleButton
from ZenUI.component.base import (
    ColorController,
    FloatController,
    OpacityController,
    StyleController
)
from ZenUI.core import (
    ZNavBarToggleButtonStyleData,
    ZDebug,
    ZGlobal,
    ZPosition
)

class ZNavBarToggleButton(ABCToggleButton):
    bodyColorCtrl: ColorController
    iconColorCtrl: ColorController
    radiusCtrl: FloatController
    opacityCtrl: OpacityController
    styleDataCtrl: StyleController[ZNavBarToggleButtonStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{
            'key': 'ZNavBarToggleButton'
        },
    }
    def __init__(self,
                 icon: QIcon,
                 parent: QWidget = None,
                 name: str = None
                 ):
        super().__init__(parent)
        self.setMaximumSize(40, 40)
        if name: self.setObjectName(name)
        self.isGroupMember = True

        self._icon = icon
        self._icon_size = QSize(20, 20)

        self._init_style_()
        self.resize(self.sizeHint())


    # region Property
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

    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        if self._checked:
            self.bodyColorCtrl.color = data.BodyToggled
            self.iconColorCtrl.color = data.IconToggled
        else:
            self.bodyColorCtrl.color = data.Body
            self.iconColorCtrl.color = data.Icon
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        if self._checked:
            self.bodyColorCtrl.setColorTo(data.BodyToggled)
            self.iconColorCtrl.setColorTo(data.IconToggled)
        else:
            self.bodyColorCtrl.setColorTo(data.Body)
            self.iconColorCtrl.setColorTo(data.Icon)

    def _hover_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggledHover)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)
        if self._tool_tip != "":
            ZGlobal.tooltip.showTip(
                text = self._tool_tip,
                target = self,
                mode = ZGlobal.tooltip.Mode.AlignTarget,
                position = ZPosition.Right,
                offset = QPoint(10, 0)
                )
    def _leave_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggled)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)
        if self._tool_tip != "": ZGlobal.tooltip.hideTip()
    def _press_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggledPressed)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)


    def _toggle_handler_(self, checked):
        data = self.styleDataCtrl.data
        if checked:
            self.iconColorCtrl.color = data.Body
            self.bodyColorCtrl.setColorTo(data.BodyToggledHover)
            self.iconColorCtrl.setColorTo(data.IconToggled)
            #self._indicator_oc.fadeIn()
        else:
            self.bodyColorCtrl.setColorTo(data.BodyHover)
            self.iconColorCtrl.setColorTo(data.Icon)
            #self._indicator_oc.fadeOut()

    # region public
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(enable)

    def sizeHint(self):
        return QSize(40, 40)

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        # 1. 获取原始 QPixmap
        if self._checked:
            pixmap = self._icon.pixmap(self._icon_size, QIcon.Mode.Normal, QIcon.State.On)
        else:
            pixmap = self._icon.pixmap(self._icon_size, QIcon.Mode.Normal, QIcon.State.Off)

        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
        painter_pix.end()

        # 3. 绘制到按钮中心
        icon_x = (self.width() - self._icon_size.width()) // 2
        icon_y = (self.height() - self._icon_size.height()) // 2
        painter.drawPixmap(icon_x, icon_y, colored_pixmap)

        # draw indicator
        # painter.setOpacity(self._indicator_oc.opacity)
        # indicator_width = 3
        # indicator_height = self._icon_size.height()
        # indicator_radius = indicator_width / 2  # 保证半径不超过宽/高一半
        # indicator_rect = QRectF(
        #     0,
        #     (rect.height() - indicator_height) / 2,
        #     indicator_width,
        #     indicator_height
        # )
        # painter.setBrush(self._icon_cc.color)
        # painter.drawRoundedRect(indicator_rect, indicator_radius, indicator_radius)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


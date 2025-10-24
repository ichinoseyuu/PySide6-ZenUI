from typing import overload
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QMargins, Slot, QPoint, QSize, QRect, QRectF,Signal
from PySide6.QtGui import QMouseEvent, QPainter, QIcon , QPixmap, QPen
from ZenUI.component.layout import ZVBoxLayout
from ZenUI.component.base import (
    QAnimatedColor,
    ZAnimatedOpacity,
    QAnimatedFloat,
    ZAnimatedPosition,
    ZAnimatedWidgetSize,
    StyleController,
    ZButtonGroup,
    ZWidget,
    ABCButton,
    ABCToggleButton
)
from ZenUI.core import (
    ZDebug,
    ZNavigationBarStyleData,
    ZNavBarButtonStyleData,
    ZNavBarToggleButtonStyleData,
    ZDebug,
    ZGlobal,
    ZPosition
)

# region ZNavBarButton
class ZNavBarButton(ABCButton):
    bodyColorCtrl: QAnimatedColor
    iconColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: StyleController[ZNavBarButtonStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZNavBarButton'}}

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 icon: QIcon = None,
                 size: QSize = QSize(40, 40),
                 tooltip: str = None
                 ):
        super().__init__(parent=parent, maximumSize=size)
        if name : self.setObjectName(name)
        if tooltip: self.setToolTip(tooltip)
        self._icon: QIcon = icon
        self._icon_size = QSize(20, 20)
        self._init_style_()
        self.resize(self.sizeHint())


    # region public method
    @property
    def icon(self) -> QIcon: return self._icon

    @icon.setter
    def icon(self, i: QIcon) -> None:
        self._icon = i
        self.update()

    def setIcon(self, i: QIcon) -> None:
        self.icon = i

    @property
    def iconSize(self) -> QSize: return self._icon_size

    @iconSize.setter
    def iconSize(self, s: QSize) -> None:
        self._icon_size = s
        self.update()

    def setIconSize(self, s: QSize) -> None:
        self.iconSize = s

    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(enable)

    def sizeHint(self):
        return QSize(40, 40)

    # region private method
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.iconColorCtrl.color = data.Icon
        self.radiusCtrl.value = data.Radius
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.bodyColorCtrl.setColorTo(data.Body)
        self.iconColorCtrl.setColorTo(data.Icon)

    # region slot
    def _hover_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)
        if self.toolTip() != '':
            ZGlobal.tooltip.showTip(
                text = self.toolTip(),
                target = self,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = ZPosition.Right,
                offset = QPoint(10, 0)
                )

    def _leave_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)
        if self.toolTip() != '': ZGlobal.tooltip.hideTip()

    def _press_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)

    def _release_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        pixmap = self._icon.pixmap(self._icon_size)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
        painter_pix.end()
        icon_x = (self.width() - self._icon_size.width()) // 2
        icon_y = (self.height() - self._icon_size.height()) // 2
        painter.drawPixmap(icon_x, icon_y, colored_pixmap)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()

# region ZNavBarToggleButton
class ZNavBarToggleButton(ABCToggleButton):
    bodyColorCtrl: QAnimatedColor
    iconColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: StyleController[ZNavBarToggleButtonStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZNavBarToggleButton'}}

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 icon: QIcon = None,
                 size: QSize = QSize(40, 40),
                 tooltip: str = None,
                 ):
        super().__init__(parent=parent, maximumSize=size)
        if name: self.setObjectName(name)
        if tooltip: self.setToolTip(tooltip)
        self.setGroupMember(True)
        self._icon = icon
        self._icon_size = QSize(20, 20)
        self._init_style_()
        self.resize(self.sizeHint())


    # region private method
    @property
    def icon(self) -> QIcon: return self._icon

    @icon.setter
    def icon(self, i: QIcon) -> None:
        self._icon = i
        self.update()

    def setIcon(self, i: QIcon) -> None:
        self.icon = i

    @property
    def iconSize(self) -> QSize: return self._icon_size

    @iconSize.setter
    def iconSize(self, s: QSize) -> None:
        self._icon_size = s
        self.update()

    def setIconSize(self, s: QSize) -> None:
        self.iconSize = s

    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(enable)

    def sizeHint(self):
        return QSize(40, 40)

    # region private method
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

    # region slot
    def _hover_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggledHover)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)
        if self.toolTip() != '':
            ZGlobal.tooltip.showTip(
                text = self.toolTip(),
                target = self,
                mode = ZGlobal.tooltip.Mode.TrackTarget,
                position = ZPosition.Right,
                offset = QPoint(10, 0)
                )

    def _leave_handler_(self):
        if self._checked:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyToggled)
        else:
            self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)
        if self.toolTip() != '': ZGlobal.tooltip.hideTip()

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
        else:
            self.bodyColorCtrl.setColorTo(data.BodyHover)
            self.iconColorCtrl.setColorTo(data.Icon)

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
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
        icon_x = (self.width() - self._icon_size.width()) // 2
        icon_y = (self.height() - self._icon_size.height()) // 2
        painter.drawPixmap(icon_x, icon_y, colored_pixmap)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


# region Panel
class Panel(QWidget):
    wheeled: Signal = Signal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._content = QWidget(self)
        self._content.setLayout(ZVBoxLayout(self._content,QMargins(0, 0, 0, 0),6,Qt.AlignTop|Qt.AlignHCenter))
        self._offset = 0

    def _updateContentGeometry(self):
        content_height = self._content.layout().sizeHint().height()
        self._content.resize(self.width(), content_height)
        self._content.move(0, -self._offset)

    def layout(self) -> ZVBoxLayout:
        return self._content.layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._updateContentGeometry()

    def wheelEvent(self, event: QMouseEvent):
        content_height = self._content.layout().sizeHint().height()
        visible_height = self.height()
        if content_height <= visible_height:
            return

        max_offset = max(0, content_height - visible_height)
        delta = event.angleDelta().y()
        step = 30
        if delta < 0:
            self._offset = min(self._offset + step, max_offset)
        elif delta > 0:
            self._offset = max(self._offset - step, 0)
        self._updateContentGeometry()
        self.wheeled.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

# region FooterPanel
class FooterPanel(QWidget):
    def __init__(self,parent: QWidget = None):
        super().__init__(parent)
        self.setLayout(ZVBoxLayout(self,QMargins(0, 0, 0, 0),6,Qt.AlignBottom|Qt.AlignHCenter))

    def layout(self) -> ZVBoxLayout:
        return super().layout()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

# region Indicator
class Indicator(ZWidget):
    bodyColorCtrl: QAnimatedColor
    opacityCtrl: ZAnimatedOpacity
    positionCtrl: ZAnimatedPosition
    sizeCtrl: ZAnimatedWidgetSize

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self.width() / 2
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()

# region ZNavigationBar
class ZNavigationBar(ZWidget):
    styleDataCtrl: StyleController[ZNavigationBarStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZNavigationBar'}}

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 btn_size: QSize = QSize(40, 40),
                 btn_icon_size: QSize = QSize(20, 20)
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._buttons: list[ZNavBarButton|ZNavBarToggleButton] = []
        self._button_map: dict[str, ZNavBarButton|ZNavBarToggleButton] = {}
        self._btn_size = btn_size
        self._btn_icon_size = btn_icon_size
        self._panel = Panel(self)
        self._footer_panel = FooterPanel(self)
        self._indicator = Indicator(self)
        self._indicator.setFixedWidth(3)
        self.setLayout(ZVBoxLayout(self, margins=QMargins(0, 0, 0, 0), spacing=0))
        self.layout().addWidget(self._panel, stretch=1)
        self.layout().addWidget(self._footer_panel, stretch=0)
        self._btn_manager = ZButtonGroup()
        self._btn_manager.toggled.connect(self._update_indicator_)
        self._panel.wheeled.connect(self._sync_indicator_)
        self._init_style_()

    # region property
    @property
    def panel(self) -> Panel:
        return self._panel

    @property
    def footerPanel(self) -> FooterPanel:
        return self._footer_panel

    # region public
    @property
    def btnSize(self) -> QSize:return self._btn_size

    @btnSize.setter
    def btnSize(self, size: QSize) -> None:
        self._btn_size = size
        for btn in self._panel.getButtons():
            btn.setMaximumSize(size)

    def setBtnSize(self, size: QSize) -> None:
        self.btnSize = size

    @property
    def btnIconSize(self) -> QSize:return self._btn_icon_size

    @btnIconSize.setter
    def btnIconSize(self, size: QSize) -> None:
        self._btn_icon_size = size
        for btn in self._panel.getButtons():
            btn.setIconSize(size)

    def setBtnIconSize(self, size: QSize) -> None:
        self.btnIconSize = size

    @overload
    def getButton(self, index: int) -> ZNavBarButton|ZNavBarToggleButton: ...

    @overload
    def getButton(self, name: str) -> ZNavBarButton|ZNavBarToggleButton: ...

    def getButton(self, arg) -> ZNavBarButton|ZNavBarToggleButton:
        if isinstance(arg, int):
            return self._buttons[arg]
        elif isinstance(arg, str):
            return self._button_map[arg]

    def getAllButtons(self) -> list[ZNavBarButton|ZNavBarToggleButton]:
        return [btn for (name, btn) in self._buttons]

    def addButton(self, name: str, icon: QIcon, panel: Panel|FooterPanel, tooltip: str = None):
        btn = ZNavBarButton(panel, name, icon, self._btn_size, tooltip)
        panel.layout().addWidget(btn)
        self._buttons.append(btn)
        self._button_map[name] = btn

    def insertButton(self, name: str, icon: QIcon, index: int, panel: Panel|FooterPanel, tooltip: str = None):
        btn = ZNavBarButton(panel, name, icon, self._btn_size, tooltip)
        panel.layout().insertWidget(index, btn)
        self._button_map[name] = btn
        if panel is self._footer_panel:
            index += self._panel.layout().count()
        self._buttons.insert(index, btn)

    def addToggleButton(self, name: str, icon: QIcon, panel: Panel|FooterPanel, tooltip: str = None):
        btn = ZNavBarToggleButton(panel, name, icon, self._btn_size, tooltip)
        panel.layout().addWidget(btn)
        self._btn_manager.addButton(btn)
        self._buttons.append(btn)
        self._button_map[name] = btn

    def insertToggleButton(self, name: str, icon: QIcon, index: int, panel: Panel|FooterPanel, tooltip: str = None):
        btn = ZNavBarToggleButton(panel, name, icon, self._btn_size, tooltip)
        panel.layout().insertWidget(index, btn)
        self._button_map[name] = btn
        if panel is self._footer_panel:
            index += self._panel.layout().count()
        self._buttons.insert(index, btn)

    def toggleToNextButton(self):
        self._btn_manager.toggleToNextButton()

    def toggleToLastButton(self):
        self._btn_manager.toggleToLastButton()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

    # region private
    def _init_style_(self):
        self._indicator.resize(3, self._btn_size.height()-20)
        self._indicator.bodyColorCtrl.color = self.styleDataCtrl.data.Indicator
        self._indicator.update()

    def _style_change_handler_(self):
        self._indicator.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Indicator)

    @Slot()
    def _update_indicator_(self):
        btn = self._btn_manager.checkedButton()
        current_pos = self._indicator.pos()
        target_pos = self._get_btn_global_pos_(btn)
        distance = abs(target_pos.y() - current_pos.y())
        factor = min(0.5, max(0.2, distance / btn.height()))
        self._indicator.positionCtrl.animation.setFactor(factor)
        self._indicator.positionCtrl.moveTo(
            target_pos.x(),
            target_pos.y() + (btn.height()-self._indicator.height())//2
            )

    @Slot()
    def _sync_indicator_(self):
        btn = self._btn_manager.checkedButton()
        if btn.parentWidget() is self._panel:
            self._indicator.stackUnder(self._footer_panel)
        else:
            self._indicator.raise_()
        target_pos = self._get_btn_global_pos_(btn)
        self._indicator.move(
            target_pos.x(),
            target_pos.y() + (btn.height()-self._indicator.height())//2
            )

    def _get_btn_global_pos_(self, btn: ZNavBarButton|ZNavBarToggleButton) -> QPoint:
        return btn.pos() + btn.parentWidget().pos()
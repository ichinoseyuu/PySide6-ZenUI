from enum import Enum
from dataclasses import dataclass
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap, QLinearGradient, QPainterPath
from PySide6.QtCore import Qt, QRect, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import ColorController,FloatController,OpacityController,StyleData
from ZenUI.core import ZSwitchStyleData,ZDebug
from .abcswitch import ZABCSwitch
from .handle import SwitchHandle

@dataclass
class SwitchStyle:
    Height: int
    Width: int
    HandleDiameter: int
    Margin: int

class ZSwitch(ZABCSwitch):
    class Style(Enum):
        Compact = SwitchStyle(Height=20, Width=40, HandleDiameter=16, Margin=2)
        Standard = SwitchStyle(Height=24, Width=48, HandleDiameter=18, Margin=3)
        Comfortable = SwitchStyle(Height=28, Width=56, HandleDiameter=20 , Margin=4)
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 weight: Style = Style.Standard):
        super().__init__(parent)
        self.setObjectName(name)
        self._style = weight
        self._handle = SwitchHandle(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._opacity_ctrl = OpacityController(self)
        self._style_data = StyleData[ZSwitchStyleData](self, 'ZSwitch')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

    # region Property
    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def styleData(self): return self._style_data

    @property
    def handle(self): return self._handle

    @property
    def switchStyle(self): return self._style

    @switchStyle.setter
    def switchStyle(self, value: Style):
        if value == self._style: return
        self._style = value
        self.update()

    # region public
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self._opacity_ctrl.fadeTo(1.0)
        else: self._opacity_ctrl.fadeTo(0.3)
        super().setEnabled(enable)

    # region private
    def _initStyle(self):
        style = self._style.value
        self.setFixedSize(QSize(style.Width, style.Height))
        self._handle.setFixedSize(QSize(style.HandleDiameter, style.HandleDiameter))
        self._handle.move(style.Margin, style.Margin)

        data = self._style_data.data
        self._body_cc.setColor(data.Body)
        self._handle.bodyColorCtrl.color = data.HandleToggled
        if not self._checked:
            self._body_cc.transparent()
            self._handle.bodyColorCtrl.color = data.Handle
        self._border_cc.color = data.Border
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        if self._checked:
            self._body_cc.setColorTo(data.Body)
            self._handle.bodyColorCtrl.setColorTo(data.HandleToggled)
        else:
            self._body_cc.setColor(data.Body)
            self._body_cc.transparent()
            self._handle.bodyColorCtrl.setColorTo(data.Handle)
        self._border_cc.setColorTo(data.Border)


    # region slot
    def hoverHandler(self):
        self._handle.scaleCtrl.setValueTo(self._handle.scale_hover)

    def leaveHandler(self):
        self._handle.scaleCtrl.setValueTo(self._handle.scale_nomal)

    def pressHandler(self):
        pass

    def releaseHandler(self):
        pass

    def toggleHandler(self, checked):
        data = self._style_data.data
        if checked:
            self._body_cc.toOpaque()
            self._handle.bodyColorCtrl.setColorTo(data.HandleToggled)
        else:
            self._body_cc.toTransparent()
            self._handle.bodyColorCtrl.setColorTo(data.Handle)
        # 根据不同权重计算手柄目标位置
        style = self._style.value
        handle_width = self._handle.width()
        margin = style.Margin
        target_x = self.width() - handle_width - margin if checked else margin
        target_y = margin
        # 移动手柄到目标位置
        self._handle.locationCtrl.moveTo(target_x, target_y)

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity_ctrl.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self.height() / 2
        if self._border_cc.color.alpha() > 0:
            # 绘制边框
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            # 调整矩形以避免边框模糊
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius,
                radius
            )
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


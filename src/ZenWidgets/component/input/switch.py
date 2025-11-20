from enum import Enum
from dataclasses import dataclass
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.base import (
    ZAnimatedColor,
    ZAnimatedOpacity,
    ZAnimatedFloat,
    ZStyleController,
    ZWidget,
    ABCToggleButton
)
from ZenWidgets.core import ZDebug
from ZenWidgets.gui import ZSwitchStyleData

@dataclass
class SwitchStyle:
    Height: int
    Width: int
    HandleDiameter: int
    Margin: int

# region SwitchHandle
class SwitchHandle(ZWidget):
    bodyCtrl: ZAnimatedColor
    scaleCtrl: ZAnimatedFloat
    def __init__(self, parent: ZWidget | None = None):
        super().__init__(parent)
        self.scale_nomal = 0.85
        self.scale_hover = 1.0
        self.scaleCtrl.setValue(self.scale_nomal)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(self.width()/2, self.height()/2)
        radius = self.height()/2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.bodyCtrl.color)
        scaled_radius = radius * self.scaleCtrl.value
        painter.drawEllipse(center, scaled_radius, scaled_radius)
        event.accept()

# region ZSwitch
class ZSwitch(ABCToggleButton):
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: ZStyleController[ZSwitchStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZSwitch'}}

    class Style(Enum):
        Compact = SwitchStyle(Height=20, Width=40, HandleDiameter=16, Margin=2)
        Standard = SwitchStyle(Height=24, Width=48, HandleDiameter=18, Margin=3)
        Comfortable = SwitchStyle(Height=28, Width=56, HandleDiameter=22 , Margin=3)

    def __init__(self,
                 parent: ZWidget | None = None,
                 tun_on: bool = False,
                 is_group_member: bool = False,
                 switch_style: Style = Style.Standard,
                 objectName: str | None = None,
                 ):
        super().__init__(parent,
                         checked=tun_on,
                         is_group_member=is_group_member,
                         objectName=objectName,
                         )
        self._switch_style: ZSwitch.Style = switch_style
        self._handle = SwitchHandle(self)
        self._init_style_()

    # private method
    def _init_style_(self):
        style = self._switch_style.value
        self.setFixedSize(style.Width, style.Height)
        self._handle.setFixedSize(style.HandleDiameter, style.HandleDiameter)
        self._handle.move(style.Margin, style.Margin)

        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColor(data.Body)
        self._handle.bodyCtrl.color = data.HandleToggled
        if not self._checked:
            self.bodyColorCtrl.transparent()
            self._handle.bodyCtrl.color = data.Handle
        self.borderColorCtrl.color = data.Border

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        if self._checked:
            self.bodyColorCtrl.setColorTo(data.Body)
            self._handle.bodyCtrl.setColorTo(data.HandleToggled)
        else:
            self.bodyColorCtrl.setColor(data.Body)
            self.bodyColorCtrl.transparent()
            self._handle.bodyCtrl.setColorTo(data.Handle)
        self.borderColorCtrl.setColorTo(data.Border)

    def _mouse_enter_(self): self._handle.scaleCtrl.setValueTo(self._handle.scale_hover)

    def _mouse_leave_(self): self._handle.scaleCtrl.setValueTo(self._handle.scale_nomal)

    def _button_toggle_(self):
        data = self.styleDataCtrl.data
        if self._checked:
            self.bodyColorCtrl.toOpaque()
            self._handle.bodyCtrl.setColorTo(data.HandleToggled)
        else:
            self.bodyColorCtrl.toTransparent()
            self._handle.bodyCtrl.setColorTo(data.Handle)
        style = self._switch_style.value
        handle_width = self._handle.width()
        margin = style.Margin
        target_x = self.width() - handle_width - margin if self._checked else margin
        target_y = margin
        self._handle.widgetPositionCtrl.moveTo(target_x, target_y)

    # public method
    def isTurnOn(self) -> bool: return self._checked

    def switchStyle(self): return self._switch_style

    def setSwitchStyle(self, v: Style):
        if v == self._switch_style: return
        self._button_toggle_()
        self._switch_style = v
        self.update()

    # event
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        radius = self.height()/2
        if self._checked:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        event.accept()


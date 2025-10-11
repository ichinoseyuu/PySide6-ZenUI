from enum import Enum
from dataclasses import dataclass
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtWidgets import QWidget
from ZenUI.component.abstract import ABCToggleButton
from ZenUI.component.base import (
    ColorController,
    OpacityController,
    PositionController,
    FloatController,
    StyleController,
    ZWidget
)
from ZenUI.core import ZSwitchStyleData,ZDebug

@dataclass
class SwitchStyle:
    Height: int
    Width: int
    HandleDiameter: int
    Margin: int


class SwitchHandle(ZWidget):
    bodyColorCtrl: ColorController
    positionCtrl: PositionController
    scaleCtrl: FloatController
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.scale_nomal = 0.85
        self.scale_hover = 1.0
        self.scaleCtrl.setValue(self.scale_nomal)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(self.width()/2, self.height()/2)
        radius = self.height()/2
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            scaled_radius = radius * self.scaleCtrl.value
            painter.drawEllipse(center, scaled_radius, scaled_radius)
        painter.end()


class ZSwitch(ABCToggleButton):
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    opacityCtrl: OpacityController
    styleDataCtrl: StyleController[ZSwitchStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZSwitch'}}

    class Style(Enum):
        Compact = SwitchStyle(Height=20, Width=40, HandleDiameter=16, Margin=2)
        Standard = SwitchStyle(Height=24, Width=48, HandleDiameter=18, Margin=3)
        Comfortable = SwitchStyle(Height=28, Width=56, HandleDiameter=22 , Margin=3)

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 style: Style = Style.Standard
                 ):
        super().__init__(parent)
        self.setObjectName(name)
        self._style = style
        self._handle = SwitchHandle(self)
        self._init_style_()


    # region public
    @property
    def handle(self): return self._handle

    @property
    def isTurnOn(self) -> bool: return self._checked

    @property
    def switchStyle(self): return self._style

    @switchStyle.setter
    def switchStyle(self, v: Style):
        if v == self._style: return
        self._style = v
        self.update()

    def setSwitchStyle(self, v: Style):
        self.switchStyle = v

    def setEnabled(self, e: bool) -> None:
        if e == self.isEnabled(): return
        if e: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(e)

    # region private
    def _init_style_(self):
        style = self._style.value
        self.setFixedSize(style.Width, style.Height)
        self._handle.setFixedSize(style.HandleDiameter, style.HandleDiameter)
        self._handle.move(style.Margin, style.Margin)

        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColor(data.Body)
        self._handle.bodyColorCtrl.color = data.HandleToggled
        if not self._checked:
            self.bodyColorCtrl.transparent()
            self._handle.bodyColorCtrl.color = data.Handle
        self.borderColorCtrl.color = data.Border
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        if self._checked:
            self.bodyColorCtrl.setColorTo(data.Body)
            self._handle.bodyColorCtrl.setColorTo(data.HandleToggled)
        else:
            self.bodyColorCtrl.setColor(data.Body)
            self.bodyColorCtrl.transparent()
            self._handle.bodyColorCtrl.setColorTo(data.Handle)
        self.borderColorCtrl.setColorTo(data.Border)


    # region slot
    def _hover_handler_(self):
        self._handle.scaleCtrl.setValueTo(self._handle.scale_hover)

    def _leave_handler_(self):
        self._handle.scaleCtrl.setValueTo(self._handle.scale_nomal)


    def _toggle_handler_(self, checked):
        data = self.styleDataCtrl.data
        if checked:
            self.bodyColorCtrl.toOpaque()
            self._handle.bodyColorCtrl.setColorTo(data.HandleToggled)
        else:
            self.bodyColorCtrl.toTransparent()
            self._handle.bodyColorCtrl.setColorTo(data.Handle)
        style = self._style.value
        handle_width = self._handle.width()
        margin = style.Margin
        target_x = self.width() - handle_width - margin if checked else margin
        target_y = margin
        self._handle.positionCtrl.moveTo(target_x, target_y)

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self.opacityCtrl.opacity)
        rect = QRectF(self.rect())
        radius = self.height() / 2
        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius, radius
                )
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


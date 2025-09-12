from enum import IntEnum
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap, QLinearGradient, QPainterPath
from PySide6.QtCore import Qt, QRect, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import ColorController,FloatController,OpacityController,StyleData
from ZenUI.core import ZSwitchStyleData,ZDebug
from .abcswitch import ZABCSwitch
from .handle import SwitchHandle

class ZSwitch(ZABCSwitch):
    class Weight(IntEnum):
        Samll = 0
        Normal = 1
        Large = 2
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 weight: Weight = Weight.Normal):
        super().__init__(parent)
        self.setObjectName(name)
        self._weight = weight
        self._handle = SwitchHandle(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
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
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def styleData(self): return self._style_data

    @property
    def handle(self): return self._handle

    @property
    def weight(self): return self._weight

    @weight.setter
    def weight(self, value: Weight):
        if value == self._weight: return
        self._weight = value
        self.update()

    # region public
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self._opacity_ctrl.fadeTo(1.0)
        else: self._opacity_ctrl.fadeTo(0.3)
        super().setEnabled(enable)

    # region private
    def _initStyle(self):
        if self._weight == self.Weight.Samll:
            self.setFixedSize(QSize(40, 20))
            self._handle.setFixedSize(QSize(12, 12))
            self._handle.move(4, 4)
            self._radius_ctrl.value = 10
        elif self._weight == self.Weight.Normal:
            self.setFixedSize(QSize(48, 24))
            self._handle.setFixedSize(QSize(16, 16))
            self._handle.move(4, 4)
            self._radius_ctrl.value = 12
        elif self._weight == self.Weight.Large:
            self.setFixedSize(QSize(56, 28))
            self._handle.setFixedSize(QSize(18, 18))
            self._handle.move(5, 5)
            self._radius_ctrl.value = 14
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
        pass

    def leaveHandler(self):
        pass

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
        handle_width = self._handle.width()
        if self._weight == self.Weight.Samll:
            # 小型开关：右侧位置 = 总宽度 - 手柄宽度 - 左侧边距(4)
            target_x = self.width() - handle_width - 4 if checked else 4
            target_y = 4  # 固定Y坐标
        elif self._weight == self.Weight.Normal:
            # 普通开关：右侧位置 = 总宽度 - 手柄宽度 - 左侧边距(4)
            target_x = self.width() - handle_width - 4 if checked else 4
            target_y = 4  # 固定Y坐标
        else:  # Large
            # 大型开关：右侧位置 = 总宽度 - 手柄宽度 - 左侧边距(5)
            target_x = self.width() - handle_width - 5 if checked else 5
            target_y = 5  # 固定Y坐标

        # 移动手柄到目标位置
        self._handle.locationCtrl.moveTo(target_x, target_y)

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity_ctrl.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self._radius_ctrl.value
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


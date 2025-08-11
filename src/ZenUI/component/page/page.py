from enum import Enum
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QSizePolicy
from PySide6.QtCore import Qt,QMargins,QRectF,Signal
from PySide6.QtGui import QPainter,QPen
from ZenUI.component.base import ColorController,FloatController,LocationController
from ZenUI.core import ZGlobal,ZPageStyleData


class ZPage(QWidget):
    resized = Signal()
    class Layout(Enum):
        Row = 0
        Column = 1
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 layout: Layout = Layout.Column,
                 margins: QMargins = QMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Qt.AlignmentFlag = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet('background-color:transparent;border: 1px solid red;')
        if layout == self.Layout.Row:
            self._layout = QHBoxLayout(self)
        elif layout == self.Layout.Column:
            self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(margins)
        self._layout.setSpacing(spacing)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        if alignment: self._layout.setAlignment(alignment)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._location_ctrl = LocationController(self)

        self._style_data: ZPageStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData('ZPage')

        ZGlobal.themeManager.themeChanged.connect(self.themeChangHandler)

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def locationCtrl(self): return self._location_ctrl

    @property
    def styleData(self): return self._style_data
    @styleData.setter
    def styleData(self, style_data: ZPageStyleData):
        self._style_data = style_data
        self._body_cc.color = style_data.Body
        self._border_cc.color = style_data.Border
        self._radius_ctrl.value = style_data.Radius
        self.update()

    def themeChangHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData('ZPage', theme.name)
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._border_cc.setColorTo(data.Border)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._radius_ctrl.value
        if self._body_cc.color.alpha() > 0:
            # draw background
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self._border_cc.color.alpha() > 0:
            # draw border
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            # adjust border width
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
                radius,
                radius
            )
        painter.end()

    def sizeHint(self):
        return self._layout.sizeHint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()

    def layout(self) -> QVBoxLayout|QHBoxLayout:
        return super().layout()
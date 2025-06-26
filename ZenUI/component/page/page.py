from enum import Enum
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QSizePolicy
from PySide6.QtCore import Qt,QMargins,QRectF
from PySide6.QtGui import QPainter,QPen
from ZenUI.component.base import BackGroundStyle,BorderStyle,CornerStyle, MoveExpAnimation
from ZenUI.core import ZGlobal,ZPageStyleData


class ZPage(QWidget):
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
        if layout == self.Layout.Row:
            self._layout = QHBoxLayout(self)
        elif layout == self.Layout.Column:
            self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(margins)
        self._layout.setSpacing(spacing)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        if alignment: self._layout.setAlignment(alignment)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # style property
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._corner_style = CornerStyle(self)

        # animation property
        self._move_animation = MoveExpAnimation(self)

        # style data
        self._style_data: ZPageStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData('ZPage')

        ZGlobal.themeManager.themeChanged.connect(self.themeChangHandler)

    @property
    def backgroundStyle(self):
        return self._background_style

    @property
    def borderStyle(self):
        return self._border_style

    @property
    def cornerStyle(self):
        return self._corner_style

    @property
    def moveAnimation(self):
        return self._move_animation

    @property
    def styleData(self):
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZPageStyleData):
        self._style_data = style_data
        self._background_style.color = style_data.body
        self._border_style.color = style_data.border
        self._corner_style.width = style_data.radius
        self.update()

    def themeChangHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData('ZPage', theme.name)
        self._corner_style.radius = data.radius
        self._background_style.setColorTo(data.body)
        self._border_style.setColorTo(data.border)
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # draw background
        rect = self.rect()
        radius = self._corner_style.radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(rect, radius, radius)
        # draw border
        painter.setPen(QPen(self._border_style.color, self._border_style.width))
        painter.setBrush(Qt.NoBrush)
        # adjust border width
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            radius,
            radius
        )

    def sizeHint(self):
        return self._layout.sizeHint()
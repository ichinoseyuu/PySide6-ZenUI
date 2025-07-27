from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import Enum
from ZenUI.component.base import ColorManager,FloatManager,LocationManager
from ZenUI.core import ZExpAnimationRefactor
from typing import TYPE_CHECKING
if TYPE_CHECKING: from .scrollpage import ZScrollPage

class ScrollHandle(QWidget):
    class State(Enum):
        Normal = 0
        Hover = 1

    class Orientation(Enum):
        Vertical = 0
        Horizontal = 1

    def __init__(self,
                 parent: QWidget = None,
                 direction: Orientation = Orientation.Vertical):
        super().__init__(parent)
        self._state: ScrollHandle.State = self.State.Normal
        self._orientation: ScrollHandle.Orientation = direction
        self._dragging: bool = False
        self._drag_start_pos: QPoint = QPoint()
        self._handle_width: int = 2
        self._handle_width_min: int = 2
        self._handle_width_max: int = 6
        # style property
        self._body_color_mgr = ColorManager(self)
        self._border_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)
        self._radius_mgr.value = self._handle_width / 2
        # anim property
        self._location_mgr = LocationManager(self)

        self._length_anim = ZExpAnimationRefactor(self, "handleLength")
        self._width_anim = ZExpAnimationRefactor(self, "handleWidth")
        self._width_anim.setBias(0.5)
        self._width_anim.setFactor(0.05)
        # trans timer
        self._trans_timer = QTimer(self)
        self._trans_timer.setSingleShot(True)
        self._trans_timer.timeout.connect(self.toTransparent)
        # init width
        if self._orientation == self.Orientation.Vertical: 
            self.setFixedWidth(self._handle_width_max) 
        else:
            self.setFixedHeight(self._handle_width_max)
        # init style
        self._body_color_mgr.transparent()
        self._border_color_mgr.transparent()

    @property
    def bodyColorMgr(self): return self._body_color_mgr

    @property
    def borderColorMgr(self): return self._border_color_mgr

    @property
    def radiusMgr(self): return self._radius_mgr

    @property
    def locationMgr(self): return self._location_mgr

    @Property(int)
    def handleLength(self): return self.height() if self._orientation == self.Orientation.Vertical else self.width()
    @handleLength.setter
    def handleLength(self, value):
        self.setFixedHeight(value) if self._orientation == self.Orientation.Vertical else self.setFixedWidth(value)

    def setHandleLengthTo(self, value):
        self._length_anim.stop()
        self._length_anim.setStartValue(self.handleLength)
        self._length_anim.setEndValue(value)
        self._length_anim.start()

    @Property(int)
    def handleWidth(self): return self._handle_width
    @handleWidth.setter
    def handleWidth(self, value):
        self._handle_width = value
        self._radius_mgr.value = value / 2
        self.update()

    def setHandleWidthTo(self, value):
        self._width_anim.stop()
        self._width_anim.setStartValue(self.handleWidth)
        self._width_anim.setEndValue(value)
        self._width_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        if self._orientation == self.Orientation.Vertical:
            rect = QRectF(self.width()-self._handle_width +.5, 3, self._handle_width-1, self.height()-3)
        else:
            rect = QRectF(3, self.height()-self._handle_width+.5, self.width()-3, self._handle_width-1)
        radius = self._radius_mgr.value
        # normal 状态只绘制边框
        if self._state == self.State.Normal:
            painter.setPen(QPen(self._border_color_mgr.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)
        # hover 状态绘制边框和内部填充
        elif self._state == self.State.Hover:
            painter.setPen(QPen(self._border_color_mgr.color, 1))
            painter.setBrush(self._body_color_mgr.color)
            painter.drawRoundedRect(rect, radius, radius)


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            # 记录鼠标按下时的全局位置和滑块位置之差
            self._drag_start_pos = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self._dragging: return

        panel = self.parent()

        new_pos = event.globalPos() - self._drag_start_pos

        if self._orientation == self.Orientation.Vertical:
            y = max(0, min(new_pos.y(), panel.height() - panel._handle_h.height() - self.height()))
            percentage = y / (panel.height() - panel._handle_h.height() - self.height())
            max_scroll = panel._content.height() - panel.height()
            scroll_pos = int(percentage * max_scroll)
            panel.scrollTo(y=scroll_pos)
        else:
            x = max(0, min(new_pos.x(), panel.width() - panel._handle_v.width() - self.width()))
            percentage = x / (panel.width() - panel._handle_v.width() - self.width())
            max_scroll = panel._content.width() - panel.width()
            scroll_pos = int(percentage * max_scroll)
            panel.scrollTo(x=scroll_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)


    def enterEvent(self, event):
        self._state = self.State.Hover
        self._trans_timer.stop()
        self.bodyColorMgr.opaque()
        self.borderColorMgr.opaque()
        self.setHandleWidthTo(self._handle_width_max)

    def leaveEvent(self, event):
        self._state = self.State.Normal
        self.setHandleWidthTo(self._handle_width_min)
        self._trans_timer.start(1200)


    def toTransparent(self):
        self.bodyColorMgr.toTransparent()
        self.borderColorMgr.toTransparent()
        self._trans_timer.stop()

    def transparent(self):
        self.bodyColorMgr.transparent()
        self.borderColorMgr.transparent()
        self._trans_timer.stop()

    def toOpaque(self):
        self.bodyColorMgr.toOpaque()
        self.borderColorMgr.toOpaque()
        self._trans_timer.start(1200)

    def opaque(self):
        self.bodyColorMgr.opaque()
        self.borderColorMgr.opaque()
        self._trans_timer.start(1200)

    def parent(self) -> 'ZScrollPage':
        return super().parent()
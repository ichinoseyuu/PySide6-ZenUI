from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import Enum
from ZenUI.component.base import BackGroundStyle,BorderStyle,CornerStyle
from ZenUI.core import ZColorTool
class ScrollHandle(QWidget):
    class Direction(Enum):
        Vertical = 0
        Horizontal = 1
    def __init__(self,
                 parent: QWidget = None,
                 direction: Direction = Direction.Vertical):
        super().__init__(parent)
        self._direction = direction
        self._dragging = False
        self._drag_start_pos = QPoint()
        # style property
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._corner_style = CornerStyle(self)
        # anim property
        self._length_anim = QPropertyAnimation(self, b"length")
        self._length_anim.setDuration(150)

    @property
    def backgroundStyle(self):
        return self._background_style

    @property
    def borderStyle(self):
        return self._border_style

    @property
    def cornerStyle(self):
        return self._corner_style

    @Property(int)
    def length(self):
        """根据方向返回长度"""
        return self.height() if self._direction == self.Direction.Vertical else self.width()

    @length.setter
    def length(self, value):
        """根据方向设置长度"""
        if self._direction == self.Direction.Vertical:
            self.resize(self.width(), value)
        else:
            self.resize(value, self.height())

    def setLengthTo(self, value):
        '长度动画'
        self._length_anim.stop()
        self._length_anim.setStartValue(self.length)
        self._length_anim.setEndValue(value)
        self._length_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(1, 1, self.width()-2, self.height()-2)
        radius = self._corner_style.radius
        # 绘制外边框
        painter.setPen(QPen(self._border_style.color, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制内部填充
        inner_rect = rect.adjusted(0, 0, 0, 0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(inner_rect, radius, radius)
        painter.end()


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            # 记录鼠标按下时的全局位置和滑块位置之差
            self._drag_start_pos = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self._dragging:
            return
        scroll_page = self.parent()
        # 计算新的滑块位置
        new_pos = event.globalPos() - self._drag_start_pos
        if self._direction == self.Direction.Vertical:
            # 垂直方向滚动
            y = max(0, min(new_pos.y(), 
                          scroll_page.height() - scroll_page._handle_h.height() - self.height()))
            percentage = y / (scroll_page.height() - scroll_page._handle_h.height() - self.height())
            max_scroll = scroll_page._content.height() - scroll_page.height()
            scroll_pos = int(percentage * max_scroll)
            scroll_page.scrollTo(y=scroll_pos)
        else:
            # 水平方向滚动
            x = max(0, min(new_pos.x(), 
                          scroll_page.width() - scroll_page._handle_v.width() - self.width()))
            percentage = x / (scroll_page.width() - scroll_page._handle_v.width() - self.width())
            max_scroll = scroll_page._content.width() - scroll_page.width()
            scroll_pos = int(percentage * max_scroll)
            scroll_page.scrollTo(x=scroll_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)


    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from enum import IntEnum, auto
from ZenUI.component.widget.widget import ZWidget

class ResizeGrip(QWidget):
    '''调整大小手柄'''
    class Edge(IntEnum):
        '''位置'''
        TopLeft = auto()
        '左上'
        TopRight = auto()
        '右上'
        BottomLeft = auto()
        '左下'
        BottomRight = auto()
        '右下'
        Top = auto()
        '上'
        Bottom = auto()
        '下'
        Left = auto()
        '左'
        Right = auto()
        '右'
    def __init__(self,
                 parent: ZWidget = None,
                 position: Edge = None,
                 grip_width: int = None):
        super().__init__(parent)
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background:red;')
        self._position = position
        self._width = grip_width
        self._can_resize = True
        self._pressed = False
        self._start_pos = None
        self._start_geometry = None
        self._init_style()

    def _init_style(self):
        '初始化样式'
        if self._position in (self.Edge.TopLeft, self.Edge.BottomRight):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            self.setFixedSize(QSize(self._width, self._width))

        elif self._position in (self.Edge.BottomLeft, self.Edge.TopRight):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            self.setFixedSize(QSize(self._width, self._width))

        elif self._position in (self.Edge.Top, self.Edge.Bottom):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self.setMaximumHeight(self._width)
            self.setMinimumHeight(self._width)

        elif self._position in (self.Edge.Left, self.Edge.Right):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self.setMaximumWidth(self._width)
            self.setMinimumWidth(self._width)

    def refreshCursor(self):
        '刷新光标'
        if self._position in (self.Edge.TopLeft, self.Edge.BottomRight):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)

        elif self._position in (self.Edge.BottomLeft, self.Edge.TopRight):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)

        elif self._position in (self.Edge.Top, self.Edge.Bottom):
            self.setCursor(Qt.CursorShape.SizeVerCursor)

        elif self._position in (self.Edge.Left, self.Edge.Right):
            self.setCursor(Qt.CursorShape.SizeHorCursor)

    def mousePressEvent(self, event: QMouseEvent):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self._start_pos = event.globalPos()
            self._start_geometry = self.window().geometry()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """处理鼠标移动事件"""
        if not self._pressed or self.window().isMaximized() or not self.window().isResizeEnabled():
            return
        delta = event.globalPos() - self._start_pos
        geo = self._start_geometry
        # 根据位置计算新的窗口位置
        if self._position == self.Edge.TopLeft:
            new_geo = QRect(
                geo.left() + delta.x(),
                geo.top() + delta.y(),
                geo.width() - delta.x(),
                geo.height() - delta.y()
            )
        elif self._position == self.Edge.Top:
            new_geo = QRect(
                geo.left(),
                geo.top() + delta.y(),
                geo.width(),
                geo.height() - delta.y()
            )
        elif self._position == self.Edge.TopRight:
            new_geo = QRect(
                geo.left(),
                geo.top() + delta.y(),
                geo.width() + delta.x(),
                geo.height() - delta.y()
            )
        elif self._position == self.Edge.Right:
            new_geo = QRect(
                geo.left(),
                geo.top(),
                geo.width() + delta.x(),
                geo.height()
            )
        elif self._position == self.Edge.BottomRight:
            new_geo = QRect(
                geo.left(),
                geo.top(),
                geo.width() + delta.x(),
                geo.height() + delta.y()
            )
        elif self._position == self.Edge.Bottom:
            new_geo = QRect(
                geo.left(),
                geo.top(),
                geo.width(),
                geo.height() + delta.y()
            )
        elif self._position == self.Edge.BottomLeft:
            new_geo = QRect(
                geo.left() + delta.x(),
                geo.top(),
                geo.width() - delta.x(),
                geo.height() + delta.y()
            )
        elif self._position == self.Edge.Left:
            new_geo = QRect(
                geo.left() + delta.x(),
                geo.top(),
                geo.width() - delta.x(),
                geo.height()
            )
        # 分别获取最小尺寸
        min_width = max(self.window().sizeHint().width(), self.window().minimumWidth())
        min_height = max(self.window().sizeHint().height(), self.window().minimumHeight())

        # 分别限制宽度和高度
        final_geo = QRect(new_geo)

        # 处理宽度限制
        if new_geo.width() < min_width:
            if self._position in (self.Edge.Left, self.Edge.TopLeft, self.Edge.BottomLeft):
                # 左侧拖拽时，固定右边界
                final_geo.setLeft(final_geo.right() - min_width)
            else:
                # 右侧拖拽时，固定左边界
                final_geo.setRight(final_geo.left() + min_width)

        # 处理高度限制
        if new_geo.height() < min_height:
            if self._position in (self.Edge.Top, self.Edge.TopLeft, self.Edge.TopRight):
                # 顶部拖拽时，固定底边
                final_geo.setTop(final_geo.bottom() - min_height)
            else:
                # 底部拖拽时，固定顶边
                final_geo.setBottom(final_geo.top() + min_height)

        # 应用新的几何尺寸
        if final_geo != geo:
            self.window().setGeometry(final_geo)
        event.accept()


    def mouseReleaseEvent(self, event: QMouseEvent):
        """处理鼠标释放事件"""
        self._pressed = False
        self._start_pos = None
        self._start_geometry = None
        event.accept()


    def enterEvent(self, event: QEnterEvent):
        """鼠标进入时显示对应的光标"""
        if not self.window().isMaximized():
            super().enterEvent(event)
            self.refreshCursor()
        else:
            # 最大化状态使用默认光标
            self.setCursor(Qt.ArrowCursor)


    def leaveEvent(self, event: QEvent):
        """鼠标离开时恢复默认光标"""
        super().leaveEvent(event)



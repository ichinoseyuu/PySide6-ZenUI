from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import overload
from ..resizegrip import ResizeGrip,Edge
class ResizeWindow(QWidget):
    '窗口抽象类'
    resized = Signal(QRect)
    moved = Signal(QPoint)
    def __init__(self,
                 resize_window: QWidget,
                 grip_width: int = 5,
                 can_resize: bool = True):
        super().__init__(resize_window)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|
                            Qt.WindowType.Tool) # 无边框窗口,置顶窗口,工具窗口
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) #透明背景
        #self.setStyleSheet("background-color:transparent;border:1px solid red;")
        #self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) #穿透鼠标事件
        from ..acrylicwindow import AcrylicWindow
        self._resize_window: AcrylicWindow = resize_window
        self._grips = []
        self._grip_width = grip_width
        '拖动调整窗口大小时，鼠标距离窗口边缘的宽度'
        self._can_resize = can_resize
        '是否允许调整窗口大小'
        self._topGrip = ResizeGrip(self, Edge.Top,self._grip_width)
        self._bottomGrip = ResizeGrip(self, Edge.Bottom,self._grip_width)
        self._leftGrip = ResizeGrip(self, Edge.Left,self._grip_width)
        self._rightGrip = ResizeGrip(self, Edge.Right,self._grip_width)
        self._topLeftGrip = ResizeGrip(self, Edge.TopLeft,self._grip_width)
        self._topRightGrip = ResizeGrip(self, Edge.TopRight,self._grip_width)
        self._bottomLeftGrip = ResizeGrip(self, Edge.BottomLeft,self._grip_width)
        self._bottomRightGrip = ResizeGrip(self, Edge.BottomRight,self._grip_width)
        self._topGrip.resized.connect(self.resizedHandler)
        self._bottomGrip.resized.connect(self.resizedHandler)
        self._leftGrip.resized.connect(self.resizedHandler)
        self._rightGrip.resized.connect(self.resizedHandler)
        self._topLeftGrip.resized.connect(self.resizedHandler)
        self._topRightGrip.resized.connect(self.resizedHandler)
        self._bottomLeftGrip.resized.connect(self.resizedHandler)
        self._bottomRightGrip.resized.connect(self.resizedHandler)
        self._resize_window._titlebar.moved.connect(self.movedHandler)

    def resizedHandler(self, rect: QRect):
        self.resized.emit(rect)

    def movedHandler(self, pos: QPoint):
        self.moved.emit(self.geometry().topLeft())

    def resizeEvent(self, event):
        """重写调整大小事件"""
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        g = self._grip_width
        self._topGrip.setGeometry(0, 0, w, g)
        self._bottomGrip.setGeometry(0, h-g, w, g)
        self._leftGrip.setGeometry(0, 0, g, h)
        self._rightGrip.setGeometry(w-g, 0, g, h)
        self._topLeftGrip.setGeometry(0, 0, g, g)
        self._topRightGrip.setGeometry(w-g, 0, g, g)
        self._bottomLeftGrip.setGeometry(0, h-g, g, g)
        self._bottomRightGrip.setGeometry(w-g, h-g, g, g)
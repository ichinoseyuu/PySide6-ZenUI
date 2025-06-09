from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from ZenUI.component.basewidget import ZWidget
from ZenUI.core import Zen,ZColorTool
class ScrollPageHandle(QWidget):
    '滚动页面的滚动条手柄'
    def __init__(self,
                 parent: ZWidget = None,
                 radius: int = 4,
                 direction: Zen.Direction = Zen.Direction.Vertical):
        super().__init__(parent)
        self._direction = direction
        self._dragging = False
        self._drag_start_pos = QPoint()
        self._radius = radius
        self._color_config = '#00000000'
        self._border_color_config = '#00000000'
        self._color = QColor(0, 0, 0, 0)
        self._border_color = QColor(0, 0, 0, 0)
        # 创建背景动画
        self._color_anim = QPropertyAnimation(self, b"color")
        self._color_anim.setDuration(150)
        self._border_color_anim = QPropertyAnimation(self, b"borderColor")
        self._border_color_anim.setDuration(150)
        # 创建长度改变动画
        self._length_anim = QPropertyAnimation(self, b"length")
        self._length_anim.setDuration(150)


    @Property(int)
    def length(self):
        """根据方向返回长度"""
        return self.height() if self._direction == Zen.Direction.Vertical else self.width()

    @length.setter
    def length(self, value):
        """根据方向设置长度"""
        if self._direction == Zen.Direction.Vertical:
            self.resize(self.width(), value)
        else:
            self.resize(value, self.height())


    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update()

    @Property(QColor)
    def borderColor(self):
        return self._border_color

    @borderColor.setter
    def borderColor(self, value):
        self._border_color = value


    def transparent(self):
        '透明'
        self.color = ZColorTool.toQColor(ZColorTool.trans(self._color_config))
        self.borderColor = ZColorTool.toQColor(ZColorTool.trans(self._border_color_config))

    def toTransparent(self):
        '渐变到透明'
        self.setColorTo(ZColorTool.toQColor(ZColorTool.trans(self._color_config)))
        self.setBorderColorTo(ZColorTool.toQColor(ZColorTool.trans(self._border_color_config)))

    def toOpaque(self):
        '渐变到不透明'
        self.setColorTo(ZColorTool.toQColor(self._color_config))
        self.setBorderColorTo(ZColorTool.toQColor(self._border_color_config))

    def opaque(self):
        '不透明'
        self.color = ZColorTool.toQColor(self._color_config)
        self.borderColor = ZColorTool.toQColor(self._border_color_config)

    def setColorTo(self, value):
        '背景颜色动画'
        self._color_anim.stop()
        self._color_anim.setStartValue(self._color)
        self._color_anim.setEndValue(value)
        self._color_anim.start()

    def setBorderColorTo(self, value):
        '边框颜色动画'
        self._border_color_anim.stop()
        self._border_color_anim.setStartValue(self._border_color)
        self._border_color_anim.setEndValue(value)
        self._border_color_anim.start()

    def configColor(self, color, border_color):
        self._color_config = color
        self._border_color_config = border_color
        self._color = ZColorTool.toQColor(color)
        self._border_color = ZColorTool.toQColor(border_color)

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
        # 绘制外边框
        painter.setPen(QPen(self.borderColor, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, self._radius, self._radius)
        # 绘制内部填充
        inner_rect = rect.adjusted(0, 0, 0, 0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRoundedRect(inner_rect, self._radius, self._radius)
        painter.end()


    def mousePressEvent(self, event: QMouseEvent):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self._dragging = True
            # 记录鼠标按下时的全局位置和滑块位置之差
            self._drag_start_pos = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        """处理鼠标移动事件"""
        if not self._dragging:
            return
        scroll_page = self.parent()
        # 计算新的滑块位置
        new_pos = event.globalPos() - self._drag_start_pos
        if self._direction == Zen.Direction.Vertical:
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
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)


    def enterEvent(self, event):
        """鼠标进入事件"""
        hover_color = ZColorTool.lighter(self._color_config)
        hover_border = ZColorTool.lighter(self._border_color_config)
        self.setColorTo(hover_color)
        self.setBorderColorTo(hover_border)

    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.setColorTo(self._color_config)
        self.setBorderColorTo(self._border_color_config)
from enum import Enum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import MoveExpAnimation,BorderStyle,CornerStyle,BackGroundStyle
from ZenUI.core import ZScrollPageStyleData,ZGlobal
from .scrollhandle import ScrollHandle
class ZScrollContent(QWidget):
    resized = Signal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._move_animation = MoveExpAnimation(self)

    @property
    def moveAnimation(self):
        return self._move_animation

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resized.emit()

class ZScrollPage(QWidget):
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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._content = ZScrollContent(self)
        if layout == self.Layout.Row:
            self._layout = QHBoxLayout(self._content)
        elif layout == self.Layout.Column:
            self._layout = QVBoxLayout(self._content)
        self._layout.setContentsMargins(margins)
        self._layout.setSpacing(spacing)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        if alignment: self._layout.setAlignment(alignment)

        # handle
        self._last_v_handle_pos: float = 0.0
        self._last_v_handle_len: float = 0.0
        self._last_h_handle_pos: float = 0.0
        self._last_h_handle_len: float = 0.0
        self._handle_v = ScrollHandle(self,ScrollHandle.Orientation.Vertical)
        self._handle_h = ScrollHandle(self,ScrollHandle.Orientation.Horizontal)

        # style property
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._corner_style = CornerStyle(self)

        # animation property
        self._move_animation = MoveExpAnimation(self)

        # style data
        self._style_data: ZScrollPageStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData('ZScrollPage')

        ZGlobal.themeManager.themeChanged.connect(self.themeChangHandler)

        self._content.resized.connect(self._update_handles_and_content)

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
    def content(self):
        return self._content

    @property
    def moveAnimation(self):
        return self._move_animation

    @property
    def styleData(self):
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZScrollPageStyleData):
        self._style_data = style_data
        self._background_style.color = style_data.body
        self._border_style.color = style_data.border
        self._corner_style.width = style_data.radius
        self._handle_h.backgroundStyle.color = style_data.handlebody
        self._handle_v.backgroundStyle.color = style_data.handlebody
        self._handle_h.borderStyle.color = style_data.handleborder
        self._handle_v.borderStyle.color = style_data.handleborder
        self._handle_h.update()
        self._handle_v.update()
        self.update()

    def themeChangHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData('ZScrollPage', theme.name)
        self._corner_style.radius = data.radius
        self._background_style.setColorTo(data.body)
        self._border_style.setColorTo(data.border)
        self._handle_h.backgroundStyle.setColorTo(data.handlebody)
        self._handle_v.backgroundStyle.setColorTo(data.handlebody)
        self._handle_h.borderStyle.setColorTo(data.handleborder)
        self._handle_v.borderStyle.setColorTo(data.handleborder)
        self._handle_h._trans_timer.start(1200)
        self._handle_v._trans_timer.start(1200)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._corner_style.radius
        # draw background
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



    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()
        size_hint = self._content.sizeHint()
        content_w = max(size_hint.width(), w)
        content_h = max(size_hint.height(), h)
        # 更新内容区域大小
        self._content.resize(content_w, content_h)
        self._update_handles_and_content()


    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ShiftModifier:
            delta = event.angleDelta().x() if event.angleDelta().x() != 0 else event.angleDelta().y()
            current_x = -self._content.x()
            step = delta / 120 * 50
            self.scrollTo(x=current_x - step)
        else:
            delta = event.angleDelta().y()
            current_y = -self._content.y()
            step = delta / 120 * 50
            self.scrollTo(y=current_y - step)
        event.accept()


    def scrollTo(self, x: int = None, y: int = None):
        """滚动到指定位置
        Args:
            x: 水平滚动位置,None表示不改变
            y: 垂直滚动位置,None表示不改变
        """
        current_x, current_y = self._content.pos().x(), self._content.pos().y()

        if y is not None:
            max_scroll_y = self._content.height() - self.height()
            if max_scroll_y > 0:
                y = max(0, min(y, max_scroll_y))
                current_y = -y

        if x is not None:
            max_scroll_x = self._content.width() - self.width()
            if max_scroll_x > 0:
                x = max(0, min(x, max_scroll_x))
                current_x = -x

        self._content.moveAnimation.moveTo(current_x, current_y)
        self._sync_scroll_handles(current_x, current_y)


    def _sync_scroll_handles(self, current_x:int, current_y:int):
        """根据内容区位置同步滑块位置"""
        # 垂直滑块
        content_height = self._content.height()
        viewport_height = self.height()
        max_scroll_y = content_height - (viewport_height - self._handle_h.height())
        if self._handle_v.isVisible() and max_scroll_y > 0:
            handle_height = self._handle_v.height()
            handle_space = viewport_height - handle_height
            scroll_y = -current_y
            handle_pos = (scroll_y / max_scroll_y) * handle_space
            # 只有位置或长度变化时才显示
            if (self._last_v_handle_pos != handle_pos):
                self._handle_v.opaque()
            self._last_v_handle_pos = handle_pos
            # 更新滑块位置
            self._handle_v.moveAnimation.moveTo(
                self.width() - self._handle_v.width(),
                handle_pos
            )

        # 水平滑块
        content_width = self._content.width()
        viewport_width = self.width()
        max_scroll_x = content_width - (viewport_width - self._handle_v.width())
        if self._handle_h.isVisible() and max_scroll_x > 0:
            handle_width = self._handle_h.width()
            handle_space = viewport_width - handle_width
            scroll_x = -current_x
            handle_pos = (scroll_x / max_scroll_x) * handle_space
            # 只有位置或长度变化时才显示
            if (self._last_h_handle_pos != handle_pos):
                self._handle_h.opaque()
            self._last_h_handle_pos = handle_pos
            # 更新滑块位置
            self._handle_h.moveAnimation.moveTo(
                handle_pos,
                self.height() - self._handle_h.height()
            )


    def _update_handles_and_content(self):
        """更新滚动条和内容区域的位置"""
        viewport = self.size()
        content= self._content.size()
        # 更新滚动条和内容区域位置
        self._update_vertical_handle(content.height(), viewport.height())
        self._update_horizontal_handle(content.width(), viewport.width())


    def _update_vertical_handle(self, ch, vh):
        # 计算新的最大滚动范围
        max_scroll = ch - vh
        if max_scroll <= 0: # 内容小于等于视口，隐藏滚动条,并重置内容位置
            self._handle_v.hide()
            self._content.move(self._content.x(), 0)
            return

        # 计算内容的相对位置（百分比）
        content_visible_ratio = -self._content.y() / ch
        # 根据内容相对位置计算新的滚动位置
        new_scroll_pos = max(0, min(int(content_visible_ratio * ch), max_scroll))
        # 更新内容位置
        self._content.moveAnimation.moveTo(self._content.x(), -new_scroll_pos)

        # 计算滑块高度
        handle_h= max(10, vh * min(1.0, vh / ch))
        # 计算滑块位置
        handle_space = vh - handle_h
        handle_pos = (new_scroll_pos / max_scroll) * handle_space
        # 更新滑块
        # 只有位置或长度变化时才显示
        self._handle_v.show()
        if (self._last_v_handle_pos != handle_pos or
            self._last_v_handle_len != handle_h):
            self._handle_v.opaque()
        self._last_v_handle_pos = handle_pos
        self._last_v_handle_len = handle_h
        self._handle_v.setHandleLengthTo(handle_h)
        self._handle_v.move(self.width() - self._handle_v.width(), self._handle_v.y())
        self._handle_v.moveAnimation.moveTo(
            self.width() - self._handle_v.width(),
            handle_pos
        )


    def _update_horizontal_handle(self, cw, vw):
        # 计算新的最大滚动范围
        max_scroll = cw - vw
        if max_scroll <= 0: # 内容小于等于视口，隐藏滚动条,并重置内容位置
            self._handle_h.hide()
            self._content.move(0, self._content.y())
            return

        # 计算内容的相对位置（百分比）
        content_visible_ratio = -self._content.x() / cw
        # 根据内容相对位置计算新的滚动位置
        new_scroll_pos = max(0, min(int(content_visible_ratio * cw), max_scroll))
        # 更新内容位置
        self._content.moveAnimation.moveTo(new_scroll_pos, self._content.y())

        # 计算滑块宽度
        handle_w = max(10, vw * min(1.0, vw / cw))
        # 计算滑块位置
        handle_space = vw - handle_w
        handle_pos = (new_scroll_pos / max_scroll) * handle_space
        # 更新滑块
        # 只有位置或长度变化时才显示
        self._handle_h.show()
        if (self._last_h_handle_pos != handle_pos or
            self._last_h_handle_len != handle_w):
            self._handle_h.opaque()
        self._last_h_handle_pos = handle_pos
        self._last_h_handle_len = handle_w
        self._handle_h.setHandleLengthTo(handle_w)
        self._handle_h.move(self._handle_h.x(), self.height() - self._handle_h.height())
        self._handle_h.moveAnimation.moveTo(
            handle_pos,
            self.height() - self._handle_h.height()
        )
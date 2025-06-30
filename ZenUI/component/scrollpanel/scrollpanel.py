from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.page import ZPage
from ZenUI.component.base import MoveExpAnimation
from .scrollhandle import ScrollHandle

class ZScrollPanel(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 layout: ZPage.Layout = ZPage.Layout.Column,
                 margins: QMargins = QMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Qt.AlignmentFlag = None,
                 scrollbar_width: int = 8):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._content = ZPage(parent=self,
                              layout=layout,
                              margins=margins,
                              spacing=spacing,
                              alignment=alignment)
        self._handle_v = ScrollHandle(self,ScrollHandle.Direction.Vertical)
        self._handle_h = ScrollHandle(self,ScrollHandle.Direction.Horizontal)
        self._handle_h.setFixedHeight(scrollbar_width)
        self._handle_v.setFixedWidth(scrollbar_width)

        # anim property
        self._move_animation = MoveExpAnimation(self)

        self._content.resized.connect(self._update_handles)


    @property
    def content(self):
        return self._content

    @property
    def moveAnimation(self):
        return self._move_animation

    def themeChangeHandler(self, theme):
        pass


    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()
        # 更新内容区域大小
        size_hint = self._content.sizeHint()
        content_w = max(size_hint.width(), w)
        content_h = max(size_hint.height(), h)
        self._content.resize(content_w, content_h)
        # 更新垂直滚动条
        self._handle_v.setGeometry(
            self.width() - self._handle_v.width(),
            0,
            self._handle_v.width(),
            h
        )
        # 更新水平滚动条
        self._handle_h.setGeometry(
            0,
            self.height() - self._handle_h.height(),
            w,
            self._handle_h.height()
        )
        # 更新内容区域和滚动条状态
        self._update_handles()


    # def enterEvent(self, event):
    #     super().enterEvent(event)
    #     if self._handle_v.isVisible():
    #         self._handle_v.backgroundStyle.toOpaque()
    #         self._handle_v.borderStyle.toOpaque()
    #     if self._handle_h.isVisible():
    #         self._handle_h.backgroundStyle.toOpaque()
    #         self._handle_h.borderStyle.toOpaque()


    # def leaveEvent(self, event):
    #     super().leaveEvent(event)
    #     if self._handle_v.isVisible():
    #         self._handle_v.backgroundStyle.toTransparent()
    #         self._handle_v.borderStyle.toTransparent()
    #     if self._handle_h.isVisible():
    #         self._handle_h.backgroundStyle.toTransparent()
    #         self._handle_h.borderStyle.toTransparent()


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
            max_scroll_y = self._content.height() - (self.height() - self._handle_h.height())
            if max_scroll_y > 0:
                y = max(0, min(y, max_scroll_y))
                current_y = -y

        if x is not None:
            max_scroll_x = self._content.width() - (self.width() - self._handle_v.width())
            if max_scroll_x > 0:
                x = max(0, min(x, max_scroll_x))
                current_x = -x

        self._content.move(current_x, current_y)
        self._update_handles()

    def _update_handles(self):
        """更新滚动条状态"""
        viewport = self.size()
        content= self._content.size()
        # 更新滚动条
        self._update_vertical_handle(content.height(), viewport.height())
        self._update_horizontal_handle(content.width(), viewport.width())


    def _update_vertical_handle(self, content_height, viewport_height):
        """更新垂直滚动条"""
        if content_height <= viewport_height:
            self._handle_v.hide()
            # 重置位置
            self._content.move(self._content.x(), 0)
            return

        self._handle_v.show()
        # 计算滑块高度
        ratio = min(1.0, viewport_height / content_height)
        handle_height = max(30, viewport_height * ratio)
        self._handle_v.setFixedHeight(handle_height)
        # 计算内容的相对位置（百分比）
        current_scroll = -self._content.y()
        content_visible_ratio = current_scroll / content_height
        # 计算新的最大滚动范围
        max_scroll = content_height - viewport_height
        # 根据内容相对位置计算新的滚动位置
        new_scroll_pos = int(content_visible_ratio * content_height)
        # 限制在有效范围内
        new_scroll_pos = max(0, min(new_scroll_pos, max_scroll))
        # 更新内容位置
        self._content.move(self._content.x(), -new_scroll_pos)
        # 计算滑块位置
        handle_space = viewport_height - handle_height
        handle_pos = (new_scroll_pos / max_scroll) * handle_space if max_scroll > 0 else 0
        # 更新滑块位置
        self._handle_v.move(
            self.width() - self._handle_v.width(),
            handle_pos
        )


    def _update_horizontal_handle(self, content_width, viewport_width):
        """更新水平滚动条"""
        if content_width <= viewport_width:
            self._handle_h.hide()
            # 重置位置
            self._content.move(0, self._content.y())
            return
        self._handle_h.show()
        # 计算滑块宽度
        ratio = min(1.0, viewport_width / content_width)
        handle_width = max(30, viewport_width * ratio)
        self._handle_h.setFixedWidth(handle_width)
        # 计算内容的相对位置（百分比）
        current_scroll = -self._content.x()
        content_visible_ratio = current_scroll / content_width
        # 计算新的最大滚动范围
        max_scroll = content_width - viewport_width
        # 根据内容相对位置计算新的滚动位置
        new_scroll_pos = int(content_visible_ratio * content_width)
        # 限制在有效范围内
        new_scroll_pos = max(0, min(new_scroll_pos, max_scroll))
        # 更新内容位置
        self._content.move(-new_scroll_pos, self._content.y())
        # 计算滑块位置
        handle_space = viewport_width - handle_width
        handle_pos = (new_scroll_pos / max_scroll) * handle_space if max_scroll > 0 else 0
        # 更新滑块位置
        self._handle_h.move(
            handle_pos,
            self.height() - self._handle_h.height()
        )


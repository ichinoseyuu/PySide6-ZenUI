from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.itemview import ZItemView
from ZenUI.component.base import (
    PositionController,
    ColorController,
    FloatController,
    StyleController,
    ZWidget
)
from ZenUI.core import (
    ZScrollPanelStyleData,
    ZDebug,
    ZExpAnimationRefactor,
    ZDirection,
    ZState
)


class ScrollContent(QWidget):
    resized = Signal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._location_ctrl = PositionController(self)
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        #self.setStyleSheet('background:transparent;border:1px solid red;')
    @property
    def locationCtrl(self):
        return self._location_ctrl

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resized.emit()


class ScrollHandle(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 direction: ZDirection = ZDirection.Vertical
                 ):
        super().__init__(parent)
        self._state: ZState = ZState.Idle
        if direction not in (ZDirection.Horizontal, ZDirection.Vertical):
            raise ValueError('Invalid direction')
        self._dir: ZDirection = direction
        self._dragging: bool = False
        self._drag_start_pos: QPoint = QPoint()
        self._handle_width: int = 2
        self._handle_width_min: int = 2
        self._handle_width_max: int = 6

        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._radius_ctrl.value = self._handle_width / 2
        self._position_ctrl = PositionController(self)

        self._length_anim = ZExpAnimationRefactor(self, "handleLength")
        self._width_anim = ZExpAnimationRefactor(self, "handleWidth")
        self._width_anim.setBias(0.5)
        self._width_anim.setFactor(0.05)

        self._trans_timer = QTimer(self)
        self._trans_timer.setSingleShot(True)
        self._trans_timer.timeout.connect(self.toTransparent)

        if self._dir == ZDirection.Vertical:
            self.setFixedWidth(self._handle_width_max)
        else:
            self.setFixedHeight(self._handle_width_max)
        # init style
        self._body_cc.transparent()
        self._border_cc.transparent()

    # region property
    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def positionCtrl(self): return self._position_ctrl

    @Property(int)
    def handleLength(self): return self.height() if self._dir == ZDirection.Vertical else self.width()

    @handleLength.setter
    def handleLength(self, value):
        self.setFixedHeight(value) if self._dir == ZDirection.Vertical else self.setFixedWidth(value)

    @Property(int)
    def handleWidth(self): return self._handle_width

    @handleWidth.setter
    def handleWidth(self, value):
        self._handle_width = value
        self._radius_ctrl.value = value / 2
        self.update()

    # region public
    def setHandleLengthTo(self, value):
        self._length_anim.stop()
        self._length_anim.setStartValue(self.handleLength)
        self._length_anim.setEndValue(value)
        self._length_anim.start()

    def setHandleWidthTo(self, value):
        self._width_anim.stop()
        self._width_anim.setStartValue(self.handleWidth)
        self._width_anim.setEndValue(value)
        self._width_anim.start()

    def toTransparent(self):
        self.bodyColorCtrl.toTransparent()
        self.borderColorCtrl.toTransparent()
        self._trans_timer.stop()

    def transparent(self):
        self.bodyColorCtrl.transparent()
        self.borderColorCtrl.transparent()
        self._trans_timer.stop()

    def toOpaque(self):
        self.bodyColorCtrl.toOpaque()
        self.borderColorCtrl.toOpaque()
        self._trans_timer.start(1200)

    def opaque(self):
        self.bodyColorCtrl.opaque()
        self.borderColorCtrl.opaque()
        self._trans_timer.start(1200)

    def parent(self) -> 'ZScrollPanel':
        return super().parent()

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        if self._dir == ZDirection.Vertical:
            rect = QRectF(self.width()-self._handle_width +.5, 3, self._handle_width-1, self.height()-3)
        else:
            rect = QRectF(3, self.height()-self._handle_width+.5, self.width()-3, self._handle_width-1)
        radius = self._radius_ctrl.value
        # normal 状态只绘制边框
        if self._state == ZState.Idle:
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)
        # hover 状态绘制边框和内部填充
        elif self._state == ZState.Hover:
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()

    # region mouseEvent
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            # 记录鼠标按下时的全局位置和滑块位置之差
            self._drag_start_pos = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self._dragging: return

        panel = self.parent()

        new_pos = event.globalPos() - self._drag_start_pos

        if self._dir == ZDirection.Vertical:
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
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)

    def enterEvent(self, event):
        self._state = ZState.Hover
        self._trans_timer.stop()
        self.bodyColorCtrl.opaque()
        self.borderColorCtrl.opaque()
        self.setHandleWidthTo(self._handle_width_max)

    def leaveEvent(self, event):
        self._state = ZState.Idle
        self.setHandleWidthTo(self._handle_width_min)
        self._trans_timer.start(1200)



class ZScrollPanel(ZWidget):
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    radiusCtrl: FloatController
    positionCtrl: PositionController
    styleDataCtrl: StyleController[ZScrollPanelStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{
            'key': 'ZScrollPanel'
        },
    }
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 style_data_light: ZScrollPanelStyleData = None,
                 style_data_dark: ZScrollPanelStyleData = None
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._content = ScrollContent(self)

        self._last_v_handle_pos: float = 0.0
        self._last_v_handle_len: float = 0.0
        self._last_h_handle_pos: float = 0.0
        self._last_h_handle_len: float = 0.0
        self._handle_v = ScrollHandle(self,ZDirection.Vertical)
        self._handle_h = ScrollHandle(self,ZDirection.Horizontal)

        self._content.resized.connect(self._update_handles_and_content)
        if style_data_light: self.styleDataCtrl.setData('Light',style_data_light)
        if style_data_dark: self.styleDataCtrl.setData('Dark',style_data_dark)
        self._init_style_()

    @property
    def content(self): return self._content

    # region public
    def scrollTo(self, x: int = None, y: int = None):
        """滚动到指定位置
        Args:
            x: 水平滚动位置,None表示不改变
            y: 垂直滚动位置,None表示不改变
        """
        current_pos = self._content.pos()
        current_x, current_y = current_pos.x(), current_pos.y()

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

        # 确保坐标值是有效的整数
        final_x = int(current_x)
        final_y = int(current_y)

        self._content.locationCtrl.moveTo(final_x, final_y)
        self._sync_scroll_handles(final_x, final_y)


    def layout(self):
        return self._content.layout()

    def setLayout(self, arg__1:QLayout):
        return self._content.setLayout(arg__1)

    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            # draw background
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self.borderColorCtrl.color.alpha() > 0:
            # draw border
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            # adjust border width
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
                radius,
                radius
            )
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()

    # region resizeEvent
    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()
        size_hint = self._content.sizeHint()
        content_w = max(size_hint.width(), w)
        content_h = max(size_hint.height(), h)
        # 更新内容区域大小
        self._content.resize(content_w, content_h)
        self._update_handles_and_content()

    # region mouseEvent
    def wheelEvent(self, event: QWheelEvent):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, ZItemView) and widget.isVisible():
                event.ignore()
                return
        current_x = -self._content.x()
        current_y = -self._content.y()

        if event.modifiers() & Qt.ShiftModifier:
            # 水平滚动
            delta = event.angleDelta().x() if event.angleDelta().x() != 0 else event.angleDelta().y()
            step = delta / 120 * 100
            new_x = current_x - step
            self.scrollTo(x=new_x, y=current_y)
        else:
            # 垂直滚动
            delta = event.angleDelta().y()
            step = delta / 120 * 100
            new_y = current_y - step
            self.scrollTo(x=current_x, y=new_y)

        event.accept()


    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = data.Radius
        self._handle_h.bodyColorCtrl.color = data.Handle
        self._handle_v.bodyColorCtrl.color = data.Handle
        self._handle_h.borderColorCtrl.color = data.HandleBorder
        self._handle_v.borderColorCtrl.color = data.HandleBorder
        self._handle_h.update()
        self._handle_v.update()
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)
        self._handle_h.bodyColorCtrl.setColorTo(data.Handle)
        self._handle_v.bodyColorCtrl.setColorTo(data.Handle)
        self._handle_h.borderColorCtrl.setColorTo(data.HandleBorder)
        self._handle_v.borderColorCtrl.setColorTo(data.HandleBorder)
        self._handle_h._trans_timer.start(1200)
        self._handle_v._trans_timer.start(1200)

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
            self._handle_v.positionCtrl.moveTo(
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
            self._handle_h.positionCtrl.moveTo(
                int(handle_pos),
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
        self._content.locationCtrl.moveTo(self._content.x(), -new_scroll_pos)

        # 计算滑块高度
        handle_h= max(30, vh * min(1.0, vh / ch))
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
        self._handle_v.positionCtrl.moveTo(
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
        self._content.locationCtrl.moveTo(new_scroll_pos, self._content.y())

        # 计算滑块宽度
        handle_w = max(30, vw * min(1.0, vw / cw))
        # 计算滑块位置
        handle_space = vw - handle_w
        handle_pos: int = (new_scroll_pos / max_scroll) * handle_space
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
        self._handle_h.positionCtrl.moveTo(
            int(handle_pos),
            self.height() - self._handle_h.height()
        )
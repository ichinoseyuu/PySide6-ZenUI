import logging
from enum import IntEnum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import PositionController,WidgetSizeController,WindowOpacityController,ColorController,FloatController,StyleController
from ZenUI.core import ZDebug,ZToolTipStyleData,ZQuickEffect,ZPosition,ZState,ZWrapMode

# region - ToolTipContent
class ToolTipContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._text: str = ""
        self._font = QFont("Microsoft YaHei", 9)
        self._wrap_mode = ZWrapMode.WrapAnywhere
        self._margins: QMargins = QMargins(10, 8, 10, 8)
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter

        self._text_cc = ColorController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)

        self.setMinimumHeight(28)
        self.setMaximumWidth(300)

    # region Property
    @property
    def textColorCtrl(self) -> ColorController: return self._text_cc

    @property
    def bodyColorCtrl(self) -> ColorController: return self._body_cc

    @property
    def borderColorCtrl(self) -> ColorController: return self._border_cc

    @property
    def radiusCtrl(self) -> FloatController: return self._radius_ctrl

    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    @property
    def wrapMode(self) -> ZWrapMode: return self._wrap_mode

    @wrapMode.setter
    def wrapMode(self, mode: ZWrapMode) -> None:
        self._wrap_mode = mode
        self.adjustSize()
        self.update()


    @property
    def margin(self) -> QMargins: return self._margins

    @margin.setter
    def margin(self, margin: QMargins) -> None:
        self._margins = margin
        self.adjustSize()
        self.update()

    @property
    def alignment(self) -> Qt.AlignmentFlag: return self._alignment

    @alignment.setter
    def alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._alignment = alignment
        self.adjustSize()
        self.update()


    # region Public
    def setText(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    def font(self): return self._font

    def setFont(self, font: QFont | str) -> None:
        if isinstance(font, str):
            self._font.setFamily(font)
        else:
            self._font = font
        self.adjustSize()
        self.update()

    def sizeHint(self):
        m = self._margins
        mw = m.left() + m.right()
        mh = m.top() + m.bottom()
        # 如果没有文本，返回最小尺寸
        if not self._text: return QSize(mw, self.minimumHeight())
        # 文本实际宽度
        fm = QFontMetrics(self._font)
        text_width = fm.horizontalAdvance(self._text) + mw + 1

        if self._wrap_mode == ZWrapMode.NoWrap:
            height = max(fm.height() + mh, self.minimumHeight())
            return QSize(text_width, height)

        # 对于自动换行模式
        if text_width <= self.minimumWidth():
            width = self.minimumWidth()
        elif text_width <= self.maximumWidth():
            width = text_width
        else:
            width = self.maximumWidth()

        height = self.heightForWidth(width)
        return QSize(width, height)

    def adjustSize(self):
        self.resize(self.sizeHint())


    def hasHeightForWidth(self):
        if self._wrap_mode == ZWrapMode.NoWrap: return False
        return True

    def heightForWidth(self, width: int) -> int:
        m = self._margins
        fm = QFontMetrics(self._font)
        rect = fm.boundingRect(0, 0,
                                width,
                                0,
                                self._get_text_flag(),
                                self._text)
        height = max(rect.height() + m.top() + m.bottom(), self.minimumHeight())
        return height

    # region Private
    def _get_text_flag(self) -> Qt.TextFlag:
        """获取文本显示模式"""
        if self._wrap_mode == ZWrapMode.NoWrap:
            return Qt.TextFlag.TextSingleLine | self._alignment
        elif self._wrap_mode == ZWrapMode.WordWrap:
            return Qt.TextFlag.TextWordWrap | self._alignment
        else:
            return Qt.TextFlag.TextWrapAnywhere | self._alignment

    # region Event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing
            )
        # 绘制背景
        rect = self.rect()
        radius = self._radius_ctrl.value
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_cc.color)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._border_cc.color, 1))
        painter.setBrush(Qt.NoBrush)
        # 调整矩形以避免边框模糊
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
            radius,
            radius
        )
        painter.setFont(self._font)
        painter.setPen(self._text_cc.color)
        # 设置文本对齐方式
        text_flags = self._get_text_flag()
        # 计算文本绘制区域
        m = self._margins
        text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        # 绘制文本
        painter.drawText(text_rect, text_flags, self._text)
        painter.end()

# region - ZToolTip
class ZToolTip(QWidget):
    class Mode(IntEnum):
        TrackMouse = 0
        TrackTarget = 1
        AlignTarget = 2
        AlignTargetForEnterPos = 3

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint|
            Qt.WindowType.ToolTip|
            Qt.WindowType.WindowTransparentForInput|
            Qt.WindowType.WindowDoesNotAcceptFocus
            )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self._target: QWidget = None
        self._mode = self.Mode.TrackMouse
        self._position = ZPosition.Top
        self._offset = QPoint(0, 0)

        self._margin = 8 # 边距，用于绘制content的阴影
        self.setMinimumHeight(44) # 最小高度
        self._content = ToolTipContent(self)

        self._location_ctrl = PositionController(self)
        self._location_ctrl.animation.setBias(1)
        self._location_ctrl.animation.setFactor(0.1)

        self._size_ctrl = WidgetSizeController(self)
        self._size_ctrl.animation.setBias(1)
        self._size_ctrl.animation.setFactor(0.1)

        self._opacity_ctrl= WindowOpacityController(self)
        self._opacity_ctrl.animation.setBias(0.02)
        self._opacity_ctrl.animation.setFactor(0.2)
        self._opacity_ctrl.animation.finished.connect(self._completely_hid_signal_handler)

        self._repeat_timer = QTimer() # 节流,防止频繁调用showTip()方法
        self._repeat_timer.setSingleShot(True)

        self._tracker_timer = QTimer()  # mouse move tracker
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._update_pos_for_tracker)

        self._hide_timer = QTimer()
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hideTip)

        self._style_data = StyleController[ZToolTipStyleData](self, 'ZToolTip')
        self._style_data.styleChanged.connect(self._style_change_handler_)
        self._init_style_()
        self.resize(self.sizeHint())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)
        QApplication.instance().installEventFilter(self)

    # region property
    @property
    def state(self) -> ZState:
        if self.windowOpacity() == 0: return ZState.Hidden
        else: return ZState.Showing

    @property
    def isHidden(self) ->bool:
        if self.windowOpacity() == 0: return True
        else: return False

    @property
    def isShowing(self) ->bool:
        if self.windowOpacity() == 0: return False
        else: return True

    @property
    def styleData(self): return self._style_data

    @property
    def mode(self) -> Mode: return self._mode
    @mode.setter
    def mode(self, mode: Mode):
        self._mode = mode
        if mode in [self.Mode.TrackMouse, self.Mode.TrackTarget, self.Mode.AlignTarget]:
            self._tracker_timer.start()
        else:
            self._tracker_timer.stop()


    @property
    def position(self) -> ZPosition: return self._position
    @position.setter
    def position(self, position: ZPosition):
        self._position = position


    @property
    def offset(self) -> QPoint: return self._offset
    @offset.setter
    def offset(self, offset: QPoint):
        self._offset = offset


    @property
    def text(self) -> str: return self._content.text
    @text.setter
    def text(self, text: str) -> None:
        self._content.text = text


    @property
    def target(self): return self._target
    @target.setter
    def target(self, widget):
        self._target = widget
        if self._target is None: self._tracker_timer.stop()

    # region public
    def showTip(self,
                text: str,
                target: QWidget,
                mode: Mode = Mode.TrackMouse,
                position: ZPosition = ZPosition.TopRight,
                offset: QPoint = QPoint(6, 6),
                hide_delay: int = 0,
                ) -> None:
        if self._repeat_timer.isActive(): return
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self.offset = offset
        self.target = target
        self._content.text = text  # 直接设置content的text
        self.position = position
        self.mode = mode
        self.raise_()
        new_pos = self._get_pos_should_be_move()
        distance = new_pos - self.pos()
        if self.windowOpacity() == 0 or distance.manhattanLength() > 150:
            self.resize(self.sizeHint())
            self.move(self._get_initial_pos())
            self._location_ctrl.moveTo(new_pos)
        else:
            self._size_ctrl.resizeTo(self.sizeHint())
            self._location_ctrl.moveTo(new_pos)

        self._opacity_ctrl.fadeIn()
        if hide_delay > 0: self._hide_timer.start(hide_delay)
        self._repeat_timer.start(33)

    def hideTip(self):
        self._opacity_ctrl.fadeOut()

    def hideTipDelayed(self, delay: int):
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self._hide_timer.start(delay)

    def sizeHint(self):
        return self._content.sizeHint() + QSize(2*self._margin, 2*self._margin)


    # region event
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            self._opacity_ctrl.fadeOut()
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.move(self._margin, self._margin)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

    # region private
    def _init_style_(self):
        data = self._style_data.data
        self._content.textColorCtrl.color = data.Text
        self._content.bodyColorCtrl.color = data.Body
        self._content.borderColorCtrl.color = data.Border
        self._content.radiusCtrl.value = data.Radius
        self._content.update()

    def _style_change_handler_(self):
        data = self._style_data.data
        self._content.radiusCtrl.value = data.Radius
        self._content.textColorCtrl.setColorTo(data.Text)
        self._content.bodyColorCtrl.setColorTo(data.Body)
        self._content.borderColorCtrl.setColorTo(data.Border)
        self._content.update()

    def _update_pos_for_tracker(self):
        pos = self._get_pos_should_be_move()
        if self.windowOpacity() == 0:
            self.move(pos)
        else:
            self._location_ctrl.moveTo(pos)
        self.show()


    def _completely_hid_signal_handler(self):
        if self._opacity_ctrl.opacity == 0:
            self.target = None
            self.hide()


    def _get_initial_pos(self) -> QPoint:
        if self._mode == self.Mode.TrackMouse:
            return QCursor.pos() - QPoint(self.width()/2, self.height()/2)
        if self._mode in [self.Mode.TrackTarget, self.Mode.AlignTarget]:
            return self._target.mapToGlobal(self._target.rect().center()) - QPoint(self.width()/2, self.height()/2)
        if self._mode == self.Mode.AlignTargetForEnterPos:
            return QCursor.pos() - QPoint(self.width()/2, self.height()/2)

    def _get_pos_should_be_move(self) -> QPoint:
        m = QCursor.pos()

        if self._target is None: return m

        # condition
        mode = self._mode
        tip_pos = self._position

        # target
        tc = self._target.mapToGlobal(self._target.rect().center())
        tw, th = self._target.width(), self._target.height()
        tt, tl, tb, tr = tc.y() - th//2, tc.x() - tw//2, tc.y() + th//2, tc.x() + tw//2

        # region
        # 计算 target 的边缘(leagcy)
        # topleft = self._target.mapToGlobal(self._target.rect().topLeft())
        # bottomright = self._target.mapToGlobal(self._target.rect().bottomRight())
        # tt, tl, tb, tr = topleft.y(), topleft.x(), bottomright.y(), bottomright.x()
        # endregion

        # self
        w, h  = self.width(), self.height()
        cw, ch = self._content.width(), self._content.height() # content
        margin = self._margin
        offset = self._offset

        if mode == self.Mode.TrackMouse:
            if tip_pos == ZPosition.Top:
                x = m.x() - w//2
                y = m.y() - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.Bottom:
                x = m.x() - w//2
                y = m.y() - margin + offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.Left:
                x = m.x() - cw - margin - offset.x()
                y = m.y() - h//2
                return QPoint(x, y)

            if tip_pos == ZPosition.Right:
                x = m.x() - margin + offset.x()
                y = m.y() - h//2
                return QPoint(x, y)

            if tip_pos == ZPosition.TopLeft:
                x = m.x() - cw - margin - offset.x()
                y = m.y() - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.TopRight:
                x = m.x() - margin + offset.x()
                y = m.y() - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.BottomLeft:
                x = m.x() - cw - margin - offset.x()
                y = m.y() - margin + offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.BottomRight:
                x = m.x() - margin + offset.x()
                y = m.y() - margin + offset.y()
                return QPoint(x, y)

        if mode in [self.Mode.TrackTarget, self.Mode.AlignTarget]:
            if tip_pos == ZPosition.Top:
                x = tc.x() - w//2
                y = tt - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.Bottom:
                x = tc.x() - w//2
                y = tb + offset.y() - margin
                return QPoint(x, y)

            if tip_pos == ZPosition.Left:
                x = tl - cw - margin - offset.x()
                y = tc.y() - h//2
                return QPoint(x, y)

            if tip_pos == ZPosition.Right:
                x = tr - margin + offset.x()
                y = tc.y() - h//2
                return QPoint(x, y)

            if tip_pos == ZPosition.TopLeft:
                x = tl - cw - margin - offset.x()
                y = tt - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.TopRight:
                x = tr - margin + offset.x()
                y = tt - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.BottomLeft:
                x = tl - cw - margin - offset.x()
                y = tb - margin + offset.y()
                return QPoint(x, y)

            if tip_pos == ZPosition.BottomRight:
                x = tr - margin + offset.x()
                y = tb - margin + offset.y()
                return QPoint(x, y)

        if mode == self.Mode.AlignTargetForEnterPos:
            pass


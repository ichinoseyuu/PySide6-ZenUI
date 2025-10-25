import logging
from enum import IntEnum
from re import S
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenWidgets.component.base import (
    QAnimatedColor,
    QAnimatedFloat,
    ZAnimatedWidgetRect,
    StyleController,
    ZWidget,
    ZPadding
)
from ZenWidgets.core import ZDebug,ZToolTipStyleData,ZQuickEffect,ZPosition,ZState,timeit

# region ToolTipContent
class ToolTipContent(ZWidget):
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    textColorCtrl: QAnimatedColor
    styleDataCtrl: StyleController[ZToolTipStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZToolTip'}}

    def __init__(self, parent=None):
        super().__init__(parent=parent, maximumWidth=300, minimumHeight=28)
        self._text: str = ""
        self.setFont(QFont("Microsoft YaHei", 9))
        self._padding = ZPadding(10, 8, 10, 8)
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        self._init_style_()

    # region public
    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, t: str) -> None:
        self._text = t
        self.adjustSize()
        self.update()

    def setText(self, t: str) -> None:
        self.text = t

    @property
    def padding(self) -> ZPadding: return self._padding

    @padding.setter
    def padding(self, p: ZPadding) -> None:
        self._padding = p
        self.adjustSize()
        self.update()

    def setPadding(self, p: ZPadding) -> None:
        self.padding = p

    @property
    def alignment(self) -> Qt.AlignmentFlag: return self._alignment

    @alignment.setter
    def alignment(self, a: Qt.AlignmentFlag) -> None:
        self._alignment = a
        self.adjustSize()
        self.update()

    def setAlignment(self, a: Qt.AlignmentFlag) -> None:
        self.alignment = a

    def sizeHint(self):
        p = self._padding

        if not self._text: return QSize(p.horizontal, self.minimumHeight())

        fm = QFontMetrics(self.font())
        text_width = fm.horizontalAdvance(self._text) + p.horizontal + 1

        if text_width <= self.minimumWidth():
            width = self.minimumWidth()
        elif text_width <= self.maximumWidth():
            width = text_width
        else:
            width = self.maximumWidth()

        height = self.heightForWidth(width)
        return QSize(width, height)

    def adjustSize(self): self.resize(self.sizeHint())

    def hasHeightForWidth(self): return True

    def heightForWidth(self, width: int) -> int:
        p = self._padding
        if not self._text: return max(p.vertical, self.minimumHeight())
        fm = QFontMetrics(self.font())
        rect = fm.boundingRect(
            0, 0, width, 0,
            Qt.TextFlag.TextWrapAnywhere | self._alignment,
            self._text
            )
        height = max(rect.height() + p.vertical, self.minimumHeight())
        return height

    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.textColorCtrl.color = data.Text
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = data.Radius
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.textColorCtrl.setColorTo(data.Text)
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)
        self.update()

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|QPainter.RenderHint.TextAntialiasing)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.bodyColorCtrl.color)
        painter.drawRoundedRect(rect, radius, radius)
        painter.setPen(QPen(self.borderColorCtrl.color, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
            radius, radius
            )
        painter.setFont(self.font())
        painter.setPen(self.textColorCtrl.color)
        p = self._padding
        text_rect = rect.adjusted(p.left, p.top, -p.right, -p.bottom)
        painter.drawText(
            text_rect,
            Qt.TextFlag.TextWrapAnywhere | self._alignment,
            self._text
            )
        painter.end()

# region ZToolTip
class ZToolTip(ZWidget):
    shown = Signal()
    hidden = Signal()

    rectCtrl: ZAnimatedWidgetRect

    class Mode(IntEnum):
        TrackMouse = 0
        TrackTarget = 1

    def __init__(self):
        super().__init__(
            f=Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.ToolTip
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.WindowDoesNotAcceptFocus,
            minimumHeight=44,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self._target: QWidget = None
        self._mode = self.Mode.TrackMouse
        self._position = ZPosition.Top
        self._offset = QPoint(0, 0)
        self._shadow_width = 8
        self._content = ToolTipContent(self)
        self._repeat_timer = QTimer()
        self._repeat_timer.setSingleShot(True)
        self._tracker_timer = QTimer()
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._update_pos_for_tracker)
        self._hide_timer = QTimer()
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hideTip)
        self.windowOpacityCtrl.animation.init(factor=0.2, bias=0.02, current_value=0)
        self.windowOpacityCtrl.completelyHide.connect(self._complete_hide)
        self.windowOpacityCtrl.completelyShow.connect(self.shown.emit)
        self.resize(self.sizeHint())
        self.widgetSizeCtrl.animation.init(factor=0.1, bias=1,current_value=self.size())
        self.widgetPositionCtrl.animation.init(factor=0.1, bias=1,current_value=self.pos())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)
        QApplication.instance().installEventFilter(self)

    # region public
    @property
    def state(self) -> ZState:
        if self.windowOpacity() == 0: return ZState.Hidden
        else: return ZState.Showing

    def isHidden(self) ->bool:
        return True if self.windowOpacity() == 0 else False

    def isShowing(self) ->bool:
        return False if self.windowOpacity() == 0 else True

    @property
    def mode(self) -> Mode: return self._mode

    @mode.setter
    def mode(self, m: Mode):
        self._mode = m

    def setMode(self, mode: Mode):
        self.mode = mode

    @property
    def position(self) -> ZPosition: return self._position

    @position.setter
    def position(self, p: ZPosition):
        self._position = p

    def setPosition(self, position: ZPosition):
        self._position = position

    @property
    def offset(self) -> QPoint: return self._offset

    @offset.setter
    def offset(self, o: QPoint):
        self._offset = o

    def setOffset(self, offset: QPoint):
        self._offset = offset

    @property
    def text(self) -> str: return self._content.text

    @text.setter
    def text(self, t: str):
        self._content.text = t

    def setText(self, text: str) -> None:
        self._content.text = text

    @property
    def target(self): return self._target

    @target.setter
    def target(self, t: QWidget):
        self._target = t
        if self._target is None: self._tracker_timer.stop()

    def setTarget(self, target):
        self.target = target

    def showTip(self, text:str, target:QWidget, mode=Mode.TrackMouse, position=ZPosition.TopRight, offset=QPoint(6, 6), hide_delay:int=0):
        if self._repeat_timer.isActive(): return
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self._target = target
        self.mode = mode
        self._offset = offset
        self._content.text = text
        self._position = position
        self.raise_()
        new_pos = self._get_pos_should_be_move()
        distance = new_pos - self.pos()

        if distance.manhattanLength() > 200:
            self.setWindowOpacity(0)
            self.resize(self.sizeHint())
            self.move(self._get_initial_pos())
            self.show()
            self._tracker_timer.start()
            self.windowOpacityCtrl.fadeIn()
        elif self.windowOpacity() == 0:
            self.resize(self.sizeHint())
            self.move(self._get_initial_pos())
            self.show()
            self._tracker_timer.start()
            self.windowOpacityCtrl.fadeIn()
        else:
            self.widgetSizeCtrl.resizeFromTo(self.size(), self.sizeHint())
            self.widgetPositionCtrl.moveTo(new_pos)
            self.show()
            self._tracker_timer.start()
            self.windowOpacityCtrl.fadeIn()

        if hide_delay > 0: self._hide_timer.start(hide_delay)
        self._repeat_timer.start(33)

    def hideTip(self):
        self.windowOpacityCtrl.fadeOut()
        self.target = None

    def hideTipDelayed(self, delay: int):
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self._hide_timer.start(delay)

    def sizeHint(self):
        return self._content.sizeHint() + QSize(2*self._shadow_width, 2*self._shadow_width)


    # region event
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            self.windowOpacityCtrl.fadeOut()
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.move(self._shadow_width, self._shadow_width)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

    # region private
    def _update_pos_for_tracker(self):
        pos = self._get_pos_should_be_move()
        self.widgetPositionCtrl.moveFromTo(self.pos(), pos)

    def _complete_hide(self):
        self.hide()
        self.hidden.emit()

    def _get_initial_pos(self):
        tip_pos = self._position
        w, h  = self.width(), self.height()
        shadow = self._shadow_width
        offset = self._offset
        if self._mode == self.Mode.TrackMouse:
            m = QCursor.pos()
            cw, ch = self._content.width(), self._content.height()
            if tip_pos == ZPosition.Top:
                return QPoint(m.x() - w//2, m.y() - ch - shadow - offset.y())

            if tip_pos == ZPosition.Bottom:
                return QPoint(m.x() - w//2, m.y() - shadow + offset.y())

            if tip_pos == ZPosition.Left:
                return QPoint(m.x() - cw - shadow - offset.x(), m.y() - h//2)

            if tip_pos == ZPosition.Right:
                return QPoint(m.x() - shadow + offset.x(), m.y() - h//2)

            if tip_pos == ZPosition.TopLeft:
                return QPoint(m.x() - cw - shadow - offset.x(), m.y() - ch - shadow - offset.y())

            if tip_pos == ZPosition.TopRight:
                return QPoint(m.x() - shadow + offset.x(), m.y() - ch - shadow - offset.y())

            if tip_pos == ZPosition.BottomLeft:
                return QPoint(m.x() - cw - shadow - offset.x(), m.y() - shadow + offset.y())

            if tip_pos == ZPosition.BottomRight:
                return QPoint(m.x() - shadow + offset.x(), m.y() - shadow + offset.y())

        if self._mode == self.Mode.TrackTarget:
            tc = self._target.mapToGlobal(self._target.rect().center())
            if tip_pos == ZPosition.Top:
                return tc - QPoint(w//2, h)

            elif tip_pos == ZPosition.Bottom:
                return tc - QPoint(w//2, 0)

            elif tip_pos == ZPosition.Left:
                return tc - QPoint(w, h//2)

            elif tip_pos == ZPosition.Right:
                return tc - QPoint(0, h//2)

            elif tip_pos == ZPosition.TopLeft:
                return tc - QPoint(w, h)

            elif tip_pos == ZPosition.TopRight:
                return tc - QPoint(0, h)

            elif tip_pos == ZPosition.BottomLeft:
                return tc - QPoint(w, 0)

            elif tip_pos == ZPosition.BottomRight:
                return tc

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

        # self
        w, h  = self.width(), self.height()
        cw, ch = self._content.width(), self._content.height() # content
        shadow = self._shadow_width
        offset = self._offset

        if mode == self.Mode.TrackMouse:
            if tip_pos == ZPosition.Top:
                return QPoint(m.x() - w//2, m.y() - ch - shadow - offset.y())

            if tip_pos == ZPosition.Bottom:
                return QPoint(m.x() - w//2, m.y() - shadow + offset.y())

            if tip_pos == ZPosition.Left:
                return QPoint(m.x() - cw - shadow - offset.x(), m.y() - h//2)

            if tip_pos == ZPosition.Right:
                return QPoint(m.x() - shadow + offset.x(), m.y() - h//2)

            if tip_pos == ZPosition.TopLeft:
                return QPoint(m.x() - cw - shadow - offset.x(), m.y() - ch - shadow - offset.y())

            if tip_pos == ZPosition.TopRight:
                return QPoint(m.x() - shadow + offset.x(), m.y() - ch - shadow - offset.y())

            if tip_pos == ZPosition.BottomLeft:
                return QPoint(m.x() - cw - shadow - offset.x(), m.y() - shadow + offset.y())

            if tip_pos == ZPosition.BottomRight:
                return QPoint(m.x() - shadow + offset.x(), m.y() - shadow + offset.y())

        if mode == self.Mode.TrackTarget:
            if tip_pos == ZPosition.Top:
                return QPoint(tc.x() - w//2, tt - ch - shadow - offset.y())

            if tip_pos == ZPosition.Bottom:
                return QPoint(tc.x() - w//2, tb + offset.y() - shadow)

            if tip_pos == ZPosition.Left:
                return QPoint(tl - cw - shadow - offset.x(), tc.y() - h//2)

            if tip_pos == ZPosition.Right:
                return QPoint(tr - shadow + offset.x(), tc.y() - h//2)

            if tip_pos == ZPosition.TopLeft:
                return QPoint(tl - cw - shadow - offset.x(), tt - ch - shadow - offset.y())

            if tip_pos == ZPosition.TopRight:
                return QPoint(tr - shadow + offset.x(), tt - ch - shadow - offset.y())

            if tip_pos == ZPosition.BottomLeft:
                return QPoint(tl - cw - shadow - offset.x(), tb - shadow + offset.y())

            if tip_pos == ZPosition.BottomRight:
                return QPoint(tr - shadow + offset.x(), tb - shadow + offset.y())


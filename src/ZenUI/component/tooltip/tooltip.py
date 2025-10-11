import logging
from enum import IntEnum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import (
    PositionController,
    WidgetSizeController,
    WindowOpacityController,
    ColorController,
    FloatController,
    StyleController,
    ZWidget,
    ZPadding
)
from ZenUI.core import ZDebug,ZToolTipStyleData,ZQuickEffect,ZPosition,ZState,ZWrapMode

# region ToolTipContent
class ToolTipContent(ZWidget):
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    radiusCtrl: FloatController
    textColorCtrl: ColorController
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
    sizeCtrl: WidgetSizeController
    positionCtrl: PositionController
    opacityCtrl: WindowOpacityController

    class Mode(IntEnum):
        TrackMouse = 0
        TrackTarget = 1
        AlignTarget = 2
        AlignTargetForEnterPos = 3

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
        self._margin = 8
        self._content = ToolTipContent(self)
        self._repeat_timer = QTimer()
        self._repeat_timer.setSingleShot(True)
        self._tracker_timer = QTimer()
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._update_pos_for_tracker)
        self._hide_timer = QTimer()
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hideTip)
        self.positionCtrl.animation.setBias(1)
        self.positionCtrl.animation.setFactor(0.1)
        self.sizeCtrl.animation.setBias(1)
        self.sizeCtrl.animation.setFactor(0.1)
        self.opacityCtrl.animation.setBias(0.02)
        self.opacityCtrl.animation.setFactor(0.2)
        self.opacityCtrl.animation.finished.connect(self._completely_hid_signal_handler)
        self.resize(self.sizeHint())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)
        QApplication.instance().installEventFilter(self)

    # region public
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
    def mode(self) -> Mode: return self._mode

    @mode.setter
    def mode(self, m: Mode):
        self._mode = m
        if m in [self.Mode.TrackMouse, self.Mode.TrackTarget, self.Mode.AlignTarget]:
            self._tracker_timer.start()
        else:
            self._tracker_timer.stop()

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
            self.positionCtrl.moveTo(new_pos)
        else:
            self.sizeCtrl.resizeTo(self.sizeHint())
            self.positionCtrl.moveTo(new_pos)

        self.opacityCtrl.fadeIn()
        if hide_delay > 0: self._hide_timer.start(hide_delay)
        self._repeat_timer.start(33)

    def hideTip(self):
        self.opacityCtrl.fadeOut()

    def hideTipDelayed(self, delay: int):
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self._hide_timer.start(delay)

    def sizeHint(self):
        return self._content.sizeHint() + QSize(2*self._margin, 2*self._margin)


    # region event
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            self.opacityCtrl.fadeOut()
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
    def _update_pos_for_tracker(self):
        pos = self._get_pos_should_be_move()
        if self.windowOpacity() == 0:
            self.move(pos)
        else:
            self.positionCtrl.moveTo(pos)
        self.show()


    def _completely_hid_signal_handler(self):
        if self.opacityCtrl.opacity == 0:
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


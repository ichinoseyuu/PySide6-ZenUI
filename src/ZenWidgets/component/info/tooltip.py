import logging
from enum import IntEnum, auto
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRectF,QSize,QPoint,QTimer,QElapsedTimer
from PySide6.QtGui import QFont,QFontMetrics,QPainter,QPen,QCursor
from ZenWidgets.component.base import (
    ZFlashEffect,
    ZAnimatedColor,
    ZAnimatedFloat,
    ZStyleController,
    ZWidget
)
from ZenWidgets.core import ZDebug,ZPosition,ZPadding
from ZenWidgets.gui import ZToolTipStyleData,ZWidgetEffect

# region ToolTipContent
class ToolTipContent(ZWidget):
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: ZAnimatedFloat
    flashCtrl: ZFlashEffect
    textColorCtrl: ZAnimatedColor
    styleDataCtrl: ZStyleController[ZToolTipStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZToolTip'}}

    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            maximumWidth=300,
            minimumHeight=28,
            font=QFont("Microsoft YaHei", 9)
            )
        self._text: str = ""
        self._padding = ZPadding(10, 8, 10, 8)
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        self._init_style_()

    # region public
    def text(self) -> str: return self._text

    def setText(self, t: str,/,flash: bool = False) -> None:
        if flash or self._text != t: self.flashCtrl.flash(0.3)
        self._text = t
        self.adjustSize()
        self.update()

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
        self.radiusCtrl.value = 5.0

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.textColorCtrl.setColorTo(data.Text)
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)

    # region event
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|QPainter.RenderHint.TextAntialiasing)
        rect = QRectF(self.rect())
        radius = self.radiusCtrl.value
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.bodyColorCtrl.color)
        painter.drawRoundedRect(rect, radius, radius)
        painter.setPen(QPen(self.borderColorCtrl.color, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),radius, radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.flashCtrl.color)
        painter.drawRoundedRect(rect, radius, radius)
        painter.setFont(self.font())
        painter.setPen(self.textColorCtrl.color)
        p = self._padding
        text_rect = rect.adjusted(p.left, p.top, -p.right, -p.bottom)
        painter.drawText(text_rect,Qt.TextFlag.TextWrapAnywhere | self._alignment,self._text)
        painter.end()

# region ZToolTip
class ZToolTip(ZWidget):
    class Mode(IntEnum):
        TrackMouse = auto()
        TrackTarget = auto()

    def __init__(self):
        super().__init__(
            f=Qt.WindowType.FramelessWindowHint|
            Qt.WindowType.WindowStaysOnTopHint|
            Qt.WindowType.WindowTransparentForInput|
            Qt.WindowType.Tool,
            minimumHeight=44,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self._content = ToolTipContent(self)
        self._target: QWidget = None
        self._mode = self.Mode.TrackMouse
        self._position = ZPosition.Top
        self._offset = QPoint(0, 0)
        self._shadow_width = 8
        self._show_cd = 33
        self._cd_timer = QElapsedTimer()

        self._tracker_timer = QTimer()
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._update_pos_for_tracker)

        self._show_timer = QTimer(singleShot=True, interval=1000)
        self._hide_timer = QTimer(singleShot=True)
        self._hide_timer.timeout.connect(self.hideTip)

        self.windowOpacityCtrl.animation.init(factor=0.2, bias=0.02, current_value=0)
        self.windowOpacityCtrl.completelyHide.connect(self.hide)

        self.widgetSizeCtrl.animation.init(factor=0.1, bias=1)
        self.widgetPositionCtrl.animation.init(factor=0.1, bias=1)
        ZWidgetEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)
        self.resize(self.sizeHint())

    # region public
    def mode(self) -> Mode: return self._mode

    def position(self) -> ZPosition: return self._position

    def offset(self) -> QPoint: return self._offset

    def text(self) -> str: return self._content.text()

    def target(self): return self._target

    def setText(self, text: str, flash: bool = False):
        self._content.setText(text, flash)

    def showTip(self,
                text: str,
                target: QWidget,
                mode: Mode = Mode.TrackMouse,
                position: ZPosition = ZPosition.Top,
                offset: QPoint = QPoint(0, 0),
                hide_delay: int = 0,
                flash: bool = False):
        if self._cd_timer.isValid() and self._cd_timer.elapsed() < self._show_cd: return
        if self._hide_timer.isActive(): self._hide_timer.stop()
        if self._show_timer.isActive(): self._show_timer.stop()
        self._target = target
        self._mode = mode
        self._offset = offset
        self._content.setText(text, flash)
        self._position = position
        if self.windowOpacity() == 0:
            self.resize(self.sizeHint())
            self.move(self._get_initial_pos())
            self._tracker_timer.start()
            self.windowOpacityCtrl.fadeIn()
        else:
            new_pos = self._get_pos_should_be_move()
            if (new_pos - self.pos()).manhattanLength() > 200:
                self.resize(self.sizeHint())
                self.move(self._get_initial_pos())
                self._tracker_timer.start()
                self.windowOpacityCtrl.fadeTo(.0, 1.0)
            else:
                self.widgetSizeCtrl.resizeFromTo(self.size(), self.sizeHint())
                self.widgetPositionCtrl.moveFromTo(self.pos(), new_pos)
                self._tracker_timer.start()
                self.windowOpacityCtrl.fadeTo(1.0)

        self.raise_()
        self.show()
        if hide_delay > 0: self._hide_timer.start(hide_delay)
        self._cd_timer.start()

    def hideTip(self):
        self.windowOpacityCtrl.fadeOut()
        self._target = None
        if self._tracker_timer.isActive():self._tracker_timer.stop()

    def hideTipDelayed(self, delay: int):
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self._hide_timer.start(delay)

    def sizeHint(self):
        return self._content.sizeHint() + QSize(2*self._shadow_width, 2*self._shadow_width)

    # region event
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
        self.widgetPositionCtrl.moveFromTo(self.pos(), self._get_pos_should_be_move())


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


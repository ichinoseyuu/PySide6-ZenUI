import logging
from enum import Enum, IntEnum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import LocationController,SizeController,WindowOpacityController,StyleData
from ZenUI.core import ZGlobal,ZToolTipStyleData,TipPos,ZQuickEffect
from .tooltipcontent import ZToolTipContent

class ZToolTip(QWidget):
    class State(Enum):
        Hidden = 0
        Showing = 1

    class Mode(IntEnum):
        TrackMouse = 0
        TrackTarget = 1
        AlignTarget = 2
        AlignTargetForEnterPos = 3

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|
                            Qt.WindowType.ToolTip|
                            Qt.WindowType.WindowTransparentForInput|
                            Qt.WindowType.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self._target: QWidget = None
        self._mode = self.Mode.TrackMouse
        self._position = TipPos.Top
        self._offset = QPoint(0, 0)

        self._margin = 8 # 边距，用于绘制content的阴影
        self.setMinimumHeight(44) # 最小高度
        self._content = ZToolTipContent(self)

        self._location_ctrl = LocationController(self)
        self._location_ctrl.animation.setBias(1)
        self._location_ctrl.animation.setFactor(0.1)

        self._size_ctrl = SizeController(self)
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

        self._style_data = StyleData[ZToolTipStyleData](self, 'ZToolTip')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()
        self.resize(self.sizeHint())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)
        #阴影设置在content上，在切换window主题时才不会产生阴影绘制错误


    @property
    def state(self) -> State:
        if self.windowOpacity() == 0: return self.State.Hidden
        else: return self.State.Showing

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
    def position(self) -> TipPos: return self._position
    @position.setter
    def position(self, position: TipPos):
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


    def _initStyle(self):
        data = self._style_data.data
        self._content.textColorCtrl.color = data.Text
        self._content.bodyColorCtrl.color = data.Body
        self._content.borderColorCtrl.color = data.Border
        self._content.radiusCtrl.value = data.Radius
        self._content.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._content.radiusCtrl.value = data.Radius
        self._content.textColorCtrl.setColorTo(data.Text)
        self._content.bodyColorCtrl.setColorTo(data.Body)
        self._content.borderColorCtrl.setColorTo(data.Border)
        self._content.update()

    def showTip(self,
                text: str,
                target: QWidget,
                mode: Mode = Mode.TrackMouse,
                position: TipPos = TipPos.TopRight,
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
        #self.target = None
        self._opacity_ctrl.fadeOut()

    def hideTipDelayed(self, delay: int):
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self._hide_timer.start(delay)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.move(self._margin, self._margin)

    def sizeHint(self):
        return self._content.sizeHint() + QSize(2*self._margin, 2*self._margin)

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
            if tip_pos == TipPos.Top:
                x = m.x() - w//2
                y = m.y() - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.Bottom:
                x = m.x() - w//2
                y = m.y() - margin + offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.Left:
                x = m.x() - cw - margin - offset.x()
                y = m.y() - h//2
                return QPoint(x, y)

            if tip_pos == TipPos.Right:
                x = m.x() - margin + offset.x()
                y = m.y() - h//2
                return QPoint(x, y)

            if tip_pos == TipPos.TopLeft:
                x = m.x() - cw - margin - offset.x()
                y = m.y() - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.TopRight:
                x = m.x() - margin + offset.x()
                y = m.y() - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.BottomLeft:
                x = m.x() - cw - margin - offset.x()
                y = m.y() - margin + offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.BottomRight:
                x = m.x() - margin + offset.x()
                y = m.y() - margin + offset.y()
                return QPoint(x, y)

        if mode in [self.Mode.TrackTarget, self.Mode.AlignTarget]:
            if tip_pos == TipPos.Top:
                x = tc.x() - w//2
                y = tt - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.Bottom:
                x = tc.x() - w//2
                y = tb + offset.y() - margin
                return QPoint(x, y)

            if tip_pos == TipPos.Left:
                x = tl - cw - margin - offset.x()
                y = tc.y() - h//2
                return QPoint(x, y)

            if tip_pos == TipPos.Right:
                x = tr - margin + offset.x()
                y = tc.y() - h//2
                return QPoint(x, y)

            if tip_pos == TipPos.TopLeft:
                x = tl - cw - margin - offset.x()
                y = tt - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.TopRight:
                x = tr - margin + offset.x()
                y = tt - ch - margin - offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.BottomLeft:
                x = tl - cw - margin - offset.x()
                y = tb - margin + offset.y()
                return QPoint(x, y)

            if tip_pos == TipPos.BottomRight:
                x = tr - margin + offset.x()
                y = tb - margin + offset.y()
                return QPoint(x, y)

        # region
        # if mode == self.Mode.AlignTarget:
        #     if tip_pos == self.TipPos.Top:
        #         x = tc.x() - w//2
        #         y = tt - ch - margin - offset.y()
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.Bottom:
        #         x = tc.x() - w//2
        #         y = tb + offset.y() - margin
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.Left:
        #         x = tl - cw - margin - offset.x()
        #         y = tc.y() - h//2
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.Right:
        #         x = tr - margin + offset.x()
        #         y = tc.y() - h//2
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.TopLeft:
        #         x = tl - cw - margin - offset.x()
        #         y = tt - ch - margin - offset.y()
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.TopRight:
        #         x = tr - margin + offset.x()
        #         y = tt - ch - margin - offset.y()
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.BottomLeft:
        #         x = tl - cw - margin - offset.x()
        #         y = tb - margin + offset.y()
        #         return QPoint(x, y)

        #     if tip_pos == self.TipPos.BottomRight:
        #         x = tr - margin + offset.x()
        #         y = tb - margin + offset.y()
        #         return QPoint(x, y)
        # endregion

        if mode == self.Mode.AlignTargetForEnterPos:
            pass

    # region
    # @timeit
    # def _get_pos_should_be_move(self) -> QPoint:
    #     m = QCursor.pos()
    #     if self._target is None: 
    #         return m

    #     # 计算目标位置和尺寸
    #     tc = self._target.mapToGlobal(self._target.rect().center())
    #     tw, th = self._target.width(), self._target.height()
    #     tt, tl, tb, tr = tc.y() - th//2, tc.x() - tw//2, tc.y() + th//2, tc.x() + tw//2

    #     # 计算自身尺寸
    #     w, h = self.width(), self.height()
    #     cw, ch = self._content.width(), self._content.height()
    #     margin = self._margin
    #     offset = self._offset

    #     # 定义位置计算字典
    #     pos_calculators = {
    #         # TrackMouse模式的位置计算
    #         (self.Mode.TrackMouse, self.TipPos.Top): lambda: QPoint(
    #             m.x() - w//2,
    #             m.y() - ch - margin - offset.y()
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.Bottom): lambda: QPoint(
    #             m.x() - w//2,
    #             m.y() - margin + offset.y()
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.Left): lambda: QPoint(
    #             m.x() - cw - margin - offset.x(),
    #             m.y() - h//2
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.Right): lambda: QPoint(
    #             m.x() - margin + offset.x(),
    #             m.y() - h//2
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.TopLeft): lambda: QPoint(
    #             m.x() - cw - margin - offset.x(),
    #             m.y() - ch - margin - offset.y()
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.TopRight): lambda: QPoint(
    #             m.x() - margin + offset.x(),
    #             m.y() - ch - margin - offset.y()
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.BottomLeft): lambda: QPoint(
    #             m.x() - cw - margin - offset.x(),
    #             m.y() + offset.y()
    #         ),
    #         (self.Mode.TrackMouse, self.TipPos.BottomRight): lambda: QPoint(
    #             m.x() - margin + offset.x(),
    #             m.y() - margin + offset.y()
    #         ),

    #         # TrackTarget模式的位置计算
    #         (self.Mode.TrackTarget, self.TipPos.Top): lambda: QPoint(
    #             tc.x() - w//2,
    #             tt - ch - margin - offset.y()
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.Bottom): lambda: QPoint(
    #             tc.x() - w//2,
    #             tb + offset.y() - margin
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.Left): lambda: QPoint(
    #             tl - cw - margin - offset.x(),
    #             tc.y() - h//2
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.Right): lambda: QPoint(
    #             tr - margin + offset.x(),
    #             tc.y() - h//2
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.TopLeft): lambda: QPoint(
    #             tl - cw - margin - offset.x(),
    #             tt - ch - margin - offset.y()
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.TopRight): lambda: QPoint(
    #             tr - margin + offset.x(),
    #             tt - ch - margin - offset.y()
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.BottomLeft): lambda: QPoint(
    #             tl - cw - margin - offset.x(),
    #             tb - margin + offset.y()
    #         ),
    #         (self.Mode.TrackTarget, self.TipPos.BottomRight): lambda: QPoint(
    #             tr - margin + offset.x(),
    #             tb - margin + offset.y()
    #         ),

    #         # AlignTarget模式的位置计算
    #         (self.Mode.AlignTarget, self.TipPos.Top): lambda: QPoint(
    #             tc.x() - w//2,
    #             tt - ch - margin - offset.y()
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.Bottom): lambda: QPoint(
    #             tc.x() - w//2,
    #             tb + offset.y() - margin
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.Left): lambda: QPoint(
    #             tl - cw - margin - offset.x(),
    #             tc.y() - h//2
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.Right): lambda: QPoint(
    #             tr - margin + offset.x(),
    #             tc.y() - h//2
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.TopLeft): lambda: QPoint(
    #             tl - cw - margin - offset.x(),
    #             tt - ch - margin - offset.y()
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.TopRight): lambda: QPoint(
    #             tr - margin + offset.x(),
    #             tt - ch - margin - offset.y()
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.BottomLeft): lambda: QPoint(
    #             tl - cw - margin - offset.x(),
    #             tb - margin + offset.y()
    #         ),
    #         (self.Mode.AlignTarget, self.TipPos.BottomRight): lambda: QPoint(
    #             tr - margin + offset.x(),
    #             tb - margin + offset.y()
    #         ),

    #         # AlignTargetForEnterPos模式的位置计算（暂留空）

    #     }

    #     calculator = pos_calculators.get((self._mode,self._position))
    #     if calculator:
    #         return calculator()

    #     return QCursor.pos()
    # endregion

import logging
from enum import Enum, IntEnum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import LocationManager,SizeManager,WindowOpacityManager
from ZenUI.core import ZGlobal,ZToolTipStyleData,ZQuickEffect,TipPos
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
                            Qt.WindowType.WindowStaysOnTopHint|
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._target: QWidget = None
        self._mode = self.Mode.TrackMouse
        self._position = TipPos.Top
        self._offset = QPoint(0, 0)

        self._margin = 8 # content margin for tooltip

        self._content = ZToolTipContent(self)

        self._location_mgr = LocationManager(self)
        self._location_mgr.animation.setBias(1)
        self._location_mgr.animation.setFactor(0.1)

        self._size_mgr = SizeManager(self)
        self._size_mgr.animation.setBias(1)
        self._size_mgr.animation.setFactor(0.1)

        self._opacity_mgr= WindowOpacityManager(self)
        self._opacity_mgr.animation.setBias(0.02)
        self._opacity_mgr.animation.setFactor(0.2)
        self._opacity_mgr.animation.finished.connect(self._completely_hid_signal_handler)

        self._repeat_timer = QTimer() # 节流,防止频繁调用showTip()方法
        self._repeat_timer.setSingleShot(True)

        self._tracker_timer = QTimer()  # mouse move tracker
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._update_pos_for_tracker)

        self._hide_timer = QTimer()
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hideTip)

        self._style_data: ZToolTipStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

        ZQuickEffect.applyDropShadowOn(widget=self,color=(0, 0, 0, 40),blur_radius=12)


    @property
    def state(self) -> State:
        if self.windowOpacity() == 0: return self.State.Hidden
        else: return self.State.Showing

    @property
    def mode(self) -> Mode: return self._mode
    @mode.setter
    def mode(self, mode: Mode):
        self._mode = mode
        if mode in [self.Mode.TrackMouse, self.Mode.TrackTarget]:
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


    @property
    def styleData(self) -> ZToolTipStyleData: return self._style_data
    @styleData.setter
    def styleData(self, data: ZToolTipStyleData):
        self._style_data = data
        self._content.textColorMgr.color = data.Text
        self._content.bodyColorMgr.color = data.Body
        self._content.borderColorMgr.color = data.Border
        self._content.radiusMgr.value = data.Radius
        self._content.update()


    def themeChangeHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__, theme.name)
        self._style_data = data
        self._content.radiusMgr.value = data.Radius
        self._content.textColorMgr.setColorTo(data.Text)
        self._content.bodyColorMgr.setColorTo(data.Body)
        self._content.borderColorMgr.setColorTo(data.Border)
        self._content.update()


    def showTip(self,
                text: str,
                target: QWidget,
                mode: Mode = Mode.TrackMouse,
                position: TipPos = TipPos.TopLeft,
                offset: QPoint = QPoint(0, 0),
                hide_delay: int = 0,
                ) -> None:
        if self._repeat_timer.isActive(): return
        if self._hide_timer.isActive(): self._hide_timer.stop()
        self.offset = offset
        self.target = target
        self._content.text = text  # 直接设置content的text
        self.position = position
        self.mode = mode

        # region 
        # tooltip 透明度为0时，直接设置大小和位置(leagcy)
        # # 计算新的大小和位置
        # new_size = self._get_size_should_be_resize()
        # new_pos = self._get_pos_should_be_move()

        # # 如果tooltip是隐藏状态，直接设置大小和位置
        # if self.windowOpacity() == 0:
        #     self.resize(new_size)
        #     self.move(new_pos)
        # else:
        #     # 如果tooltip已经显示，使用动画过渡
        #     self._resize_anim.resizeTo(new_size)
        #     self._move_anim.moveTo(new_pos)
        # 计算新的大小和位置
        # endregion
        new_pos = self._get_pos_should_be_move()
        distance = new_pos - self.pos()
        if self.windowOpacity() == 0 or distance.manhattanLength() > 150:
            self.resize(self.sizeHint())
            self.move(self._get_initial_pos())
            self._location_mgr.moveTo(new_pos)
        else:
            self._size_mgr.resizeTo(self.sizeHint())
            self._location_mgr.moveTo(new_pos)

        self._opacity_mgr.fadeIn()
        if hide_delay > 0: self._hide_timer.start(hide_delay)
        self._repeat_timer.start(33)

    def hideTip(self):
        #self.target = None
        self._opacity_mgr.fadeOut()

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
            self._location_mgr.moveTo(pos)


    def _update_size(self):
        size = self._get_size_should_be_resize()
        if self.windowOpacity() == 0:
            self.resize(size)
        else:
            self._size_mgr.resizeTo(size)


    def _completely_hid_signal_handler(self):
        if self._opacity_mgr.opacity == 0:
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

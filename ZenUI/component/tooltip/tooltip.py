import logging
from enum import Enum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import MoveExpAnimation,ResizeExpAnimation,WindowOpacityExpAnimation
from ZenUI.component.navigationbar import ZNavBarButton,ZNavBarToggleButton
from ZenUI.component.slider import ZSlider
from ZenUI.core import ZGlobal,ZToolTipStyleData,ZQuickEffect
from .tooltipcontent import ZToolTipContent

class ZToolTip(QWidget):
    class State(Enum):
        Hidden = 0
        Showing = 1
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|
                            Qt.WindowType.WindowStaysOnTopHint|
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._state = self.State.Hidden
        self._inside_of: QWidget = None
        self._margin = 8

        self._content = ZToolTipContent(self)

        self._move_anim = MoveExpAnimation(self)
        self._move_anim.animation.setBias(0.5)
        self._move_anim.animation.setFactor(0.15)
        self._opacity_anim= WindowOpacityExpAnimation(self)
        self._opacity_anim.animation.setBias(0.05)
        self._opacity_anim.animation.setFactor(0.2)
        self._opacity_anim.animation.finished.connect(self._completely_hid_signal_handler)
        self._resize_anim = ResizeExpAnimation(self)
        self._resize_anim.animation.setBias(0.5)
        self._resize_anim.animation.setFactor(0.15)

        self._style_data: ZToolTipStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData('ZToolTip')

        self._tracker_timer = QTimer()  # mouse move tracker
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._update_pos)

        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)
        ZQuickEffect.applyDropShadowOn(widget=self,color=(0, 0, 0, 40),blur_radius=12)

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State):
        self._state = state



    @property
    def styleData(self) -> ZToolTipStyleData:
        return self._style_data

    @styleData.setter
    def styleData(self, data: ZToolTipStyleData):
        self._style_data = data
        self._content.textStyle.color = data.Text
        self._content.backgroundStyle.color = data.Body
        self._content.borderStyle.color = data.Border
        self._content.cornerStyle.radius = data.Radius
        self._content.update()

    def themeChangeHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData('ZToolTip', theme.name)
        self._style_data = data
        self._content.cornerStyle.radius = data.Radius
        self._content.textStyle.setColorTo(data.Text)
        self._content.backgroundStyle.setColorTo(data.Body)
        self._content.borderStyle.setColorTo(data.Border)
        self._content.update()

    def insideOf(self):
        return self._inside_of

    def setInsideOf(self, widget):
        self._inside_of = widget
        if widget is None:
            self._tracker_timer.stop()
            return
        self._tracker_timer.start()
        pos = self._get_pos_should_be_move()
        self.move(pos)


    def setText(self, text: str, flash: bool = True) -> None:
        if flash and self._content.text != text: self._flash()
        self._content.text = text
        self._update_size()
        #QTimer.singleShot(0, self._update_size)



    def _update_size(self):
        self._content.adjustSize() # adjust size to content
        size = self._content.size() + QSize(2*self._margin, 2*self._margin)
        self._resize_anim.resizeTo(size)


    def _flash(self):
        pass


    def _completely_hid_signal_handler(self):
        if self._opacity_anim.opacity == 0:
            self.resize(2*self._margin, self._content.minimumHeight() + 2*self._margin)
            self._content.text = ''
            self._state = self.State.Hidden
        else:
            self._state = self.State.Showing


    def _update_pos(self):
        pos = self._get_pos_should_be_move()
        self._move_anim.moveTo(pos)


    def _get_pos_should_be_move(self) -> QPoint:
        if isinstance(self._inside_of, (ZNavBarButton, ZNavBarToggleButton)):
            offset = QPoint(self._inside_of.width(), (self._inside_of.height()-self.height())/2)
            pos = self._inside_of.mapToGlobal(offset)
            return pos

        if isinstance(self._inside_of, ZSlider):
            handle = self._inside_of.handle
            ancher = handle.mapToGlobal(handle.rect().center())
            if self._inside_of.orientation == ZSlider.Orientation.Horizontal:
                x = ancher.x() - self.width() / 2  # 水平居中对齐
                y = ancher.y() - self.height() - 6  # 显示在滑块上方，留出6px间距
                return QPoint(x, y)
            x = ancher.x() - self.width() - 6 # 显示在滑块右侧，留出6px间距
            y = ancher.y() - self.height() / 2  # 垂直居中对齐
            return QPoint(x, y)

        pos = QCursor.pos()
        x, y = pos.x()-self.width()/2, pos.y()-self.height()
        return QPoint(x, y)

    def showTip(self):
        self._opacity_anim.fadeIn()


    def hideTip(self):
        self._opacity_anim.fadeOut()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = event.size().height()
        self._content.move(self._margin, h - self._content.height() - self._margin)
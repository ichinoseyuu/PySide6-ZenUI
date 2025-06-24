import logging
from enum import Enum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import MoveExpAnimation,ResizeExpAnimation,WindowOpacityExpAnimation
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

        self._tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._refresh_position)

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
        self._content.textStyle.color = QColor(data.text)
        self._content.backgroundStyle.color = QColor(data.body)
        self._content.borderStyle.color = QColor(data.border)
        self._content.cornerStyle.radius = data.radius
        self._content.update()

    def themeChangeHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData('ZToolTip', theme.name)
        self._style_data = data
        self._content.cornerStyle.radius = data.radius
        self._content.textStyle.setColorTo(QColor(data.text))
        self._content.backgroundStyle.setColorTo(QColor(data.body))
        self._content.borderStyle.setColorTo(QColor(data.border))
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
        self._refresh_size()
        #QTimer.singleShot(0, self._refresh_size)



    def _refresh_size(self):
        self._content.adjustSize() # 调整内容大小
        size = self._content.size() + QSize(2*self._margin, 2*self._margin)
        self._resize_anim.resizeTo(size)# 设为文字标签的大小加上阴影间距


    def _flash(self):
        pass


    def _completely_hid_signal_handler(self):
        if self._opacity_anim.opacity == 0:
            self.resize(2*self._margin, self._content.minimumHeight()+2*self._margin)
            self._content.text = ''
            self._state = self.State.Hidden
        else:
            self._state = self.State.Showing


    def _refresh_position(self):
        '更新位置'
        pos = self._get_pos_should_be_move()
        self._move_anim.moveTo(pos)


    def _get_pos_should_be_move(self):
        pos = QCursor.pos()
        x, y = pos.x()-self.width()/2, pos.y()-self.height()
        return QPoint(x, y)

    def showTip(self):
        '显示工具提示'
        self._opacity_anim.fadeIn()


    def hideTip(self):
        '隐藏工具提示'
        self._opacity_anim.fadeOut()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = event.size().height()
        self._content.move(self._margin, h - self._content.height() - self._margin)
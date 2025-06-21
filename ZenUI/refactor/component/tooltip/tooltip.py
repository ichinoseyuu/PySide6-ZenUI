from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.refactor.core import (ZGlobal,ZToolTipStyleData,MoveExpAnimation,
                                 ResizeExpAnimation,OpacityExpAnimation,ZQuickEffect)
from .tooltipcontent import ZToolTipContent
import logging
class ZToolTip(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ZToolTip")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|
                            Qt.WindowType.WindowStaysOnTopHint|
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.setStyleSheet("background-color: transparent; border: 1px solid red;")
        self._inside_of: QWidget = None
        self._margin = 8
        self._content = ZToolTipContent(self)
        self._move_anim = MoveExpAnimation(self)
        self._opacity_anim= OpacityExpAnimation(self)
        self._resize_anim = ResizeExpAnimation(self)
        self._opacity_anim.animation.finished.connect(self._completely_hid_signal_handler)
        self._style_data: ZToolTipStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData('ZToolTip')
        self._tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._refresh_position)
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)
        ZQuickEffect.applyDropShadowOn(widget=self,
                        color=(0, 0, 0, 40),
                        blur_radius=12)

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


    def _completely_hid_signal_handler(self):
        if self._opacity_anim.opacity == 0:
            self.resize(2 * self._margin, 36 + 2 * self._margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self._content.text = ''  # 清空文本内容
            logging.info('完全隐藏')
        else:
            logging.info('不完全隐藏')


    def _refresh_position(self):
        '更新位置'
        pos = self._get_pos_should_be_move()
        self._move_anim.moveTo(pos)


    def _get_pos_should_be_move(self):
        '获取应该移动到的位置'
        pos = QCursor.pos()
        x, y = pos.x()-self.width()/2, pos.y()-self.height()
        return QPoint(x, y)

    def setInsideOf(self, widget):
        """设置当前位于哪个控件内部"""
        self._inside_of = widget
        if widget is None:
            self._tracker_timer.stop()
            return
        self._tracker_timer.start()
        pos = self._get_pos_should_be_move()
        self.move(pos)

    def insideOf(self):
        """返回最后一次被调用显示时的发出者"""
        return self._inside_of


    def setText(self, text: str, flash: bool = True) -> None:
        """设置提示文本内容"""
        if self._content.text == text: return
        self._content.text = text
        #self._refresh_text(flash)
        QTimer.singleShot(0, lambda: self._refresh_text(flash))


    def _refresh_text(self, flash: bool):
        """刷新文本显示"""
        self._refresh_size()
        # if flash: self.flash()


    def _refresh_size(self):
        """用于设置大小动画结束值并启动动画"""
        self._content.adjustSize()
        logging.info(f'刷新大小{self._content.sizeHint()}')
        w, h = self._content.width(), self._content.height()
        self._resize_anim.resizeTo(QSize(w + 2*self._margin, h + 2*self._margin))# 设为文字标签的大小加上阴影间距


    # def flash(self):
    #     '闪烁效果'
    #     self._layer_highlight.setColor(self._colors.flash)
    #     self._layer_highlight.setColorTo(ZColorTool.trans(self._colors.flash))


    def showTip(self):
        '显示工具提示'
        self._opacity_anim.fadeIn()


    def hideTip(self):
        '隐藏工具提示'
        self._opacity_anim.fadeOut()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        h =size.height()
        self._content.move(self._margin, h - self._content.height() - self._margin)



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|
                            Qt.WindowType.WindowStaysOnTopHint)
    def enterEvent(self, event):
        super().enterEvent(event)
        tooltip.setInsideOf(window)
        tooltip.setText("这是一个提示框")
        tooltip.showTip()
        print(tooltip.size(),tooltip.adjustSize())

    def leaveEvent(self, event):
        super().leaveEvent(event)
        tooltip.setInsideOf(None)
        tooltip.hideTip()

if __name__ == '__main__':
    app = QApplication([])
    tooltip = ZToolTip()
    window = Window()
    window.resize(400, 300)
    window.show()
    app.exec()
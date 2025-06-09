from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.label import ZTextLabel
from ZenUI.component.slider import ZSlider
from ZenUI.component.tooltip.layer import ToolTipLayer
from ZenUI.component.tooltip.config import ToolTipConfig
from ZenUI.core import ZQuickEffect, Zen, ZColorTool


class ZToolTip(ZWidget):
    """提示框
    - 自动跟随鼠标或目标控件
    - 支持富文本显示
    - 主题切换
    - 显示/隐藏动画
    - 闪烁特效
    """
    def __init__(self):
        super().__init__(name='tooltip')
        self.setWindowFlags(Qt.FramelessWindowHint|
                            Qt.WindowStaysOnTopHint|
                            Qt.Tool |
                            Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._is_shown = False
        '是否已经显示'
        self._completely_hide = False
        '是否已经完全隐藏'
        self._inside_of: QWidget = None
        '鼠标悬停的控件'
        self._margin = ToolTipConfig.MARGIN
        '给阴影预留的间隔空间'
        self._layer_background = ToolTipLayer(self)
        self._layer_background.move(self._margin, self._margin)
        self._board = QWidget(self)
        self._label_text = ZTextLabel(parent=self._board,word_wrap=True)
        self._label_text.setFixedStyleSheet(f"padding: {ToolTipConfig.PADDING}px")
        self._label_text.setWidgetFlag(Zen.WidgetFlag.InstantResize)
        self._label_text.setWidgetFlag(Zen.WidgetFlag.AdjustSizeOnTextChanged)
        self._board.move(self._margin, self._margin)
        self._layer_highlight = ToolTipLayer(self)
        self._layer_highlight.move(self._margin, self._margin)
        self._init_style()
        #self.setText("", flash=False) # 通过输入空文本初始化大小
        ZQuickEffect.applyDropShadowOn(widget=self,
                        color=ToolTipConfig.SHADOW_COLOR,
                        blur_radius=ToolTipConfig.SHADOW_BLUR)
        self.updateStyle()


    def _init_anim(self):
        super()._init_anim()
        self._tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._refresh_position)
        # 当透明度动画结束时处理隐藏与否
        self.AnimGroup().fromToken("opacity").finished.connect(
            self._completely_hid_signal_handler
            )

    def _init_style(self):
        self._color_sheet.loadColorConfig(Zen.WidgetType.ToolTip)
        self._colors.overwrite(self._color_sheet.getSheet())
        self._layer_background._bg_color_a = self._colors.background_a
        self._layer_background._border_color = self._colors.border
        self._layer_background.set_style_getter('background_color', lambda: self._layer_background._bg_color_a)
        self._layer_background.set_style_getter('border_color', lambda: self._layer_background._border_color)
        self._layer_background.setFixedStyleSheet("border-width: 1px;\nborder-style: solid;\nborder-radius: 2px;")
        self._layer_highlight._bg_color_a = self._colors.flash
        self._layer_highlight.set_style_getter('background_color', lambda: self._layer_highlight._bg_color_a)
        self._layer_highlight.setFixedStyleSheet("border-radius: 2px;")


    def _theme_changed_handler(self, theme):
        super()._theme_changed_handler(theme)
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self._layer_background.setColor(self._colors.background_a)
        self._layer_background.setBorderColor(self._colors.border)
        self._layer_highlight.setColor(ZColorTool.trans(self._colors.flash))


    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self._completely_hide = True
            self.resize(2 * self._margin, 36 + 2 * self._margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self._label_text.setText("")   # 清空文本内容
        else:
            self._completely_hide = False

    def _refresh_position(self):
        '更新位置'
        pos = self._get_pos_should_be_move()
        self.moveTo(pos[0], pos[1])

    def _get_slider_tooltip_pos(self):
        '获取slider组件提示框位置'
        handle = self._inside_of.handle()
        pos = handle.mapToGlobal(handle.rect().center())
        if self._inside_of._direction == Zen.Direction.Horizontal:
            # 水平滑块：提示框在滑块上方居中
            x = pos.x() - self.width() / 2  # 水平居中对齐
            y = pos.y() - self.height() - 6  # 显示在滑块上方，留出6px间距
            return x, y
        elif self._inside_of._direction == Zen.Direction.Vertical:
            # 垂直滑块：提示框在滑块右侧居中
            x = pos.x() - self.width() - 6 # 显示在滑块右侧，留出6px间距
            y = pos.y() - self.height() / 2  # 垂直居中对齐
            return x, y

    def _get_pos_should_be_move(self):
        '获取应该移动到的位置'
        if isinstance(self._inside_of, ZSlider):
            return self._get_slider_tooltip_pos()
        else:
            pos = QCursor.pos()
            x, y = pos.x()-self.width()/2, pos.y()-self.height()
            return x, y

    def setInsideOf(self, widget):
        """设置当前位于哪个控件内部"""
        self._inside_of = widget
        if widget is None:
            # 关闭位置刷新定时器
            self._tracker_timer.stop()
            return
        # 开启位置刷新定时器
        self._tracker_timer.start()
        # 初始化位置
        pos = self._get_pos_should_be_move()
        self.move(pos[0], pos[1]) 

    def insideOf(self):
        """返回最后一次被调用显示时的发出者"""
        return self._inside_of


    def setText(self, text: str, flash: bool = True) -> None:
        """设置提示文本内容"""
        if self._label_text.text() == text: return
        self._label_text.setText(str(text))
        # 使用单个计时器延迟刷新
        QTimer.singleShot(0, lambda: self._refresh_text(flash))


    def _refresh_text(self, flash: bool):
        """刷新文本显示"""
        self._refresh_size()
        if flash: self.flash()


    def _refresh_size(self):
        """用于设置大小动画结束值并启动动画"""
        self._label_text.adjustSize()
        w = self._label_text.width()
        h = self._label_text.height()
        self.resizeTo(w + 2*self._margin, h + 2*self._margin)  # 设为文字标签的大小加上阴影间距


    def flash(self):
        '闪烁效果'
        self._layer_highlight.setColor(self._colors.flash)
        self._layer_highlight.setColorTo(ZColorTool.trans(self._colors.flash))


    def showTip(self):
        '显示工具提示'
        self._is_shown = True
        self.setOpacityTo(1.0)


    def hideTip(self):
        '隐藏工具提示'
        self._is_shown = False
        self.setOpacityTo(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width() - 2 * self._margin, size.height() - 2 * self._margin
        # 重设内部控件大小
        self._layer_background.resize(w, h)
        self._board.resize(w, h)
        self._layer_highlight.resize(w, h)
        # 移动文本位置，阻止重设大小动画进行时奇怪的文字移动
        self._label_text.move(0, h - self._label_text.height())
        # self._label_text.move(0, h - self.height() + 16)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()

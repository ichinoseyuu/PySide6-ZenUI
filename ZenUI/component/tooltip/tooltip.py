from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component import ZWidget,ZTextLabel
from ZenUI.core import Zen,ZColorTool,ZQuickEffect,ZColorSheet
from ZenUI.component.widget.colorlayer import ZColorLayer


class ZToolTip(ZWidget):
    '''提示框'''
    def __init__(self):
        super().__init__(name='tooltip')
        self._is_shown = False
        self._completely_hide = False # 是否已经完全隐藏 透明度是不是0
        self._inside_of = None 
        self._margin = 8 # 周围给阴影预留的间隔空间
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        ZQuickEffect.WidgetShadow.applyDropShadowOn(self, (0, 0, 0, 128), blur_radius=int(self._margin*1.5))
        self._setup_ui()
        self.setText("", flash=False)  # 通过输入空文本初始化大小
        self._init_style()
        self._schedule_update()

    # region Override
    def _init_anim(self):
        super()._init_anim()
        self._tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._refresh_position)
        self._tracker_timer.start()
        # 当透明度动画结束时处理隐藏与否
        self.AnimGroup().fromToken("opacity").finished.connect(self._completely_hid_signal_handler)


    # region Private
    def _setup_ui(self):
        """创建ui"""
        self._layer_background = ZColorLayer(self)
        self._layer_background.move(self._margin, self._margin)

        self._board = QWidget(self)
        self._label_text = ZTextLabel(parent=self._board,
                               word_wrap=True)
        self._label_text.setFixedStyleSheet("padding: 8px")
        self._label_text.setWidgetFlag(Zen.WidgetFlag.InstantResize)
        self._label_text.setWidgetFlag(Zen.WidgetFlag.AdjustSizeOnTextChanged)
        #self._label_text.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self._board.move(self._margin, self._margin)

        self._layer_highlight = ZColorLayer(self)
        self._layer_highlight.move(self._margin, self._margin)

    def _init_style(self):
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.ToolTip)
        self._layer_background._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._layer_background._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._layer_background.set_style_getter('background_color', lambda: self._layer_background._bg_color_a)
        self._layer_background.set_style_getter('border_color', lambda: self._layer_background._border_color)
        self._layer_highlight._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Flash)
        self._layer_highlight.set_style_getter('background_color', lambda: self._layer_highlight._bg_color_a)

    def _theme_changed_handler(self, theme):
        self._layer_background.setColor(self._color_sheet.getColor(theme, Zen.ColorRole.Background_A))
        self._layer_background.setBorderColor(self._color_sheet.getColor(theme, Zen.ColorRole.Border))
        self._layer_highlight.setColor(ZColorTool.trans(self._color_sheet.getColor(theme, Zen.ColorRole.Flash)))

    def _refresh_size(self):
        """用于设置大小动画结束值并启动动画"""
        self._label_text.adjustSize()
        w = self._label_text.width()
        h = self._label_text.height()
        self.resizeTo(w + 2 * self._margin, h + 2 * self._margin)  # 设为文字标签的大小加上阴影间距


    def _refresh_position(self):
        pos = QCursor.pos()
        x, y = pos.x() - self.width() / 2, pos.y()
        self.moveTo(x , y - self.height())    # 动画跟踪，效果更佳，有了锚点直接输入鼠标坐标即可


    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self._completely_hide = True
            self.resize(2 * self._margin, 36 + 2 * self._margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self._label_text.setText("")   # 清空文本内容
        else:
            self._completely_hide = False

    # region Public
    def setInsideOf(self, widget):
        """设置当前位于哪个控件内部"""
        self._inside_of = widget


    def insideOf(self):
        """返回最后一次被调用显示时的发出者"""
        return self._inside_of


    def setText(self, text, flash=True):
        """设置工具提示的内容，支持富文本"""
        text_changed = self._label_text.text() != text
        if not text_changed: return
        self._label_text.setText(str(text))
        if flash:
            QTimer.singleShot(0, lambda:(self._refresh_size(), self.flash()))
        else:
            QTimer.singleShot(0, self._refresh_size)



    def flash(self):
        """ 激活高光层动画，使高光层闪烁 """
        self._layer_highlight.setColor(self._color_sheet.getColor(Zen.ColorRole.Flash))
        self._layer_highlight.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Flash)))


    def showTip(self):
        self._is_shown = True
        self.setOpacityTo(1.0)


    def hideTip(self):
        self._is_shown = False
        self.setOpacityTo(0)

    # region Event
    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width() - 2 * self._margin, size.height() - 2 * self._margin
        # 重设内部控件大小
        self._layer_background.resize(w, h)
        self._board.resize(w, h)
        self._layer_highlight.resize(w, h)
        # 移动文本位置，阻止重设大小动画进行时奇怪的文字移动
        # self._label_text.move(0, h - self._label_text.height()) 2024.9.23 - 存在快速滑动鼠标时文字错位的情况
        self._label_text.move(0, h - self.height() + 16)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()

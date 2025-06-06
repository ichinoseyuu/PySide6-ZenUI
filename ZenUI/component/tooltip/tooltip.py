from textwrap import dedent
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QCursor
from ZenUI.component.basewidget import ZWidget,ZLayer
from ZenUI.component.label import ZTextLabel
from ZenUI.core import ZQuickEffect, Zen, ZColorTool

class ToolTipLayer(ZLayer):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._style_vars = {
            'background_color': 'transparent',
            'border_color': 'transparent'}
        '默认样式'
        self._style_getters = {}
        '动态样式'
        self._style_format = dedent('''\
            background-color: {background_color};
            border-color: {border_color};''')
        self._init_style()
        self._schedule_update()

    def set_style_var(self, key: str, value):
        """设置静态样式变量"""
        self._style_vars[key] = value

    def set_style_getter(self, key: str, getter):
        """设置动态样式获取器"""
        self._style_getters[key] = getter

    def _init_style(self):
        self._anim_bg_color_a.setBias(0.1)


    def reloadStyleSheet(self):
        try:
            # 合并静态变量和动态获取的变量
            current_vars = self._style_vars.copy()
            for key, getter in self._style_getters.items():
                current_vars[key] = getter()
            return self._style_format.format(**current_vars) +'\n'+ self._stylesheet_fixed
        except KeyError as e:
            print(f"缺少样式变量: {e}")

class ZToolTip(ZWidget):
    '''提示框'''
    def __init__(self):
        super().__init__(name='tooltip')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._is_shown = False
        '是否已经显示'
        self._completely_hide = False
        '是否已经完全隐藏 透明度是不是0'
        self._inside_of = None
        '鼠标悬停的控件'
        self._margin = 8
        '给阴影预留的间隔空间'
        self.raise_()
        self._setup_ui()
        self._init_style()
        self.setText("", flash=False) # 通过输入空文本初始化大小
        ZQuickEffect.applyDropShadowOn(self, (0, 0, 0, 100), blur_radius=int(self._margin*1.5))
        self.updateStyle()

    # region Zwidget
    def _init_anim(self):
        super()._init_anim()
        self._tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self._tracker_timer.setInterval(int(1000/60))
        self._tracker_timer.timeout.connect(self._refresh_position)
        self._tracker_timer.start()
        # 当透明度动画结束时处理隐藏与否
        self.AnimGroup().fromToken("opacity").finished.connect(self._completely_hid_signal_handler)

    def _theme_changed_handler(self, theme):
        super()._theme_changed_handler(theme)
        self._colors.overwrite(self._color_sheet.getSheet(theme))

        self._layer_background.setColor(self._colors.background_a)
        self._layer_background.setBorderColor(self._colors.border)
        self._layer_highlight.setColor(ZColorTool.trans(self._colors.flash))


    # region Tooltip
    def _setup_ui(self):
        """创建ui"""
        self._layer_background = ToolTipLayer(self)
        self._layer_background.move(self._margin, self._margin)

        self._board = QWidget(self)
        self._label_text = ZTextLabel(parent=self._board,
                               word_wrap=True)
        self._label_text.setFixedStyleSheet("padding: 8px")
        self._label_text.setWidgetFlag(Zen.WidgetFlag.InstantResize)
        self._label_text.setWidgetFlag(Zen.WidgetFlag.AdjustSizeOnTextChanged)
        self._board.move(self._margin, self._margin)

        self._layer_highlight = ToolTipLayer(self)
        self._layer_highlight.move(self._margin, self._margin)

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


    def _refresh_size(self):
        """用于设置大小动画结束值并启动动画"""
        self._label_text.adjustSize()
        w = self._label_text.width()
        h = self._label_text.height()
        self.resizeTo(w + 2 * self._margin, h + 2 * self._margin)  # 设为文字标签的大小加上阴影间距


    def _refresh_position(self):
        pos = QCursor.pos()
        x, y = pos.x() - self.width() / 2, pos.y()
        self.moveTo(x , y - self.height()) # 动画跟踪，效果更佳，直接输入鼠标坐标即可


    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self._completely_hide = True
            self.resize(2 * self._margin, 36 + 2 * self._margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self._label_text.setText("")   # 清空文本内容
        else:
            self._completely_hide = False


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
        '闪烁效果'
        self._layer_highlight.setColor(self._color_sheet.getColor(Zen.ColorRole.Flash))
        self._layer_highlight.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Flash)))


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
        # self._label_text.move(0, h - self._label_text.height()) 2024.9.23 - 存在快速滑动鼠标时文字错位的情况
        self._label_text.move(0, h - self.height() + 16)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()

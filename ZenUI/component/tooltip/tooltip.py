from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component import ZenWidget, ZenTextLabel
from ZenUI.core import Zen,ColorTool,ColorSheet,ZenEffect

class ToolTipBG(ZenWidget):
    """用于ToolTip的背景层"""
    def _init_style(self):
        self._fixed_stylesheet = "border-radius: 2px;\nborder: 1px solid transparent;"
        self._color_sheet = ColorSheet(self, Zen.WidgetType.ToolTip)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._anim_bg_color_a.setBias(0.1)
        self._anim_bg_color_a.setCurrent(ColorTool.toArray(self._bg_color_a))

    def reloadStyleSheet(self):
        if self._fixed_stylesheet:
            return self._fixed_stylesheet + f'background-color: {self._bg_color_a};'
        else:
            return f'background-color: {self._bg_color_a};'

    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Background_A))


class ToolTipHighlight(ZenWidget):
    """用于ToolTip的高亮层"""
    def _init_style(self):
        self._fixed_stylesheet = "border-radius: 2px;\nborder: 1px solid transparent;"
        self._anim_bg_color_a.setBias(0.1)
        self.setColor("#00f0f0f0")

    def reloadStyleSheet(self):
        return self._fixed_stylesheet + f'background-color: {self._bg_color_a};'



class ZenToolTip(ZenWidget):
    '''提示框'''
    def __init__(self):
        super().__init__(name='tooltip')
        self._is_shown = False
        self._completely_hide = False # 是否已经完全隐藏 透明度是不是0
        self._inside_of = None 
        self._margin = 8 # 周围给阴影预留的间隔空间
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        ZenEffect.WidgetShadow.applyDropShadowOn(self, (0, 0, 0, 128), blur_radius=int(self._margin*1.5))
        self._setup_ui()
        self.setText("", flash=False)  # 通过输入空文本初始化大小
        
    # region Override
    def _init_anim(self):
        super()._init_anim()
        self.tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self.tracker_timer.setInterval(int(1000/60))
        self.tracker_timer.timeout.connect(self._refresh_position)
        self.tracker_timer.start()
        # 当透明度动画结束时处理隐藏与否
        self.AnimGroup().fromToken("opacity").finished.connect(self._completely_hid_signal_handler)


    # region Private
    def _setup_ui(self):
        """创建ui"""
        self.bgLayer = ToolTipBG(self)
        self.container = QWidget(self)
        self.text = ZenTextLabel(self.container)
        self.text.setWordWrap(True)
        self.highlightLayer = ToolTipHighlight(self)
        self.text.setFixedStyleSheet("padding: 8px")
        self.text.setWidgetFlag(Zen.WidgetFlag.InstantResize)
        self.text.setWidgetFlag(Zen.WidgetFlag.AdjustSizeOnTextChanged)
        #self.text.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        # 移动到合适的位置
        self.bgLayer.move(self._margin, self._margin)
        self.container.move(self._margin, self._margin)
        self.highlightLayer.move(self._margin, self._margin)


    def _refresh_size(self):
        """用于设置大小动画结束值并启动动画"""
        self.text.adjustSize()
        w = self.text.width()
        h = self.text.height()
        self.resizeTo(w + 2 * self._margin, h + 2 * self._margin)  # 设为文字标签的大小加上阴影间距


    def _refresh_position(self):
        pos = QCursor.pos()
        x, y = pos.x() - self.width() / 2, pos.y()
        self.moveTo(x , y - self.height())    # 动画跟踪，效果更佳，有了锚点直接输入鼠标坐标即可


    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self._completely_hide = True
            self.resize(2 * self._margin, 36 + 2 * self._margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self.text.setText("")   # 清空文本内容
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
        text_changed = self.text.text() != text
        if not text_changed: return
        self.text.setText(str(text))
        if flash:
            QTimer.singleShot(0, lambda:(self._refresh_size(), self.flash()))
        else:
            QTimer.singleShot(0, self._refresh_size)



    def flash(self):
        """ 激活高光层动画，使高光层闪烁 """
        self.highlightLayer.setColor(self.bgLayer._color_sheet.getColor(Zen.ColorRole.Flash))
        self.highlightLayer.setColorTo(ColorTool.trans(self.bgLayer._color_sheet.getColor(Zen.ColorRole.Flash)))


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
        self.bgLayer.resize(w, h)
        self.container.resize(w, h)
        self.highlightLayer.resize(w, h)
        # 移动文本位置，阻止重设大小动画进行时奇怪的文字移动
        # self.text.move(0, h - self.text.height()) 2024.9.23 - 存在快速滑动鼠标时文字错位的情况
        self.text.move(0, h - self.height() + 16)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI._legacy.component.basewidget.widget import ZWidget
from ZenUI._legacy.core import ZExpAnim,AnimGroup,ZColorTool,Zen

class ZLayer(QWidget):
    '颜色层，用于实现组件颜色渐变等效果'
    moved = Signal(object)
    resized = Signal(object)
    opacityChanged = Signal(float)
    def __init__(self, parent: ZWidget = None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground) #启用样式表

        self._widget_flags = {}
        '组件属性，控制是否具备动画等'
        self._stylesheet_fixed = ''
        '固有样式表，每次调用`setStyleSheet`方法时，都会在样式表前附加这段固定内容'
        self._stylesheet = ''
        '控件样式表'
        self._stylesheet_cache = ''
        '样式表缓存，更新样式时使用'
        self._stylesheet_dirty = True
        '样式表是否被更改'
        self._can_update = True
        '是否可以更新样式表'

        self._x1, self._y1, self._x2, self._y2 = None, None, None, None
        '组件可移动区域坐标'
        self._move_anchor = QPoint(0, 0)
        '移动锚点'

        self._bg_color_a = '#00000000'
        '背景颜色，用于渐变模式的起始点'
        self._bg_color_b = '#00000000'
        '背景颜色,用于渐变模式的终点'
        self._gradient_anchor =[0, 0, 1, 1]
        '渐变锚点，用于控制渐变方向和范围'

        self._border_color = '#00000000'
        '边框颜色'

        self._init_anim()


    # region Style
    def _init_style(self):
        """
        重写初始样式，创建新组件类使用，配置新组件的初始颜色，动画等
        - 子类实现，基类初始化自行调用
        """
        pass

    def setStyleSheet(self):
        """设置样式表"""
        self._stylesheet = self.reloadStyleSheet()
        super().setStyleSheet(self._stylesheet)
        self._can_update = True

    def styleSheet(self):
        '获取样式表'
        return self._stylesheet

    def setFixedStyleSheet(self, stylesheet: str):
        """
        设置样式表固定内容
        - 此后每次运行`setStyleSheet`方法时，都会在样式表前附加这段固定内容
        """
        self._stylesheet_fixed = stylesheet
        self._stylesheet_dirty = True

    def fixedStyleSheet(self):
        '获取样式表固定内容'
        return self._stylesheet_fixed

    def reloadStyleSheet(self):
        """重新加载样式表，创建新组件类使用，定义组件样式表"""
        if not self._stylesheet_dirty and self._stylesheet_cache: return self._stylesheet_cache


    def updateStyle(self):
        '''
        更新控件样式
        - 调用`setStyleSheet`方法
        - 同一帧只会刷新一次样式表
        '''
        if self._can_update:
            self._can_update = False
            QTimer.singleShot(0, self.setStyleSheet)



    # region WidgetFlag
    def setWidgetFlag(self, flag:Zen.WidgetFlag, on: bool = True):
        """设置`widgetflag`"""
        self._widget_flags[flag.name] = on


    def isWidgetFlagOn(self, flag):
        """查找`widgetflag`是否开启"""
        if flag.name not in self._widget_flags.keys():
            return False
        return self._widget_flags[flag.name]


    def _move_anim_handler(self, arr):
        x, y = arr
        self.move(int(x), int(y))

    def _resize_anim_handler(self, arr):
        w, h = arr
        self.resize(int(w), int(h))

    def _bg_color_a_handler(self, color_value):
        self._bg_color_a = ZColorTool.toCode(color_value)
        self.updateStyle()

    def _bg_color_b_handler(self, color_value):
        self._bg_color_b = ZColorTool.toCode(color_value)
        self.updateStyle()

    def _border_color_handler(self, color_value):
        self._border_color = ZColorTool.toCode(color_value)
        self.updateStyle()

    # region Move
    def moveTo(self, x: int, y: int):
        """
        如果开启了动画，将控件动态的移动到指定位置
        """
        x, y = self._legalize_moving_target(x, y)
        if self.isWidgetFlagOn(Zen.WidgetFlag.InstantMove) is False:
            self._anim_move.setTarget([x, y])
            self.activateMoveAnim()
        else:
            self.move(x, y)

    def _legalize_moving_target(self, x: int, y: int):
        """合法化移动目标"""
        if self.isWidgetFlagOn(Zen.WidgetFlag.HasMoveLimits) is False:
            return x, y
        x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
        x = max(x1, min(x2 - self.width(), x))
        y = max(y1, min(y2 - self.height(), y))
        return x, y

    def move(self, *args):  # 重写移动方法，从而按照锚点的位置移动控件
        """移动控件到指定位置"""
        point = QPoint(*args)
        anchor_adjusted_point = point - self._move_anchor
        super().move(anchor_adjusted_point)

    def moveEvent(self, event):
        """重写移动事件"""
        # moveEvent 事件一旦被调用，控件的位置会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 pos()
        super().moveEvent(event)
        pos = event.pos() + self._move_anchor
        self._anim_move.setCurrent([pos.x(), pos.y()])
        if self.isWidgetFlagOn(Zen.WidgetFlag.EnableAnimationSignals):
            self.moved.emit([event.pos().x(), event.pos().y()])

    def setMoveLimits(self, x1: int, y1: int, x2: int, y2: int):
        """
        设置移动限制，移动限制会阻止动画目标超出矩形范围限制
        Args:
            x1: 起始点横坐标
            y1: 起始点纵坐标
            x2: 终点横坐标
            y2: 终点纵坐标
        """
        # 拖动控件只能在这个范围内运动
        # 注意！必须满足 x1 <= x2, y1 <= y2
        self.setWidgetFlag(Zen.WidgetFlag.HasMoveLimits, True)
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2

    def setMoveAnchor(self, x, y):
        """设置移动锚点，移动锚点用于确定控件移动时锚点位置"""
        self._move_anchor = QPoint(x, y)

    def moveAnchor(self):
        """获取移动锚点"""
        return self._move_anchor


    # region Resize
    def resizeTo(self, w: int, h: int):
        """
        如果开启了动画，将控件动态的调整到指定大小
        """
        if self.isWidgetFlagOn(Zen.WidgetFlag.InstantResize) is False and self.isVisible() is True:
            self._anim_resize.setTarget([w, h])
            self.activateResizeAnim()
        else:
            self.resize(w, h)

    def resizeEvent(self, event):
        """重写调整大小事件"""
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self._anim_resize.setCurrent([w, h])
        if self.isWidgetFlagOn(Zen.WidgetFlag.EnableAnimationSignals):
            self.resized.emit([w, h])

    # region BGColor
    def setColorTo(self, code_1, code_2=None):
        """
        如果开启了动画，将控件动态的调整到指定颜色
        Args:
            code_1: 颜色代码，格式为 `#AARRGGBB` 或 `#RRGGBB`
            code_2: 第二个颜色代码，仅当渐变模式启用时使用
        """
        is_gradient = self.isWidgetFlagOn(Zen.WidgetFlag.GradientColor)
        is_instant = self.isWidgetFlagOn(Zen.WidgetFlag.InstantSetColor)
        # 当 InstantSetColor 标志启用时，直接设置颜色

        if is_instant:
            self.setColor(code_1, code_2) if is_gradient else self.setColor(code_1)
            return
        # 启动动画：根据是否是渐变色来处理
        color_value_1 = ZColorTool.toArray(code_1)
        self._anim_bg_color_a.setTarget(color_value_1)
        self._anim_bg_color_a.try_to_start()

        if is_gradient and code_2 is not None:
            color_value_2 = ZColorTool.toArray(code_2)
            self._anim_bg_color_b.setTarget(color_value_2)
            self._anim_bg_color_b.try_to_start()


    def setColor(self, code_1, code_2=None):
        """
        设置背景颜色
        Args:
            code_1: 颜色代码，格式为 `#AARRGGBB` 或 `#RRGGBB`
            code_2: 第二个颜色代码，仅当渐变模式启用时使用
        """
        color_value_1 = ZColorTool.toArray(code_1)
        self._anim_bg_color_a.setCurrent(color_value_1)
        self._bg_color_a_handler(color_value_1)

        if code_2 is not None:
            color_value_2 = ZColorTool.toArray(code_2)
            self._anim_bg_color_b.setCurrent(color_value_2)
            self._bg_color_b_handler(color_value_2)
        #print("setColor", color_value_1, color_value_2)

    def setGradientAnchor(self, x1, y1, x2, y2):
        """
        设置渐变锚点
        Args:
            x1: 渐变起始点 横坐标
            y1: 渐变起始点 纵坐标
            x2: 渐变结束点 横坐标
            y2: 渐变结束点 纵坐标
        """
        self._gradient_anchor = [x1, y1, x2, y2]
        self._schedule_update()

    def gradientAnchor(self):
        """获取渐变锚点"""
        return self._gradient_anchor


    # region BorderColor
    def setBorderColorTo(self, code):
        """
        如果开启了动画，将控件动态的调整到指定边框颜色
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        self._anim_border_color.setTarget(ZColorTool.toArray(code))
        self._anim_border_color.try_to_start()

    def setBorderColor(self, code):
        """
        设置边框颜色
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        color_value = ZColorTool.toArray(code)
        self._anim_border_color.setCurrent(color_value)
        self._border_color_handler(color_value)



    # region Animation

    def _init_anim(self):
        """
        创建动画，并添加到动画组
        - 需要创建新动画时，调用此方法，以初始化动画
        """
        self._anim_move = ZExpAnim(self)
        self._anim_move.setFactor(0.25)
        self._anim_move.setBias(1)
        self._anim_move.setCurrent([0, 0])
        self._anim_move.setTarget([0, 0])
        self._anim_move.ticked.connect(self._move_anim_handler)

        self._anim_resize = ZExpAnim(self)
        self._anim_resize.setFactor(0.25)
        self._anim_resize.setBias(1)
        self._anim_resize.setCurrent([0, 0])
        self._anim_resize.setTarget([0, 0])
        self._anim_resize.ticked.connect(self._resize_anim_handler)

        self._anim_bg_color_a = ZExpAnim(self)
        self._anim_bg_color_a.setFactor(0.25)
        self._anim_bg_color_a.setBias(1)
        self._anim_bg_color_a.ticked.connect(self._bg_color_a_handler)

        self._anim_bg_color_b = ZExpAnim(self)
        self._anim_bg_color_b.setFactor(0.25)
        self._anim_bg_color_b.setBias(1)
        self._anim_bg_color_b.ticked.connect(self._bg_color_b_handler)

        self._anim_border_color = ZExpAnim(self)
        self._anim_border_color.setFactor(0.25)
        self._anim_border_color.setBias(1)
        self._anim_border_color.ticked.connect(self._border_color_handler)

        # 创建动画组，以tokenize以上动画
        self._anim_group = AnimGroup()
        self._anim_group.addMember(self._anim_move, token="move")
        self._anim_group.addMember(self._anim_resize, token="resize")
        self._anim_group.addMember(self._anim_bg_color_a, token="color_a")
        self._anim_group.addMember(self._anim_bg_color_b, token="color_b")
        self._anim_group.addMember(self._anim_border_color, token="border_color")

    def activateOpacityAnim(self):
        "激活透明度动画"
        self._anim_opacity.try_to_start()

    def deactivateOpacityAnim(self):
        "关闭透明度动画"
        self._anim_opacity.stop()

    def isOpacityAnimActive(self):
        "透明度动画是否激活"
        return self._anim_opacity.isActive()


    def activateMoveAnim(self):
        "激活移动动画"
        self._anim_move.try_to_start()

    def deactivateMoveAnim(self):
        "关闭移动动画"
        self._anim_move.stop()

    def isMoveAnimActive(self):
        "移动动画是否激活"
        return self._anim_move.isActive()


    def activateResizeAnim(self):
        "激活大小调整动画"
        self._anim_resize.try_to_start()

    def deactivateResizeAnim(self):
        "关闭大小调整动画"
        self._anim_resize.stop()

    def isResizeAnimActive(self):
        "大小调整动画是否激活"
        return self._anim_resize.isActive()

    def AnimGroup(self):
        """返回动画组"""
        return self._anim_group

    # region Event
    def hideEvent(self, a0):
        '''重写隐藏事件'''
        super().hideEvent(a0)
        if self.isWidgetFlagOn(Zen.WidgetFlag.DeleteOnHidden):
            self.deleteLater()


    def event(self, event):
        '''重写事件'''
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)
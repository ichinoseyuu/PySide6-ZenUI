from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.core import ZenExpAnim, ColorTool, Zen,AnimGroup, ZenGlobal
class ABCLabel(QLabel):
    moved = Signal(object)
    resized = Signal(object)
    opacityChanged = Signal(float)
    def __init__(self, parent: QWidget=None, name: str = None):
        super().__init__(parent)
        if name:
            self.setObjectName(name)

        self._fixed_stylesheet = '' #固定样式表

        self._widget_flags = {} # 组件属性，控制是否具备动画等

        self._x1, self._y1, self._x2, self._y2 = None, None, None, None # 组件可移动区域
        self._move_anchor = QPoint(0, 0)  # 移动时的基准点位置

        self._color_sheet = None # 颜色表
        self._theme_manager = ZenGlobal.ui.theme_manager #主题管理器，用于接受主题切换的信号
        self._theme_manager.themeChanged.connect(self._theme_changed_handler)

        self._bg_color_a = 'transparent'
        self._bg_color_b = 'transparent'
        self._gradient_anchor =[0, 0, 1, 1]  #渐变锚点
        self._border_color = 'transparent'
        self._text_color = 'black'
        self._can_update = True

        self._anim_move = ZenExpAnim(self)
        self._anim_move.setFactor(0.25)
        self._anim_move.setBias(1)
        self._anim_move.setCurrent([0, 0])
        self._anim_move.setTarget([0, 0])
        self._anim_move.ticked.connect(self._move_anim_handler)

        self._anim_resize = ZenExpAnim(self)
        self._anim_resize.setFactor(0.25)
        self._anim_resize.setBias(1)
        self._anim_resize.setCurrent([0, 0])
        self._anim_resize.setTarget([0, 0])
        self._anim_resize.ticked.connect(self._resize_anim_handler)

        self._anim_opacity = ZenExpAnim(self)
        self._anim_opacity.setFactor(0.25)
        self._anim_opacity.setBias(0.01)
        self._anim_opacity.ticked.connect(self._opacity_anim_handler)

        self._anim_bg_color_a = ZenExpAnim(self)
        self._anim_bg_color_a.setFactor(0.25)
        self._anim_bg_color_a.setBias(1)
        self._anim_bg_color_a.ticked.connect(self._bg_color_a_handler)

        self._anim_bg_color_b = ZenExpAnim(self)
        self._anim_bg_color_b.setFactor(0.25)
        self._anim_bg_color_b.setBias(1)
        self._anim_bg_color_b.ticked.connect(self._bg_color_b_handler)

        self._anim_border_color = ZenExpAnim(self)
        self._anim_border_color.setFactor(0.25)
        self._anim_border_color.setBias(1)
        self._anim_border_color.ticked.connect(self._border_color_handler)

        self._anim_text_color = ZenExpAnim(self)
        self._anim_text_color.setFactor(0.25)
        self._anim_text_color.setBias(1)
        self._anim_text_color.ticked.connect(self._text_color_handler)

        # 创建动画组，以tokenize以上动画
        self._anim_group = AnimGroup()
        self._anim_group.addMember(self._anim_move, token="move")
        self._anim_group.addMember(self._anim_resize, token="resize")
        self._anim_group.addMember(self._anim_opacity, token="opacity")
        self._anim_group.addMember(self._anim_bg_color_a, token="color_a")
        self._anim_group.addMember(self._anim_bg_color_b, token="color_b")
        self._anim_group.addMember(self._anim_border_color, token="border_color")
        self._anim_group.addMember(self._anim_text_color, token="text_color")


    # region StyleSheet
    def setStyleSheet(self, stylesheet: str):
        """设置样式表"""
        super().setStyleSheet(stylesheet)
        #print(new_stylesheet)
        self._can_update = True

    def setFixedStyleSheet(self, stylesheet: str):
        """
        设置样式表固定内容,此后每次运行 setStyleSheet 方法时，都会在样式表前附加这段固定内容\n
        可以覆盖 reloadStyleSheet 方法里已经指定的样式表内容
        """
        self._fixed_stylesheet = stylesheet

    def reloadStyleSheet(self):
        """
        重载样式表,创建新组件类的时候使用，定义组件初始化的样式表，新组件类来实现
        """
        return

    def _schedule_update(self):
        """ 调度一次更新样式的方法，避免重复调用 """
        if self._can_update:
            self._can_update = False
            QTimer.singleShot(0, self.updateStyleSheet)

    def updateStyleSheet(self):
        """ 更新样式表 """
        self.setStyleSheet(self.reloadStyleSheet())


    # region WidgetFlag
    def setWidgetFlag(self, flag:Zen.WidgetFlag, on: bool = True):
        """设置 widget flag"""
        self._widget_flags[flag.name] = on

    def isWidgetFlagOn(self, flag):
        """widget flag是否开启"""
        if flag.name not in self._widget_flags.keys():
            return False
        return self._widget_flags[flag.name]


    # region Group
    def AnimGroup(self):
        """返回动画组"""
        return self._anim_group


    # region Slot
    def _theme_changed_handler(self, arg_1):
        '''主题改变时调用，子类实现'''
        return

    def _move_anim_handler(self, arr):
        x, y = arr
        self.move(int(x), int(y))

    def _resize_anim_handler(self, arr):
        w, h = arr
        self.resize(int(w), int(h))

    def _opacity_anim_handler(self, opacity: float):
        self.setOpacity(opacity)

    def _bg_color_a_handler(self, color_value):
        self._bg_color_a = ColorTool.toCode(color_value)
        self._schedule_update()

    def _bg_color_b_handler(self, color_value):
        self._bg_color_b = ColorTool.toCode(color_value)
        self._schedule_update()

    def _border_color_handler(self, color_value):
        self._border_color = ColorTool.toCode(color_value)
        self._schedule_update()

    def _text_color_handler(self, color_value):
        self._text_color = ColorTool.toCode(color_value)
        self._schedule_update()

    # region Move
    def moveTo(self, x: int, y: int):
        """
        将控件移动到指定位置,如果开启动画,则动态移动
        """
        x, y = self._legalize_moving_target(x, y)
        if self.isWidgetFlagOn(Zen.WidgetFlag.InstantMove) is False:
            self._anim_move.setTarget([x, y])
            self.activateMoveAnim()
        else:
            self.move(x, y)

    def _legalize_moving_target(self, x: int, y: int):
        # 使移动的位置合法
        if self.isWidgetFlagOn(Zen.WidgetFlag.HasMoveLimits) is False:
            return x, y

        x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2
        x = max(x1, min(x2 - self.width(), x))
        y = max(y1, min(y2 - self.height(), y))
        return x, y

    def move(self, *args):  # 重写移动方法，从而按照锚点的位置移动控件
        point = QPoint(*args)
        anchor_adjusted_point = point - self._move_anchor
        super().move(anchor_adjusted_point)

    def moveEvent(self, event):
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
            x1: 左上 横坐标
            y1: 左上 纵坐标
            x2: 右下 横坐标
            y2: 右下 纵坐标
        """
        # 拖动控件只能在这个范围内运动
        # 注意！必须满足 x1 <= x2, y1 <= y2
        self.setWidgetFlag(Zen.WidgetFlag.HasMoveLimits, True)
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2

    def setMoveAnchor(self, x, y):
        self._move_anchor = QPoint(x, y)

    def moveAnchor(self):
        return self._move_anchor


    # region Resize
    def resizeTo(self, w: int, h: int):
        """
        将控件调整到指定大小,如果开启动画,则动态改变大小
        """
        if self.isWidgetFlagOn(Zen.WidgetFlag.InstantResize) is False and self.isVisible() is True:
            self._anim_resize.setTarget([w, h])
            self.activateResizeAnim()
        else:
            self.resize(w, h)

    def resizeEvent(self, event):
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self._anim_resize.setCurrent([w, h])
        if self.isWidgetFlagOn(Zen.WidgetFlag.EnableAnimationSignals):
            self.resized.emit([w, h])


    # region Opacity
    def setOpacityTo(self, opacity: float):
        """
        带动画地设置控件的透明度
        Args:
            opacity: 透明度值 0-1
        """
        if self.isWidgetFlagOn(Zen.WidgetFlag.InstantSetOpacity) is False:
            self._anim_opacity.setCurrent(self.windowOpacity())
            self._anim_opacity.setTarget(opacity)
            self.activateOpacityAnim()
        else:
            self.setOpacity(opacity)

    def setOpacity(self, opacity: float):
        """
        设置透明度
        Args:
            opacity: 透明度值 0-1
        """
        self._anim_opacity.setCurrent(opacity)
        self.setWindowOpacity(opacity)
        if self.isWidgetFlagOn(Zen.WidgetFlag.EnableAnimationSignals):
            self.opacityChanged.emit(opacity)
        if (opacity == 0) and self.isWidgetFlagOn(Zen.WidgetFlag.DeleteOnHidden):
            self.deleteLater()


    # region BGColor
    def setColorTo(self, code_1, code_2=None):
        """
        设置背景颜色，同时启动动画
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
        color_value_1 = ColorTool.toArray(code_1)
        self._anim_bg_color_a.setTarget(color_value_1)
        self._anim_bg_color_a.try_to_start()

        if is_gradient and code_2 is not None:
            color_value_2 = ColorTool.toArray(code_2)
            self._anim_bg_color_b.setTarget(color_value_2)
            self._anim_bg_color_b.try_to_start()


    def setColor(self, code_1, code_2=None):
        """
        设置背景颜色
        Args:
            code_1: 颜色代码，格式为 `#AARRGGBB` 或 `#RRGGBB`
            code_2: 第二个颜色代码，仅当渐变模式启用时使用
        """
        color_value_1 = ColorTool.toArray(code_1)
        self._anim_bg_color_a.setCurrent(color_value_1)
        self._bg_color_a_handler(color_value_1)

        if code_2 is not None:
            color_value_2 = ColorTool.toArray(code_2)
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

    # region BorderColor
    def setBorderColorTo(self, code):
        """
        设置边框颜色，同时启动动画,
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        self._anim_border_color.setTarget(ColorTool.toArray(code))
        self._anim_border_color.try_to_start()

    def setBorderColor(self, code):
        """
        设置边框颜色
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        color_value = ColorTool.toArray(code)
        self._anim_border_color.setCurrent(color_value)
        self._border_color_handler(color_value)


    # region TextColor
    def setTextColorTo(self, code):
        """
        设置字体颜色，同时启动动画,
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        self._anim_text_color.setTarget(ColorTool.toArray(code))
        self._anim_text_color.try_to_start()

    def setTextColor(self, code):
        """
        设置字体颜色
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        color_value = ColorTool.toArray(code)
        self._anim_text_color.setCurrent(color_value)
        self._text_color_handler(color_value)



    # region Animation
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


    # region Event
    def hideEvent(self, a0):
        super().hideEvent(a0)
        if self.isWidgetFlagOn(Zen.WidgetFlag.DeleteOnHidden):
            self.deleteLater()


    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)
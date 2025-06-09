from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import overload
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.advancedbutton.widget import ButtonLayer
from ZenUI.core import ZExpAnim,AnimGroup,ZColorTool,ZenGlobal,Zen,ZSize,ZColorSheet,ZColors
class ABCButton(QPushButton):
    '''按钮抽象类'''
    moved = Signal(object)
    resized = Signal(object)
    hovered = Signal() # 悬停信号
    leaved = Signal() # 离开信号
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None,
                 icon_size: ZSize = None,
                 tooltip: str = None,
                 immediate_tooltip: bool = False,
                 interrupt_tooltip: bool = False,
                 min_width: int = None,
                 min_height: int = None,
                 min_size: ZSize = None,
                 max_width: int = None,
                 max_height: int = None,
                 max_size: ZSize = None,
                 fixed_size: ZSize = None,
                 sizepolicy: tuple[Zen.SizePolicy, Zen.SizePolicy] = None):
        super().__init__(parent=parent)
        # 父类参数初始化
        if name: self.setObjectName(name)
        if text: self.setText(text)
        if icon: self.setIcon(icon)
        if icon_size: self.setIconSize(icon_size.toQsize())
        if min_width: self.setMinimumWidth(min_width)
        if min_height: self.setMinimumHeight(min_height)
        if min_size: self.setMinimumSize(min_size.toQsize())
        if max_width: self.setMaximumWidth(max_width)
        if max_height: self.setMaximumHeight(max_height)
        if max_size: self.setMaximumSize(max_size.toQsize())
        if fixed_size: self.setFixedSize(fixed_size.toQsize())
        if sizepolicy: self.setSizePolicy(sizepolicy[0].value, sizepolicy[1].value)

        # 信号绑定
        self.hovered.connect(self._hovered_handler) # 链接悬停信号,用于实现悬停动画
        self.pressed.connect(self._pressed_handler) # 链接按钮按下信号,用于实现按下动画
        self.released.connect(self._released_handler) # 链接按钮释放信号,用于实现释放动画
        self.clicked.connect(self._clicked_handler) # 链接按钮按下信号,用于实现点击动画
        self.leaved.connect(self._leaved_handler) # 链接按钮离开信号,用于实现离开动画

        self.setAttribute(Qt.WidgetAttribute.WA_Hover) # 启用 hover 事件
        self.setAttribute(Qt.WidgetAttribute.WA_NoMousePropagation) # 防止鼠标事件传播到父组件
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)  # 确保鼠标事件不会穿透到父组件
        self.installEventFilter(self)

        # Widget 特性
        self._color_sheet = ZColorSheet(self)
        '颜色表，用于存储组件颜色，如背景色，边框色等'
        self._color_sheet.colorChanged.connect(self._colors_refresh_handler) #颜色改变时刷新样式
        self._colors = ZColors()
        '用于快速访问颜色'
        self._theme_manager = ZenGlobal.ui.theme_manager 
        '主题管理器，用于接受主题切换的信号'
        self._theme_manager.themeChanged.connect(self._theme_changed_handler) # 主题切换信号连接
        self._widget_flags = {}
        '组件属性，控制是否具备动画等'
        self._stylesheet_fixed = ''  # 每次调用setStyleSheet方法时，都会在样式表前附加这段固定内容
        '固有样式表'
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

        self._init_anim() # 初始化动画

        # PushButton 特性
        self._layer_hover = ButtonLayer(self)
        '悬停层'
        self._layer_pressed = ButtonLayer(self)
        '按下层'
        self._tooltip = ''
        '提示文本'
        self._text_color = '#000000'
        '文本颜色'
        self._icon_color = '#000000'
        '图标颜色'

        self._enabled_repetitive_clicking = False
        '是否启用重复点击'

        self._immediate_tooltip = immediate_tooltip
        '是否立即显示提示文本'
        self._interrupt_tooltip = interrupt_tooltip
        '悬停移动是否中断提示文本显示'


        self._repeat_click_timer = QTimer(self)
        '重复点击计时器，用于实现重复点击'
        self._repeat_click_timer.setInterval(50)
        self._repeat_click_timer.timeout.connect(self.clicked.emit)

        self._repeat_click_trigger = QTimer(self) 
        '重复点击触发器，点击后延时 500ms 触发重复点击计时器'
        self._repeat_click_trigger.setSingleShot(True)
        self._repeat_click_trigger.timeout.connect(self._repeat_click_timer.start)
        self._repeat_click_trigger.setInterval(500)

        self._tooltip_timer = QTimer(self)  # 创建定时器
        '提示文本定时器，用于实现提示文本的显示'
        self._tooltip_timer.setSingleShot(True)  # 设置为单次触发
        self._tooltip_timer.setInterval(500)  # 设置500ms延迟
        self._tooltip_timer.timeout.connect(self._show_tooltip)  # 连接显示tooltip的槽函数

        # 参数初始化
        if tooltip: self._tooltip = tooltip



    # region Style
    def _init_style(self):
        """
        重写初始样式，创建新组件类使用，配置新组件的初始颜色，动画等
        - 子类实现，初始化时需要自行调用
        """
        pass

    def setStyleSheet(self):
        """设置样式表"""
        self._stylesheet = self.reloadStyleSheet()
        self.setIconColor()
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

    # region Other
    def setToolTip(self, text: str): 
        """设置工具提示"""
        # 劫持这个按钮的tooltip，只能设置outfit的tooltip
        self._tooltip = text

    def toolTip(self): 
        """获取工具提示"""
        return self._tooltip

    def _show_tooltip(self):
        """显示工具提示"""
        pass

    def _hide_tooltip(self):
        """隐藏工具提示"""
        pass

    def setRepetitiveClicking(self, state):
        """设置是否启用重复点击"""
        self._enabled_repetitive_clicking = state

    def hoverLayer(self):
        """获取悬浮层"""
        return self._layer_hover

    def pressLayer(self):
        """获取按下层"""
        return self._layer_pressed

    def minimumSizeHint(self):
        return QSize(48, 32)



    # region WidgetFlag
    def setWidgetFlag(self, flag:Zen.WidgetFlag, on: bool = True):
        """设置`widgetflag`"""
        self._widget_flags[flag.name] = on

    def isWidgetFlagOn(self, flag):
        """查找`widgetflag`是否开启"""
        if flag.name not in self._widget_flags.keys():
            return False
        return self._widget_flags[flag.name]



    # region Slot
    def _theme_changed_handler(self, arg_1):
        '''
        主题改变时的样式切换
        - 接收到主题改变信号时自动调用
        '''
        pass

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

    def _text_color_handler(self, color_value):
        self._text_color = ZColorTool.toCode(color_value)
        self.updateStyle()

    def _icon_color_handler(self, color_value):
        self._icon_color = ZColorTool.toCode(color_value)
        self.updateStyle()

    def _colors_refresh_handler(self, arg):
        '颜色刷新信号槽函数,用于`self._colors`的颜色'
        if arg and self._color_sheet.isSheetNull() is False:
            self._colors.overwrite(self._color_sheet.getSheet())

    def _hovered_handler(self):
        '''悬停信号槽函数'''
        pass

    def _pressed_handler(self):
        '''按下信号槽函数'''
        pass

    def _released_handler(self):
        '''释放信号槽函数'''
        pass

    def _clicked_handler(self):
        '''点击信号槽函数'''
        pass

    def _toggled_handler(self, checked: bool):
        '''切换信号槽函数'''
        pass

    def _leaved_handler(self):
        '''离开信号槽函数'''
        pass

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
        w, h = event.size().width(), event.size().height()
        self._layer_hover.resize(w, h)
        self._layer_pressed.resize(w, h)
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
        self.updateStyle()

    def gradientAnchor(self):
        """获取渐变锚点"""
        return self._gradient_anchor



    # region TextColor
    def setTextColorTo(self, code):
        """
        如果开启了动画，将控件动态的调整到指定文字颜色
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        self._anim_text_color.setTarget(ZColorTool.toArray(code))
        self._anim_text_color.try_to_start()

    def setTextColor(self, code):
        """
        设置字体颜色
        Args:
            code: 格式为`#AARRGGBB`或者`#RRGGBB`
        """
        color_value = ZColorTool.toArray(code)
        self._anim_text_color.setCurrent(color_value)
        self._text_color_handler(color_value)

    # region IconColor
    def setIconColorTo(self, code):
        """如果开启了动画，将控件动态的调整到指定图标颜色"""
        self._anim_icon_color.setTarget(ZColorTool.toArray(code))
        self._anim_icon_color.try_to_start()

    @overload
    def setIconColor(self, code: str) -> None:
        '设置图标颜色'
        pass
    @overload
    def setIconColor(self) -> None:
        '设置图标颜色'
        pass

    def setIconColor(self, *args):
        """设置图标颜色"""
        if len(args) == 1:
            color_value = ZColorTool.toArray(args[0])
            self._anim_icon_color.setCurrent(color_value)
            self._icon_color_handler(color_value)
            return
        icon = self.icon()
        if not icon: return
        # if self._icon_color_is_font_color: # 如果图标颜色与字体颜色相同，则直接使用字体颜色
        #     color = self._text_color  # color = self.palette().color(self.palette().ColorRole.Text)  # 获取当前字体颜色
        # else: color = self._icon_color
        color = self._icon_color
        if self.isCheckable():
            # 获取每种状态下的图标
            pixmap_off = icon.pixmap(self.iconSize(), QIcon.Mode.Normal, QIcon.State.Off)
            pixmap_on = icon.pixmap(self.iconSize(), QIcon.Mode.Normal, QIcon.State.On)
            # 为每个图标填充颜色
            colored_pixmap_off = self._changePixmapColor(pixmap_off, color)
            colored_pixmap_on = self._changePixmapColor(pixmap_on, color)
            # 设置新的图标
            new_icon = QIcon()
            new_icon.addPixmap(colored_pixmap_off, QIcon.Mode.Normal, QIcon.State.Off)
            new_icon.addPixmap(colored_pixmap_on, QIcon.Mode.Normal, QIcon.State.On)
            self.setIcon(new_icon)
        else:
            colored_pixmap = self._changePixmapColor(icon.pixmap(self.iconSize()), color)
            self.setIcon(QIcon(colored_pixmap))


    def _changePixmapColor(self, pixmap: QPixmap, color: str) -> QPixmap:
        """将图标颜色更改为指定颜色"""
        colored_pixmap = pixmap.copy()
        with QPainter(colored_pixmap) as painter:
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(colored_pixmap.rect(), color)
        return colored_pixmap

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

        self._anim_text_color = ZExpAnim(self)
        self._anim_text_color.setFactor(0.25)
        self._anim_text_color.setBias(1)
        self._anim_text_color.ticked.connect(self._text_color_handler)

        self._anim_icon_color = ZExpAnim(self)
        self._anim_icon_color.setFactor(0.25)
        self._anim_icon_color.setBias(1)
        self._anim_icon_color.ticked.connect(self._icon_color_handler)

        self._anim_group = AnimGroup()
        self._anim_group.addMember(self._anim_move, token="move")
        self._anim_group.addMember(self._anim_resize, token="resize")
        self._anim_group.addMember(self._anim_bg_color_a, token="color_a")
        self._anim_group.addMember(self._anim_bg_color_b, token="color_b")
        self._anim_group.addMember(self._anim_border_color, token="border_color")
        self._anim_group.addMember(self._anim_text_color, token="text_color")
        self._anim_group.addMember(self._anim_icon_color, token="icon_color")

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


    def toggleIconAnim(self):
        "切换图标动画的开关状态"
        self._anim_icon_color.setEnable(not self._anim_icon_color.isEnabled())

    def AnimGroup(self):
        """返回动画组"""
        return self._anim_group

    # region Event
    def hideEvent(self, a0):
        super().hideEvent(a0)
        if self.isWidgetFlagOn(Zen.WidgetFlag.DeleteOnHidden):
            self.deleteLater()

    def _show_tooltip(self):
        if self._tooltip != "":
            ZenGlobal.ui.windows["ToolTip"].setText(self._tooltip)
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(self)
            ZenGlobal.ui.windows["ToolTip"].showTip()

    def _hide_tooltip(self):
        if self._tooltip != "":
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(None)
            ZenGlobal.ui.windows["ToolTip"].hideTip()

    def eventFilter(self, obj, event):
        """事件过滤器处理鼠标移动"""
        #print(f"Event type received: {event.type()}")  # 打印所有事件类型
        if obj is self:
            if event.type() == QEvent.Type.HoverEnter:
                # 根据是否立即显示决定处理方式
                if self._immediate_tooltip: self._show_tooltip()
                # 非立即显示模式下启动计时器
                else: self._tooltip_timer.start()
                return False
            elif event.type() == QEvent.Type.HoverMove:
                # 只在中断模式下处理移动事件
                if self._interrupt_tooltip and not self._immediate_tooltip:
                    self._tooltip_timer.stop()
                    self._hide_tooltip()
                    self._tooltip_timer.start()
                return False
            elif event.type() == QEvent.Type.Leave:
                # 离开时停止计时器并隐藏提示
                self._tooltip_timer.stop()
                self._hide_tooltip()
                return False
            elif event.type() == QEvent.Type.ToolTip:
                # 阻止原生tooltip显示
                return True
        return super().eventFilter(obj, event)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hovered.emit()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.leaved.emit()

    def mousePressEvent(self, event):
        self.pressed.emit()
        if self._enabled_repetitive_clicking:
            self._repeat_click_trigger.start()

    def mouseReleaseEvent(self, event):
        self.released.emit()
        #判断按下按钮鼠标还在不在按钮内
        if self.rect().contains(event.pos()):
            self.clicked.emit()
            self.setChecked(not self.isChecked())
        self._repeat_click_trigger.stop()
        self._repeat_click_timer.stop()

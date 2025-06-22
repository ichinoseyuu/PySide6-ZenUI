from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import overload
from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.component.window.widget import ZTitleBar,ResizeGrip,WindowPanel
from ZenUI._legacy.core import Zen,ZMargins,ZQuickEffect,ZExpAnim,AnimGroup
class ABCWindow(QWidget):
    '窗口抽象类'
    moved = Signal(object)
    resized = Signal(object)
    opacityChanged = Signal(float)
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 shadow_width: int = 8,
                 border_radius: int = 4,
                 grip_width: int = 5,
                 can_resize: bool = True):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 无边框窗口
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) #透明背景
        #self.setStyleSheet('background-color:transparent;')
        self._widget_flags = {}
        '组件属性，控制是否具备动画等'
        self._grips = []
        self._grip_width = grip_width
        '拖动调整窗口大小时，鼠标距离窗口边缘的宽度'
        self._shadow_width = shadow_width
        '窗口阴影宽度'
        self._border_radius = border_radius
        '窗口圆角半径'
        self._x1, self._y1, self._x2, self._y2 = None, None, None, None
        '组件可移动区域坐标'
        self._move_anchor = QPoint(self._shadow_width, self._shadow_width)
        '移动锚点'
        self._can_resize = can_resize
        '是否允许调整窗口大小'
        self._ismaximized = False
        '是否最大化'
        self._normal_geometry = QRect()
        '窗口正常状态下的几何信息'
        self._init_anim()
        self._setup_ui()
        self.setOpacity(0)
        self.setOpacityTo(1.0)


    def _setup_ui(self):
        radius = self._border_radius
        margin = int(radius/2)
        self._centerWidget = WindowPanel(parent=self,
                         name="_centerWidget",
                         fixed_stylesheet=f'border-radius:{radius}px;',
                         style=WindowPanel.Style.Monochrome,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(margin, margin, margin, margin))
        self._topGrip = ResizeGrip(self, ResizeGrip.Edge.Top,self._grip_width)
        self._bottomGrip = ResizeGrip(self, ResizeGrip.Edge.Bottom,self._grip_width)
        self._leftGrip = ResizeGrip(self, ResizeGrip.Edge.Left,self._grip_width)
        self._rightGrip = ResizeGrip(self, ResizeGrip.Edge.Right,self._grip_width)
        self._topLeftGrip = ResizeGrip(self, ResizeGrip.Edge.TopLeft,self._grip_width)
        self._topRightGrip = ResizeGrip(self, ResizeGrip.Edge.TopRight,self._grip_width)
        self._bottomLeftGrip = ResizeGrip(self, ResizeGrip.Edge.BottomLeft,self._grip_width)
        self._bottomRightGrip = ResizeGrip(self, ResizeGrip.Edge.BottomRight,self._grip_width)
        ZQuickEffect.applyDropShadowOn(self._centerWidget, (0, 0, 0, 128), blur_radius=int(self._shadow_width*1.5))
        self._titlebar = ZTitleBar(self,self._shadow_width)
        self._centerWidget.layout().addWidget(self._titlebar)

    # region Style
    def _init_style(self):
        """
        重写初始样式，创建新组件类使用，配置新组件的初始颜色，动画等
        - 子类实现，自行调用
        """
        pass


    # region WidgetFlag
    def setWidgetFlag(self, flag:Zen.WidgetFlag, on: bool = True):
        """设置`widgetflag`"""
        self._widget_flags[flag.name] = on


    def isWidgetFlagOn(self, flag):
        """查找`widgetflag`是否开启"""
        if flag.name not in self._widget_flags.keys():
            return False
        return self._widget_flags[flag.name]

# region Other
    def showMaximized(self):
        """最大化窗口"""
        screen = QApplication.primaryScreen()
        # 保存当前几何信息
        panel_geo = self.panelGeometry()
        window_geo = self.geometry()
        # 创建新的 QRect，正确合并窗口位置和面板大小
        self._normal_geometry = QRect(
            window_geo.x() + self._shadow_width,  # 窗口x + 阴影宽度
            window_geo.y() + self._shadow_width,  # 窗口y + 阴影宽度
            panel_geo.width(),                   # 面板宽度
            panel_geo.height()                   # 面板高度
        )
        self._centerWidget.setFixedStyleSheet('border-radius: 0px;')
        self._centerWidget.updateStyle()
        self.resize(screen.size().width(), screen.size().height())
        self.moveTo(screen.geometry().x(), screen.geometry().y())
        self._ismaximized = True

    def showNormal(self):
        """恢复窗口大小"""
        self._centerWidget.setFixedStyleSheet(f'border-radius: {self._border_radius}px;')
        self._centerWidget.updateStyle()
        self.resizeTo(self.normalGeometry().size().width(),self.normalGeometry().size().height())
        self.moveTo(self.normalGeometry().topLeft().x(), self.normalGeometry().topLeft().y())
        self._ismaximized = False


    def isMaximized(self):
        '是否最大化'
        return self._ismaximized

    def normalGeometry(self):
        '获取窗口原始大小'
        return self._normal_geometry

    def panelGeometry(self):
        '获取面板大小'
        return self._centerWidget.geometry()

    def setResizeEnabled(self, enable: bool):
        """设置是否允许调整窗口大小"""
        self._can_resize = enable

    def isResizeEnabled(self):
        """是否允许调整窗口大小"""
        return self._can_resize

    def setCenter(self):
        ''' 将窗口放在屏幕中心 '''
        # 获取当前屏幕的尺寸
        screen = QApplication.primaryScreen()
        # 计算窗口应该放置的位置，使其位于屏幕中央
        x = (screen.geometry().width() - self.geometry().width()) // 2
        y = (screen.geometry().height() - self.geometry().height()) // 2
        # 设置窗口位置为屏幕中心
        self.move(x, y)

    def addWidget(self, widget):
        self._centerWidget.layout().addWidget(widget)

    def insertWidget(self, index, widget):
        self._centerWidget.layout().insertWidget(index, widget)

    def removeWidget(self, widget):
        self._centerWidget.layout().removeWidget(widget)

    def addLayout(self, layout):
        self._centerWidget.layout().addLayout(layout)

    def setWindowTitle(self, arg__1):
        self._titlebar.setTitle(arg__1)

    def sizeHint(self):
        return self._centerWidget.sizeHint()

    # region SlotFunc
    def _move_anim_handler(self, arr):
        x, y = arr
        self.move(int(x), int(y))

    def _resize_anim_handler(self, arr):
        w, h = arr
        self.resize(int(w), int(h))

    def _opacity_anim_handler(self, opacity: float):
        self.setOpacity(opacity)


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
    @overload
    def resize(self, size: QSize):
        """重写 resize 方法，自动添加阴影宽度"""
        pass
    @overload
    def resize(self, w: int, h: int):
        """重写 resize 方法，自动添加阴影宽度"""
        pass
    def resize(self, *args):
        """重写 resize 方法，自动添加阴影宽度"""
        if len(args) == 1:
            size = args[0] + QSize(self._shadow_width * 2, self._shadow_width * 2)
            super().resize(size)
        elif len(args) == 2 :
            w, h = args
            super().resize(w + self._shadow_width * 2, h + self._shadow_width * 2)
        else:
            raise TypeError("resize() takes 1 or 2 arguments, but {} were given".format(len(args)))

    def setMinimumHeight(self, minh):
        return super().setMinimumHeight(minh) + self._shadow_width * 2

    def setMinimumWidth(self, minw):
        return super().setMinimumWidth(minw) + self._shadow_width * 2

    def setMaximumHeight(self, maxh):
        return super().setMaximumHeight(maxh) + self._shadow_width * 2

    def setMaximumWidth(self, maxw):
        return super().setMaximumWidth(maxw) + self._shadow_width * 2

    def setMinimumSize(self, *args):
        if len(args) == 1 and isinstance(args[0], QSize):
            super().setMinimumSize(args[0] + QSize(self._shadow_width * 2, self._shadow_width * 2))
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            super().setMinimumSize(args[0] + self._shadow_width * 2, args[1] + self._shadow_width * 2)

    def setMaximumSize(self, *args):
        if len(args) == 1 and isinstance(args[0], QSize):
            super().setMaximumSize(args[0] + QSize(self._shadow_width * 2, self._shadow_width * 2))
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            super().setMaximumSize(args[0] + self._shadow_width * 2, args[1] + self._shadow_width * 2)

    def resizeEvent(self, event):
        """重写调整大小事件"""
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        shadow = self._shadow_width
        grip = self._grip_width
        center_w = w - 2 * shadow
        center_h = h - 2 * shadow
        self._anim_resize.setCurrent([center_w, center_h])
        if self.isWidgetFlagOn(Zen.WidgetFlag.EnableAnimationSignals):
            self.resized.emit([center_w, center_h])
        self._centerWidget.setGeometry(shadow, shadow, center_w, center_h)
        self._topGrip.setGeometry(shadow, shadow, center_w, grip)
        self._bottomGrip.setGeometry(shadow, shadow + center_h - grip, center_w, grip)
        self._leftGrip.setGeometry(shadow, shadow, grip, center_h)
        self._rightGrip.setGeometry(w - grip - shadow, shadow, grip, center_h)
        self._topLeftGrip.setGeometry(shadow, shadow, grip, grip)
        self._topRightGrip.setGeometry(w - grip - shadow, shadow, grip, grip)
        self._bottomLeftGrip.setGeometry(shadow, shadow + center_h - grip, grip, grip)
        self._bottomRightGrip.setGeometry(w - grip - shadow, shadow + center_h - grip, grip, grip)


    # region Opacity
    def setOpacityTo(self, opacity: float):
        """
        如果开启了动画，将控件动态的调整到指定透明度
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


    # region Animation
    def _init_anim(self):
        """
        创建动画，并添加到动画组
        - 需要创建新动画时，调用此方法，以初始化动画
        """
        self._anim_move = ZExpAnim(self)
        self._anim_move.setFactor(0.8)
        self._anim_move.setBias(1)
        self._anim_move.setCurrent([0, 0])
        self._anim_move.setTarget([0, 0])
        self._anim_move.ticked.connect(self._move_anim_handler)

        self._anim_resize = ZExpAnim(self)
        self._anim_resize.setFactor(0.8)
        self._anim_resize.setBias(1)
        self._anim_resize.setCurrent([0, 0])
        self._anim_resize.setTarget([0, 0])
        self._anim_resize.ticked.connect(self._resize_anim_handler)

        self._anim_opacity = ZExpAnim(self)
        self._anim_opacity.setFactor(0.2)
        self._anim_opacity.setBias(0.01)
        self._anim_opacity.ticked.connect(self._opacity_anim_handler)

        # 创建动画组，以tokenize以上动画
        self._anim_group = AnimGroup()
        self._anim_group.addMember(self._anim_move, token="move")
        self._anim_group.addMember(self._anim_resize, token="resize")
        self._anim_group.addMember(self._anim_opacity, token="opacity")

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

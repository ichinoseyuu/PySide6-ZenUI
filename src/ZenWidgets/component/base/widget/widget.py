import inspect
from typing import TypeVar,cast,get_origin,overload,Any,Union,Optional,TYPE_CHECKING
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QEvent,QPoint,QSize,Signal
from PySide6.QtGui import QMouseEvent
from ZenWidgets.component.base.controller import *
from ZenWidgets.core import make_getter,ZState,ZStyle
if TYPE_CHECKING:
    from ZenWidgets.component.layouts.layout import ZBoxLayout

T = TypeVar('T')

class ZPlaceHolderWidget(QWidget):
    '''占位组件'''

    def parentWidget(self) -> Optional['ZWidget']:
        return super().parentWidget()

    def layout(self) -> Optional['ZBoxLayout']:
        return super().layout()

    def heightHint(self) -> int: return self.sizeHint().height()

    def widthHint(self) -> int: return self.sizeHint().width()

class ZContentWidget(QWidget):
    '''内容组件'''
    def parentWidget(self) -> Optional['ZWidget']:
        return super().parentWidget()

    def layout(self) -> Optional['ZBoxLayout']:
        return super().layout()

    def heightHint(self) -> int: return self.sizeHint().height()

    def widthHint(self) -> int: return self.sizeHint().width()

class ZWidget(QWidget):
    '''ZenWidgets 组件的基类'''
    __controllers_types__ = (
        ZAnimatedColor,
        ZAnimatedOpacity,
        ZAnimatedPoint,
        ZAnimatedPointF,
        ZAnimatedSize,
        ZAnimatedRect,
        ZAnimatedFloat,
        ZAnimatedLinearGradient,
        ZStyleController,
        ZFlashEffect,
        ZOpacityEffect,
        ZAnimatedInt,
    )
    '''控制器类型'''
    __controllers_kwargs__: dict[str, Any] = {}
    '''控制器参数'''
    dragged = Signal(QPoint)
    '''拖拽信号'''
    moved = Signal(QPoint)
    '''移动信号'''
    resized = Signal(QSize)
    '''调整大小信号'''
    def __init__(self,
                 parent: Optional['ZWidget'] = None,
                 *args,
                 style: ZStyle = ZStyle.Default,
                 dragable: bool = False,
                 move_anchor: QPoint = QPoint(0, 0),
                 objectName: str | None = None,
                 toolTip: str | None = None,
                 **kwargs
                 ):
        super().__init__(parent,
                         *args,
                         objectName=objectName,
                         toolTip=toolTip,
                         **kwargs
                         )
        self._state: ZState = ZState.Idle
        self._style: ZStyle = style
        self._move_anchor: QPoint = move_anchor
        self._draggable: bool = dragable
        self._drag_pos: QPoint | None = None
        self._windowOpacityCtrl: ZWindowOpacity = ZWindowOpacity(self)
        self._widgetSizeCtrl: ZWidgetSize = ZWidgetSize(self)
        self._widgetPositionCtrl: ZWidgetPosition = ZWidgetPosition(self)
        self._widgetRectCtrl: ZWidgetRect = ZWidgetRect(self)
        self._opacityCtrl: ZAnimatedOpacity = ZAnimatedOpacity(self)
        self._create_controllers_()

    # region property
    @property
    def windowOpacityCtrl(self) -> ZWindowOpacity: return self._windowOpacityCtrl

    @property
    def widgetSizeCtrl(self) -> ZWidgetSize: return self._widgetSizeCtrl

    @property
    def widgetPositionCtrl(self) -> ZWidgetPosition: return self._widgetPositionCtrl

    @property
    def widgetRectCtrl(self) -> ZWidgetRect: return self._widgetRectCtrl

    @property
    def opacityCtrl(self) -> ZAnimatedOpacity: return self._opacityCtrl

    # region private method
    def _create_controllers_(self) -> None:
        '''创建控制器，不需要子类重写'''
        allowed_types = self.__controllers_types__
        controllers_kwargs: dict[str, Any] = {}
        annotations: dict[str, Any] = {}
        # 遍历类的继承链，从ZWidget类和其子类中获取注解和控制器参数，让子类的注解覆盖父类的注解
        for cls in reversed(self.__class__.__mro__):
            if not issubclass(cls, ZWidget): continue
            controllers_kwargs.update(getattr(cls, '__controllers_kwargs__', {}))
            annotations.update(getattr(cls, '__annotations__', {}))

        # 过滤出属于控制器类型的注解
        filtered_annotations: dict[str, Any] = {}
        for name, ctrl_type in annotations.items():
            # 获取注解的实际类型
            origin_type = get_origin(ctrl_type) or ctrl_type
            # 如果注解类型是控制器类型，则添加到过滤后的注解中
            if inspect.isclass(origin_type) and issubclass(origin_type, allowed_types):
                filtered_annotations[name] = ctrl_type

        # 创建控制器实例并绑定到实例与类上（若需要则创建 property）
        for name, ctrl_type in filtered_annotations.items():
            ckwargs = controllers_kwargs.get(name, {})
            controller = ctrl_type(self, **ckwargs)
            # 创建实例变量
            setattr(self, f'_{name}', controller)
            # 创建类属性
            if not hasattr(self.__class__, name): setattr(self.__class__, name, property(make_getter(name)))
            # 如果是样式控制器，则绑定样式改变时的槽函数
            if ctrl_type.__name__ == 'ZStyleController':
                style_controller = cast(ZStyleController[T], controller)
                style_controller.styleChanged.connect(self._style_change_handler_)

    def _init_style_(self) -> None:
        '''初始化样式'''
        ...

    def _style_change_handler_(self) -> None:
        '''样式变化槽函数'''
        ...

    def _show_tooltip_(self) -> None:
        '''显示提示框'''
        ...

    def _hide_tooltip_(self) -> None:
        '''隐藏提示框'''
        ...

    # region public method
    def state(self) -> ZState: return self._state

    def style(self) -> ZStyle: return self._style

    def moveAnchor(self): return self._move_anchor

    def isFlat(self) -> bool: return self._style == ZStyle.Flat

    def isPressed(self) -> bool: return self._state == ZState.Pressed

    def isHover(self) -> bool: return self._state == ZState.Hover

    def isHidden(self) ->bool: return True if self.windowOpacity() == 0 else False

    def isShowing(self) ->bool: return False if self.windowOpacity() == 0 else True

    def isDraggable(self) -> bool: return self._draggable

    def isMoving(self) -> bool: return self.widgetPositionCtrl.animation.isRunning()

    def isResizing(self) -> bool: return self.widgetSizeCtrl.animation.isRunning()

    def isFading(self) -> bool: return self.opacityCtrl.animation.isRunning()

    def isWindowFading(self) -> bool: return self.windowOpacityCtrl.animation.isRunning()

    def setDraggable(self, d: bool) -> None:
        if d == self._draggable: return
        self._draggable = d

    def setStyle(self, s: ZStyle):
        self._style = s
        self.update()

    @overload
    def setMoveAnchor(self, x: int, y: int) -> None: ...

    @overload
    def setMoveAnchor(self, pos: QPoint) -> None: ...

    def setMoveAnchor(self, *args): self._move_anchor = QPoint(*args)

    @overload
    def moveTo(self, x: int, y: int) -> None: ...

    @overload
    def moveTo(self, pos: QPoint) -> None: ...

    def moveTo(self, *args): self.widgetPositionCtrl.moveTo(*args)

    @overload
    def resizeTo(self, w: int, h: int) -> None: ...

    @overload
    def resizeTo(self, size: QSize) -> None: ...

    def resizeTo(self, *args): self.widgetSizeCtrl.resizeTo(*args)

    @overload
    def move(self, x: int, y: int) -> None: ...

    @overload
    def move(self, pos: QPoint) -> None: ...

    def move(self, *args): point = QPoint(*args); super().move(point - self._move_anchor)

    def fadeIn(self) -> None:
        self.opacityCtrl.fadeIn()

    def fadeOut(self) -> None:
        self.opacityCtrl.fadeOut()

    def windowFadeIn(self) -> None:
        self.windowOpacityCtrl.fadeIn()

    def windowFadeOut(self) -> None:
        self.windowOpacityCtrl.fadeOut()

    def setEnabled(self, e: bool) -> None:
        if e == self.isEnabled(): return
        if e: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(e)

    def parentWidget(self) -> Optional['ZWidget']:
        return super().parentWidget()

    def layout(self) -> Optional['ZBoxLayout']:
        return super().layout()

    def heightHint(self) -> int: return self.sizeHint().height()

    def widthHint(self) -> int: return self.sizeHint().width()

    # region event
    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ToolTip: return True
        return super().event(event)

    def moveEvent(self, event):
        super().moveEvent(event)
        self.moved.emit(self.pos())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit(self.size())

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if self._draggable and event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if self._draggable and event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.pos() - self._drag_pos
            if delta.manhattanLength() >= 5:
                self.dragged.emit(delta)


class ZPlaceHolderWidget(ZWidget):
    '''占位组件'''
    pass


class ZContentWidget(ZWidget):
    '''内容组件'''
    pass
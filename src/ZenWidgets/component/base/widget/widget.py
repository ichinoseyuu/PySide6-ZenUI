import inspect
import logging
from typing import TypeVar, cast, get_origin, overload
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QEvent,QPoint,QSize,Signal
from PySide6.QtGui import QColor
from ZenWidgets.component.base.controller import *
from ZenWidgets.core import ZButtonStyleData,make_getter,ZState

T = TypeVar('T')

class ZWidget(QWidget):
    __controllers_kwargs__ = {}
    __controllers_types__ = [
        ZAnimatedWindowOpacity,
        ZAnimatedWidgetPosition,
        ZAnimatedWidgetSize,
        ZAnimatedWidgetRect,
        QAnimatedWindowBody,
        StyleController,
        QAnimatedColor,
        QAnimatedLinearGradient,
        ZAnimatedOpacity,
        ZAnimatedPoint,
        ZAnimatedPointF,
        ZAnimatedSize,
        ZAnimatedRect,
        QAnimatedFloat,
        QAnimatedInt
        ]

    windowOpacityCtrl: ZAnimatedWindowOpacity
    widgetSizeCtrl: ZAnimatedWidgetSize
    widgetPositionCtrl: ZAnimatedWidgetPosition

    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self._state = ZState.Idle
        self._move_anchor = QPoint(0, 0)
        self._x1, self._y1, self._x2, self._y2 = None, None, None, None
        controllers_kwargs = {}
        annotations = {}
        for cls in reversed(inspect.getmro(self.__class__)):
            if not issubclass(cls, ZWidget):
                continue
            controllers_kwargs.update(getattr(cls, '__controllers_kwargs__', {}))
            annotations.update(getattr(cls, '__annotations__', {}))

        allowed_types = tuple(self.__controllers_types__)
        filtered_annotations = {}
        for name, ctrl_type in annotations.items():
            # 获取泛型的原始类型（如StyleController[T]的原始类型是StyleController）
            origin_type = get_origin(ctrl_type) or ctrl_type
            if inspect.isclass(origin_type) and issubclass(origin_type, allowed_types):
                filtered_annotations[name] = ctrl_type

        # 使用合并后的配置创建控制器
        for name, ctrl_type in filtered_annotations.items():
            #logging.info(f'creating {name}({ctrl_type.__name__}) for {self.__class__.__name__}')
            kwargs = controllers_kwargs.get(name, {})
            controller = ctrl_type(self,** kwargs)
            setattr(self, f'_{name}', controller)
            if not hasattr(self.__class__, name):
                setattr(self.__class__, name, property(make_getter(name)))

            if ctrl_type.__name__ == 'StyleController':
                style_controller = cast(StyleController[T], controller)
                style_controller.styleChanged.connect(self._style_change_handler_)


    def _init_style_(self) -> None:
        '''初始化样式'''

    def _style_change_handler_(self) -> None:
        '''主题改变时的槽函数'''

    # region public method
    def state(self) -> ZState:
        return self._state

    def setToolTip(self, tip: str) -> None:
        super().setToolTip(tip)
        self.update()

    def setMoveLimits(self, x1: int, y1: int, x2: int, y2: int):
        if x1 > x2 or y1 > y2: raise ValueError('x1 must less than x2,y1 must less than y2')
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2

    def moveAnchor(self): return self._move_anchor

    @overload
    def setMoveAnchor(self, x: int, y: int) -> None: ...

    @overload
    def setMoveAnchor(self, pos: QPoint) -> None: ...

    def setMoveAnchor(self, *args): self._move_anchor = QPoint(*args)

    @overload
    def moveTo(self, x: int, y: int) -> None: ...

    @overload
    def moveTo(self, pos: QPoint) -> None: ...

    def moveTo(self, *args):
        pos = QPoint(*args)
        x, y = self._legalize_moving_target(pos.x(), pos.y())
        self.widgetPositionCtrl.moveTo(x, y)

    @overload
    def resizeTo(self, w: int, h: int) -> None: ...

    @overload
    def resizeTo(self, size: QSize) -> None: ...

    def resizeTo(self, *args): self.widgetSizeCtrl.resizeTo(*args)

    @overload
    def move(self, x: int, y: int) -> None: ...

    @overload
    def move(self, pos: QPoint) -> None: ...

    def move(self, *args):
        point = QPoint(*args) - self._move_anchor
        super().move(point)

    # region private method
    def _legalize_moving_target(self, x: int, y: int) -> tuple[int, int]:
        '''限制移动范围'''
        return max(self._x1, min(self._x2 - self.width(), x)), max(self._y1, min(self._y2 - self.height(), y))

    # region event
    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ToolTip:
            return True
        return super().event(event)


# region ==========================
class MyWidget(ZWidget):
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat

    __controllers_kwargs__ = {
        'bodyColorCtrl': {
            'color': QColor('#202020')
        },
        'borderColorCtrl': {
            'color': QColor('#1d1d1d')
        },
        'radiusCtrl': {
            'value': 5.0
        }
    }
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

class MyWidgetSub(MyWidget):
    locationCtrl: ZAnimatedWidgetPosition
    sizeCtrl: ZAnimatedWidgetSize
    opacityCtrl: ZAnimatedOpacity
    styleCtrl: StyleController[ZButtonStyleData]

    __controllers_kwargs__ = {
        'styleCtrl': {
            'key': 'ZButton'
        }
    }
    def __init__(self, parent=None):
        super().__init__(parent)
        #print(self.styleCtrl.data)

from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    app = QApplication([])
    w = MyWidgetSub()
    w.show()
    # print(w.bodyColorCtrl.color)
    # print(w.borderColorCtrl.color)
    # print(w.radiusCtrl.value)
    # print(w.locationCtrl.pos)
    # print(w.sizeCtrl.size)
    # print(w.opacityCtrl.opacity)
    # print(w.__controllers_kwargs__)
    # print(w.__controllers_types__)
    # print(w.styleCtrl.data)
    # 打印所有属性名（包括property和实例变量）
    print(id(type(w).styleCtrl.fget))
    w2 = MyWidgetSub()
    print(id(type(w2).styleCtrl.fget))
    print(w is w2)  # False
    print(type(w) is type(w2))
    # print("property attributes:")
    # for name in dir(w):
    #     if isinstance(getattr(type(w), name, None), property):
    #         print(f"  {name} (property)")
    # for name, ctrl in w.__dict__.items():
    #     print(name, ctrl)
    # print(StyleController[StyleDataT] is StyleController)
    # print(StyleController[ZButtonStyleData],f'\n',StyleController[StyleDataT],f'\n',StyleController)
    app.exec()
import inspect
import logging
from typing import TypeVar, cast, get_origin
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from ZenUI.component.base.controller import *
from ZenUI.core import ZDebug,ZButtonStyleData

# 定义一个泛型类型变量，用于匹配StyleController的泛型参数
T = TypeVar('T')

class ZWidget(QWidget):
    __controllers_types__ = [
        ColorController,
        LinearGradientController,
        OpacityController,
        WindowOpacityController,
        PositionController,
        PointController,
        PointFController,
        WidgetSizeController,
        SizeController,
        RectController,
        GeometryController,
        FloatController,
        IntegerController,
        StyleController,
        ]
    __controllers_kwargs__ = {}
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        # 合并 ZWidget 所以子类（包括ZWidget）的__controllers_kwargs__和注解
        controllers_kwargs = {}
        annotations = {}
        for cls in inspect.getmro(self.__class__):
            if not issubclass(cls, ZWidget):
                continue
            controllers_kwargs.update(getattr(cls, '__controllers_kwargs__', {}))
            annotations.update(getattr(cls, '__annotations__', {}))

        # 筛选允许的控制器类型
        allowed_types = tuple(self.__controllers_types__)
        # filtered_annotations = {
        #     name: ctrl_type
        #     for name, ctrl_type in annotations.items()
        #     if inspect.isclass(ctrl_type) and issubclass(ctrl_type, allowed_types)
        # } # 使用字典推导式筛选允许的控制器类型，对泛型注解的处理不正确

        filtered_annotations = {}
        for name, ctrl_type in annotations.items():
            # 获取泛型的原始类型（如StyleController[T]的原始类型是StyleController）
            origin_type = get_origin(ctrl_type) or ctrl_type
            # 检查原始类型是否在允许的类型列表中
            if inspect.isclass(origin_type) and issubclass(origin_type, allowed_types):
                filtered_annotations[name] = ctrl_type

        # 使用合并后的配置创建控制器
        for name, ctrl_type in filtered_annotations.items():
            if ZDebug.is_logging:
                logging.info(f'Creating {name}({ctrl_type.__name__}) for {self.__class__.__name__}')

            # 从合并后的配置中获取参数
            kwargs = controllers_kwargs.get(name, {})
            # 根据类型创建控制器实例
            controller = ctrl_type(self,** kwargs)

            # 生成 _name 成员存到实例上
            setattr(self, f'_{name}', controller)
            # 生成类上添加一次 property
            if not hasattr(self.__class__, name):
                def make_getter(attr_name):
                    def getter(self):
                        return getattr(self, f'_{attr_name}')
                    return getter
                setattr(self.__class__, name, property(make_getter(name)))

            # 当控制器类型是StyleController时，连接styleChanged信号到槽函数
            if ctrl_type.__name__ == 'StyleController':
                style_controller = cast(StyleController[T], controller)
                style_controller.styleChanged.connect(self._style_change_handler_)


    def _init_style_(self):
        '''初始化样式'''

    def _style_change_handler_(self):
        '''主题改变时的槽函数'''


class MyWidget(ZWidget):
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    radiusCtrl: FloatController

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
    def __init__(self, parent=None):
        super().__init__(parent)

class MyWidgetSub(MyWidget):
    locationCtrl: PositionController
    sizeCtrl: WidgetSizeController
    opacityCtrl: OpacityController
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
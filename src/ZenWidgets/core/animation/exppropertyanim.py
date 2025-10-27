from typing import Any,overload
import numpy
from PySide6.QtCore import *
from PySide6.QtGui import *

class TypeConversionFuncs:
    functions = {
        QPoint.__name__: [
            lambda x: numpy.array((x.x(), x.y()), dtype="float32"),
            lambda x: QPoint(int(x[0]), int(x[1]))
        ],
        QPointF.__name__: [
            lambda x: numpy.array((x.x(), x.y()), dtype="float32"),
            lambda x: QPointF(float(x[0]), float(x[1])),
        ],
        QSize.__name__: [
            lambda x: numpy.array((x.width(), x.height()), dtype="float32"),
            lambda x: QSize(int(x[0]), int(x[1])),
        ],
        QSizeF.__name__: [
            lambda x: numpy.array((x.width(), x.height()), dtype="float32"),
            lambda x: QSizeF(float(x[0]), float(x[1])),
        ],
        QRect.__name__: [
            lambda x: numpy.array((x.x(), x.y(), x.width(), x.height()), dtype="float32"),
            lambda x: QRect(int(x[0]), int(x[1]), int(x[2]), int(x[3]))
        ],
        QRectF.__name__: [
            lambda x: numpy.array((x.x(), x.y(), x.width(), x.height()), dtype="float32"),
            lambda x: QRect(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
        ],
        QColor.__name__: [
            lambda x: numpy.array(x.getRgb(), dtype="float32"),
            lambda x: QColor(int(x[0]), int(x[1]), int(x[2]), int(x[3]))
        ]
    }


class ZExpPropertyAnimation(QAbstractAnimation):
    valueChanged = Signal(object)

    def __init__(self, target: QObject, property_name=None, parent=None) -> None:
        super().__init__(parent)
        self.start_after_timer = QTimer(self)

        self._target = target
        self._property_name = None
        self._property_type = None
        self._in_func = None
        self._out_func = None
        self._start_value = None
        self._end_value = None
        self._current_value = None
        self.factor = 1/4
        self.bias = 0.5

        self._velocity_inertia = 0.0  #值介于0和1之间，值越大，动画越难加速。
        self._velocity = 0

        if property_name is not None:
            self.setPropertyName(property_name)
        if target.objectName() == 'hslider_1':print(self._target.property(self._property_name))
        self.finished.connect(self.resetStartValue)


    def init(self, factor:float=None, bias:float=None, current_value=None, end_value=None) -> None:
        if factor is not None: self.setFactor(factor)
        if bias is not None: self.setBias(bias)
        if current_value is not None: self.setStartValue(current_value)
        if end_value is not None: self.setEndValue(end_value)
        self.resetVelocity()

    def isRunning(self) -> bool:
        return self.state() == QAbstractAnimation.State.Running

    def setFactor(self, factor: float):
        """
        设置动画的衰减因子，控制动画的平滑度

        该因子决定了当前进度对步长的影响程度：
        - 值越接近 0 ：步长衰减越快，动画会显得更平滑（缓动效果明显），但需要更多帧数完成
        - 值越接近 1 ：步长衰减越慢，动画会更直接快速，但可能出现跳帧现象

        注意：
        - 必须在 (0, 1) 区间内
        - 典型值范围建议在 0.1 ~ 0.5 之间

        """
        if not 0 < factor < 1:
            raise ValueError(f"Factor must be between 0 and 1 (exclusive), got {factor}")
        self.factor = factor


    def setBias(self, bias: float):
        """
        设置最小步长阈值，防止动画在接近目标时过慢

        作用：
        1. 保证动画在接近终点时能直接到达目标值（避免无限逼近）
        2. 控制动画的初始速度基准值

        特性：
        - 值越大：动画初期移动越快，但可能错过精确位置需要回弹
        - 值越小：动画精度越高，但初期移动缓慢

        建议：
        - 应根据目标值的量级设置（如操作像素坐标推荐 1 ~ 5 之间）
        - 对于大数值范围（如 0 - 1000 ）可适当增大
        """
        if bias <= 0:
            raise ValueError(f"Bias must be positive, got {bias}")
        self.bias = bias


    def target(self) -> QObject:
        return self._target


    def propertyName(self) -> str:
        return self._property_name


    def endValue(self, raw=False) -> Any:
        if raw is True:
            return self._end_value
        else:
            return self._out_func(self._end_value)


    def currentValue(self, raw=False) -> Any:
        if raw is True:
            return self._current_value
        else:
            return self._out_func(self._current_value)


    def distance(self) -> numpy.array:
        return self._end_value - self._current_value


    def duration(self) -> int:
        return -1


    def start(self, *args, **kwargs):
        # new 2025.10.14
        if self._start_value is None:
            self.fromProperty()
        if (self._current_value == self._end_value).all():
            # If current value equals end value, do not start the animation
            return
        if self.state() != QAbstractAnimation.State.Running:
            super().start(*args, **kwargs)


    def startAfter(self, msec: int):
        self.start_after_timer.singleShot(msec, self.start)


    def fromProperty(self):
        """ load value from target's property """
        self.setStartValue(self._target.property(self._property_name))


    def toProperty(self):
        """ set target's property to animation value """
        self._target.setProperty(self._property_name, self._out_func(self._current_value))


    def setPropertyName(self, name: str) -> None:
        self._property_name = name
        self._property_type = type(self._target.property(name))
        self._loadConversionFuncs()
        self._end_value = self._in_func(self._target.property(name))
        self._current_value = self._in_func(self._target.property(name))


    def setEndValue(self, value: Any) -> None:
        if isinstance(value, self._property_type):
            self._end_value = self._in_func(value)
        else:
            self._end_value = numpy.array(value)


    def setStartValue(self, value: Any) -> None:
        # if isinstance(value, self._property_type):
        #     self._current_value = self._in_func(value)
        # else:
        #     self._current_value = numpy.array(value)
        # self.valueChanged.emit(self._current_value)
        if isinstance(value, self._property_type):
            self._start_value = self._in_func(value)
        else:
            self._start_value = numpy.array(value)
        self._current_value = self._start_value.copy()
        self.valueChanged.emit(self._current_value)

    def resetStartValue(self) -> None:
        """重置起始值为无效状态"""
        self._start_value = None

    def resetVelocity(self):
        self._velocity = 0 * self._current_value


    def setVelocityInertia(self, n: float):
        '''值介于 0 和 1 之间，值越大，动画越难加速。'''
        self._velocity_inertia = n


    def updateCurrentTime(self, _) -> None:
        #print(self.distance())
        if (self.distance() == 0).all():
            self.stop()
            return
        distance = self._end_value - self._current_value
        flag = numpy.array(abs(distance) <= self.bias, dtype="int8")
        step = abs(distance) * self.factor + self.bias                   # 基本指数动画运算
        step = step * (numpy.array(distance > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        step = step * (1 - flag) + distance * flag                       # 差距小于偏置的项，返回差距

        self._velocity = self._velocity * self._velocity_inertia + step * (1 - self._velocity_inertia)

        self._current_value = self._current_value + self._velocity
        self.valueChanged.emit(self._current_value)
        try:
            self._target.setProperty(self._property_name, self._out_func(self._current_value))
        except RuntimeError:
            pass


    def _loadConversionFuncs(self) -> None:
        if self._property_type.__name__ in TypeConversionFuncs.functions.keys():
            self._in_func = TypeConversionFuncs.functions.get(self._property_type.__name__)[0]
            self._out_func = TypeConversionFuncs.functions.get(self._property_type.__name__)[1]
        else:
            self._in_func = lambda x: numpy.array(x)
            self._out_func = lambda x: self._property_type(numpy.array(x, dtype="float32"))
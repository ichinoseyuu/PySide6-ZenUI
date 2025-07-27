from typing import Any
import numpy
from PySide6.QtCore import *
from PySide6.QtGui import *

__all__ = ['ZExpAnimation','AnimationGroup','ExpAccelerateAnim',
           'SqrExpAnimation','CounterAnimation']

global_fps = 60

class Curve:
    @staticmethod
    def LINEAR(x):
        return x

class ABCAnimation(QObject):
    ticked = Signal(object)     # 动画进行一刻的信号
    finished = Signal(object)   # 动画完成的信号，回传目标值

    def __init__(self, parent=None):
        super().__init__(parent)

        self.enabled = True
        self.target_ = numpy.array(0)         # 目标值
        self.current_ = numpy.array(0)        # 当前值
        self.counter = 0                     # 计数器

        # 构建计时器
        self.timer = QTimer()
        self.timer.setInterval(int(1000/global_fps))
        self.timer.timeout.connect(self._process)  # 每经历 interval 时间，传入函数就被触发一次
        # self.timer.setTimerType(Qt.PreciseTimer)

        # 构建行为计时器
        self.action_timer = QTimer()
        self.action_timer.setSingleShot(True)
        # self.action_timer.setTimerType(Qt.PreciseTimer)

    def setEnable(self, state: bool):
        self.enabled = state
        if state is False:
            self.stop()


    def isEnabled(self):
        return self.enabled


    def setFPS(self, fps: int):
        """设置动画的帧率"""
        self.timer.setInterval(int(1000 / fps))


    def setTarget(self, target):
        """
        设置动画的目标值
        Args:
            target: 任何可以参与计算的值
        """
        self.target_ = numpy.array(target)


    def setCurrent(self, current):
        """
        设置动画的当前值
        Args:
            current: 任何可以参与计算的值
        """
        self.current_ = numpy.array(current)


    def current(self):
        """
        返回动画计数器的当前值
        Returns:
            当前值
        """
        return self.current_


    def target(self):
        """
        返回动画计数器的目标值
        Returns:
            目标值
        """
        return self.target_


    def _distance(self):
        """
        计算当前值与目标值之间的距离
        Returns:
            距离
        """
        return self.target_ - self.current_


    def _step_length(self):
        "步长计算，由子类实现"
        raise NotImplementedError()


    def _process(self):
        "处理动画的过程，由子类实现"
        raise NotImplementedError()


    def isCompleted(self):
        """检查是否达到动画应该停止的点，由子类实现"""
        raise NotImplementedError()


    def isActive(self):
        """检查动画是否正在运行 """
        return self.timer.isActive()


    def stop(self, delay: int | None = None):
        """
        停止动画
        Args:
            delay: 此操作生效前的时间延迟
        """
        if delay is None:
            self.timer.stop()
        else:
            self.action_timer.singleShot(delay, self.timer.stop)


    def start(self, delay: int | None = None):
        """
        开始动画
        Args:
            delay: 此操作生效前的时间延迟
        """
        if self.isEnabled() is False:
            return
        if delay is None:
            self.timer.start()
        else:
            self.action_timer.singleShot(delay, self.timer.start)

    def setInterval(self, interval: int):
        """
        设置动画的时间间隔
        Args:
            interval: 时间间隔，单位毫秒
        """
        self.timer.setInterval(interval)


    def try_to_start(self, delay=None):
        """
        尝试启动动画，如果动画已经启动则不启动
        """
        if not self.isActive():
            self.start(delay=delay)
        return not self.isActive()


class ZExpAnimation(ABCAnimation):
    """ 级数动画类，每次动画的进行步长都与当前进度有关 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.factor = 0.25
        self.bias = 1

    def init(self, factor: float, bias: float, current: Any, target: Any, fps: int = 60):
        self.setFactor(factor)
        self.setBias(bias)
        self.setCurrent(current)
        self.setTarget(target)
        self.setFPS(fps)


    def setFactor(self, factor: float):
        """
        设置动画因子
        Args:
            factor: 介于0和1之间的数字,表示动画的步长与当前进度的关系, 数值越小则动画越平滑, 但性能开销越大
        """
        self.factor = factor


    def setBias(self, bias: float):
        """
        设置动画偏差
        Args:
            bias: 大于0的正浮点数, 表示动画的步长与当前进度的偏差, 数值越大则动画越快, 但可能造成动画跨度大, 不精确
        """
        if bias <= 0:
            raise ValueError(f"Bias is expected to be positive but met {bias}")
        self.bias = bias


    def _step_length(self):
        """ 计算当前步长 """
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = abs(dis) * self.factor + self.bias  # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut  # 对于差距小于偏置的项，直接返回差距
        return arr


    def _process(self):
        """ 处理动画 """
        # 如果已经到达既定位置，终止计时器，并发射停止信号
        if self.isCompleted():
            self.stop()
            self.finished.emit(self.target_)
            return
        step_length = self._step_length()
        self.setCurrent(self.current_ + step_length)
        self.ticked.emit(self.current_)

    def isCompleted(self):
        """检查是否达到动画应该停止的点"""
        return (self._distance() == 0).all()



class ExpAccelerateAnim(ZExpAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.accelerate_function = lambda x: x ** 1.6
        self.step_length_bound = 0
        self.frame_counter = 0

    def setAccelerateFunction(self, function):
        self.accelerate_function = function

    def setStepLengthBound(self, bound):
        self.step_length_bound = bound

    def refreshStepLengthBound(self):
        self.setStepLengthBound(min(self.accelerate_function(self.frame_counter), 10000))  # prevent getting too large

    def _step_length(self):
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = numpy.clip(abs(dis) * self.factor + self.bias, 0, self.step_length_bound)  # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut  # 对于差距小于偏置的项，直接返回差距
        return arr

    def _process(self):
        self.frame_counter += 1
        self.refreshStepLengthBound()
        super()._process()

    def stop(self, delay=None):
        super().stop(delay)
        self.frame_counter = 0
        self.refreshStepLengthBound()


class SqrExpAnimation(ABCAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mean_rate = 0.5
        self.base = 1/2
        self.peak = 10
        self.bias = 1
        raise NotImplementedError()

    def setMeanRate(self, mean_rate):
        self.mean_rate = mean_rate

    def setBase(self, base):
        self.base = base

    def setPeak(self, peak):
        self.peak = peak

    def setBias(self, bias):
        self.bias = bias

    def _step_length(self):
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = abs(dis) * self.factor + self.bias  # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut  # 对于差距小于偏置的项，直接返回差距
        return arr

    def isCompleted(self):
        return (self._distance() == 0).all()


class CounterAnimation(ABCAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.duration = 1000  # 动画总时长，单位毫秒
        self.reversed = False  # 是否倒序运行动画
        self.counter_addend = self._get_addend()
        self.curve = Curve.LINEAR

    def setReversed(self, reversed_):
        """
        Set whether the animation is reversed
        :param reversed_:
        :return:
        """
        self.reversed = reversed_

    def setDuration(self, duration):
        """
        Set the duration of the animation.
        :param duration: ms
        :return:
        """
        self.duration = duration
        self.counter_addend = self._get_addend()

    def setInterval(self, interval: int):
        super().setInterval(interval)
        self.counter_addend = self._get_addend()

    def _get_addend(self):
        """
        Get the addend for the counter
        :return:
        """
        duration = self.duration
        interval = self.timer.interval()  # 两个值全是 毫秒 ms
        return interval / duration

    def setCurve(self, curve_func):
        """
        Set the animation curve.
        :param curve_func: a function which expect an input between 0 and 1, return a float number
        :return:
        """
        self.curve = curve_func

    def isCompleted(self):
        """
        To check whether we meet the point that the animation should stop
        :return: bool
        """
        self.counter = max(min(1, self.counter), 0)  # 规范计数器数值，防止超出范围
        return (self.reversed is False and self.counter == 1) or (self.reversed and self.counter == 0)

    def _process(self):
        # 如果已经到达既定位置，终止计时器，并发射停止信号
        if self.isCompleted():
            self.stop()
            self.finished.emit(self.target_)
            return

        # 计数器更新
        self.counter = self.counter + (-1 if self.reversed else 1) * self.counter_addend

        # 更新数值
        self.setCurrent(self.curve(self.counter))

        # 发射信号
        self.ticked.emit(self.current_)


class AnimationGroup:
    """
    动画组，为多个动画的管理提供支持，允许使用token访问动画对象
    """
    def __init__(self):
        self._animations = []
        self._tokens = []

    def addMember(self, ani, token: str):
        if token in self._tokens:
            raise ValueError(f"代号已经存在：{token}")
        self._animations.append(ani)
        self._tokens.append(token)

    def fromToken(self, aim_token: str) -> ABCAnimation:
        for ani, token in zip(self._animations, self._tokens):
            if token == aim_token:
                return ani
        raise ValueError(f"未在代号组中找到传入的代号：{aim_token}")






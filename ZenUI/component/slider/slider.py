from PySide6.QtWidgets import QWidget
from ZenUI.component.basewidget.widget import ZWidget
from ZenUI.component.basewidget.layer import ZLayer
from ZenUI.core import Zen
class Handle(ZLayer):
    '滑块'
    def __init__(self, parent: ZWidget = None):
        super().__init__(parent)


    def enterEvent(self, event):
        super().enterEvent(event)


    def leaveEvent(self, event):
        super().leaveEvent(event)

class ZSlider(QWidget):
    '滑块组件'
    def __init__(self,
                 parent: ZWidget = None,
                 name: Zen.Direction = Zen.Direction.Horizontal):
        super().__init__(parent)
        self._value = 0
        self._min = 0
        self._max = 100
        self._step = 1
        self._track = ZLayer(self)
        '轨道'
        self._fill = ZLayer(self)
        '填充'
        self._handle = ZLayer(self)
        '滑块'

    def track(self) -> ZLayer:
        '获取轨道对象'
        return self._track


    def fill(self) -> ZLayer:
        '获取填充对象'
        return self._fill


    def handle(self) -> ZLayer:
        '获取滑块对象'
        return self._handle


    def setValue(self, value: int):
        '设置数值'
        self._value = value


    def value(self) -> int:
        '获取数值'
        return self._value


    def setRange(self, min: int, max: int):
        '设置范围'
        self._min = min
        self._max = max


    def range(self) -> tuple:
        '获取范围'
        return self._min, self._max

    def setStep(self, step: int):
        '设置步长'
        self._step = step


    def step(self) -> int:
        '获取步长'
        return self._step
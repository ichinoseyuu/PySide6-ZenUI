from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.slider.baselayer import BaseLayer
from ZenUI.component.slider.handle import Handle
from ZenUI.core import Zen,ZColorSheet

class ZSlider(ZWidget):
    '滑块组件'
    valueChanged = Signal(object) #数值改变信号
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 direction: Zen.Direction = Zen.Direction.Horizontal,
                 track_width: int = 4,
                 track_length: int = 100,
                 handle_radius: int = 10,
                 value_range: tuple = (0,100),
                 value: int = 0,
                 step: int = 1):
        super().__init__(parent, name)
        self._direction = direction
        '方向'
        self._track_width = track_width
        '轨道宽度'
        self._track_length = track_length
        '轨道长度'
        self._handle_radius = handle_radius
        '滑块半径'
        self._value = 0
        '当前数值'
        self._percentage = 0
        '当前的百分比'
        self._min = value_range[0]
        '最小值'
        self._max = value_range[1]
        '最大值'
        self._step = step
        '滑动步长'
        self._track = BaseLayer(self)
        '轨道'
        self._fill = BaseLayer(self)
        '填充'
        self._handle = Handle(parent=self,radius=handle_radius)
        '滑块'
        self._init_style()
        self.setValue(value)


    def _init_style(self):
        #设置样式
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.Slider)
        self._colors.overwrite(self._color_sheet.getSheet())
        self._track._bg_color_a = self._colors.track
        self._track._stylesheet_fixed =f'border-radius: {int(self._track_width/2)}px;'
        self._fill._bg_color_a = self._colors.fill
        self._fill._stylesheet_fixed =f'border-radius: {int(self._track_width/2)}px;'
        self._handle.configColor(self._colors.handle_inner, self._colors.handle_outer, self._colors.handle_border)

        #设置大小
        if self._direction == Zen.Direction.Horizontal:
            self.setFixedHeight(self._handle_radius*2)
            self.setFixedWidth(self._track_length + self._handle_radius*2)

        elif self._direction == Zen.Direction.Vertical:
            self.setFixedWidth(self._handle_radius*2)
            self.setFixedHeight(self._track_length + self._handle_radius*2)


    def _theme_changed_handler(self, theme):
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self._track.setColor(self._colors.track)
        self._fill.setColor(self._colors.fill)
        self._handle.configColor(self._colors.handle_inner, self._colors.handle_outer, self._colors.handle_border)


    def _fill_track(self,value):
        '填充轨道'
        # 计算步长的小数位数
        step_str = str(self._step)
        decimal_places = len(step_str.split('.')[-1]) if '.' in step_str else 0
        # 根据步长调整值
        adjusted_value = round(value / self._step) * self._step
        # 限制在范围内
        self._value = max(self._min, min(adjusted_value, self._max))
        # 格式化数值到正确的小数位
        self._value = round(self._value, decimal_places)
        self.valueChanged.emit(self._value)
        # 计算百分比
        self._percentage = round((self._value - self._min) / (self._max - self._min), 3)
        if self._direction == Zen.Direction.Horizontal:
            self._fill.setFixedWidth(self._percentage * self._track_length)
        elif self._direction == Zen.Direction.Vertical:
            self._fill.setFixedHeight(self._percentage * self._track_length)
            x = (self.width() - self._fill.width()) / 2
            y = self._track_length - self._fill.height() + self._handle_radius
            self._fill.move(x, y)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()

        if self._direction == Zen.Direction.Horizontal:
            self._track.resize(self._track_length, self._track_width)
            self._track.move(self._handle_radius, (h-self._track_width)/2)
            self._fill.resize(self._track_length, self._track_width)
            self._fill.move(self._handle_radius, (h-self._track_width)/2)

        elif self._direction == Zen.Direction.Vertical:
            self._track.resize(self._track_width, self._track_length)
            self._track.move((w-self._track_width)/2, self._handle_radius)
            self._fill.resize(self._track_width, self._track_length)
            self._fill.move((w-self._track_width)/2, self._handle_radius)
            self._handle.move(0,self._track_length)


    def setValue(self, value: int|float):
        '设置数值'
        # 计算步长的小数位数
        step_str = str(self._step)
        decimal_places = len(step_str.split('.')[-1]) if '.' in step_str else 0
        # 根据步长调整值
        adjusted_value = round(value / self._step) * self._step
        # 限制在范围内
        self._value = max(self._min, min(adjusted_value, self._max))
        # 格式化数值到正确的小数位
        self._value = round(self._value, decimal_places)
        self.valueChanged.emit(self._value)
        # 计算百分比
        self._percentage = round((self._value - self._min) / (self._max - self._min), 3)
        if self._direction == Zen.Direction.Horizontal:
            self._fill.setFixedWidth(self._percentage * self._track_length)
            self._handle.move(self._percentage * self._track_length, (self.height() - 2 * self._handle_radius) / 2)
        elif self._direction == Zen.Direction.Vertical:
            self._fill.setFixedHeight(self._percentage * self._track_length)
            x = (self.width() - self._fill.width()) / 2
            y = self._track_length - self._fill.height() + self._handle_radius
            self._fill.move(x, y)
            self._handle.move((self.width() - 2 * self._handle_radius) / 2,self._track_length - self._percentage * self._track_length)

    def percentage(self):
        '获取百分比'
        return self._percentage


    def value(self):
        '获取数值'
        return self._value


    def track(self):
        '获取轨道对象'
        return self._track


    def fill(self):
        '获取填充对象'
        return self._fill


    def handle(self):
        '获取滑块对象'
        return self._handle
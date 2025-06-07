from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from typing import Union, Tuple
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.slider.sliderlayer import SliderLayer
from ZenUI.component.slider.sliderhandle import SliderHandle
from ZenUI.core import Zen,ZColorSheet

class ZSlider(ZWidget):
    """滑块控件"""
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
        self._track = SliderLayer(self)
        '轨道'
        self._fill = SliderLayer(self)
        '填充'
        self._handle = SliderHandle(parent=self,radius=handle_radius)
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


    def _normalize_value(self, value: float) -> float:
        """标准化输入值，将输入值调整为合法的步进值,并确保在范围内"""
        # 计算步长小数位
        step_str = str(self._step)
        decimal_places = len(step_str.split('.')[-1]) if '.' in step_str else 0
        # 调整到步进值
        adjusted = round(value / self._step) * self._step
        # 确保在范围内
        clamped = max(self._min, min(adjusted, self._max))
        # 格式化小数位
        return round(clamped, decimal_places)


    def _update_track(self) -> None:
        """更新轨道和填充条位置"""
        if self._direction == Zen.Direction.Horizontal:
            self._update_horizontal_track()
        else:
            self._update_vertical_track()


    def _update_horizontal_track(self):
        """更新水平方向轨道"""
        y = (self.height() - self._track_width) / 2
        # 更新轨道
        self._track.setGeometry(
            self._handle_radius, 
            y,
            self._track_length,
            self._track_width
            )
        # 更新填充条
        self._fill.setGeometry(
            self._handle_radius,
            y, 
            self._percentage * self._track_length,
            self._track_width
            )
        # 更新滑块
        self._handle.move(
            self._percentage * self._track_length,
            (self.height() - 2 * self._handle_radius) / 2
            )

    def _update_vertical_track(self):
        """更新垂直方向轨道"""
        x = (self.width() - self._track_width) / 2
        # 更新轨道
        self._track.setGeometry(
            x,
            self._handle_radius,
            self._track_width,
            self._track_length
        )
        # 更新填充条
        fill_height = self._percentage * self._track_length
        self._fill.setGeometry(
            x,
            self._track_length - fill_height + self._handle_radius,
            self._track_width,
            fill_height
        )
        # 更新滑块
        self._handle.move(
            (self.width() - 2 * self._handle_radius) / 2,
            self._track_length - self._percentage * self._track_length
        )


    def setValue(self, value: Union[int, float]) -> None:
        """设置当前值"""
        # 标准化值
        self._value = self._normalize_value(value)
        # 计算百分比
        self._percentage = (self._value - self._min) / (self._max - self._min)
        # 更新UI
        self._update_track()
        # 发送信号
        self.valueChanged.emit(self._value)

    def value(self):
        '获取数值'
        return self._value

    def percentage(self):
        '获取百分比'
        return self._percentage

    def track(self):
        '获取轨道对象'
        return self._track

    def fill(self):
        '获取填充对象'
        return self._fill

    def handle(self):
        '获取滑块对象'
        return self._handle

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_track()


    def _theme_changed_handler(self, theme):
        """主题改变处理"""
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self._track.setColor(self._colors.track)
        self._fill.setColor(self._colors.fill)
        self._handle.configColor(
            self._colors.handle_inner,
            self._colors.handle_outer,
            self._colors.handle_border
        )
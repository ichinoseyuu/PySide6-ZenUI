from PySide6.QtSvgWidgets import QSvgWidget
from enum import Enum,auto
from ZenUI.component.advancedbutton.abc_advanced_button import ABCAdvancedButton
from ZenUI.component.advancedbutton.layers import Layer,Text
from ZenUI.core import Zen, ZColorTool, ZColorSheet

class ZAdvancedButton(ABCAdvancedButton):
    class Background(Enum):
        Transparent = auto()
        Filled = auto()
        Gradient = auto()
    # class Shadow(Enum):
    #     On = auto()
    #     Off = auto()
    # class Table(Enum):
    #     Filled = auto()
    #     Border = auto()
    #     Strip = auto()
    #     Square = auto()
    #     Round = auto()
    #     None_ = auto()
    def __init__(self,
                 parent = None,
                 name: str = None,
                 text: str = None,
                 icon: str = None,
                 radius: int = 2,
                 background = Background.Transparent):
        super().__init__(parent = parent, name= name)
        self._background = background #背景类型
        self._radius = radius #圆角半径
        # setup ui
        self._layer_hover = Layer(self)
        self._layer_highlight = Layer(self)
        self._layer_icon = QSvgWidget(self)
        self._layer_text = Text(self)
        if icon:
            self._layer_icon.load(icon)
        if text:
            self._layer_text.setText(text)




    def _init_(self):
        sheet = f'border: 1px solid transparent;\nborder-radius: {self._radius}px;'
        self._fixed_stylesheet = sheet
        self._layer_highlight._fixed_stylesheet = sheet
        self._layer_hover._fixed_stylesheet = sheet
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.AdavancedButton)
        if self._background == self.Background.Filled:
            self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
            self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        elif self._background == self.Background.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)
            self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
            self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
            self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
            self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        if self._layer_text.text():
            self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
            self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        pass


    def setText(self, text: str):
        '''设置按钮文字'''
        self._layer_text.setText(text)

    def text(self):
        '''获取按钮文字'''
        return self._layer_text.text()

    def setIcon(self, icon: str):
        '''设置按钮图标'''
        self._layer_icon.load(icon)


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import Enum, auto
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.button.abstract_button import ABCButton
from ZenUI.core import ZColorTool,ZenGlobal,Zen,ZSize,ZColorSheet,ZQuickEffect
class ZPushButton(ABCButton):
    '''按钮'''
    class IdleStyle(Enum):
        '''闲置样式'''
        Monochrome = auto()
        '单色背景'
        Gradient = auto()
        '渐变背景'
        MonochromeWithBorder = auto()
        '单色背景+边框'
        Border = auto()
        '仅边框'
        Transparent = auto()
        '透明'

    class HoverStyle(Enum):
        '''悬停样式'''
        ColorChange = auto()
        '背景颜色变化'
        IconTextColorChange = auto()
        '文字和图片颜色变化'
        AddBorder = auto()
        '添加边框'
        SizeIncrease = auto()
        '变大'
        Transparent = auto()
        '透明'

    class PressedStyle(Enum):
        '''按下样式'''
        ColorChange = auto()
        '背景颜色变化'
        Flash = auto()
        '闪烁'
        IconTextColorChange = auto()
        '文字和图片颜色变化'
        SizeDecrease = auto()
        '变小'
        Transparent = auto()
        '透明'

    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None,
                 icon_size: ZSize = None,
                 tooltip: str = None,
                 min_width: int = None,
                 min_height: int = None,
                 min_size: ZSize = None,
                 max_width: int = None,
                 max_height: int = None,
                 max_size: ZSize = None,
                 fixed_size: ZSize = None,
                 sizepolicy: tuple[Zen.SizePolicy, Zen.SizePolicy] = None,
                 border_radius: int = 2,
                 display_tooltip_immediate: bool = False,
                 idle_style: IdleStyle = IdleStyle.Gradient,
                 hover_style: HoverStyle = HoverStyle.ColorChange,
                 pressed_style: PressedStyle = PressedStyle.ColorChange):
        super().__init__(parent=parent,
                         name=name,
                         text=text,
                         icon=icon,
                         icon_size=icon_size,
                         tooltip=tooltip,
                         min_width=min_width,
                         min_height=min_height,
                         min_size=min_size,
                         max_width=max_width,
                         max_height=max_height,
                         max_size=max_size,
                         fixed_size=fixed_size,
                         sizepolicy=sizepolicy,
                         border_radius=border_radius,
                         display_tooltip_immediate=display_tooltip_immediate)
        self._idle_style = idle_style
        self._hover_style = hover_style
        self._pressed_style = pressed_style
        self._init_style()
        self._schedule_update()



    def _init_style(self):
        # 判断背景是否有边框，hover层是否添加边框，若是则抛出异常
        if ((self._idle_style in [ZPushButton.IdleStyle.MonochromeWithBorder, ZPushButton.IdleStyle.Border]) 
                and self._hover_style == ZPushButton.HoverStyle.AddBorder):
            raise ValueError("can't add border when bg_style is MonochromeWithBorder or Border")

        self._color_sheet = ZColorSheet(self, Zen.WidgetType.PushButton) #获取颜色配置
        self._fixed_stylesheet = f'border-radius: {self._border_radius}px;' #固定样式
        self._layer_hover._fixed_stylesheet = f'border-radius: {self._border_radius}px;' #hover层固定样式
        self._layer_press._fixed_stylesheet = f'border-radius: {self._border_radius}px;' #press层固定样式

        # 判断背景是否渐变，若是则给窗口添加渐变属性
        if self._idle_style == ZPushButton.IdleStyle.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)

        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)

        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))

        # 判断hover层的样式
        if self._hover_style == ZPushButton.HoverStyle.ColorChange:
            self._layer_hover.set_style_getter('background_color', lambda: self._layer_hover._bg_color_a)
            self._layer_hover.set_style_getter('border_radius', lambda: self._border_radius)

        elif self._hover_style == ZPushButton.HoverStyle.AddBorder:
            self._layer_hover.set_style_getter('border_color', lambda: self._layer_hover._border_color)
            self._layer_hover.set_style_getter('border_radius', lambda: self._border_radius)

        elif self._hover_style == ZPushButton.HoverStyle.IconTextColorChange:
            self._layer_hover.hide()

        elif self._hover_style == ZPushButton.HoverStyle.SizeIncrease:
            self._layer_hover.hide()

        # 判断press层的样式
        if self._pressed_style in [ZPushButton.PressedStyle.ColorChange,ZPushButton.PressedStyle.Flash]:
            self._layer_press.set_style_getter('background_color', lambda: self._layer_press._bg_color_a)
            self._layer_press.set_style_getter('border_radius', lambda: self._border_radius)

        elif self._pressed_style == ZPushButton.PressedStyle.SizeDecrease:
            self._layer_press.hide()


    def reloadStyleSheet(self):
        #判断背景层样式
        if self._idle_style == ZPushButton.IdleStyle.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},
            stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});
            border: 1px solid transparent;''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._idle_style == ZPushButton.IdleStyle.Monochrome:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: {self._bg_color_a};
            border: 1px solid transparent;''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._idle_style == ZPushButton.IdleStyle.MonochromeWithBorder:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: {self._bg_color_a};
            border: 1px solid {self._border_color};''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._idle_style == ZPushButton.IdleStyle.Border:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: transparent;
            border: 1px solid {self._border_color};''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._idle_style == ZPushButton.IdleStyle.Transparent:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: transparent;
            border: 1px solid transparent;''')
            return self._fixed_stylesheet +'\n'+ sheet

    def _show_tooltip(self):
        if self._tooltip != "" and "ToolTip" in ZenGlobal.ui.windows:
            ZenGlobal.ui.windows["ToolTip"].setText(self._tooltip)
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(self)
            ZenGlobal.ui.windows["ToolTip"].showTip()

    def _hide_tooltip(self):
        if self._tooltip != "" and "ToolTip" in ZenGlobal.ui.windows:
            ZenGlobal.ui.windows["ToolTip"].setInsideOf(None)
            ZenGlobal.ui.windows["ToolTip"].hideTip()

    def _hovered_handler(self):
        if self._hover_style == ZPushButton.HoverStyle.ColorChange:
            self._layer_hover.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Hover))

        elif self._hover_style == ZPushButton.HoverStyle.AddBorder:
            self._layer_hover.setBorderColorTo(self._color_sheet.getColor(Zen.ColorRole.BorderHover))

        elif self._hover_style == ZPushButton.HoverStyle.IconTextColorChange:
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextHover))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconHover))

        elif self._hover_style == ZPushButton.HoverStyle.SizeIncrease:
            pass



    def _leaved_handler(self):
        if self._hover_style == ZPushButton.HoverStyle.ColorChange:
            self._layer_hover.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Hover)))

        elif self._hover_style == ZPushButton.HoverStyle.AddBorder:
            self._layer_hover.setBorderColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.BorderHover)))

        elif self._hover_style == ZPushButton.HoverStyle.IconTextColorChange:
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

        elif self._hover_style == ZPushButton.HoverStyle.SizeIncrease:
            pass



    def _pressed_handler(self):
        if self._pressed_style == ZPushButton.PressedStyle.ColorChange:
            self._layer_press.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Pressed))

        elif self._pressed_style == ZPushButton.PressedStyle.Flash:
            self._layer_press.setColor(self._color_sheet.getColor(Zen.ColorRole.Flash))
            self._layer_press.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Flash)))

        elif self._pressed_style == ZPushButton.PressedStyle.SizeDecrease:
            pass


    def _released_handler(self):
        if self._pressed_style == ZPushButton.PressedStyle.ColorChange:
            self._layer_press.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Pressed)))

        elif self._pressed_style == ZPushButton.PressedStyle.SizeDecrease:
            pass


    def _clicked_handler(self):
        pass


    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Background_A), self._color_sheet.getColor(theme, Zen.ColorRole.Background_B))
        self.setBorderColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Border))
        self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Text))
        self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Icon))

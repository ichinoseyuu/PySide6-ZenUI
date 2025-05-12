from PySide6.QtGui import QIcon
from enum import IntFlag
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.button.abstract_button import ABCButton
from ZenUI.core import ZColorTool,ZenGlobal,Zen,ZSize,ZColorSheet,ZColors

class ZPushButton(ABCButton):
    '''按钮'''
    class IdleStyle(IntFlag):
        '''闲置样式'''
        None_ = 0 #0b0
        Monochrome = 1 << 0  #0b1
        '单色背景'
        Gradient = 1 << 1 #0b10
        '渐变背景'
        Border = 1 << 2 #0b100
        '边框'

    class HoverStyle(IntFlag):
        '''悬停样式'''
        None_ = 0
        Color = 1 << 0
        '背景颜色变化'
        Icon = 1 << 1
        '图片颜色变化'
        Text = 1 << 2
        '文字颜色变化'
        Border = 1 << 3
        '添加边框'

    class PressedStyle(IntFlag):
        '''按下样式'''
        None_ = 0
        Color = 1 << 0
        '背景颜色变化'
        Flash = 1 << 1
        '闪烁'
        Icon = 1 << 2
        '图片颜色变化'
        Text = 1 << 3
        '文字颜色变化'
        Border = 1 << 4
        '添加边框'
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
                 display_tooltip_immediate: bool = False,
                 fixed_stylesheet: str = None,
                 hover_stylesheet: str = None,
                 pressed_stylesheet: str = None,
                 idle_style: IdleStyle = IdleStyle.Gradient,
                 hover_style: HoverStyle = HoverStyle.Color,
                 pressed_style: PressedStyle = PressedStyle.Color):
        super().__init__(parent=parent,
                         name=name,
                         text=text,
                         icon=icon,
                         icon_size=icon_size,
                         tooltip=tooltip,
                         display_tooltip_immediate=display_tooltip_immediate,
                         min_width=min_width,
                         min_height=min_height,
                         min_size=min_size,
                         max_width=max_width,
                         max_height=max_height,
                         max_size=max_size,
                         fixed_size=fixed_size,
                         sizepolicy=sizepolicy)
        if (idle_style & (self.IdleStyle.Gradient|self.IdleStyle.Monochrome) and
            (hover_style & self.HoverStyle.Border or pressed_style & self.PressedStyle.Border)):
            raise ValueError('Cannot set border style when background is monochrome or gradient')
        self._idle_style = idle_style
        self._hover_style = hover_style
        self._pressed_style = pressed_style
        # 参数初始化
        if fixed_stylesheet: self.setFixedStyleSheet(fixed_stylesheet)
        if hover_stylesheet: self._layer_hover.setFixedStyleSheet(hover_stylesheet)
        if pressed_stylesheet: self._layer_pressed.setFixedStyleSheet(pressed_stylesheet)
        self._init_style()
        self.updateStyle()


    def _init_style(self):
        # 添加背景样式互斥检查
        bg_style = self._idle_style & (self.IdleStyle.Monochrome | self.IdleStyle.Gradient)
        if bin(bg_style).count('1') > 1:
            raise ValueError("Monochrome and Gradient are mutually exclusive")

        # 判断背景是否渐变，若是则给窗口添加渐变属性
        if self._idle_style & self.IdleStyle.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)

        self._color_sheet.loadColorConfig(Zen.WidgetType.PushButton) #获取颜色配置
        self._colors.overwrite(self._color_sheet.getSheet()) #获取颜色表

        self._bg_color_a = self._colors.background_a
        self._bg_color_b = self._colors.background_b
        self._border_color = self._colors.border
        self._text_color = self._colors.text
        self._icon_color = self._colors.icon

        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))

        # 判断hover层的样式
        if self._hover_style & self.HoverStyle.Color:
            self._layer_hover.set_style_getter('background_color', lambda: self._layer_hover._bg_color_a)

        if self._hover_style & self.HoverStyle.Border:
            self._layer_hover.set_style_getter('border_color', lambda: self._layer_hover._border_color)

        # 判断press层的样式
        if self._pressed_style & (self.PressedStyle.Color|self.PressedStyle.Flash):
            self._layer_pressed.set_style_getter('background_color', lambda: self._layer_pressed._bg_color_a)

        if self._pressed_style & self.PressedStyle.Border:
            self._layer_pressed.set_style_getter('border_color', lambda: self._layer_pressed._border_color)


    def _theme_changed_handler(self, theme):
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self.setColor(self._colors.background_a, self._colors.background_b)
        self.setBorderColor(self._colors.border)
        self.setTextColor(self._colors.text)
        self.setIconColor(self._colors.icon)
        self._layer_hover.setBorderColor(ZColorTool.trans(self._colors.border_hover))
        self._layer_pressed.setBorderColor(ZColorTool.trans(self._colors.border_pressed))


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        #判断背景层样式
        if self._idle_style == self.IdleStyle.None_:
            # 无样式时重置所有
            sheet = dedent(f'''\
                color: {self._text_color};
                background-color: transparent;
                border: none;''')
            return self._stylesheet_fixed +'\n'+ sheet

        sheet = [f'color: {self._text_color};']

        # 处理背景样式
        if self._idle_style & self.IdleStyle.Monochrome:
            sheet.append(f"background-color: {self._bg_color_a};")

        elif self._idle_style & self.IdleStyle.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet.append(dedent(f"""\
                background-color: qlineargradient(
                x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
                stop:0 {self._bg_color_a}, stop:1 {self._bg_color_b});"""))

        # 处理边框样式
        if self._idle_style & self.IdleStyle.Border:
            sheet.append(f"border-color: {self._border_color};")
        else:
            sheet.append("border: none;")

        return self._stylesheet_fixed +'\n'+ '\n'.join(sheet) 


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
        if self._hover_style & self.HoverStyle.Color:
            self._layer_hover.setColorTo(self._colors.hover)

        if self._hover_style & self.HoverStyle.Border:
            self._layer_hover.setBorderColorTo(self._colors.border_hover)
            if self._idle_style & self.IdleStyle.Border:
                self.setBorderColorTo(ZColorTool.trans(self._colors.border))

        if self._hover_style & self.HoverStyle.Icon:
            self.setIconColorTo(self._colors.icon_hover)

        if self._hover_style & self.HoverStyle.Text:
            self.setTextColorTo(self._colors.text_hover)



    def _leaved_handler(self):
        if self._hover_style & self.HoverStyle.Color:
            self._layer_hover.setColorTo(ZColorTool.trans(self._colors.hover))

        if self._hover_style & self.HoverStyle.Border:
            self._layer_hover.setBorderColorTo(ZColorTool.trans(self._colors.border_hover))
            if self._idle_style & self.IdleStyle.Border:
                self.setBorderColorTo(self._colors.border)


        if self._hover_style & self.HoverStyle.Icon:
            self.setIconColorTo(self._colors.icon)

        if self._hover_style & self.HoverStyle.Text:
            self.setTextColorTo(self._colors.text)



    def _pressed_handler(self):
        if self._pressed_style & self.PressedStyle.Color:
            self._layer_pressed.setColorTo(self._colors.pressed)

        if self._pressed_style & self.PressedStyle.Border:
            self._layer_pressed.setBorderColorTo(self._colors.border_pressed)
            if self._hover_style & self.HoverStyle.Border:
                self._layer_hover.setBorderColorTo(ZColorTool.trans(self._colors.border_hover))

        if self._pressed_style & self.PressedStyle.Icon:
            self.setIconColorTo(self._colors.icon_pressed)

        if self._pressed_style & self.PressedStyle.Text:
            self.setTextColorTo(self._colors.text_pressed)


    def _released_handler(self):
        if self._pressed_style & self.PressedStyle.Color:
            self._layer_pressed.setColorTo(ZColorTool.trans(self._colors.pressed))

        if self._pressed_style & self.PressedStyle.Border:
            self._layer_pressed.setBorderColorTo(ZColorTool.trans(self._colors.border_pressed))
            if self._hover_style & self.HoverStyle.Border:
                self._layer_hover.setBorderColorTo(self._colors.border_hover)

        if self._pressed_style & self.PressedStyle.Icon:
            if self._hover_style & self.HoverStyle.Icon:
                self.setIconColorTo(self._colors.icon_hover)
            else:
                self.setIconColorTo(self._colors.icon)

        if self._pressed_style & self.PressedStyle.Text:
            if self._hover_style & self.HoverStyle.Text:
                self.setTextColorTo(self._colors.text_hover)
            else:
                self.setTextColorTo(self._colors.text)


    def _clicked_handler(self):
        if self._pressed_style & self.PressedStyle.Flash:
            self._layer_pressed.setColor(self._colors.flash)
            self._layer_pressed.setColorTo(ZColorTool.trans(self._colors.flash))

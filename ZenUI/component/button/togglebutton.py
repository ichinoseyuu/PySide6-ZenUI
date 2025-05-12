from PySide6.QtGui import QIcon,QCursor
from enum import IntFlag, IntEnum, auto
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.button.abstract_toggle_button import ABCToggleButton
from ZenUI.core import ZColorTool,ZenGlobal,Zen,ZSize,ZColorSheet,ZColors
class ZToggleButton(ABCToggleButton):
    '''切换按钮'''
    class CheckedStyle(IntFlag):
        '''选中背景样式'''
        None_ = 0
        Monochrome = 1 << 0
        '单色背景'
        Border = 1 << 1
        '添加边框'
        Icon = 1 << 2
        '图片颜色变化'
        Text = 1 << 3
        '文字颜色变化'

    class Indicator(IntEnum):
        '''指示条'''
        Enabled = auto()
        '启用'
        Disabled = auto()
        '禁用'

    class HoverStyle(IntFlag):
        '''悬停样式'''
        None_ = 0
        Color = 1 << 0
        '背景颜色变化'
        Border = 1 << 1
        '添加边框'
        Icon = 1 << 2
        '图片颜色变化'
        Text = 1 << 3
        '文字颜色变化'

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

    class IndicatorPos(IntEnum):
        """标签位置"""
        Left = auto()
        Right = auto()
        Top = auto()
        Bottom = auto()

    def __init__(self,
                 parent: ZWidget = None,
                 checked: bool = False,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None,
                 icon_size: ZSize = None,
                 tooltip: str = None,
                 display_tooltip_immediate: bool = False,
                 min_width: int = None,
                 min_height: int = None,
                 min_size: ZSize = None,
                 max_width: int = None,
                 max_height: int = None,
                 max_size: ZSize = None,
                 fixed_size: ZSize = None,
                 sizepolicy: tuple[Zen.SizePolicy, Zen.SizePolicy] = None,
                 indicator_pos: IndicatorPos = IndicatorPos.Left,
                 indicator_width: int = 4,
                 indicator_margin: int = 2,
                 indicator_padding: int = 10,
                 fixed_stylesheet: str = None,
                 hover_stylesheet: str = None,
                 pressed_stylesheet: str = None,
                 indicator_stylesheet: str = None,
                 checked_style: CheckedStyle = CheckedStyle.None_,
                 hover_style: HoverStyle = HoverStyle.Color,
                 pressed_style: PressedStyle = PressedStyle.Color,
                 indicator: Indicator = Indicator.Disabled):
        super().__init__(parent=parent,
                         checked=checked,
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
        # 父类参数初始化
        self._indicator_position = indicator_pos
        '指示条位置，表示指示条在按钮的哪个位置(左/右/上/下)'
        self._indicator_width = indicator_width
        '指示条的宽度，即指示条的粗细'
        self._indicator_margin = indicator_margin
        '指示条到按钮边缘的距离'
        self._indicator_padding = indicator_padding
        '指示条长度的内边距，用于控制指示条不会占满整个边缘'
        # 参数初始化
        self._checked_style = checked_style
        self._hover_style = hover_style
        self._pressed_style = pressed_style
        self._indicator_state = indicator
        if fixed_stylesheet: self.setFixedStyleSheet(fixed_stylesheet)
        if hover_stylesheet: self._layer_hover.setFixedStyleSheet(hover_stylesheet)
        if pressed_stylesheet: self._layer_pressed.setFixedStyleSheet(pressed_stylesheet)
        if indicator_stylesheet: self._indicator.setFixedStyleSheet(indicator_stylesheet)
        self._init_style()
        self.updateStyle()



    def _init_style(self):
        self._color_sheet.loadColorConfig(Zen.WidgetType.ToggleButton) #获取颜色配置
        self._colors.overwrite(self._color_sheet.getSheet()) #获取颜色表

        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)

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

        # tab层的样式
        if self._indicator_state == self.Indicator.Disabled:
            self._indicator.hide()
        else:
            self._indicator.set_style_getter('background_color', lambda: self._indicator._bg_color_a)


    def _init_indicator(self, w, h):
        if self._indicator_state == self.Indicator.Disabled: return
        margin, padding, width= self._indicator_margin, self._indicator_padding, self._indicator_width
        if self._indicator_position == self.IndicatorPos.Left:
            self._indicator.setGeometry(margin, padding, width, h - 2*padding)
            return
        if self._indicator_position == self.IndicatorPos.Right:
            self._indicator.setGeometry(w - margin - width, padding, width, h - 2*padding)
            return
        if self._indicator_position == self.IndicatorPos.Top:
            self._indicator.setGeometry(padding, margin, w - 2*padding, width)
            return
        self._indicator.setGeometry(padding, h - margin - width, w - 2*padding, width)


    def _theme_changed_handler(self, theme):
        self._colors.overwrite(self._color_sheet.getSheet(theme)) # 更新颜色表

        checked = self.isChecked()
        # 更新指示条颜色
        if self._indicator_state == self.Indicator.Enabled:
            indicator_color = (self._colors.indicator_selected if checked
                            else ZColorTool.trans(self._colors.indicator_selected))
            self._indicator.setColor(indicator_color)

        # 背景色
        if self._checked_style & self.CheckedStyle.Monochrome:
            color = self._colors.selected_a if checked else ZColorTool.trans(self._colors.selected_a)
            self.setColor(color)

        # 边框色
        if self._checked_style & self.CheckedStyle.Border:
            border_color = (self._colors.border_selected if checked 
                          else ZColorTool.trans(self._colors.border_selected))
            self.setBorderColor(border_color)

        # 文本色
        is_hovered = self.rect().contains(self.mapFromGlobal(QCursor.pos()))
        if self._checked_style & self.CheckedStyle.Text:
            if is_hovered and self._hover_style & self.HoverStyle.Text:
                self.setTextColor(self._colors.text_hover)
            else:
                self.setTextColor(self._colors.text_selected if checked else self._colors.text)
        else:
            self.setTextColor(self._colors.text)

        # 图标色
        if self._checked_style & self.CheckedStyle.Icon:
            if is_hovered and self._hover_style & self.HoverStyle.Icon:
                self.setIconColor(self._colors.icon_hover)
            else:
                self.setIconColor(self._colors.icon_selected if checked else self._colors.icon)
        else:
            self.setIconColor(self._colors.icon)


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        #判断背景层样式
        if self._checked_style & (self.CheckedStyle.None_):
            sheet = dedent(f'''\
                color: {self._text_color};
                background-color: transparent;
                border-color: transparent;
                border: none;''')
            return self._stylesheet_fixed +'\n'+ sheet

        sheet = [f'color: {self._text_color};']

        if self._checked_style & self.CheckedStyle.Monochrome:
            sheet.append(f"background-color: {self._bg_color_a};")

        if self._checked_style & self.CheckedStyle.Border:
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
            if self._checked_style & self.CheckedStyle.Border:
                self.setBorderColorTo(ZColorTool.trans(self._colors.border_selected))

        if self._hover_style & self.HoverStyle.Text:
            self.setTextColorTo(self._colors.text_hover)

        if self._hover_style & self.HoverStyle.Icon:
            self.setIconColorTo(self._colors.icon_hover)



    def _leaved_handler(self):
        checked = self.isChecked()
        if self._hover_style & self.HoverStyle.Color:
            self._layer_hover.setColorTo(ZColorTool.trans(self._colors.hover))

        if self._hover_style & self.HoverStyle.Border:
            self._layer_hover.setBorderColorTo(ZColorTool.trans(self._colors.border_hover))
            if self._checked_style & self.CheckedStyle.Border and checked:
                self.setBorderColorTo(self._colors.border_selected)
            else:
                self.setBorderColorTo(ZColorTool.trans(self._colors.border_selected))

        if self._hover_style & self.HoverStyle.Text:
            if self._checked_style & self.CheckedStyle.Text and checked:
                self.setTextColorTo(self._colors.text_selected)
            else:
                self.setTextColorTo(self._colors.text)

        if self._hover_style & self.HoverStyle.Icon:
            if self._checked_style & self.CheckedStyle.Icon and checked:
                self.setIconColorTo(self._colors.icon_selected)
            else:
                self.setIconColorTo(self._colors.icon)



    def _pressed_handler(self):
        if self._pressed_style & self.PressedStyle.Color:
            self._layer_pressed.setColorTo(self._colors.pressed)

        if self._pressed_style & self.PressedStyle.Border:
            self._layer_pressed.setBorderColorTo(self._colors.border_pressed)
            if self._hover_style & self.HoverStyle.Border:
                self._layer_hover.setBorderColorTo(ZColorTool.trans(self._colors.border_hover))

        if self._pressed_style & self.PressedStyle.Text:
            self.setTextColorTo(self._colors.text_pressed)

        if self._pressed_style & self.PressedStyle.Icon:
            self.setIconColorTo(self._colors.icon_pressed)


    def _released_handler(self):
        if self._pressed_style & self.PressedStyle.Color:
            self._layer_pressed.setColorTo(ZColorTool.trans(self._colors.pressed))

        if self._pressed_style & self.PressedStyle.Border:
            self._layer_pressed.setBorderColorTo(ZColorTool.trans(self._colors.border_pressed))
            if self._hover_style & self.HoverStyle.Border:
                self._layer_hover.setBorderColorTo(self._colors.border_hover)

        if self._pressed_style & self.PressedStyle.Text:
            if self._hover_style & self.HoverStyle.Text:
                self.setTextColorTo(self._colors.text_hover)
            elif self._checked_style & self.CheckedStyle.Text and self.isChecked():
                self.setTextColorTo(self._colors.text_selected)
            else:
                self.setTextColorTo(self._colors.text)

        if self._pressed_style & self.PressedStyle.Icon:
            if self._hover_style & self.HoverStyle.Icon:
                self.setIconColorTo(self._colors.icon_hover)
            elif self._checked_style & self.CheckedStyle.Icon and self.isChecked():
                self.setIconColorTo(self._colors.icon_selected)
            else:
                self.setIconColorTo(self._colors.icon)


    def _clicked_handler(self):
        if self._pressed_style & self.PressedStyle.Flash:
            self._layer_pressed.setColor(self._colors.flash)
            self._layer_pressed.setColorTo(ZColorTool.trans(self._colors.flash))


    def _toggled_handler(self, checked):
        # 更新指示条颜色
        if self._indicator_state == self.Indicator.Enabled:
            indicator_color = (self._colors.indicator_selected if checked
                            else ZColorTool.trans(self._colors.indicator_selected))
            self._indicator.setColorTo(indicator_color)

        # 背景色
        if self._checked_style & self.CheckedStyle.Monochrome:
            color = self._colors.selected_a if checked else ZColorTool.trans(self._colors.selected_a)
            self.setColorTo(color)

        # 边框色
        if self._checked_style & self.CheckedStyle.Border:
            border_color = (self._colors.border_selected if checked 
                          else ZColorTool.trans(self._colors.border_selected))
            self.setBorderColorTo(border_color)

        # 文本色
        if self._checked_style & self.CheckedStyle.Text and checked:
            if self._hover_style & self.HoverStyle.Text:
                self.setTextColorTo(self._colors.text_hover)
            else:
                self.setTextColorTo(self._colors.text_selected)
        elif not checked:
            if self._hover_style & self.HoverStyle.Text:
                self.setTextColorTo(self._colors.text_hover)
            else:
                self.setTextColorTo(self._colors.text)

        # 图标色
        if self._checked_style & self.CheckedStyle.Icon and checked:
            if self._hover_style & self.HoverStyle.Icon:
                self.setIconColorTo(self._colors.icon_hover)
            else:
                self.setIconColorTo(self._colors.icon_selected)
        elif not checked:
            if self._hover_style & self.HoverStyle.Icon:
                self.setIconColorTo(self._colors.icon_hover)
            else:
                self.setIconColorTo(self._colors.icon)


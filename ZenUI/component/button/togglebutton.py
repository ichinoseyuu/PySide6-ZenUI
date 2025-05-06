from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import Enum, auto
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.button.abstract_toggle_button import ABCToggleButton
from ZenUI.core import ZColorTool,ZenGlobal,Zen,ZSize,ZColorSheet
class ZToggleButton(ABCToggleButton):
    '''切换按钮'''
    class CheckedStyle(Enum):
        '''选中背景样式'''
        Monochrome = auto()
        '单色背景'
        Gradient = auto()
        '渐变背景'
        AddBorder = auto()
        '添加边框'
        IconTextColorChange = auto()
        '文字和图片颜色变化'
        Transparent = auto()
        '透明'


    class HoverStyle(Enum):
        '''悬停样式'''
        ColorChange = auto()
        '背景颜色变化'
        AddBorder = auto()
        '添加边框'
        IconTextColorChange = auto()
        '文字和图片颜色变化'
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
                 checked: bool = False,
                 have_tab: bool = False,
                 tab_pos: Zen.Position = Zen.Position.Left,
                 tab_width: int = 4,
                 tab_border_radius = 2,
                 tab_offset: int = 2,
                 tab_len_offset: int = 10,
                 display_tooltip_immediate: bool = False,
                 checked_style: CheckedStyle = CheckedStyle.Transparent,
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
                         checked=checked,
                         have_tab=have_tab,
                         tab_pos=tab_pos,
                         tab_border_radius=tab_border_radius,
                         tab_width=tab_width,
                         tab_offset=tab_offset,
                         tab_len_offset=tab_len_offset,
                         display_tooltip_immediate=display_tooltip_immediate)
        self._checked_style = checked_style
        self._hover_style = hover_style
        self._pressed_style = pressed_style
        self._init_style()
        self._schedule_update()



    def _init_style(self):
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.ToggleButton) #获取颜色配置

        # 判断背景是否渐变，若是则给窗口添加渐变属性
        if self._checked_style == ZToggleButton.CheckedStyle.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)
        # self._bg_color_a = ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Background_A))
        # self._bg_color_b = ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Background_B))
        # self._border_color = self._color_sheet.getColor(Zen.ColorRole.BorderHover)
        self._text_color = self._color_sheet.getColor(Zen.ColorRole.Text)
        self._icon_color = self._color_sheet.getColor(Zen.ColorRole.Icon)

        # self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        # self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        # self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))

        # 判断hover层的样式
        if self._hover_style == ZToggleButton.HoverStyle.ColorChange:
            self._layer_hover.set_style_getter('background_color', lambda: self._layer_hover._bg_color_a)
            self._layer_hover.set_style_getter('border_radius', lambda: self._border_radius)

        elif self._hover_style == ZToggleButton.HoverStyle.AddBorder:
            self._layer_hover.set_style_getter('border_color', lambda: self._layer_hover._border_color)
            self._layer_hover.set_style_getter('border_radius', lambda: self._border_radius)

        elif self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange:
            self._layer_hover.hide()

        elif self._hover_style == ZToggleButton.HoverStyle.SizeIncrease:
            self._layer_hover.hide()

        # 判断press层的样式
        if self._pressed_style in [ZToggleButton.PressedStyle.ColorChange,ZToggleButton.PressedStyle.Flash]:
            self._layer_press.set_style_getter('background_color', lambda: self._layer_press._bg_color_a)
            self._layer_press.set_style_getter('border_radius', lambda: self._border_radius)

        elif self._pressed_style == ZToggleButton.PressedStyle.SizeDecrease:
            self._layer_press.hide()

        # tab层的样式
        if self._have_tab:
            # if self._tab_pos == Zen.Position.Left:
            #     self._fixed_stylesheet = f'text-align: left;\npadding-left: {self._tab_width+2*self._tab_offset}px;'

            # elif self._tab_pos == Zen.Position.Right:
            #     self._fixed_stylesheet = f'text-align: right;\npadding-right: {self._tab_width+2*self._tab_offset}px;'

            # elif self._tab_pos == Zen.Position.Top:
            #     self._fixed_stylesheet = f'padding-top: {self._tab_width+self._tab_offset}px;'

            # elif self._tab_pos == Zen.Position.Bottom:
            #     self._fixed_stylesheet = f'padding-bottom: {self._tab_width+self._tab_offset}px;'

            self._layer_tab.set_style_getter('background_color', lambda: self._layer_tab._bg_color_a)
            self._layer_tab.set_style_getter('border_radius', lambda: self._tab_border_radius)
        else:
            self._layer_tab.hide()

    def reloadStyleSheet(self):
        #判断背景层样式
        if self._checked_style == ZToggleButton.CheckedStyle.Monochrome:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: {self._bg_color_a};
            border: 1px solid transparent;
            border-radius: {self._border_radius}px;''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._checked_style == ZToggleButton.CheckedStyle.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},
            stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});
            border: 1px solid transparent;
            border-radius: {self._border_radius}px;''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._checked_style == ZToggleButton.CheckedStyle.AddBorder:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: transparent;
            border: 1px solid {self._border_color};
            border-radius: {self._border_radius}px;''')
            return self._fixed_stylesheet +'\n'+ sheet
        if self._checked_style in [ZToggleButton.CheckedStyle.IconTextColorChange,
                                   ZToggleButton.CheckedStyle.Transparent]:
            sheet = dedent(f'''\
            color: {self._text_color};
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: {self._border_radius}px;''')
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
        if self._hover_style == ZToggleButton.HoverStyle.ColorChange:
            self._layer_hover.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Hover))

        elif self._hover_style == ZToggleButton.HoverStyle.AddBorder:
            self._layer_hover.setBorderColorTo(self._color_sheet.getColor(Zen.ColorRole.BorderHover))

        elif self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange:
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextHover))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconHover))

        elif self._hover_style == ZToggleButton.HoverStyle.SizeIncrease:
            pass


    def _leaved_handler(self):
        if self._hover_style == ZToggleButton.HoverStyle.ColorChange:
            self._layer_hover.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Hover)))

        elif self._hover_style == ZToggleButton.HoverStyle.AddBorder:
            self._layer_hover.setBorderColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.BorderHover)))

        elif self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange:
            if self._checked_style == ZToggleButton.CheckedStyle.IconTextColorChange and self.isChecked():
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextSelected))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconSelected))
            else:
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

        elif self._hover_style == ZToggleButton.HoverStyle.SizeIncrease:
            pass




    def _pressed_handler(self):
        if self._pressed_style == ZToggleButton.PressedStyle.ColorChange:
            self._layer_press.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Pressed))

        elif self._pressed_style == ZToggleButton.PressedStyle.Flash:
            self._layer_press.setColor(self._color_sheet.getColor(Zen.ColorRole.Flash))
            self._layer_press.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Flash)))

        elif self._pressed_style == ZToggleButton.PressedStyle.IconTextColorChange:
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextHover))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconPressed))

        elif self._pressed_style == ZToggleButton.PressedStyle.SizeDecrease:
            pass


    def _released_handler(self):
        if self._pressed_style == ZToggleButton.PressedStyle.ColorChange:
            self._layer_press.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Pressed)))

        elif self._pressed_style == ZToggleButton.PressedStyle.IconTextColorChange:
            self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextPressed))
            self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconPressed))

        elif self._pressed_style == ZToggleButton.PressedStyle.SizeDecrease:
            pass



    def _clicked_handler(self):
        pass


    def _toggled_handler(self, checked):
        if checked:
            self._layer_tab.setColorTo(self._color_sheet.getColor(Zen.ColorRole.TabSelected))

            if self._checked_style == ZToggleButton.CheckedStyle.Monochrome:
                self.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected_A))

            elif self._checked_style == ZToggleButton.CheckedStyle.Gradient:
                self.setColorTo(self._color_sheet.getColor(Zen.ColorRole.Selected_A),
                                self._color_sheet.getColor(Zen.ColorRole.Selected_B))

            elif self._checked_style == ZToggleButton.CheckedStyle.AddBorder:
                self.setBorderColorTo(self._color_sheet.getColor(Zen.ColorRole.BorderSelected))

            elif self._checked_style == ZToggleButton.CheckedStyle.IconTextColorChange:
                if self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange:
                    self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextHover))
                    self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconHover))
                else:
                    self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextSelected))
                    self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconSelected))

        else:
            self._layer_tab.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.TabSelected)))

            if self._checked_style == ZToggleButton.CheckedStyle.Monochrome:
                self.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Selected_A)))

            elif self._checked_style == ZToggleButton.CheckedStyle.Gradient:
                self.setColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Selected_A)),
                                ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.Selected_B)))

            elif self._checked_style == ZToggleButton.CheckedStyle.AddBorder:
                self.setBorderColorTo(ZColorTool.trans(self._color_sheet.getColor(Zen.ColorRole.BorderSelected)))

            elif self._checked_style == ZToggleButton.CheckedStyle.IconTextColorChange:
                if (self.rect().contains(self.mapFromGlobal(QCursor.pos())) and
                    self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange):
                    self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextHover))
                    self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconHover))
                else:
                    self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                    self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

    def _theme_changed_handler(self, theme):
        #self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Background_A), self._color_sheet.getColor(theme, Zen.ColorRole.Background_B))
        #self.setBorderColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Border))
        if self.isChecked():
            self._layer_tab.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.TabSelected))
            if self._checked_style == ZToggleButton.CheckedStyle.Monochrome:
                self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A))
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

            elif self._checked_style == ZToggleButton.CheckedStyle.Gradient:
                self.setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A),
                                self._color_sheet.getColor(theme, Zen.ColorRole.Selected_B))
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

            elif self._checked_style == ZToggleButton.CheckedStyle.AddBorder:
                self.setBorderColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.BorderSelected))
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

            elif self._checked_style == ZToggleButton.CheckedStyle.IconTextColorChange:
                if (self.rect().contains(self.mapFromGlobal(QCursor.pos())) and
                    self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange):
                    self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.TextHover))
                    self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.IconHover))
                else:
                    self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.TextSelected))
                    self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.IconSelected))
        else:
            self._layer_tab.setColorTo(ZColorTool.trans(self._color_sheet.getColor(theme, Zen.ColorRole.TabSelected)))
            if self._checked_style == ZToggleButton.CheckedStyle.Monochrome:
                self.setColorTo(ZColorTool.trans(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A)))
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

            elif self._checked_style == ZToggleButton.CheckedStyle.Gradient:
                self.setColorTo(ZColorTool.trans(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_A)),
                                ZColorTool.trans(self._color_sheet.getColor(theme, Zen.ColorRole.Selected_B)))
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

            elif self._checked_style == ZToggleButton.CheckedStyle.AddBorder:
                self.setBorderColorTo(ZColorTool.trans(self._color_sheet.getColor(theme, Zen.ColorRole.BorderSelected)))
                self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

            elif self._checked_style == ZToggleButton.CheckedStyle.IconTextColorChange:
                if (self.rect().contains(self.mapFromGlobal(QCursor.pos())) and
                    self._hover_style == ZToggleButton.HoverStyle.IconTextColorChange):
                    self.setTextColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.TextHover))
                    self.setIconColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.IconHover))
                else:
                    self.setTextColorTo(self._color_sheet.getColor(Zen.ColorRole.Text))
                    self.setIconColorTo(self._color_sheet.getColor(Zen.ColorRole.Icon))

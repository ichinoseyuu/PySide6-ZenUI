from PySide6.QtGui import QIcon
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.advancedbutton.abcbutton import ABCButton
from ZenUI.core import ZColorTool,ZenGlobal,Zen,ZSize

class ZGradientButton(ABCButton):
    '''
    渐变按钮
    - 渐变背景
    - 悬停时变色
    - 按下时变色
    '''
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
                 pressed_stylesheet: str = None):
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
        # 参数初始化
        if fixed_stylesheet: self.setFixedStyleSheet(fixed_stylesheet)
        if hover_stylesheet: self._layer_hover.setFixedStyleSheet(hover_stylesheet)
        if pressed_stylesheet: self._layer_pressed.setFixedStyleSheet(pressed_stylesheet)
        self._init_style()
        self.updateStyle()


    def _init_style(self):
        self._color_sheet.loadColorConfig(Zen.WidgetType.GradientButton) #获取颜色配置
        self._colors.overwrite(self._color_sheet.getSheet()) #获取颜色表

        self._bg_color_a = self._colors.background_a
        self._bg_color_b = self._colors.background_b
        self._text_color = self._colors.text
        self._icon_color = self._colors.icon

        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))

        # 判断hover层的样式
        self._layer_hover.set_style_getter('background_color', lambda: self._layer_hover._bg_color_a)

        # 判断press层的样式
        self._layer_pressed.set_style_getter('background_color', lambda: self._layer_pressed._bg_color_a)

    def _theme_changed_handler(self, theme):
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self.setColor(self._colors.background_a,self._colors.background_b)
        self.setTextColor(self._colors.text)
        self.setIconColor(self._colors.icon)



    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        #判断背景层样式
        x1, y1, x2, y2 = self._gradient_anchor
        sheet = dedent(f'''\
            color: {self._text_color};
            background-color: qlineargradient(
            x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
            stop:0 {self._bg_color_a}, stop:1 {self._bg_color_b});
            border: none;''')
        return self._stylesheet_fixed +'\n'+ sheet


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
        self._layer_hover.setColorTo(self._colors.hover)


    def _leaved_handler(self):
        self._layer_hover.setColorTo(ZColorTool.trans(self._colors.hover))


    def _pressed_handler(self):
        self._layer_pressed.setColorTo(self._colors.pressed)


    def _released_handler(self):
        self._layer_pressed.setColorTo(ZColorTool.trans(self._colors.pressed))
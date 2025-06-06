from PySide6.QtGui import QIcon
from textwrap import dedent
from ZenUI.component.basewidget.widget import ZWidget
from ZenUI.component.advancedbutton.abstract.abcbutton import ABCButton
from ZenUI.core import ZColorTool,ZenGlobal,Zen,ZSize

class ZNoBackgroundButton(ABCButton):
    '''
    无背景按钮
    - 悬停时图标和文字变色
    - 按下时图标和文字变色
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
                 fixed_stylesheet: str = None):
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
        self._init_style()
        self.updateStyle()


    def _init_style(self):
        self._color_sheet.loadColorConfig(Zen.WidgetType.NoBackgroundButton) #获取颜色配置
        self._colors.overwrite(self._color_sheet.getSheet()) #获取颜色表

        self._text_color = self._colors.text
        self._icon_color = self._colors.icon

        self._anim_text_color.setCurrent(ZColorTool.toArray(self._text_color))
        self._anim_icon_color.setCurrent(ZColorTool.toArray(self._icon_color))

        # 判断hover层的样式
        self._layer_hover.hide()

        # 判断press层的样式
        self._layer_pressed.hide()


    def _theme_changed_handler(self, theme):
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self.setTextColor(self._colors.text)
        self.setIconColor(self._colors.icon)


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        #判断背景层样式
        sheet = dedent(f'''\
            color: {self._text_color};
            background-color: transparent;
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
        self.setIconColorTo(self._colors.icon_hover)
        self.setTextColorTo(self._colors.text_hover)


    def _leaved_handler(self):
        self.setIconColorTo(self._colors.icon)
        self.setTextColorTo(self._colors.text)


    def _pressed_handler(self):
        self.setIconColorTo(self._colors.icon_pressed)
        self.setTextColorTo(self._colors.text_pressed)


    def _released_handler(self):
        self.setIconColorTo(self._colors.icon_hover)
        self.setTextColorTo(self._colors.text_hover)


    def _toggled_handler(self, checked):
        if self._theme_manager.theme() == Zen.Theme.Dark:
            self.setIconColor('#ff202020')
        else:
            self.setIconColor('#fff3f3f3')
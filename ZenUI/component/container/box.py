from enum import Enum, auto
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.layout.column import ZColumnLayout
from ZenUI.component.layout.row import ZRowLayout
from ZenUI.core import Zen,ZColorTool,ZColorSheet,ZMargins

class ZBox(ZWidget):
    '''盒子'''
    class Style(Enum):
        '''背景样式'''
        Monochrome = auto()
        '纯色'
        Gradient = auto()
        '渐变'
        MonochromeWithBorder = auto()
        '纯色带边框'
        GradientWithBorder = auto()
        '渐变带边框'
        OnlyBorder = auto()
        '仅边框'
        Transparent = auto()
        '透明'

    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 fixed_stylesheet: str = None,
                 style: Style = Style.OnlyBorder,
                 layout: Zen.Layout = Zen.Layout.Column,
                 margins: ZMargins = ZMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Zen.Alignment = None):
        super().__init__(parent, name)
        self._fixed_stylesheet = fixed_stylesheet
        self._style = style
        if layout:
            if layout == Zen.Layout.Row:
                self.setLayout(ZRowLayout(parent=self,
                                            margins=margins,
                                            spacing=spacing,
                                            alignment=alignment))
            elif layout == Zen.Layout.Column:
                self.setLayout(ZColumnLayout(parent=self,
                                            margins=margins,
                                            spacing=spacing,
                                            alignment=alignment))
        self._init_style()
        self._schedule_update()


    def _init_style(self):
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.Box)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))
        if self._style in (ZBox.Style.Gradient, ZBox.Style.GradientWithBorder):
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)


    def reloadStyleSheet(self):
        if self._style == ZBox.Style.Monochrome:
            sheet = f'background-color: {self._bg_color_a};\nborder-color: transparent;'

        elif self._style == ZBox.Style.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = dedent(f'''\
            background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},
            stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});
            border-color: transparent;''')

        elif self._style == ZBox.Style.MonochromeWithBorder:
            sheet = f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'

        elif self._style == ZBox.Style.GradientWithBorder:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = dedent(f'''\
            background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},
            stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});
            border-color: {self._border_color};''')

        elif self._style == ZBox.Style.OnlyBorder:
            sheet = f'background-color: transparent;\nborder-color: {self._border_color};'

        elif self._style == ZBox.Style.Transparent:
            sheet = 'background-color: transparent;\nborder-color: transparent;'

        if not self.objectName(): raise ValueError("Widget must have a name when StyleSheetApplyToChildren is False")
        style_parts = [
            f"#{self.objectName()}{{",
            sheet,
            self._fixed_stylesheet,
            "}"
        ]
        return '\n'.join(filter(None, style_parts))


    def _theme_changed_handler(self, theme):
        if self._style == ZBox.Style.Monochrome:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A))

        elif self._style == ZBox.Style.Gradient:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A),
                            self._color_sheet.getColor(theme,Zen.ColorRole.Background_B))
        elif self._style == ZBox.Style.MonochromeWithBorder:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A))
            self.setBorderColor(self._color_sheet.getColor(theme,Zen.ColorRole.Border))

        elif self._style == ZBox.Style.GradientWithBorder:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A),
                            self._color_sheet.getColor(theme,Zen.ColorRole.Background_B))
            self.setBorderColor(self._color_sheet.getColor(theme,Zen.ColorRole.Border))

        elif self._style == ZBox.Style.OnlyBorder:
            self.setBorderColor(self._color_sheet.getColor(theme,Zen.ColorRole.Border))



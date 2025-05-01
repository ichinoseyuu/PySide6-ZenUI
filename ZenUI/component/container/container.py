from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.layout.column import ZColumnLayout
from ZenUI.component.layout.row import ZRowLayout
from ZenUI.core import Zen,ZColorTool,ZColorSheet,ZMargins

class ZContainer(ZWidget):
    '''基本容器'''
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 layout: Zen.Layout = Zen.Layout.Column,
                 margins: ZMargins = ZMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Zen.Alignment = None):
        super().__init__(parent, name)
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


    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.Container)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))


    def reloadStyleSheet(self):
        if self.isWidgetFlagOn(Zen.WidgetFlag.GradientColor):
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = f'background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});'
        else:
            sheet = f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'
        is_apply_to_children = self.isWidgetFlagOn(Zen.WidgetFlag.StyleSheetApplyToChildren)
        if is_apply_to_children:
            if self._fixed_stylesheet:
                return self._fixed_stylesheet +'\n'+ sheet
            else:
                return sheet
        else:
            if not self.objectName(): raise ValueError("Widget must have a name when StyleSheetApplyToChildren is False")
            if self._fixed_stylesheet:
                return f"#{self.objectName()}"+"{\n"+  sheet +'\n'+self._fixed_stylesheet +"\n}"
            else:
                return f"#{self.objectName()}"+"{\n"+ sheet +"\n}"

    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A),self._color_sheet.getColor(theme,Zen.ColorRole.Background_B))
        self.setBorderColorTo(self._color_sheet.getColor(theme,Zen.ColorRole.Border))

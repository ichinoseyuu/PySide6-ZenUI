from ZenUI.component.widget.widget import ZWidget
from ZenUI.core import Zen, ZExpAnim, ZColorSheet, ZColorTool,ZMargins
from enum import Enum, auto
from textwrap import dedent
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.layout.column import ZColumnLayout
from ZenUI.component.layout.row import ZRowLayout
from ZenUI.core import Zen,ZColorTool,ZColorSheet,ZMargins

class ZDrawer(ZWidget):
    '''抽屉'''
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
                 layout: Zen.Layout = None,
                 margins: ZMargins = ZMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Zen.Alignment = Zen.Alignment.Center,
                 can_expand: bool = True,
                 state: Zen.State = Zen.State.Expand,
                 dir: Zen.Direction = Zen.Direction.Vertical,
                 collapse_width: int = 0,
                 expand_width: int = 150):
        super().__init__(parent= parent,name= name)
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
        self._can_expand = can_expand # 是否可以展开
        self._state = state # 当前状态
        if dir not in [Zen.Direction.Vertical, Zen.Direction.Horizontal]:
            raise ValueError(f"This dir {dir} is not support")
        self._dir = dir # 方向
        self._collapse_width = collapse_width # 折叠时的宽度
        self._expand_width = expand_width # 展开时的宽度

        if self._state == Zen.State.Collapsed:
            self.setMinimumWidth(self._collapse_width)
            self.setMaximumWidth(self._collapse_width)
            self._anim_collapse.setCurrent(self._collapse_width)
        elif self._state == Zen.State.Expand:
            self.setMinimumWidth(self._expand_width)
            self.setMaximumWidth(self._expand_width)
            self._anim_collapse.setCurrent(self._expand_width)
        else:
            raise ValueError(f"This state {self._state} is not support")
        self._init_style()
        self._schedule_update()


    def _init_style(self):
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.Drawer)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))
        if self._style in (self.Style.Gradient, self.Style.GradientWithBorder):
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)


    def _init_anim(self):
        super()._init_anim()
        self._anim_collapse = ZExpAnim(self)
        self._anim_collapse.setFactor(0.4)
        self._anim_collapse.setBias(1)
        self._anim_collapse.ticked.connect(self._collapse_handler)
        self._anim_group.addMember(self._anim_collapse,'collapse')


    def reloadStyleSheet(self):
        if self._style == self.Style.Monochrome:
            sheet = f'background-color: {self._bg_color_a};\nborder-color: transparent;'

        elif self._style == self.Style.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = dedent(f'''\
            background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},
            stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});
            border-color: transparent;''')

        elif self._style == self.Style.MonochromeWithBorder:
            sheet = f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'

        elif self._style == self.Style.GradientWithBorder:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = dedent(f'''\
            background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},
            stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});
            border-color: {self._border_color};''')

        elif self._style == self.Style.OnlyBorder:
            sheet = f'background-color: transparent;\nborder-color: {self._border_color};'

        elif self._style == self.Style.Transparent:
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
        if self._style == self.Style.Monochrome:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A))

        elif self._style == self.Style.Gradient:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A),
                            self._color_sheet.getColor(theme,Zen.ColorRole.Background_B))
        elif self._style == self.Style.MonochromeWithBorder:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A))
            self.setBorderColor(self._color_sheet.getColor(theme,Zen.ColorRole.Border))

        elif self._style == self.Style.GradientWithBorder:
            self.setColor(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A),
                            self._color_sheet.getColor(theme,Zen.ColorRole.Background_B))
            self.setBorderColor(self._color_sheet.getColor(theme,Zen.ColorRole.Border))

        elif self._style == self.Style.OnlyBorder:
            self.setBorderColor(self._color_sheet.getColor(theme,Zen.ColorRole.Border))

    def _collapse_handler(self, width):
        newWidth = int(width)
        if self._dir == Zen.Direction.Vertical:
            self.setMinimumWidth(newWidth)
            self.setMaximumWidth(newWidth)
        else:
            self.setMinimumHeight(newWidth)
            self.setMaximumHeight(newWidth)


    def toggleState(self):
        '''切换侧边栏状态'''
        if not self._can_expand: return
        if self._state == Zen.State.Expand:
            self._anim_collapse.setTarget(self._collapse_width)
            self._anim_collapse.start()
            self._state = Zen.State.Collapsed
        else:
            self._anim_collapse.setTarget(self._expand_width)
            self._anim_collapse.start()
            self._state = Zen.State.Expand


    def setCurrentWidth(self, width):
        '''设置当前宽度'''
        self._anim_border_color.setCurrent(width)
        self._collapse_handler(width)


    def sidebarWidth(self):
        '''获取侧边栏的折叠和展开尺寸'''
        return self._collapse_width, self._expand_width


    def setSidebarWidth(self, collapse_width: int, expand_width: int):
        '''设置侧边栏的折叠和展开尺寸'''
        self._collapse_width = collapse_width
        self._expand_width = expand_width
        self._updateSidebarWidth()


    def collapseDir(self):
        '''获取折叠方向'''
        return self._dir


    def setCollapseDir(self, dir: Zen.Direction):
        '''设置折叠方向'''
        self._dir = dir
        self._updateSidebarWidth()


    def _updateSidebarWidth(self):
        '''切换折叠方向和更改折叠尺寸时需要更新控件'''
        if self._state == Zen.State.Collapsed:
            if self._dir == Zen.Direction.Vertical:
                self.setMinimumSize(self._collapse_width, 0)
                self.setMaximumSize(self._collapse_width, 32768)
            else:
                self.setMinimumSize(0, self._collapse_width)
                self.setMaximumSize(32768, self._collapse_width)
            for child in self.children():
                if isinstance(child, ZDrawer):
                    child._updateSidebarWidth()
                    print('Update SidebarWidth')
        else:
            if self._dir == Zen.Direction.Vertical:
                self.setMinimumSize(self._expand_width, 0)
                self.setMaximumSize(self._expand_width, 32768)
            else:
                self.setMinimumSize(0, self._expand_width)
                self.setMaximumSize(32768, self._expand_width)
            for child in self.children():
                if isinstance(child, ZDrawer):
                    child._updateSidebarWidth()
                    print('Update SidebarWidth')



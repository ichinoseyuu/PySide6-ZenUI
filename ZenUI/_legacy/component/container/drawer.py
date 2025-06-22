from enum import IntFlag, IntEnum, auto
from textwrap import dedent
from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.component.layout import ZColumnLayout,ZRowLayout
from ZenUI._legacy.core import Zen,ZExpAnim,ZColorTool,ZMargins

class ZDrawer(ZWidget):
    '''抽屉'''
    class Style(IntFlag):
        '''背景样式'''
        None_ = 0
        Monochrome = 1 << 0
        '纯色'
        Gradient = 1 << 1
        '渐变'
        Border = 1 << 2
        '边框'

    class State(IntEnum):
        '''抽屉状态'''
        Collapsed = auto()
        '折叠'
        Expand = auto()
        '展开'

    class Direction(IntEnum):
        '''抽屉方向'''
        Vertical = auto()
        '垂直'
        Horizontal = auto()
        '水平'

    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 fixed_stylesheet: str = None,
                 style: Style = Style.None_,
                 layout: Zen.Layout = None,
                 margins: ZMargins = ZMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment: Zen.Alignment = Zen.Alignment.Center,
                 can_expand: bool = True,
                 state:State = State.Expand,
                 dir: Direction = Direction.Vertical,
                 collapse_width: int = 0,
                 expand_width: int = 150):
        super().__init__(parent= parent,name= name)
        self._style = style
        '抽屉样式'
        self._can_expand = can_expand
        '是否可以展开'
        self._state = state
        '抽屉状态'
        self._dir = dir
        '抽屉方向'
        self._collapse_width = collapse_width
        '折叠时的宽度'
        self._expand_width = expand_width
        '展开时的宽度'
        if fixed_stylesheet: self.setFixedStyleSheet(fixed_stylesheet)
        if layout == Zen.Layout.Row:
            self.setLayout(ZRowLayout(parent=self,margins=margins,spacing=spacing,alignment=alignment))
        if layout == Zen.Layout.Column:
            self.setLayout(ZColumnLayout(parent=self,margins=margins,spacing=spacing,alignment=alignment))
        if self._state == self.State.Collapsed:
            self.setMinimumWidth(self._collapse_width)
            self.setMaximumWidth(self._collapse_width)
            self._anim_collapse.setCurrent(self._collapse_width)
        if self._state == self.State.Expand:
            self.setMinimumWidth(self._expand_width)
            self.setMaximumWidth(self._expand_width)
            self._anim_collapse.setCurrent(self._expand_width)
        self._init_style()
        self.updateStyle()

    # region ZWidget
    def _init_style(self):
        bg_style = self._style & (self.Style.Monochrome| self.Style.Gradient)
        if bin(bg_style).count('1') > 1:
            raise ValueError("Monochrome and Gradient are mutually exclusive")

        if self._style & self.Style.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)

        self._color_sheet.loadColorConfig(Zen.WidgetType.Drawer)
        self._colors.overwrite(self._color_sheet.getSheet())

        self._bg_color_a = self._colors.background_a
        self._bg_color_b = self._colors.background_b
        self._border_color = self._colors.border
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))



    def _init_anim(self):
        super()._init_anim()
        self._anim_collapse = ZExpAnim(self)
        self._anim_collapse.setFactor(0.4)
        self._anim_collapse.setBias(1)
        self._anim_collapse.ticked.connect(self._collapse_handler)
        self._anim_group.addMember(self._anim_collapse,'collapse')


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        if not self.objectName(): raise ValueError("Widget must have a name")

        sheet = []
        style_parts = [
            f"#{self.objectName()}{{",
            self._stylesheet_fixed,
            '\n'.join(sheet),
            "}"]

        if self._style & self.Style.None_:
            sheet = dedent(f'''\
                background-color: transparent;
                border: none;''')
            self._stylesheet_cache = '\n'.join(filter(None, style_parts))
            self._stylesheet_dirty = False
            return self._stylesheet_cache

        if self._style & self.Style.Monochrome:
            sheet.append(f"background-color: {self._bg_color_a};")

        if self._style & self.Style.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet.append(dedent(f"""\
                background-color: qlineargradient(
                x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
                stop:0 {self._bg_color_a}, stop:1 {self._bg_color_b});"""))

        if self._style & self.Style.Border:
            sheet.append(f"border-color: {self._border_color};")
        else:
            sheet.append("border: none;")

        self._stylesheet_cache = '\n'.join(filter(None, style_parts))
        self._stylesheet_dirty = False
        return self._stylesheet_cache


    def _theme_changed_handler(self, theme):
        if self._style & self.Style.None_: return

        self._colors.overwrite(self._color_sheet.getSheet(theme))

        if self._style & self.Style.Monochrome:
            self.setColor(self._colors.background_a)

        if self._style & self.Style.Gradient:
            self.setColor(self._colors.background_a,self._colors.background_b)

        if self._style & self.Style.Border:
            self.setBorderColor(self._colors.border)

    # region ZDrawer
    def _collapse_handler(self, width):
        newWidth = int(width)
        if self._dir == self.Direction.Vertical:
            self.setMinimumWidth(newWidth)
            self.setMaximumWidth(newWidth)
        else:
            self.setMinimumHeight(newWidth)
            self.setMaximumHeight(newWidth)


    def toggleState(self):
        '''切换侧边栏状态'''
        if not self._can_expand: return
        if self._state == self.State.Expand:
            self._anim_collapse.setTarget(self._collapse_width)
            self._anim_collapse.start()
            self._state = self.State.Collapsed
        else:
            self._anim_collapse.setTarget(self._expand_width)
            self._anim_collapse.start()
            self._state = self.State.Expand


    def setCurrentWidth(self, width: int):
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


    def setCollapseDir(self, dir: Direction):
        '''设置折叠方向'''
        self._dir = dir
        self._updateSidebarWidth()


    def _updateSidebarWidth(self):
        '''切换折叠方向和更改折叠尺寸时需要更新控件'''
        if self._state == self.State.Collapsed:
            if self._dir == self.Direction.Vertical:
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
            if self._dir == self.Direction.Vertical:
                self.setMinimumSize(self._expand_width, 0)
                self.setMaximumSize(self._expand_width, 32768)
            else:
                self.setMinimumSize(0, self._expand_width)
                self.setMaximumSize(32768, self._expand_width)
            for child in self.children():
                if isinstance(child, ZDrawer):
                    child._updateSidebarWidth()
                    print('Update SidebarWidth')




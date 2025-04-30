from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.container.container import ZContainer
from ZenUI.core import Zen, ZExpAnim, ZColorSheet, ZColorTool
class ZCollapsibleContainer(ZContainer):
    '''可折叠容器'''
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 layout: Zen.Layout = None,
                 can_expand: bool = True,
                 state: Zen.State = Zen.State.Expand,
                 dir: Zen.Direction = Zen.Direction.Vertical,
                 collapse_width: int = 0,
                 expand_width: int = 150):
        super().__init__(parent, name, layout)
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

    def _init_style(self):
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.CollapsibleContainer)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))


    def _init_anim(self):
        super()._init_anim()
        self._anim_collapse = ZExpAnim(self)
        self._anim_collapse.setBias(0.25)
        self._anim_collapse.setFactor(0.2)
        self._anim_collapse.ticked.connect(self._collapse_handler)
        self._anim_group.addMember(self._anim_collapse,'collapse')


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
                if isinstance(child, ZCollapsibleContainer):
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
                if isinstance(child, ZCollapsibleContainer):
                    child._updateSidebarWidth()
                    print('Update SidebarWidth')
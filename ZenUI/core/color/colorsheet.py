from PySide6.QtCore import QObject,Signal
from typing import Optional,Dict, overload
import copy
from ZenUI.core.enumrates import Zen

class ZColorSheet(QObject):
    '''
    每个控件的自己的颜色表
    - 同类型控件之间独立
    - 需要从`ColorConfig`中获取相应的颜色表
    '''
    colorChanged = Signal(bool) # 颜色表改变信号,参数为是否需要重新加载颜色表
    '颜色表改变信号,参数为是否需要重新加载颜色表'
    def __init__(self, parent, widget_type: Zen.WidgetType = None):
        super().__init__(parent)
        from ZenUI.core.globals.globals import ZenGlobal
        self.theme_manager = ZenGlobal.ui.theme_manager
        self._parent = parent
        self.widget_type = widget_type
        self.sheet = {}
        if self.widget_type: self.sheet = copy.deepcopy(ZenGlobal.ui.color_config.getConfig(self.widget_type))

    def loadColorConfig(self, widget_type: Zen.WidgetType):
        '加载颜色表'
        from ZenUI.core.globals.globals import ZenGlobal
        self.widget_type = widget_type
        self.sheet = copy.deepcopy(ZenGlobal.ui.color_config.getConfig(self.widget_type))

    @overload
    def getColor(self, role: Zen.ColorRole) -> Optional[str]:
        '获取当前主题下颜色对象的颜色'
        pass

    @overload
    def getColor(self, theme: Zen.Theme, role: Zen.ColorRole) -> Optional[str]:
        '获取指定主题下颜色对象的颜色'
        pass

    def getColor(self, *args) -> Optional[str]:
        if len(args) == 1:
            # 获取当前主题下颜色
            role = args[0]
            return self.sheet[self.theme_manager.theme()][role]
        elif len(args) == 2:
            # 获取指定主题下颜色
            theme, role = args
            return self.sheet[theme][role]
        else:
            raise ValueError("Invalid number of arguments. Must be 1 or 2.")


    @overload
    def getSheet(self) -> Dict[Zen.ColorRole, Optional[str]]:
        '获取当前主题下颜色表'
        pass

    @overload
    def getSheet(self, theme: Zen.Theme, role: Zen.ColorRole) -> Dict[Zen.ColorRole, Optional[str]]:
        '获取指定主题下颜色表'
        pass

    def getSheet(self, *args) -> Dict[Zen.ColorRole, Optional[str]]:
        if len(args) == 0:
            # 获取当前主题下颜色表
            return self.sheet[self.theme_manager.theme()]
        elif len(args) == 1:
            # 获取指定主题下颜色表
            theme = args[0]
            return self.sheet[theme]


    @overload
    def setColor(self, role: Zen.ColorRole, color: Optional[str]) -> None:
        '设置当前主题下颜色对象的颜色'
        pass

    @overload
    def setColor(self, theme: Zen.Theme, role: Zen.ColorRole, color: Optional[str]) -> None:
        '设置指定主题下颜色对象的颜色'
        pass

    def setColor(self, *args) -> None:
        if len(args) == 2:
            # 设置当前主题下颜色
            role, color = args
            theme = self.theme_manager.theme()
            self.sheet[theme][role] = color
            self.colorChanged.emit(True)
        elif len(args) == 3:
            # 设置指定主题下颜色
            theme, role, color = args
            self.sheet[theme][role] = color
            if theme == self.theme_manager.theme():
                self.colorChanged.emit(True)
            else:
                self.colorChanged.emit(False)
        else:
            raise ValueError("Invalid number of arguments. Must be 2 or 3.")

    def isSheetNull(self) -> bool:
        '颜色表是否为空'
        return not self.sheet

    def isRoleNull(self, role: Zen.ColorRole) -> bool:
        '颜色表中的颜色是否为空'
        return self.sheet[self.theme_manager.theme()][role] is None
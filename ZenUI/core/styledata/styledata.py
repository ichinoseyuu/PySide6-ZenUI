from typing import Union, overload, Dict
from ..theme import ZThemeManager
from .models import (ZButtonStyleData, ZTitleBarButtonData, ZFramelessWindowStyleData,
                     ZTextBlockStyleData,ZToolTipStyleData, ZToggleButtonStyleData,
                     ZNavBarButtonStyleData)
from .theme_data import THEME_DATA
from .style_factory import ZStyleDataFactory

StyleDataType = Union[ZButtonStyleData, ZTitleBarButtonData,ZFramelessWindowStyleData,
                      ZTextBlockStyleData,ZToolTipStyleData, ZToggleButtonStyleData,
                      ZNavBarButtonStyleData]

class ZStyleDataManager:
    def __init__(self):
        super().__init__()
        self._factory = ZStyleDataFactory()
        self._cache: Dict[str, StyleDataType] = {}  # 添加缓存字典

    def _get_cache_key(self, name: str, theme: str) -> str:
        return f"{theme}:{name}"

    @overload
    def getStyleData(self, name: str) -> StyleDataType:
        ...

    @overload
    def getStyleData(self, name: str, theme: str) -> StyleDataType:
        ...

    def getStyleData(self, *args) -> StyleDataType:
        if len(args) == 1:
            name = args[0]
            theme = ZThemeManager().getTheme().name
        else:
            name, theme = args

        # 检查缓存
        cache_key = self._get_cache_key(name, theme)
        if cache_key in self._cache:
            return self._cache[cache_key]

        theme_data = THEME_DATA.get(theme, {})
        component_data = theme_data.get(name, {})

        # 创建样式数据并缓存
        style_data = ZStyleDataFactory.create(name, component_data)
        self._cache[cache_key] = style_data

        return style_data

    def clearCache(self) -> None:
        """切换主题时清除缓存"""
        self._cache.clear()

    def invalidateCache(self, name: str = None, theme: str = None) -> None:
        """只清除特定主题的缓存"""
        if name is None and theme is None:
            self.clearCache()
            return

        keys_to_remove = []
        for key in self._cache:
            cached_theme, cached_name = key.split(':')
            if (theme and theme == cached_theme) or (name and name == cached_name):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self._cache.pop(key)

    def preloadCommonStyles(self, theme: str = None) -> None:
        """预加载常用的样式数据"""
        common_components = [
            'Button',
            'MinimizeButton',
            'MaximizeButton',
            'CloseButton',
            'FramelessWindow',
            'TextBlock',
            'ToolTip',
            'ToggleButton'
        ]

        themes = [theme] if theme else list(THEME_DATA.keys())

        for t in themes:
            for component in common_components:
                self.getStyleData(component, t)
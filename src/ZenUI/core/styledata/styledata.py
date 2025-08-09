from typing import Union, overload, Dict, Any,TYPE_CHECKING
from dataclasses import fields, is_dataclass
from enum import Enum
from PySide6.QtGui import QColor
from ..theme import ZThemeManager
from .models import *
from .theme_data import *
    
StyleDataType = Union[ZButtonStyleData, ZTitleBarButtonData,ZFramelessWindowStyleData,
                      ZTextBlockStyleData,ZToolTipStyleData, ZToggleButtonStyleData,
                      ZNavBarButtonStyleData,ZNavBarToggleButtonStyleData,ZPageStyleData,
                      ZScrollPageStyleData,ZSliderStyleData,ZCardStyleData]

class ZStyleDataFactory:
    dataclass_map = {
        'ZCard': ZCardStyleData,
        'ZTextBlock': ZTextBlockStyleData,
        'ZPage': ZPageStyleData,
        'ZScrollPage': ZScrollPageStyleData,
        'ZSlider': ZSliderStyleData,
        'ZButton': ZButtonStyleData,
        'ZToggleButton': ZToggleButtonStyleData,
        'ZThemeButton': ZTitleBarButtonData,
        'ZNavBarButton': ZNavBarButtonStyleData,
        'ZNavBarToggleButton': ZNavBarToggleButtonStyleData,
        'ZMinimizeButton': ZTitleBarButtonData,
        'ZMaximizeButton': ZTitleBarButtonData,
        'ZCloseButton': ZTitleBarButtonData,
        'ZFramelessWindow': ZFramelessWindowStyleData,
        'ZToolTip': ZToolTipStyleData,
        }
    @staticmethod
    def create(name: str, data: Dict[str, Any]) -> StyleDataType:
        cls = ZStyleDataFactory.dataclass_map.get(name)
        if cls is None:
            raise ValueError(f"Unknown style data class for component: {name}")
        return ZStyleDataFactory.dict_to_dataclass(cls, data)


    def dict_to_dataclass(cls, data: dict) -> StyleDataType:
        if not is_dataclass(cls):
            raise TypeError(f"{cls} is not a dataclass")
        field_map = {f.name: f.type for f in fields(cls)}
        filtered = {}
        for k, v in data.items():
            # 统一 key 为字符串
            key_str = k.value if isinstance(k, Enum) else str(k)
            if key_str in field_map:
                target_type = field_map[key_str]
                # 自动类型转换
                if target_type is QColor:
                    filtered[key_str] = QColor(v)
                elif target_type is int:
                    filtered[key_str] = int(v)
                elif target_type is float:
                    filtered[key_str] = float(v)
                else:
                    filtered[key_str] = v
        return cls(**filtered)


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
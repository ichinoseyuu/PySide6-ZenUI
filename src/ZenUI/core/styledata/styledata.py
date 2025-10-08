import logging
from typing import overload, Dict, Any
from dataclasses import fields, is_dataclass
from enum import Enum
from PySide6.QtGui import QColor
from ZenUI.core.theme import ZThemeManager
from ZenUI.core.utils import singleton
from ZenUI.core.styledata.models import *
from ZenUI.core.styledata.theme_data import *

class ZStyleDataFactory:
    dataclass_map = {
        'ZComboBox': ZComboBoxStyleData,
        'ZItem': ZItemStyleData,
        'ZItemView': ZItemViewStyleData,
        'ZNavigationBar': ZNavigationBarStyleData,
        'ZSwitch': ZSwitchStyleData,
        'ZTextBox': ZTextBoxStyleData,
        'ZRichTextBlock':ZRichTextBlockStyleData,
        'ZTextBlock': ZTextBlockStyleData,
        'ZPanel': ZPanelStyleData,
        'ZScrollPanel': ZScrollPanelStyleData,
        'ZSlider': ZSliderStyleData,
        'ZButton': ZButtonStyleData,
        'ZToggleButton': ZToggleButtonStyleData,
        'ZThemeButton': ZTitleBarButtonStyleData,
        'ZNavBarButton': ZNavBarButtonStyleData,
        'ZNavBarToggleButton': ZNavBarToggleButtonStyleData,
        'ZMinimizeButton': ZTitleBarButtonStyleData,
        'ZMaximizeButton': ZTitleBarButtonStyleData,
        'ZCloseButton': ZTitleBarButtonStyleData,
        'ZFramelessWindow': ZFramelessWindowStyleData,
        'ZToolTip': ZToolTipStyleData,
    }

    @classmethod
    def create(cls, name: str, data: Dict[str, Any]) -> StyleDataT:
        data_type = cls.dataclass_map.get(name)
        if data_type is None:
            raise ValueError(f"Unknown style data class for component: {name}")
        #logging.info(f"Creating style data for component: {name}")
        return cls.dictToDataclass(data_type, data)

    @staticmethod
    def dictToDataclass(data_type: StyleDataT, data: dict) -> StyleDataT:
        if not is_dataclass(data_type):
            raise TypeError(f"{data_type} is not a dataclass")
        # 将 StyleDataT 转换为字段映射
        field_map = {f.name: f.type for f in fields(data_type)}

        filtered = {}
        for k, v in data.items():
            # 统一 data 字典中的键名统一为字符串
            key_str = k.value if isinstance(k, Enum) else str(k)
            # 从字段映射中匹配 data 字典中的键名
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
        return data_type(**filtered)

@singleton
class ZStyleDataManager:
    def __init__(self):
        super().__init__()
        self._factory = ZStyleDataFactory()
        self._cache: Dict[str, StyleDataT] = {}  # 添加缓存字典

    def _get_cache_key(self, name: str, theme: str) -> str:
        return f"{theme}:{name}"

    @overload
    def getStyleData(self, name: str) -> StyleDataT: ...

    @overload
    def getStyleData(self, name: str, theme: str) -> StyleDataT: ...

    def getStyleData(self, *args) -> StyleDataT:
        if len(args) == 1:
            name = args[0]
            theme = ZThemeManager().getTheme().name
        else:
            name, theme = args

        # 检查缓存
        cache_key = self._get_cache_key(name, theme)
        if cache_key in self._cache:
            return self._cache[cache_key]


        # 获取主题数据(251105)
        # theme_data = THEME_DATA.get(theme, {})
        # component_data = theme_data.get(name, {})


        theme_data = THEME_DATA.get(theme, {})
        component_data = {}
        # 新增：支持从元组键中匹配组件样式
        for key, data in theme_data.items():
            # 如果键是字符串且完全匹配，则合并样式数据（覆盖元组中可能存在的同名配置）
            if isinstance(key, str) and name == key:
                component_data.update(data)
                break
            # 如果键是元组且当前组件名在元组中，则合并样式数据
            elif isinstance(key, tuple) and name in key:
                component_data.update(data)
                break

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
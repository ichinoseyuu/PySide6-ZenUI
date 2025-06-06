from typing import Dict, ClassVar
from dataclasses import dataclass
from ZenUI.core.enumrates import Zen

@dataclass
class ZColors:
    """
    颜色数据类
    - 表示某个控件的某个主题的所有颜色
    """
    # 显式定义所有可能的属性，提供类型提示
    background_a: str = None
    '背景颜色a'
    background_b: str = None
    '背景颜色b'
    hover: str = None
    '悬停背景颜色'
    pressed: str = None
    '按下背景颜色'
    flash: str = None
    '闪烁背景颜色'
    selected_a: str = None
    '选中背景颜色a'
    selected_b: str = None
    '选中背景颜色b'
    border: str = None
    '边框颜色'
    border_hover: str = None
    '悬停边框颜色'
    border_pressed: str = None
    '按下边框颜色'
    border_selected: str = None
    '选中边框颜色'
    text: str = None
    '文本颜色'
    text_hover: str = None
    '悬停文本颜色'
    text_pressed: str = None
    '按下文本颜色'
    text_selected: str = None
    '选中文本颜色'
    icon: str = None
    '图标颜色'
    icon_hover: str = None
    '悬停图标颜色'
    icon_pressed: str = None
    '按下图标颜色'
    icon_selected: str = None
    '选中图标颜色'
    indicator_selected: str = None
    '指示条选中颜色'

    @staticmethod
    def _generate_color_map() -> Dict[str, str]:
        """根据ColorRole枚举自动生成颜色映射"""
        def camel_to_snake(name: str) -> str:
            """将驼峰命名转换为下划线命名"""
            import re
            # 1. 先处理大写字母开头的情况
            name = name[0].lower() + name[1:]
            # 2. 在大写字母前添加下划线并转小写
            return re.sub(r'([A-Z])', r'_\1', name).lower()

        return {
            camel_to_snake(role.name): role.name
            for role in Zen.ColorRole
        }
    # 使用类方法生成color_map
    _color_map: ClassVar[Dict[str, str]] = _generate_color_map()

    def __init__(self, color_dict: Dict[Zen.ColorRole, str] = None):
        '根据传入的颜色表初始化颜色属性'
        if color_dict: self.overwrite(color_dict)

    def overwrite(self, color_dict: Dict[Zen.ColorRole, str]):
        '根据传入的颜色表覆盖颜色属性'
        for attr_name, role_name in self._color_map.items():
            role = getattr(Zen.ColorRole, role_name)
            setattr(self, attr_name, color_dict.get(role))

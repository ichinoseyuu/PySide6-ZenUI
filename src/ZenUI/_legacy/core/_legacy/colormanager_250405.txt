from typing import Union, Optional, Dict, Set
import numpy
import re
from dataclasses import dataclass
from ..enum.zen import Zen
class ColorTool:
    """颜色工具类，提供颜色转换、颜色验证等功能"""
    @staticmethod
    def RGBToARGB(code: str):
        """将`#RRGGBB`转换为`#AARRGGBB`"""
        code_data = code.replace("#", "")
        length = len(code_data)
        if length != 6: raise ValueError(f"Unexpected length of input: {code}, length: {length}")
        return f"#ff{code_data}"


    @staticmethod
    def ARGBForceToRGB(code: str):
        """将`#AARRGGBB`强制转换为`#RRGGBB`"""
        code_data = code.replace("#", "")
        length = len(code_data)
        if length != 8: raise ValueError(f"Unexpected length of input: {code}, length: {length}")
        return f"#FF{code_data.upper()}"


    @staticmethod
    def ARGBToRGBA(code: str):
        """将`#AARRGGBB`转换为`#RRGGBBAA`"""
        code_data = code.replace("#", "")
        length = len(code_data)
        if length != 8: raise ValueError(f"Unexpected length of input: {code}, length: {length}")
        a, r, g, b = int(code_data[0:2], 16), int(code_data[2:4], 16), int(code_data[4:6], 16), int(code_data[6:8], 16)
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}{int(a):02x}"


    @staticmethod
    def RGBAToARGB(code: str):
        """将`#RRGGBBAA`转换为`#AARRGGBB`"""
        code_data = code.replace("#", "")
        length = len(code_data)
        if length != 8: raise ValueError(f"Unexpected length of input: {code}, length: {length}")
        r, g, b, a= int(code_data[0:2], 16), int(code_data[2:4], 16), int(code_data[4:6], 16), int(code_data[6:8], 16)
        return f"#{int(a):02x}{int(r):02x}{int(g):02x}{int(b):02x}"


    @classmethod
    def toArray(cls, code: str):
        """
        根据传入的颜色代码，返回一个包含颜色信息的数组
        Args:
            code (str): 颜色代码，可以是`#RRGGBB`或者`#AARRGGBB`

        Returns:
            """
        # 检查输入是否为列表或元组，如果是则转换为numpy数组并返回
        if not isinstance(code, (str)): raise ValueError(f"Unexpected type of input: {code}, type: {type(code)}")
        code_data = code.lstrip("#")
        if len(code_data) == 6:
            r, g, b = int(code_data[0:2], 16), int(code_data[2:4], 16), int(code_data[4:6], 16)
            return numpy.array([r, g, b], dtype=numpy.int16)
        if len(code_data) == 8:
            a, r, g, b = int(code_data[0:2], 16), int(code_data[2:4], 16), int(code_data[4:6], 16), int(code_data[6:8], 16)
            return numpy.array([a, r, g, b], dtype=numpy.int16)


    @staticmethod
    def toCode(value: Union[numpy.ndarray, list]):
        """将`array(A, R, G, B, dtype=int16)`转换为`#AARRGGBB`"""
        if len(value) == 3:
            r, g, b = value
            return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
        elif len(value) == 4:
            a, r, g, b = value
            return f"#{int(a):02x}{int(r):02x}{int(g):02x}{int(b):02x}"
        else:
            raise ValueError(f"Unexpected shape of input: {value}, shape: {value.shape}")


    @classmethod
    def mix(cls, code_fore: str, code_post: str, weight: float = 0.5):
        """混合两个颜色代码，返回混合后的颜色代码"""
        fore_array = cls.toArray(code_fore)
        post_array = cls.toArray(code_post)
        mixed_rgb = fore_array * weight + post_array * (1-weight)
        return cls.toCode(mixed_rgb)


    @classmethod
    def trans(cls, code: str, trans: float = 0):
        """给指定的`#RRGGBB`颜色代码设置一个透明度，返回新的颜色代码"""
        value = cls.toArray(code)
        value_proceed = value * numpy.array([trans, 1, 1, 1])
        code_proceed = cls.toCode(value_proceed)
        return code_proceed

    @staticmethod
    def isValidColor(color: str) -> bool:
        """验证颜色格式，支持 RGB 和 ARGB 格式"""
        # 正则表达式匹配 ARGB (#AARRGGBB) 或 RGB (#RRGGBB)
        hex_color_pattern = r"^#([0-9a-fA-F]{8}|[0-9a-fA-F]{6})$"
        return bool(re.match(hex_color_pattern, color))


class ColorConfig:
    """颜色配置类，为每一个控件类型创建一个字典，可以设置和获取颜色"""
    def __init__(self):
        self.colors: Dict[Zen.ColorRole, Optional[str]] = {role: None for role in Zen.ColorRole}

    def setColor(self, role: Zen.ColorRole, color: Optional[str]):
        """设置颜色，如果没有颜色则设置为 None"""
        if color and not ColorTool.isValidColor(color):
            raise ValueError(f"Invalid color format: {color}")
        self.colors[role] = color

    def getColor(self, role: Zen.ColorRole) -> Optional[str]:
        """获取指定对象颜色"""
        return self.colors.get(role, None)



class ColorConfigManager:
    """控件类型的颜色配置管理类，继承这个类可以实现一套配置，每套配置独立且互不干扰"""
    def __init__(self):
        self.widget_colors: Dict[Zen.WidgetType, ColorConfig] = {}


    def setWidgetColor(self, type: Zen.WidgetType, role: Zen.ColorRole, color: Optional[str]):
        """为指定的控件类型设置颜色"""
        if type not in self.widget_colors:
            self.widget_colors[type] = ColorConfig()
        self.widget_colors[type].setColor(role, color)

    def getWidgetColor(self, type: Zen.WidgetType, role: Zen.ColorRole) -> Optional[str]:
        """获取指定控件类型的颜色"""
        widget_config = self.widget_colors.get(type)
        if widget_config is not None:
            color = widget_config.getColor(role)
            if color is not None:
                return color
            else:
                raise ValueError(f"Color not set for role {role} and widget type {type}")
        raise ValueError(f"Widget type {type} not found in widget_colors")

    def getWidgetColorDict(self, type: Zen.WidgetType) -> Dict[Zen.ColorRole, Optional[str]]:
        """获取指定控件类型的颜色字典"""
        widget_config = self.widget_colors.get(type)
        if widget_config is not None:
            return widget_config.colors


class ColorSetter:
    """控件颜色设置器，用于快速、便捷的设置某套配置内的控件颜色"""
    def __init__(self, manager: ColorConfigManager, type: Zen.WidgetType):
        self.widget_type = type
        self.manager = manager

    def setBackground_A(self, color):
        """设置控件背景颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Background_A, color)

    def setBackground_B(self, color):
        """设置控件背景颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Background_B, color)

    def setHover(self, color):
        """设置控件悬停颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Hover, color)

    def setPressed(self, color):
        """设置控件按下颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Pressed, color)

    def setFlash(self, color):
        """设置控件闪烁颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Flash, color)

    def setText(self, color):
        """设置控件文本颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Text, color)

    def setBorder(self, color):
        """设置控件边框颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Border, color)

    def setDisabled(self, color):
        """设置控件禁用颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Disabled, color)

    def setIcon(self, color):
        """设置控件图标颜色"""
        self.manager.setWidgetColor(self.widget_type, Zen.ColorRole.Icon, color)

class ColorGetter:
    """控件颜色获取器，用于快速、便捷的获取某套配置内的控件颜色"""
    def __init__(self, manager: ColorConfigManager, type: Zen.WidgetType):
        self.widget_type = type
        self.manager = manager

    def getBackground_A(self):
        """获取控件背景颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Background_A)

    def getBackground_B(self):
        """获取控件背景颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Background_B)

    def getHover(self):
        """获取控件悬停颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Hover)
    def getPressed(self):
        """获取控件按下颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Pressed)

    def getFlash(self):
        """获取控件闪烁颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Flash)

    def getText(self):
        """获取控件文本颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Text)

    def getBorder(self):
        """获取控件边框颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Border)

    def getDisabled(self):
        """获取控件禁用颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Disabled)
    def getIcon(self):
        """获取控件图标颜色"""
        return self.manager.getWidgetColor(self.widget_type, Zen.ColorRole.Icon)

class ColorMap:
    """颜色映射表，每类控件自己的颜色表"""
    def __init__(self):
        self._color_map = {}

    def __getitem__(self, role: Zen.ColorRole):
        return self._color_map[role]

    def __setitem__(self, token, code: str):
        self._color_map[token] = code

    def __delitem__(self, token):
        del self._color_map[token]

@dataclass
class ColorSheet:
    """颜色表，包含所有控件类型的颜色表"""
    Hover: str ='#ffffff'
    Pressed: str ='#ffffff'
    Flash: str ='#ffffff'
    Text: str ='#ffffff'
    Border: str ='#ffffff'
    Disabled: str ='#ffffff'
    Icon: str ='#ffffff'
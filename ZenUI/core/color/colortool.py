from typing import Union
import numpy
import re

class ZColorTool:
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

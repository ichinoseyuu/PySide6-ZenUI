from typing import Union
import numpy
import re

class ZColorTool:
    """颜色工具类，提供颜色转换、颜色验证等功能"""
    @staticmethod
    def RGBToARGB(color: Union[str, numpy.ndarray, tuple, list]):
        """将`#RRGGBB`转换为`#AARRGGBB`"""
        if isinstance(color, str):
            color_data = color.replace("#", "")
            length = len(color_data)
            if length != 6: raise ValueError(f"Unexpected length of input: {color}, length: {length}")
            return f"#ff{color_data}"
        elif isinstance(color, numpy.ndarray | tuple | list):
            r, g, b = color[0], color[1], color[2]
            return numpy.array([255, r, g, b], dtype=numpy.int16)


    @staticmethod
    def ARGBForceToRGB(color: Union[str, numpy.ndarray, tuple, list]):
        """将`#AARRGGBB`强制转换为`#RRGGBB`"""
        if isinstance(color, str):
            color_data = color.replace("#", "")
            length = len(color_data)
            if length != 8: raise ValueError(f"Unexpected length of input: {color}, length: {length}")
            return f"#FF{color_data.upper()}"
        elif isinstance(color, numpy.ndarray | tuple | list):
            return numpy.array([color[1], color[2], color[3]], dtype=numpy.int16)


    @staticmethod
    def ARGBToRGBA(color: Union[str, numpy.ndarray, tuple, list]):
        """将`#AARRGGBB`转换为`#RRGGBBAA`"""
        if isinstance(color, str):
            color_data = color.replace("#", "")
            length = len(color_data)
            if length != 8: raise ValueError(f"Unexpected length of input: {color}, length: {length}")
            a, r, g, b = int(color_data[0:2], 16), int(color_data[2:4], 16), int(color_data[4:6], 16), int(color_data[6:8], 16)
            return f"#{int(r):02x}{int(g):02x}{int(b):02x}{int(a):02x}"
        elif isinstance(color, numpy.ndarray | tuple | list):
            return numpy.array([color[1], color[2], color[3], color[0]], dtype=numpy.int16)


    @staticmethod
    def RGBAToARGB(color: Union[str, numpy.ndarray, tuple, list]):
        """将`#RRGGBBAA`转换为`#AARRGGBB`"""
        if isinstance(color, str):
            color_data = color.replace("#", "")
            length = len(color_data)
            if length != 8: raise ValueError(f"Unexpected length of input: {color}, length: {length}")
            r, g, b, a= int(color_data[0:2], 16), int(color_data[2:4], 16), int(color_data[4:6], 16), int(color_data[6:8], 16)
            return f"#{int(a):02x}{int(r):02x}{int(g):02x}{int(b):02x}"
        elif isinstance(color, numpy.ndarray | tuple | list):
            return numpy.array([color[3], color[0], color[1], color[2]], dtype=numpy.int16)


    @classmethod
    def toArray(cls, code: str):
        """将`#RRGGBB`或`#AARRGGBB`转换为RGB或ARGB数组"""
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
    def toHSV(color: Union[numpy.ndarray, list, tuple, str]):
        """将`#RRGGBB`或`#AARRGGBB`转换为HSV颜色空间"""
        # 1. 确保 RGB 值正确获取
        if isinstance(color, str):
            color = ZColorTool.toArray(color)
        # 2. 根据数组长度正确获取 RGB 值
        if len(color) == 3:
            r, g, b = color / 255.0  # 归一化到 0-1
        elif len(color) == 4:
            r, g, b = color[1:] / 255.0  # 跳过 alpha 通道
        else:
            raise ValueError(f"Unexpected color format: {color}")
        # 3. 计算 HSV
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        # 计算色相 H
        h = 0
        if df != 0:  # 避免除以零
            if mx == r:
                h = 60 * ((g - b) / df % 6)
            elif mx == g:
                h = 60 * ((b - r) / df + 2)
            elif mx == b:
                h = 60 * ((r - g) / df + 4)
            h = (h + 360) % 360  # 确保 h 在 0-360 范围内
        # 计算饱和度 S
        s = 0 if mx == 0 else (df / mx) * 100
        # 计算明度 V
        v = mx * 100
        return h, s, v

    @staticmethod
    def HSVToRGB(color: Union[numpy.ndarray, list, tuple]):
        """将HSV颜色空间转换为RGB颜色空间"""
        h, s, v = color
        c = (v/100) * (s/100)
        x = c * (1 - abs((h/60) % 2 - 1))
        m = (v/100) - c
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
        return numpy.array([r, g, b], dtype=numpy.int16)


    @staticmethod
    def toHSL(color: Union[numpy.ndarray, list, tuple, str]):
        """将`#RRGGBB`或`#AARRGGBB`转换为HSL颜色空间"""
        # 1. 确保 RGB 值正确获取
        if isinstance(color, str):
            color = ZColorTool.toArray(color)
        # 2. 根据数组长度正确获取 RGB 值
        if len(color) == 3:
            r, g, b = color / 255.0  # 归一化到 0-1
        elif len(color) == 4:
            r, g, b = color[1:] / 255.0  # 跳过 alpha 通道
        else:
            raise ValueError(f"Unexpected color format: {color}")
        # 3. 计算 HSL
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        l = (mx + mn) / 2
        if df == 0:
            s = 0
        else:
            s = df / (1 - abs(2*l - 1))
        return h, s, l

    @staticmethod
    def HSLToRGB(color: Union[numpy.ndarray, list, tuple]):
        """将HSL颜色空间转换为RGB颜色空间"""
        h, s, l = color
        c = (1 - abs(2*l - 1)) * s
        x = c * (1 - abs((h/60) % 2 - 1))
        m = l - c / 2
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
        return numpy.array([r, g, b], dtype=numpy.int16)

    @staticmethod
    def toCode(value: Union[numpy.ndarray, list, tuple]):
        """将RGB或ARGB数组转换为`#RRGGBB`或`#AARRGGBB`颜色代码"""
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

    @classmethod
    def overlay(cls, base_color: str, overlay_color: str) -> str:
        """
        将一个颜色叠加到另一个颜色上
        Args:
            base_color: 底色，格式为 #RRGGBB 或 #AARRGGBB
            overlay_color: 叠加色，格式为 #RRGGBB 或 #AARRGGBB
        Returns:
            str: 叠加后的颜色，格式为 #AARRGGBB
        """
        # 转换为数组
        base = cls.toArray(base_color)
        over = cls.toArray(overlay_color)
        # 确保两个颜色都是 ARGB 格式
        if len(base) == 3:
            base = numpy.append([255], base)
        if len(over) == 3:
            over = numpy.append([255], over)
        # 将 Alpha 值归一化到 0-1
        base_alpha = base[0] / 255
        over_alpha = over[0] / 255
        # 计算混合后的 Alpha 值
        final_alpha = over_alpha + base_alpha * (1 - over_alpha)
        # 计算混合后的 RGB 值
        if final_alpha == 0:
            final_rgb = numpy.array([0, 0, 0])
        else:
            final_rgb = (over[1:] * over_alpha + base[1:] * base_alpha * (1 - over_alpha)) / final_alpha
        # 组合最终颜色
        final_color = numpy.append([final_alpha * 255], final_rgb)
        return cls.toCode(final_color.astype(numpy.int16))

    @staticmethod
    def adjust(color: str, lightness: float = 0, saturation: float = 0):
        """
        调整颜色的亮度和饱和度
        Args:
            color: 输入颜色，格式为 #RRGGBB 或 #AARRGGBB
            lightness: 亮度调整值，范围 [-1, 1]
            saturation: 饱和度调整值，范围 [-1, 1]
        Returns:
            str: 调整后的颜色代码
        """
        color_arr = ZColorTool.toArray(color)
        # 使用现有的 toHSL 方法转换为 HSL
        h, s, l = ZColorTool.toHSL(color)
        # 调整亮度和饱和度
        l = min(1, max(0, l + lightness))
        s = min(1, max(0, s + saturation))
        # 使用现有的 HSLToRGB 方法转换回 RGB
        rgb = ZColorTool.HSLToRGB((h, s, l))
        # 保持原始的透明度
        if len(color_arr) == 4:
            return ZColorTool.toCode(numpy.array([color_arr[0], rgb[0], rgb[1], rgb[2]], dtype=numpy.int16))
        else:
            return ZColorTool.toCode(rgb)

    @staticmethod
    def darker(color: str, amount: float = 0.1) -> str:
        """获取较深的颜色"""
        color_array = ZColorTool.toArray(color)
        if len(color_array) == 3:
            color_array = numpy.append([255], color_array)
        # 降低RGB值
        color_array[1:] = color_array[1:] * (1 - amount)
        return ZColorTool.toCode(color_array.astype(numpy.int16))

    @staticmethod
    def isValidColor(color: str) -> bool:
        """验证颜色格式，支持 RGB 和 ARGB 格式"""
        # 正则表达式匹配 ARGB (#AARRGGBB) 或 RGB (#RRGGBB)
        hex_color_pattern = r"^#([0-9a-fA-F]{8}|[0-9a-fA-F]{6})$"
        return bool(re.match(hex_color_pattern, color))

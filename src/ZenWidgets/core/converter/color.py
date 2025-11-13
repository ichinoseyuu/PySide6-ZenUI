from typing import Union, Literal
import numpy
import re
from PySide6.QtGui import QColor

class ColorConverter:
    """提供颜色转换、调整及运算功能，统一支持QColor和字符串输入输出"""

    @staticmethod
    def _to_numpy(color: Union[str, QColor, numpy.ndarray, tuple, list]) -> numpy.ndarray:
        """统一转换输入为numpy数组（ARGB格式，alpha通道在前）"""
        if isinstance(color, numpy.ndarray):
            return ColorConverter._normalize_array(color)

        if isinstance(color, QColor):
            new_color = QColor(color)
            return numpy.array([
                new_color.alpha(),
                new_color.red(),
                new_color.green(),
                new_color.blue()
            ], dtype=numpy.int16)

        if isinstance(color, (tuple, list)):
            return ColorConverter._normalize_array(numpy.array(color))

        if isinstance(color, str):
            if not ColorConverter.isValid(color):
                raise ValueError(f"Invalid color string: {color}")
            code = color.lstrip('#')
            if len(code) == 6:  # RGB -> ARGB
                r, g, b = int(code[:2],16), int(code[2:4],16), int(code[4:6],16)
                return numpy.array([255, r, g, b], dtype=numpy.int16)
            else:  # ARGB
                a, r, g, b = int(code[:2],16), int(code[2:4],16), int(code[4:6],16), int(code[6:8],16)
                return numpy.array([a, r, g, b], dtype=numpy.int16)

        raise TypeError(f"Unsupported color type: {type(color)}")

    @staticmethod
    def _normalize_array(arr: numpy.ndarray) -> numpy.ndarray:
        """标准化数组为ARGB格式（4元素）"""
        if len(arr) == 3:  # RGB -> ARGB
            return numpy.array([255, arr[0], arr[1], arr[2]], dtype=numpy.int16)
        if len(arr) == 4:  # 确保是ARGB格式
            return arr.astype(numpy.int16)
        raise ValueError(f"Invalid color array length: {len(arr)}")

    @staticmethod
    def _to_output(
        arr: numpy.ndarray,
        output_type: Literal['str', 'qcolor'] = 'str'
    ) -> Union[str, QColor]:
        """转换numpy数组为指定输出类型"""
        if output_type == 'str':
            return f"#{arr[0]:02x}{arr[1]:02x}{arr[2]:02x}{arr[3]:02x}"
        elif output_type == 'qcolor':
            return QColor(arr[1], arr[2], arr[3], arr[0])
        raise ValueError(f"Unsupported output type: {output_type}")

    @classmethod
    def convert(
        cls,
        color: Union[str, QColor, numpy.ndarray, tuple, list],
        format: Literal['argb', 'rgb', 'rgba'] = 'argb',
        output_type: Literal['str', 'qcolor'] = 'str'
    ) -> Union[str, QColor]:
        """
        颜色格式转换主方法
        Args:
            color: 输入颜色
            format: 目标格式（argb/rgb/rgba）
            output_type: 输出类型
        """
        arr = cls._to_numpy(color)  # 内部统一为ARGB数组

        if format == 'rgb':
            # 移除alpha通道
            result = arr[1:4]
            return cls._to_output(numpy.array([255, *result]), output_type).replace('#ff', '#')
        elif format == 'rgba':
            # ARGB -> RGBA
            rgba = [arr[1], arr[2], arr[3], arr[0]]
            return cls._to_output(numpy.array([255, *rgba]), output_type).replace('#ff', '#')
        return cls._to_output(arr, output_type)

    @classmethod
    def adjust(
        cls,
        color: Union[str, QColor, numpy.ndarray, tuple, list],
        lightness: float = 0,
        saturation: float = 0,
        output_type: Literal['str', 'qcolor'] = 'str'
    ) -> Union[str, QColor]:
        """调整颜色亮度和饱和度"""
        arr = cls._to_numpy(color)
        rgb = arr[1:4] / 255.0

        # 转换为HSL
        mx, mn = max(rgb), min(rgb)
        df = mx - mn
        l = (mx + mn) / 2

        h = 0.0
        if df != 0:
            if mx == rgb[0]:
                h = (60 * ((rgb[1]-rgb[2])/df) + 360) % 360
            elif mx == rgb[1]:
                h = (60 * ((rgb[2]-rgb[0])/df) + 120) % 360
            else:
                h = (60 * ((rgb[0]-rgb[1])/df) + 240) % 360

        s = 0.0 if df == 0 else df / (1 - abs(2*l - 1))

        # 应用调整
        l = numpy.clip(l + lightness, 0, 1)
        s = numpy.clip(s + saturation, 0, 1)

        # HSL转RGB
        c = (1 - abs(2*l - 1)) * s
        x = c * (1 - abs((h/60) % 2 - 1))
        m = l - c/2

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

        new_rgb = numpy.array([(r+m)*255, (g+m)*255, (b+m)*255], dtype=numpy.int16)
        return cls._to_output(numpy.array([arr[0], *new_rgb]), output_type)

    @classmethod
    def mix(
        cls,
        color1: Union[str, QColor, numpy.ndarray, tuple, list],
        color2: Union[str, QColor, numpy.ndarray, tuple, list],
        weight: float = 0.5,
        output_type: Literal['str', 'qcolor'] = 'str'
    ) -> Union[str, QColor]:
        """混合两种颜色"""
        arr1 = cls._to_numpy(color1).astype(numpy.float32)
        arr2 = cls._to_numpy(color2).astype(numpy.float32)
        mixed = arr1 * weight + arr2 * (1 - weight)
        return cls._to_output(mixed.astype(numpy.int16), output_type)

    @classmethod
    def overlay(
        cls,
        base: Union[str, QColor, numpy.ndarray, tuple, list],
        overlay: Union[str, QColor, numpy.ndarray, tuple, list],
        output_type: Literal['str', 'qcolor'] = 'str'
    ) -> Union[str, QColor]:
        """叠加颜色"""
        base_arr = cls._to_numpy(base).astype(numpy.float32)
        over_arr = cls._to_numpy(overlay).astype(numpy.float32)

        # 计算alpha混合
        base_alpha = base_arr[0] / 255
        over_alpha = over_arr[0] / 255
        final_alpha = over_alpha + base_alpha * (1 - over_alpha)

        if final_alpha == 0:
            final_rgb = numpy.array([0, 0, 0])
        else:
            final_rgb = (over_arr[1:] * over_alpha +
                        base_arr[1:] * base_alpha * (1 - over_alpha)) / final_alpha

        result = numpy.array([final_alpha * 255, *final_rgb], dtype=numpy.int16)
        return cls._to_output(result, output_type)

    @classmethod
    def setAlpha(
        cls,
        color: Union[str, QColor, numpy.ndarray, tuple, list],
        alpha: Union[float, int],
        output_type: Literal['str', 'qcolor'] = 'str'
    ) -> Union[str, QColor]:
        """设置颜色透明度"""
        arr = cls._to_numpy(color)
        if isinstance(alpha, float):
            alpha = numpy.clip(alpha * 255, 0, 255)
        arr[0] = numpy.clip(alpha, 0, 255)
        return cls._to_output(arr, output_type)

    @staticmethod
    def isValid(color: str) -> bool:
        """验证颜色字符串格式"""
        return bool(re.match(r"^#([0-9a-fA-F]{8}|[0-9a-fA-F]{6})$", color))
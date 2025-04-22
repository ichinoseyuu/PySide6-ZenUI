from enum import Enum
from PySide6.QtGui import QFont
class Font(Enum):
    class Weight(Enum):
        """字体粗细"""
        light = QFont.Weight.Light
        Normal = QFont.Weight.Normal
        Medium = QFont.Weight.Medium
        DemiBold = QFont.Weight.DemiBold
        Bold = QFont.Weight.Bold


    class Family(Enum):
        """字体样式
        Attributes:
            yahei (str = 'Microsoft YaHei'): 微软雅黑
            youyuan (str = '幼圆'): 幼圆
            arial (str = 'Arial'): Arial
            simsun (str =  '宋体'): 宋体
        """
        yahei = 'Microsoft YaHei'
        youyuan = '幼圆'
        arial = 'Arial'
        simsun = '宋体'


    class Size(Enum):
        """字体大小
        Attributes:
            small (int = 9): 小号字体
            medium (int = 10): 中号字体
            large (int = 11): 大号字体
            huge (int = 12): 超大号字体
        """
        small = 9
        medium = 10
        large = 11
        huge = 12


    class TitleSize(Enum):
        """标题字体大小
        Attributes:
            small (int = 9): 小号字体
            medium (int = 10): 中号字体
            large (int = 11): 大号字体
            huge (int = 12): 超大号字体
        """
        small = 14
        medium = 20
        large = 24
        huge = 32

    class Style(Enum):
        """字体样式
        Attributes:
            Normal (QFont.Style.StyleNormal): 正常
            Italic (QFont.Style.StyleItalic): 斜体
            Oblique (QFont.Style.StyleOblique): 倾斜
        """
        Normal = QFont.Style.StyleNormal
        Italic = QFont.Style.StyleItalic
        Oblique = QFont.Style.StyleOblique
from enum import Enum
from PySide6.QtGui import QFont
class ZFont(QFont):
    class Family(Enum):
        """字体样式
        Attributes:
            yahei (str = 'Microsoft YaHei'): 微软雅黑
            youyuan (str = '幼圆'): 幼圆
            arial (str = 'Arial'): Arial
            simsun (str =  '宋体'): 宋体
        """
        YaHei = 'Microsoft YaHei'
        YouYuan = '幼圆'
        Arial = 'Arial'
        Simsun = '宋体'


    class Size(Enum):
        """字体大小"""
        Small = 9
        "小号字体:9"
        Medium = 10
        "中号字体:10"
        Large = 11
        "大号字体:11"
        Huge = 12
        "超大号字体:12"
        Title_Small = 14
        "标题小号字体:14"
        Title_Medium = 20
        "标题中号字体:20"
        Title_Large = 24
        "标题大号字体:24"
        Title_Huge = 32
        "标题超大号字体:32"
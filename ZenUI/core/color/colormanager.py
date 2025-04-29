from typing import Union, Optional, Dict, overload
import numpy
import re
import copy
from ZenUI.core.enumrates.zen import Zen
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
    """颜色配置管理类，继承这个类可以实现一套配置，每套配置独立且互不干扰"""
    def __init__(self):
        self.config: Dict[Zen.WidgetType, Dict[Zen.Theme, Dict[Zen.ColorRole, Optional[str]]]] = {
                widget: {theme: {} for theme in Zen.Theme}
                for widget in Zen.WidgetType
                }

    def setColor(self, widget_type: Zen.WidgetType, theme: Zen.Theme, role: Zen.ColorRole, color: Optional[str]):
        """为指定的控件类型的颜色对象设置颜色"""
        self.config[widget_type][theme][role] = color

    def setColors(self, widget_type: Zen.WidgetType, theme: Zen.Theme, dict: Dict[Zen.ColorRole, Optional[str]]):
        """为指定的控件类型的颜色对象设置颜色"""
        self.config[widget_type][theme] = dict

    def getColor(self, widget_type: Zen.WidgetType, theme: Zen.Theme, role: Zen.ColorRole) -> Optional[str]:
        """获取指定控件类型的颜色对象的颜色"""
        return self.config[widget_type][theme][role]

    def getColorDict(self, widget_type: Zen.WidgetType) -> Dict[Zen.Theme, Dict[Zen.ColorRole, Optional[str]]]:
        """获取指定控件类型的颜色字典"""
        return self.config[widget_type]


class ZenColorConfig(ColorConfig):
    '''ZenUi主题色彩配置管理'''
    def __init__(self):
        super().__init__()
        self.setColors(Zen.WidgetType.PushButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Background_A: '#63469f',
                        Zen.ColorRole.Background_B: '#955595',
                        Zen.ColorRole.Hover: '#10ffffff',
                        Zen.ColorRole.Flash: '#20ffffff',
                        Zen.ColorRole.Text: '#dcdcdc',
                        Zen.ColorRole.Icon: '#dcdcdc'})

        self.setColors(Zen.WidgetType.PushButton, Zen.Theme.Light,
                       {Zen.ColorRole.Background_A: '#8adee2',
                        Zen.ColorRole.Background_B: '#9bf3ff',
                        Zen.ColorRole.Hover: '#10000000',
                        Zen.ColorRole.Flash: '#20000000',
                        Zen.ColorRole.Text: '#1c191f',
                        Zen.ColorRole.Icon: '#1c191f'})

        self.setColors(Zen.WidgetType.TansButton, Zen.Theme.Dark,
                       {Zen.ColorRole.Hover: '#10ffffff',
                        Zen.ColorRole.Flash: '#20ffffff',
                        Zen.ColorRole.Text: '#dcdcdc',
                        Zen.ColorRole.Icon: '#dcdcdc'})

        self.setColors(Zen.WidgetType.TansButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: '#10000000',
                        Zen.ColorRole.Flash: '#20000000',
                        Zen.ColorRole.Text: '#2c2a2e',
                        Zen.ColorRole.Icon: '#8a8a8a'})

        self.setColors(Zen.WidgetType.TabButton, Zen.Theme.Dark,
                       {Zen.ColorRole.Hover: '#10ffffff',
                        Zen.ColorRole.Flash: '#20ffffff',
                        Zen.ColorRole.Text: '#ffb4b4b4',
                        Zen.ColorRole.Icon: '#ffb4b4b4',
                        Zen.ColorRole.Selected: '#ff8a5a9f'})

        self.setColors(Zen.WidgetType.TabButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: '#15000000',
                        Zen.ColorRole.Flash: '#25000000',
                        Zen.ColorRole.Text: '#ff545256',
                        Zen.ColorRole.Icon: '#ffbfbfbf',
                        Zen.ColorRole.Selected: '#ff22a7f2'})

        self.setColors(Zen.WidgetType.TextLabel, Zen.Theme.Dark,
                       {Zen.ColorRole.Text: '#ffffff'})

        self.setColors(Zen.WidgetType.TextLabel, Zen.Theme.Light,
                       {Zen.ColorRole.Text: '#000000'})

        self.setColors(Zen.WidgetType.Container, Zen.Theme.Dark,
                       {Zen.ColorRole.Background_A: '#231f26',
                        Zen.ColorRole.Background_B: '#231f26',
                        Zen.ColorRole.Border: '#4e4e4e'})

        self.setColors(Zen.WidgetType.Container, Zen.Theme.Light,
                       {Zen.ColorRole.Background_A: '#fafafa',
                        Zen.ColorRole.Background_B: '#fafafa',
                        Zen.ColorRole.Border: '#9f9f9f'})

        self.setColors(Zen.WidgetType.CollapsibleContainer, Zen.Theme.Dark,
                       {Zen.ColorRole.Background_A: '#201c23',
                        Zen.ColorRole.Background_B: '#201c23',
                        Zen.ColorRole.Border: '#4e4e4e'})

        self.setColors(Zen.WidgetType.CollapsibleContainer, Zen.Theme.Light,
                       {Zen.ColorRole.Background_A: '#ededed',
                        Zen.ColorRole.Background_B: '#dedede',
                        Zen.ColorRole.Border: '#9f9f9f'})

        self.setColors(Zen.WidgetType.Titlebar, Zen.Theme.Dark,
                       {Zen.ColorRole.Background_A: '#1c191f',
                        Zen.ColorRole.Border: '#161616'})

        self.setColors(Zen.WidgetType.Titlebar, Zen.Theme.Light,
                       {Zen.ColorRole.Background_A: '#ffffff',
                        Zen.ColorRole.Border: '#e6e6e6'})

        self.setColors(Zen.WidgetType.ToolTip, Zen.Theme.Dark,
                       {Zen.ColorRole.Background_A: '#1c191f',
                        Zen.ColorRole.Flash: '#7fffffff'})

        self.setColors(Zen.WidgetType.ToolTip, Zen.Theme.Light,
                       {Zen.ColorRole.Background_A: '#ffffff',
                        Zen.ColorRole.Flash: '#7f999999'})

class ColorSheet:
    """每个控件的自己的颜色表，同类型控件之间独立，需要从`ColorConfig`中获取相应的颜色表"""
    def __init__(self, parent, widget_type: Zen.WidgetType):
        from ZenUI.core.globals.globals import ZenGlobal
        self.ui_global = ZenGlobal.ui
        self.parent = parent
        self.widget_type = widget_type
        self._copyColorSheet()


    def _copyColorSheet(self):
        self.sheet = copy.deepcopy(self.ui_global.color_config.getColorDict(self.widget_type))

    @overload
    def getColor(self, role: Zen.ColorRole) -> Optional[str]:
        """获取当前主题下颜色对象的颜色"""
        pass

    @overload
    def getColor(self, theme: Zen.Theme, role: Zen.ColorRole) -> Optional[str]:
        """获取指定主题下颜色对象的颜色"""
        pass

    def getColor(self, *args) -> Optional[str]:
        """根据传入的参数获取颜色"""
        if len(args) == 1:
            # 获取当前主题下颜色
            role = args[0]
            return self.sheet[self.ui_global.theme_manager.theme()][role]
        elif len(args) == 2:
            # 获取指定主题下颜色
            theme, role = args
            return self.sheet[theme][role]
        else:
            raise ValueError("Invalid number of arguments. Must be 1 or 2.")

    @overload
    def setColor(self, role: Zen.ColorRole, color: Optional[str]) -> None:
        """设置当前主题下颜色对象的颜色"""
        pass

    @overload
    def setColor(self, theme: Zen.Theme, role: Zen.ColorRole, color: Optional[str]) -> None:
        """设置指定主题下颜色对象的颜色"""
        pass

    def setColor(self, *args) -> None:
        """根据传入的参数设置颜色"""
        if len(args) == 2:
            # 设置当前主题下颜色
            role, color = args
            theme = self.ui_global.theme_manager.theme()
            self.sheet[theme][role] = color
            self.parent._theme_changed_handler(theme)
        elif len(args) == 3:
            # 设置指定主题下颜色
            theme, role, color = args
            self.sheet[theme][role] = color
            if theme == self.ui_global.theme_manager.theme():
                self.parent._theme_changed_handler(theme)
        else:
            raise ValueError("Invalid number of arguments. Must be 2 or 3.")
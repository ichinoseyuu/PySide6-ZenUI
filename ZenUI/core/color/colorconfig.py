from typing import Optional, Dict
from ZenUI.core.metaclass.metaclass import NoInstanceClass
from ZenUI.core.enumrates.zen import Zen
from ZenUI.core.color.colortool import ZColorTool
class ZAccentColor(NoInstanceClass):
    # Dark theme colors
    DARK_ACCENT_A = '#ff63469f'
    DARK_ACCENT_B = '#ff955595'
    DARK_BORDER = '#ff1d1d1d'
    DARK_TEXT = '#ffdcdcdc'
    DARK_ICON = '#ffdcdcdc'
    DARK_LAYER = '#10ffffff'
    DARK_SELECTED = ZColorTool.mix(DARK_ACCENT_B, DARK_ACCENT_A,0.6)

    # Light theme colors
    LIGHT_ACCENT_A = '#ffa5d2f1'
    LIGHT_ACCENT_B = '#ffd0e8f2'
    LIGHT_BORDER = '#ffe5e5e5'
    LIGHT_BORDER_HOVER = ZColorTool.adjust(LIGHT_ACCENT_A,0,-0.1)
    LIGHT_BORDER_PRESSED = ZColorTool.adjust(LIGHT_ACCENT_B,0,-0.1)
    LIGHT_TEXT = '#ff313131'
    LIGHT_TEXT_HOVER = ZColorTool.adjust(LIGHT_ACCENT_A,-0.1,-0.1)
    LIGHT_TEXT_PRESSED = ZColorTool.adjust(LIGHT_ACCENT_B,-0.1,-0.1)
    LIGHT_ICON = '#ff565656'
    LIGHT_ICON_HOVER = ZColorTool.adjust(LIGHT_ACCENT_A,-0.1,-0.1)
    LIGHT_ICON_PRESSED = ZColorTool.adjust(LIGHT_ACCENT_B,-0.1,-0.1)
    LIGHT_LAYER = '#10000000'
    LIGHT_SELECTED = ZColorTool.mix(LIGHT_ACCENT_B, LIGHT_ACCENT_A,0.1)



class ZColorConfig:
    """
    颜色配置管理类
    - 继承这个类可以实现一套配置
    - 每套配置独立且互不干扰
    """
    def __init__(self):
        self.config: Dict[Zen.WidgetType, Dict[Zen.Theme, Dict[Zen.ColorRole, Optional[str]]]] = {
                widget: {theme: {} for theme in Zen.Theme}
                for widget in Zen.WidgetType
                }

    def setColor(self, widget_type: Zen.WidgetType, theme: Zen.Theme, role: Zen.ColorRole, color: Optional[str]):
        '设置指定控件的颜色对象的颜色'
        self.config[widget_type][theme][role] = color

    def setConfig(self, widget_type: Zen.WidgetType, theme: Zen.Theme, dict: Dict[Zen.ColorRole, Optional[str]]):
        '设置指定控件某个主题的所有颜色'
        self.config[widget_type][theme] = dict

    def getColor(self, widget_type: Zen.WidgetType, theme: Zen.Theme, role: Zen.ColorRole) -> Optional[str]:
        '获取指定控件的颜色对象的颜色'
        return self.config[widget_type][theme][role]

    def getConfig(self, widget_type: Zen.WidgetType) -> Dict[Zen.Theme, Dict[Zen.ColorRole, Optional[str]]]:
        '获取指定控件某个主题的所有颜色'
        return self.config[widget_type]


class ZThemeColorConfig(ZColorConfig):
    '''主题色彩配置管理'''
    def __init__(self):
        super().__init__()
        self.setConfig(Zen.WidgetType.PushButton, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.Hover: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Flash: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Border: ZAccentColor.DARK_BORDER,
                        Zen.ColorRole.BorderHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.BorderPressed: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.IconHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.IconPressed: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        Zen.ColorRole.TextHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.TextPressed: ZAccentColor.DARK_ACCENT_A
                        })

        self.setConfig(Zen.WidgetType.PushButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ZAccentColor.LIGHT_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ZAccentColor.LIGHT_ACCENT_B,
                        Zen.ColorRole.Hover: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Flash: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Border: ZAccentColor.LIGHT_BORDER,
                        Zen.ColorRole.BorderHover: ZAccentColor.LIGHT_BORDER_HOVER,
                        Zen.ColorRole.BorderPressed: ZAccentColor.LIGHT_BORDER_PRESSED,
                        Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.IconHover: ZAccentColor.LIGHT_ICON_HOVER,
                        Zen.ColorRole.IconPressed: ZAccentColor.LIGHT_ICON_PRESSED,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        Zen.ColorRole.TextHover: ZAccentColor.LIGHT_TEXT_HOVER,
                        Zen.ColorRole.TextPressed: ZAccentColor.LIGHT_TEXT_PRESSED,
                        })

        self.setConfig(Zen.WidgetType.FillButton, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ZColorTool.mix(ZAccentColor.DARK_ACCENT_A, ZAccentColor.DARK_ACCENT_B),
                        Zen.ColorRole.Hover: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Border: ZAccentColor.DARK_BORDER,
                        Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        })

        self.setConfig(Zen.WidgetType.FillButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ZColorTool.mix(ZAccentColor.LIGHT_ACCENT_A, ZAccentColor.LIGHT_ACCENT_B),
                        Zen.ColorRole.Hover: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Border: ZAccentColor.LIGHT_BORDER,
                        Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        })
        print(ZColorTool.mix(ZAccentColor.LIGHT_ACCENT_A, ZAccentColor.LIGHT_ACCENT_B))
        self.setConfig(Zen.WidgetType.GradientButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.BackgroundA: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.Hover: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GradientButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ZAccentColor.LIGHT_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ZAccentColor.LIGHT_ACCENT_B,
                        Zen.ColorRole.Hover: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GhostButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Flash: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.BorderHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GhostButton, Zen.Theme.Light,
                       {Zen.ColorRole.Flash: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.BorderHover: ZAccentColor.LIGHT_BORDER_HOVER,
                        Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        })


        self.setConfig(Zen.WidgetType.TransparentButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Hover: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        })

        self.setConfig(Zen.WidgetType.TransparentButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        })

        self.setConfig(Zen.WidgetType.NoBackgroundButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.IconHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.IconPressed: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        Zen.ColorRole.TextHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.TextPressed: ZAccentColor.DARK_ACCENT_A,
                        })

        self.setConfig(Zen.WidgetType.NoBackgroundButton, Zen.Theme.Light,
                       {Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.IconHover: ZAccentColor.LIGHT_ICON_HOVER,
                        Zen.ColorRole.IconPressed: ZAccentColor.LIGHT_ICON_PRESSED,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        Zen.ColorRole.TextHover: ZAccentColor.LIGHT_TEXT_HOVER,
                        Zen.ColorRole.TextPressed: ZAccentColor.LIGHT_TEXT_PRESSED,
                        })

        self.setConfig(Zen.WidgetType.ToggleButton, Zen.Theme.Dark,
                       {Zen.ColorRole.Hover: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Flash: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.SelectedA: ZAccentColor.DARK_LAYER,
                        Zen.ColorRole.Border: ZAccentColor.DARK_BORDER,
                        Zen.ColorRole.BorderHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.BorderPressed: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.BorderSelected: ZAccentColor.DARK_SELECTED,
                        Zen.ColorRole.Icon: ZAccentColor.DARK_ICON,
                        Zen.ColorRole.IconHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.IconPressed: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.IconSelected: ZAccentColor.DARK_SELECTED,
                        Zen.ColorRole.Text: ZAccentColor.DARK_TEXT,
                        Zen.ColorRole.TextHover: ZAccentColor.DARK_ACCENT_B,
                        Zen.ColorRole.TextPressed: ZAccentColor.DARK_ACCENT_A,
                        Zen.ColorRole.TextSelected: ZAccentColor.DARK_SELECTED,
                        Zen.ColorRole.IndicatorSelected: ZAccentColor.DARK_SELECTED
                        })

        self.setConfig(Zen.WidgetType.ToggleButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Pressed: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Flash: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.SelectedA: ZAccentColor.LIGHT_LAYER,
                        Zen.ColorRole.Border: ZAccentColor.LIGHT_BORDER,
                        Zen.ColorRole.BorderHover: ZAccentColor.LIGHT_BORDER_HOVER,
                        Zen.ColorRole.BorderPressed: ZAccentColor.LIGHT_BORDER_PRESSED,
                        Zen.ColorRole.BorderSelected: ZAccentColor.LIGHT_SELECTED,
                        Zen.ColorRole.Icon: ZAccentColor.LIGHT_ICON,
                        Zen.ColorRole.IconHover: ZAccentColor.LIGHT_ICON_HOVER,
                        Zen.ColorRole.IconPressed: ZAccentColor.LIGHT_ICON_PRESSED,
                        Zen.ColorRole.IconSelected: ZAccentColor.LIGHT_SELECTED,
                        Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT,
                        Zen.ColorRole.TextHover: ZAccentColor.LIGHT_TEXT_HOVER,
                        Zen.ColorRole.TextPressed: ZAccentColor.LIGHT_TEXT_PRESSED,
                        Zen.ColorRole.TextSelected: ZAccentColor.LIGHT_SELECTED,
                        Zen.ColorRole.IndicatorSelected: ZAccentColor.LIGHT_SELECTED
                        })

        self.setConfig(Zen.WidgetType.TextLabel, Zen.Theme.Dark,
                       {Zen.ColorRole.Text: ZAccentColor.DARK_TEXT})

        self.setConfig(Zen.WidgetType.TextLabel, Zen.Theme.Light,
                       {Zen.ColorRole.Text: ZAccentColor.LIGHT_TEXT})

        self.setConfig(Zen.WidgetType.Box, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: '#ff202020',
                        Zen.ColorRole.BackgroundB: '#ff202020',
                        Zen.ColorRole.Border: '#ff1d1d1d'
                        })

        self.setConfig(Zen.WidgetType.Box, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#fff3f3f3',
                        Zen.ColorRole.BackgroundB: '#fff3f3f3',
                        Zen.ColorRole.Border: '#ffe5e5e5'
                        })

        self.setConfig(Zen.WidgetType.Drawer, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: '#ff202020',
                        Zen.ColorRole.BackgroundB: '#ff202020',
                        Zen.ColorRole.Border: '#ff4e4e4e'
                        })

        self.setConfig(Zen.WidgetType.Drawer, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#fff3f3f3',
                        Zen.ColorRole.BackgroundB: '#fff3f3f3',
                        Zen.ColorRole.Border: '#ff9f9f9f'
                        })

        self.setConfig(Zen.WidgetType.StackPage, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: '#ff272727',
                        Zen.ColorRole.BackgroundB: '#ff272727',
                        Zen.ColorRole.Border: '#ff1d1d1d'
                        })

        self.setConfig(Zen.WidgetType.StackPage, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#fff9f9f9',
                        Zen.ColorRole.BackgroundB: '#fff9f9f9',
                        Zen.ColorRole.Border: '#ffe5e5e5'
                        })

        self.setConfig(Zen.WidgetType.Titlebar, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: '#ff202020',
                        Zen.ColorRole.Border: '#00161616'
                        })

        self.setConfig(Zen.WidgetType.Titlebar, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#fff3f3f3',
                        Zen.ColorRole.Border: '#00e6e6e6'
                        })

        self.setConfig(Zen.WidgetType.ToolTip, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: '#ff202020',
                        Zen.ColorRole.Border: '#ff1d1d1d',
                        Zen.ColorRole.Flash: '#7fffffff'
                        })

        self.setConfig(Zen.WidgetType.ToolTip, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#fff3f3f3',
                        Zen.ColorRole.Border: '#ffe5e5e5',
                        Zen.ColorRole.Flash: '#7f999999'
                        })

        self.setConfig(Zen.WidgetType.Window, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: '#ff202020',
                        Zen.ColorRole.BackgroundB: '#ff202020',
                        Zen.ColorRole.Border: '#ff1d1d1d'
                        })

        self.setConfig(Zen.WidgetType.Window, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#fff3f3f3',
                        Zen.ColorRole.BackgroundB: '#fff3f3f3',
                        Zen.ColorRole.Border: '#ffe5e5e5'
                        })
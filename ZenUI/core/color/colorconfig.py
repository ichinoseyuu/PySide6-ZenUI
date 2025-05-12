from typing import Optional, Dict
from ZenUI.core.enumrates.zen import Zen

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
                       {Zen.ColorRole.BackgroundA: '#ff63469f',
                        Zen.ColorRole.BackgroundB: '#ff955595',
                        Zen.ColorRole.Hover: '#10ffffff',
                        Zen.ColorRole.Pressed: '#10ffffff',
                        Zen.ColorRole.Flash: '#20ffffff',
                        Zen.ColorRole.Border: '#ff63469f',
                        Zen.ColorRole.BorderHover: '#ff955595',
                        Zen.ColorRole.BorderPressed: '#ff804f99',
                        Zen.ColorRole.Icon: '#ffdcdcdc',
                        Zen.ColorRole.IconHover: '#ff955595',
                        Zen.ColorRole.IconPressed: '#ff804f99',
                        Zen.ColorRole.Text: '#ffdcdcdc',
                        Zen.ColorRole.TextHover: '#ff955595',
                        Zen.ColorRole.TextPressed: '#ff804f99'
                        })

        self.setConfig(Zen.WidgetType.PushButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: '#ff8adee2',
                        Zen.ColorRole.BackgroundB: '#ff9bf3ff',
                        Zen.ColorRole.Hover: '#10000000',
                        Zen.ColorRole.Pressed: '#10ffffff',
                        Zen.ColorRole.Flash: '#20000000',
                        Zen.ColorRole.Border: '#ff8adee2',
                        Zen.ColorRole.BorderHover: '#ff9bf3ff',
                        Zen.ColorRole.BorderPressed: '#ff8adee2',
                        Zen.ColorRole.Icon: '#ff565656',
                        Zen.ColorRole.IconHover: '#ff82d1d6',
                        Zen.ColorRole.IconPressed: '#ff82d1d6',
                        Zen.ColorRole.Text: '#ff313131',
                        Zen.ColorRole.TextHover: '#ff9bf3ff',
                        Zen.ColorRole.TextPressed: '#ff8adee2',
                        })

        self.setConfig(Zen.WidgetType.ToggleButton, Zen.Theme.Dark,
                       {Zen.ColorRole.Hover: '#10ffffff',
                        Zen.ColorRole.Pressed: '#10ffffff',
                        Zen.ColorRole.Flash: '#20ffffff',
                        Zen.ColorRole.SelectedA: '#10ffffff',
                        Zen.ColorRole.Border: '#ff63469f',
                        Zen.ColorRole.BorderHover: '#ff005595',
                        Zen.ColorRole.BorderPressed: '#ff800099',
                        Zen.ColorRole.BorderSelected: '#ff7f5700',
                        Zen.ColorRole.Icon: '#ffdcdcdc',
                        Zen.ColorRole.IconHover: '#ff955595',
                        Zen.ColorRole.IconPressed: '#ff804f99',
                        Zen.ColorRole.IconSelected: '#ff7f57a1',
                        Zen.ColorRole.Text: '#ffdcdcdc',
                        Zen.ColorRole.TextHover: '#ff955595',
                        Zen.ColorRole.TextPressed: '#ff804f99',
                        Zen.ColorRole.TextSelected: '#ff7f57a1',
                        Zen.ColorRole.IndicatorSelected: '#ff7f57a1'
                        })

        self.setConfig(Zen.WidgetType.ToggleButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: '#10000000',
                        Zen.ColorRole.Pressed: '#10ffffff',
                        Zen.ColorRole.Flash: '#20000000',
                        Zen.ColorRole.SelectedA: '#10000000',
                        Zen.ColorRole.Border: '#ff8adee2',
                        Zen.ColorRole.BorderHover: '#ff8adee2',
                        Zen.ColorRole.BorderPressed: '#ff8adee2',
                        Zen.ColorRole.BorderSelected: '#ff8adee2',
                        Zen.ColorRole.Icon: '#ff565656',
                        Zen.ColorRole.IconHover: '#ff82d1d6',
                        Zen.ColorRole.IconPressed: '#ff82d1d6',
                        Zen.ColorRole.IconSelected: '#ff82d1d6',
                        Zen.ColorRole.Text: '#ff313131',
                        Zen.ColorRole.TextHover: '#ff82d1d6',
                        Zen.ColorRole.TextPressed: '#ff82d1d6',
                        Zen.ColorRole.TextSelected: '#ff82d1d6',
                        Zen.ColorRole.IndicatorSelected: '#ff82d1d6'
                        })

        self.setConfig(Zen.WidgetType.TextLabel, Zen.Theme.Dark,
                       {Zen.ColorRole.Text: '#ffdcdcdc'})

        self.setConfig(Zen.WidgetType.TextLabel, Zen.Theme.Light,
                       {Zen.ColorRole.Text: '#ff313131'})

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
from typing import Optional, Dict
from ZenUI.core.metaclass import NoInstanceClass
from ZenUI.core.enumrates import Zen
from ZenUI.core.color.colortool import ZColorTool

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

    def outline(self):
        '输出所有配置'
        for widget_type in self.config:
            for theme in self.config[widget_type]:
                for role in self.config[widget_type][theme]:
                    print(f'[{widget_type.name}]:[{theme.name}]:[{role.name}]:[{self.config[widget_type][theme][role]}]')
        #保存到.json文件
        import json
        with open('colorconfig.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        print('保存成功')

class ColorPresets(NoInstanceClass):
    # VAR NAME FORMET: [Theme]_[WidgetType]_[Color]
    # Dark theme colors
    DARK_BTN_ACCENT_A = '#ff63469f'
    DARK_BTN_ACCENT_B = '#ff955595'
    DARK_BTN_BORDER = '#ff1d1d1d'
    DARK_BTN_TEXT = '#ffdcdcdc'
    DARK_BTN_ICON = '#ffdcdcdc'
    DARK_BTN_LAYER = '#10ffffff'
    DARK_BTN_SELECTED = ZColorTool.mix(DARK_BTN_ACCENT_B, DARK_BTN_ACCENT_A,0.6)

    DARK_BOX_BG_A = '#ff202020'
    DARK_BOX_BG_B = '#ff202020'
    DARK_BOX_BORDER = '#ff1d1d1d'

    DARK_DRAWER_BG_A = '#ff202020'
    DARK_DRAWER_BG_B = '#ff202020'
    DARK_DRAWER_BORDER = '#ff1d1d1d'

    DARK_STACKPAGE_BG_A = '#ff272727'
    DARK_STACKPAGE_BG_B = '#ff272727'
    DARK_STACKPAGE_BORDER = '#ff1d1d1d'

    DARK_TITLEBAR_BG = '#ff202020'
    DARK_TITLEBAR_BORDER = '#00161616'

    DARK_TOOLTIP_BG = '#ff313131'
    DARK_TOOLTIP_BORDER = '#ff1d1d1d'
    DARK_TOOLTIP_FLASH = '#7fffffff'

    DARK_WINDOW_BG_A = '#ff202020'
    DARK_WINDOW_BG_B = '#ff202020'
    DARK_WINDOW_BORDER = '#ff1d1d1d'

    # Light theme colors
    LIGHT_BTN_ACCENT_A = '#ffa5d2f1'
    LIGHT_BTN_ACCENT_B = '#ffd0e8f2'
    LIGHT_BTN_BORDER = '#ffe5e5e5'
    LIGHT_BTN_BORDER_HOVER = ZColorTool.adjust(LIGHT_BTN_ACCENT_A,0,-0.1)
    LIGHT_BTN_BORDER_PRESSED = ZColorTool.adjust(LIGHT_BTN_ACCENT_B,0,-0.1)
    LIGHT_BTN_TEXT = '#ff313131'
    LIGHT_BTN_TEXT_HOVER = ZColorTool.adjust(LIGHT_BTN_ACCENT_A,-0.1,-0.1)
    LIGHT_BTN_TEXT_PRESSED = ZColorTool.adjust(LIGHT_BTN_ACCENT_B,-0.1,-0.1)
    LIGHT_BTN_ICON = '#ff565656'
    LIGHT_BTN_ICON_HOVER = ZColorTool.adjust(LIGHT_BTN_ACCENT_A,-0.1,-0.1)
    LIGHT_BTN_ICON_PRESSED = ZColorTool.adjust(LIGHT_BTN_ACCENT_B,-0.1,-0.1)
    LIGHT_BTN_LAYER = '#10000000'
    LIGHT_BTN_SELECTED = ZColorTool.mix(LIGHT_BTN_ACCENT_B, LIGHT_BTN_ACCENT_A,0.1)

    LIGHT_BOX_BG_A = '#fff3f3f3'
    LIGHT_BOX_BG_B = '#fff3f3f3'
    LIGHT_BOX_BORDER = '#ffe5e5e5'

    LIGHT_DRAWER_BG_A = '#fff3f3f3'
    LIGHT_DRAWER_BG_B = '#fff3f3f3'
    LIGHT_DRAWER_BORDER = '#ffe5e5e5'

    LIGHT_STACKPAGE_BG_A = '#fff9f9f9'
    LIGHT_STACKPAGE_BG_B = '#fff9f9f9'
    LIGHT_STACKPAGE_BORDER = '#ffe5e5e5'

    LIGHT_TITLEBAR_BG = '#fff3f3f3'
    LIGHT_TITLEBAR_BORDER = '#00e6e6e6'

    LIGHT_TOOLTIP_BG = '#fff3f3f3'
    LIGHT_TOOLTIP_BORDER = '#ffe5e5e5'
    LIGHT_TOOLTIP_FLASH = '#7f999999'

    LIGHT_WINDOW_BG_A = '#fff3f3f3'
    LIGHT_WINDOW_BG_B = '#fff3f3f3'
    LIGHT_WINDOW_BORDER = '#ffe5e5e5'

class ZThemeColorConfig(ZColorConfig):
    '''主题色彩配置管理'''
    def __init__(self):
        super().__init__()
        self.setConfig(Zen.WidgetType.PushButton, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.Hover: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Flash: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Border: ColorPresets.DARK_BTN_BORDER,
                        Zen.ColorRole.BorderHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.BorderPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.IconHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.IconPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        Zen.ColorRole.TextHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.TextPressed: ColorPresets.DARK_BTN_ACCENT_A
                        })

        self.setConfig(Zen.WidgetType.PushButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_BTN_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.LIGHT_BTN_ACCENT_B,
                        Zen.ColorRole.Hover: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Flash: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_BTN_BORDER,
                        Zen.ColorRole.BorderHover: ColorPresets.LIGHT_BTN_BORDER_HOVER,
                        Zen.ColorRole.BorderPressed: ColorPresets.LIGHT_BTN_BORDER_PRESSED,
                        Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.IconHover: ColorPresets.LIGHT_BTN_ICON_HOVER,
                        Zen.ColorRole.IconPressed: ColorPresets.LIGHT_BTN_ICON_PRESSED,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        Zen.ColorRole.TextHover: ColorPresets.LIGHT_BTN_TEXT_HOVER,
                        Zen.ColorRole.TextPressed: ColorPresets.LIGHT_BTN_TEXT_PRESSED,
                        })

        self.setConfig(Zen.WidgetType.FillButton, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ZColorTool.mix(ColorPresets.DARK_BTN_ACCENT_A, ColorPresets.DARK_BTN_ACCENT_B),
                        Zen.ColorRole.Hover: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Border: ColorPresets.DARK_BTN_BORDER,
                        Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.FillButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ZColorTool.mix(ColorPresets.LIGHT_BTN_ACCENT_A, ColorPresets.LIGHT_BTN_ACCENT_B),
                        Zen.ColorRole.Hover: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_BTN_BORDER,
                        Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GradientButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.Hover: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GradientButton, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_BTN_ACCENT_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.LIGHT_BTN_ACCENT_B,
                        Zen.ColorRole.Hover: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GhostButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Flash: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.BorderHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.GhostButton, Zen.Theme.Light,
                       {Zen.ColorRole.Flash: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.BorderHover: ColorPresets.LIGHT_BTN_BORDER_HOVER,
                        Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        })


        self.setConfig(Zen.WidgetType.TransparentButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Hover: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.TransparentButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        })

        self.setConfig(Zen.WidgetType.NoBackgroundButton, Zen.Theme.Dark, 
                       {Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.IconHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.IconPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        Zen.ColorRole.TextHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.TextPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        })

        self.setConfig(Zen.WidgetType.NoBackgroundButton, Zen.Theme.Light,
                       {Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.IconHover: ColorPresets.LIGHT_BTN_ICON_HOVER,
                        Zen.ColorRole.IconPressed: ColorPresets.LIGHT_BTN_ICON_PRESSED,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        Zen.ColorRole.TextHover: ColorPresets.LIGHT_BTN_TEXT_HOVER,
                        Zen.ColorRole.TextPressed: ColorPresets.LIGHT_BTN_TEXT_PRESSED,
                        })

        self.setConfig(Zen.WidgetType.ToggleButton, Zen.Theme.Dark,
                       {Zen.ColorRole.Hover: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Flash: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.SelectedA: ColorPresets.DARK_BTN_LAYER,
                        Zen.ColorRole.Border: ColorPresets.DARK_BTN_BORDER,
                        Zen.ColorRole.BorderHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.BorderPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.BorderSelected: ColorPresets.DARK_BTN_SELECTED,
                        Zen.ColorRole.Icon: ColorPresets.DARK_BTN_ICON,
                        Zen.ColorRole.IconHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.IconPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.IconSelected: ColorPresets.DARK_BTN_SELECTED,
                        Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT,
                        Zen.ColorRole.TextHover: ColorPresets.DARK_BTN_ACCENT_B,
                        Zen.ColorRole.TextPressed: ColorPresets.DARK_BTN_ACCENT_A,
                        Zen.ColorRole.TextSelected: ColorPresets.DARK_BTN_SELECTED,
                        Zen.ColorRole.IndicatorSelected: ColorPresets.DARK_BTN_SELECTED
                        })

        self.setConfig(Zen.WidgetType.ToggleButton, Zen.Theme.Light,
                       {Zen.ColorRole.Hover: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Pressed: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Flash: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.SelectedA: ColorPresets.LIGHT_BTN_LAYER,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_BTN_BORDER,
                        Zen.ColorRole.BorderHover: ColorPresets.LIGHT_BTN_BORDER_HOVER,
                        Zen.ColorRole.BorderPressed: ColorPresets.LIGHT_BTN_BORDER_PRESSED,
                        Zen.ColorRole.BorderSelected: ColorPresets.LIGHT_BTN_SELECTED,
                        Zen.ColorRole.Icon: ColorPresets.LIGHT_BTN_ICON,
                        Zen.ColorRole.IconHover: ColorPresets.LIGHT_BTN_ICON_HOVER,
                        Zen.ColorRole.IconPressed: ColorPresets.LIGHT_BTN_ICON_PRESSED,
                        Zen.ColorRole.IconSelected: ColorPresets.LIGHT_BTN_SELECTED,
                        Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT,
                        Zen.ColorRole.TextHover: ColorPresets.LIGHT_BTN_TEXT_HOVER,
                        Zen.ColorRole.TextPressed: ColorPresets.LIGHT_BTN_TEXT_PRESSED,
                        Zen.ColorRole.TextSelected: ColorPresets.LIGHT_BTN_SELECTED,
                        Zen.ColorRole.IndicatorSelected: ColorPresets.LIGHT_BTN_SELECTED
                        })

        self.setConfig(Zen.WidgetType.TextLabel, Zen.Theme.Dark,
                       {Zen.ColorRole.Text: ColorPresets.DARK_BTN_TEXT})

        self.setConfig(Zen.WidgetType.TextLabel, Zen.Theme.Light,
                       {Zen.ColorRole.Text: ColorPresets.LIGHT_BTN_TEXT})

        self.setConfig(Zen.WidgetType.Box, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_BOX_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.DARK_BOX_BG_B,
                        Zen.ColorRole.Border: ColorPresets.DARK_BOX_BORDER
                        })

        self.setConfig(Zen.WidgetType.Box, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_BOX_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.LIGHT_BOX_BG_B,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_BOX_BORDER
                        })

        self.setConfig(Zen.WidgetType.Drawer, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_DRAWER_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.DARK_DRAWER_BG_B,
                        Zen.ColorRole.Border: ColorPresets.DARK_DRAWER_BORDER
                        })

        self.setConfig(Zen.WidgetType.Drawer, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_DRAWER_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.LIGHT_DRAWER_BG_B,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_DRAWER_BORDER
                        })

        self.setConfig(Zen.WidgetType.StackPage, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_STACKPAGE_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.DARK_STACKPAGE_BG_B,
                        Zen.ColorRole.Border: ColorPresets.DARK_STACKPAGE_BORDER
                        })

        self.setConfig(Zen.WidgetType.StackPage, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_STACKPAGE_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.LIGHT_STACKPAGE_BG_B,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_STACKPAGE_BORDER
                        })

        self.setConfig(Zen.WidgetType.Titlebar, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_TITLEBAR_BG,
                        Zen.ColorRole.Border: ColorPresets.DARK_TITLEBAR_BORDER
                        })

        self.setConfig(Zen.WidgetType.Titlebar, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_TITLEBAR_BG,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_TITLEBAR_BORDER
                        })

        self.setConfig(Zen.WidgetType.ToolTip, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_TOOLTIP_BG,
                        Zen.ColorRole.Border: ColorPresets.DARK_TOOLTIP_BORDER,
                        Zen.ColorRole.Flash: ColorPresets.DARK_TOOLTIP_FLASH
                        })

        self.setConfig(Zen.WidgetType.ToolTip, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_TOOLTIP_BG,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_TOOLTIP_BORDER,
                        Zen.ColorRole.Flash: ColorPresets.LIGHT_TOOLTIP_FLASH
                        })

        self.setConfig(Zen.WidgetType.Window, Zen.Theme.Dark,
                       {Zen.ColorRole.BackgroundA: ColorPresets.DARK_WINDOW_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.DARK_WINDOW_BG_B,
                        Zen.ColorRole.Border: ColorPresets.DARK_WINDOW_BORDER
                        })

        self.setConfig(Zen.WidgetType.Window, Zen.Theme.Light,
                       {Zen.ColorRole.BackgroundA: ColorPresets.LIGHT_WINDOW_BG_A,
                        Zen.ColorRole.BackgroundB: ColorPresets.LIGHT_WINDOW_BG_B,
                        Zen.ColorRole.Border: ColorPresets.LIGHT_WINDOW_BORDER
                        })
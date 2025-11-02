from enum import Enum
from dataclasses import dataclass,fields,is_dataclass
import logging
from typing import TypeVar,Dict,Union, cast
from PySide6.QtGui import QColor
from ZenWidgets.core import SingletonMeta,NonInstantiableMeta,ColorConverter
from ZenWidgets.gui.theme import ZThemeManager

__All__ = [
    'ZPaletteKey',
    'ZStyleDataKey',
    'ZPalette',
    'ZStyleDataManager',
    'ZButtonStyleData',
    'ZFramelessWindowStyleData',
    'ZHeadLineStyleData',
    'ZToolTipStyleData',
    'ZToggleButtonStyleData',
    'ZNavBarButtonStyleData',
    'ZNavBarToggleButtonStyleData',
    'ZScrollPanelStyleData',
    'ZSliderStyleData',
    'ZLineEditStyleData',
    'ZLoginEditStyleData',
    'ZNumberEditStyleData',
    'ZPanelStyleData',
    'ZSwitchStyleData',
    'ZNavigationBarStyleData',
    'ZComboBoxStyleData',
    'ZItemStyleData',
    'ZItemViewStyleData'
]

# region ZPaletteKey
class ZPaletteKey(Enum):
    Background = 'Background'
    Body = 'Body'
    BodyDarker = 'BodyDarker'
    BodyLighter = 'BodyLighter'
    BodyNeutral = 'BodyNeutral'
    Border ='Border'
    BorderMuted = 'BorderMuted'
    Text = 'Text'
    TextMuted = 'TextMuted'
    TextMutedMore = 'TextMutedMore'
    Icon = 'Icon'
    IconMuted = 'IconMuted'
    Primary = 'Primary'
    Secondary = 'Secondary'
    Accent = 'Accent'
    Info = 'Info'
    Success = 'Success'
    Warning = 'Warning'
    Danger = 'Danger'

# region ZStyleDataKey
class ZStyleDataKey(Enum):
    Text = 'Text'
    TextBackSectcted = 'TextBackSectcted'
    TextToggled = 'TextToggled'
    Icon = 'Icon'
    IconToggled = 'IconToggled'
    Body = 'Body'
    BodySatrt = 'BodyStart'
    BodyEnd = 'BodyEnd'
    BodyFocused = 'BodyFocused'
    BodyToggled = 'BodyToggled'
    BodyToggledHover = 'BodyToggledHover'
    BodyToggledPressed = 'BodyToggledPressed'
    Border = 'Border'
    BorderToggled = 'BorderToggled'
    Handle = 'Handle'
    HandleToggled = 'HandleToggled'
    HandleBorder = 'HandleBorder'
    HandleInner = 'HandleInner'
    HandleOuter = 'HandleOuter'
    Track = 'Track'
    TrackBorder = 'TrackBorder'
    FillArea = 'FillArea'
    FillAreaStart = 'FillAreaStart'
    FillAreaEnd = 'FillAreaEnd'
    FillAreaBorder = 'FillAreaBorder'
    Underline = 'Underline'
    UnderlineFocused = 'UnderlineFocused'
    Cursor = 'Cursor'
    Mask = 'Mask'
    Indicator = 'Indicator'
    PlaceHolder = 'PlaceHolder'

# region light_palette
light_palette = {
    ZPaletteKey.Background: '#F2F2F2',
    ZPaletteKey.Body: '#FAFAFA',
    ZPaletteKey.BodyDarker: '#F9F9F9',
    ZPaletteKey.BodyLighter: '#FFFFFF',
    ZPaletteKey.BodyNeutral: '#CFCFCF',
    ZPaletteKey.Border: '#E0E0E0',
    ZPaletteKey.BorderMuted: '#EBEBEB',
    ZPaletteKey.Text: '#333333',
    ZPaletteKey.TextMuted: '#666666',
    ZPaletteKey.TextMutedMore: '#9f9f9f',
    ZPaletteKey.Icon: '#737373',
    ZPaletteKey.IconMuted: '#8C8C8C',
    ZPaletteKey.Primary: '#7FCDFF',
    ZPaletteKey.Secondary: '#B8DFFF',
    ZPaletteKey.Accent: '#FFAFCD',
    ZPaletteKey.Info: '#D5DADD',
    ZPaletteKey.Success: '#D1F0C2',
    ZPaletteKey.Warning: '#F0E4C2',
    ZPaletteKey.Danger: '#F0C2C2'
}

# region dark_palette
dark_palette = {
    ZPaletteKey.Background: '#141414',
    ZPaletteKey.Body: '#1C1C1C',
    ZPaletteKey.BodyDarker: '#171717',
    ZPaletteKey.BodyLighter: '#212121',
    ZPaletteKey.BodyNeutral: '#505050',
    ZPaletteKey.Border: '#2B2B2B',
    ZPaletteKey.BorderMuted: '#242424',
    ZPaletteKey.Text: '#F2F2F2',
    ZPaletteKey.TextMuted: '#D9D9D9',
    ZPaletteKey.TextMutedMore: '#B3B3B3',
    ZPaletteKey.Icon: '#CCCCCC',
    ZPaletteKey.IconMuted: '#B3B3B3',
    ZPaletteKey.Primary: '#675496',
    ZPaletteKey.Secondary: '#C8B3FD',
    ZPaletteKey.Accent: '#FE9ADD',
    ZPaletteKey.Info: '#75738C',
    ZPaletteKey.Success: '#8FB87A',
    ZPaletteKey.Warning: '#BAA35E',
    ZPaletteKey.Danger: '#CC6666'
}

# region ZPalette
class ZPalette(metaclass=NonInstantiableMeta):
    """全局唯一的调色板"""
    Background: QColor
    Body: QColor
    BodyDarker: QColor
    BodyLighter: QColor
    BodyNeutral: QColor
    Border: QColor
    BorderMuted: QColor
    Text: QColor
    TextMuted: QColor
    TextMutedMore: QColor
    Icon: QColor
    IconMuted: QColor
    Primary: QColor
    Secondary: QColor
    Accent: QColor
    Info: QColor
    Success: QColor
    Warning: QColor
    Danger: QColor

    Transparent_000 = QColor('#00000000')
    '''- #00000000'''
    Transparent_FFF = QColor('#00FFFFFF')
    '''- #00FFFFFF'''
    Black = QColor('#000000')
    '''- #000000'''
    Black_11 = QColor('#1B1B1B')
    '''- #1B1B1B'''
    Black_19 = QColor('#303030')
    '''- #303030'''
    Black_28 = QColor('#474747')
    '''- #474747'''
    Black_37 = QColor('#5E5E5E')
    '''- #5E5E5E'''
    Black_47 = QColor('#777777')
    '''- #777777'''
    Black_57 = QColor('#919191')
    '''- #919191'''
    Black_67 = QColor('#ABABAB')
    '''- #ABABAB'''
    Black_78 = QColor('#C6C6C6')
    '''- #C6C6C6'''
    Black_89 = QColor('#E2E2E2')
    '''- #E2E2E2'''
    Black_95 = QColor('#F1F1F1')
    '''- #F1F1F1'''
    White = QColor('#FFFFFF')
    '''- #FFFFFF'''

    # Transparent = cast(QColor,lambda: QColor('#00FFFFFF') if ZThemeManager().isLightTheme() else QColor('#00000000'))
    # """
    # 根据主题自动选择透明色
    # - LightTheme: '#00FFFFFF'
    # - DarkTheme: '#00000000'
    # """
    # Transparent_reverse = cast(QColor,lambda: QColor('#00000000') if ZThemeManager().isLightTheme() else QColor('#00FFFFFF'))
    # """
    # 根据主题自动选择与主题反色的透明色
    # - LightTheme: '#00000000'
    # - DarkTheme: '#00FFFFFF'
    # """
    @classmethod
    def Transparent(cls) -> QColor:
        """
        根据主题自动选择透明色
        - LightTheme: '#00FFFFFF'
        - DarkTheme: '#00000000'
        """
        return cls.Transparent_FFF if ZThemeManager().isLightTheme() else cls.Transparent_000

    @classmethod
    def Transparent_reverse(cls) -> QColor:
        """
        根据主题自动选择与主题反色的透明色
        - LightTheme: '#00000000'
        - DarkTheme: '#00FFFFFF'
        """
        return cls.Transparent_000 if ZThemeManager().isLightTheme() else cls.Transparent_FFF
    @classmethod
    def loadFromDict(cls, palette_dict: Dict[ZPaletteKey, str]) -> None:
        """
        从字典加载调色板配置并更新成员变量

        :param palette_dict: 键为ZPaletteKey枚举，值为颜色字符串的字典
        """
        # 获取所有字段名映射（用于校验）
        field_names = cls.__annotations__.keys()

        for key, color_str in palette_dict.items():
            # 检查键是否有效
            if not isinstance(key, ZPaletteKey):
                raise ValueError(f"无效的调色板键类型: {type(key)}, 应为ZPaletteKey")
            # 检查是否存在对应的成员变量
            if key.value not in field_names:
                raise ValueError(f"调色板中不存在键: {key.value}")
            # 转换颜色并赋值
            setattr(cls, key.value, QColor(color_str))

    @classmethod
    def loadLightPalette(cls) -> None:
        """
        加载内置浅色调色板
        """
        cls.loadFromDict(light_palette)

    @classmethod
    def loadDarkPalette(cls) -> None:
        """
        加载内置深色调色板
        """
        cls.loadFromDict(dark_palette)

# region style_data_map
style_data_map={
    'Light': {
        'ZItem': {
            ZStyleDataKey.Body: ZPalette.Transparent_000,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
            ZStyleDataKey.Indicator: lambda: ZPalette.Primary,
        },
        'ZSwitch':{
            ZStyleDataKey.Body: lambda: ZPalette.Primary,
            ZStyleDataKey.Border: lambda: ZPalette.Border,
            ZStyleDataKey.Handle: ZPalette.Black_67,
            ZStyleDataKey.HandleToggled: lambda: ZPalette.BodyLighter,
        },
        ('ZLineEdit','ZLoginEdit', 'ZNumberEdit'): {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.BodyFocused: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.PlaceHolder: lambda: ZPalette.TextMutedMore,
            ZStyleDataKey.TextBackSectcted: lambda: ZPalette.Secondary,
            ZStyleDataKey.Cursor: lambda: ZPalette.Primary,
            ZStyleDataKey.Underline: lambda: ZPalette.BodyDarker.darker(120),
            ZStyleDataKey.UnderlineFocused: lambda: ZPalette.Primary,
        },
        'ZHeadLine':{
            ZStyleDataKey.Body: ZPalette.Transparent_000,
            ZStyleDataKey.Border: ZPalette.Transparent_000,
            ZStyleDataKey.Text: lambda: ZPalette.Text,
            ZStyleDataKey.TextBackSectcted: lambda: ZPalette.Primary,
            ZStyleDataKey.Indicator: lambda: ZPalette.Primary,
        },
        ('ZPanel', 'ZItemView'): {
            ZStyleDataKey.Body: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
        },
        'ZScrollPanel': {
            ZStyleDataKey.Body: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Handle: lambda: ZPalette.BodyNeutral,
            ZStyleDataKey.HandleBorder: lambda: ZPalette.BodyNeutral,
        },
        'ZSlider': {
            ZStyleDataKey.Track: lambda: ZPalette.BodyDarker,
            ZStyleDataKey.TrackBorder: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.FillAreaStart: lambda: ZPalette.Primary,
            ZStyleDataKey.FillAreaEnd: lambda: ZPalette.Secondary,
            ZStyleDataKey.FillAreaBorder: lambda: ZPalette.Primary,
            ZStyleDataKey.HandleInner: lambda: ZPalette.Secondary,
            ZStyleDataKey.HandleOuter:lambda: ZPalette.BodyLighter,
            ZStyleDataKey.HandleBorder: lambda: ZPalette.BorderMuted
        },
        ('ZButton', 'ZComboBox'): {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
        },
        'ZFlatButton': {
            ZStyleDataKey.Border: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
        },
        'ZToggleButton': {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.BodyToggled: lambda: ZPalette.Primary,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.TextToggled: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.Icon,
            ZStyleDataKey.IconToggled: lambda: ZPalette.Icon,
        },
        'ZFlatToggleButton': {
            ZStyleDataKey.Body: ZPalette.Transparent_000,
            ZStyleDataKey.BodyToggled: lambda: ZPalette.Primary,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.BorderToggled:lambda: ZPalette.Primary,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.TextToggled: lambda: ZPalette.TextMutedMore,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
            ZStyleDataKey.IconToggled: lambda: ZPalette.Primary,
        },
        'ZNavigationBar': {
            ZStyleDataKey.Indicator: lambda: ZPalette.Primary,
        },
        'ZNavBarButton': {
            ZStyleDataKey.Body: ZPalette.Transparent_000,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
        },
        'ZNavBarToggleButton': {
            ZStyleDataKey.Body: ZPalette.Transparent_000,
            ZStyleDataKey.Icon: lambda: ZPalette.Icon,
            ZStyleDataKey.IconToggled: lambda: ZPalette.Primary,
        },
        'ZFramelessWindow': {
            ZStyleDataKey.Body: lambda: ZPalette.Background
        },
        'ZToolTip': {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
        }
    },
    'Dark': {
        'ZItem': {
            ZStyleDataKey.Body: ZPalette.Transparent_FFF,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
            ZStyleDataKey.Indicator: lambda: ZPalette.Primary,
        },
        'ZSwitch':{
            ZStyleDataKey.Body: lambda: ZPalette.Primary,
            ZStyleDataKey.Border: lambda: ZPalette.Border,
            ZStyleDataKey.Handle: ZPalette.Black_67,
            ZStyleDataKey.HandleToggled: ZPalette.Black_67
        },
        ('ZLineEdit', 'ZLoginEdit', 'ZNumberEdit'): {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.BodyFocused: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.PlaceHolder: lambda: ZPalette.TextMutedMore,
            ZStyleDataKey.TextBackSectcted: lambda: ZPalette.Primary,
            ZStyleDataKey.Cursor: lambda: ZPalette.Primary,
            ZStyleDataKey.Underline: lambda: ZPalette.BodyLighter.lighter(150),
            ZStyleDataKey.UnderlineFocused: lambda: ZPalette.Primary,
        },
        'ZHeadLine':{
            ZStyleDataKey.Body: ZPalette.Transparent_000,
            ZStyleDataKey.Border: ZPalette.Transparent_000,
            ZStyleDataKey.Text: lambda: ZPalette.Text,
            ZStyleDataKey.TextBackSectcted: lambda: ZPalette.Primary,
            ZStyleDataKey.Indicator: lambda: ZPalette.Primary,
        },
        ('ZPanel', 'ZItemView'): {
            ZStyleDataKey.Body: lambda: ZPalette.BodyDarker,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
        },
        'ZScrollPanel': {
            ZStyleDataKey.Body: lambda: ZPalette.BodyDarker,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Handle: lambda: ZPalette.BodyNeutral,
            ZStyleDataKey.HandleBorder: lambda: ZPalette.BodyNeutral,
        },
        'ZSlider': {
            ZStyleDataKey.Track: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.TrackBorder: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.FillAreaStart: lambda: ZPalette.Primary,
            ZStyleDataKey.FillAreaEnd: lambda: ZPalette.Secondary,
            ZStyleDataKey.FillAreaBorder: lambda: ZPalette.Primary,
            ZStyleDataKey.HandleInner: lambda: ZPalette.Secondary,
            ZStyleDataKey.HandleOuter:lambda: ZPalette.BodyLighter,
            ZStyleDataKey.HandleBorder: lambda: ZPalette.Border
        },
        ('ZButton', 'ZComboBox'): {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.Text,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
        },
        'ZFlatButton': {
            ZStyleDataKey.Border: lambda: ZPalette.BodyLighter,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
        },
        'ZToggleButton': {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.BodyToggled: lambda: ZPalette.Primary,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMutedMore,
            ZStyleDataKey.TextToggled: lambda: ZPalette.TextMuted,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
            ZStyleDataKey.IconToggled: lambda: ZPalette.Icon,
        },
        'ZFlatToggleButton': {
            ZStyleDataKey.Body: ZPalette.Transparent_FFF,
            ZStyleDataKey.BodyToggled: lambda: ZPalette.Primary,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.BorderToggled:lambda: ZPalette.Primary,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
            ZStyleDataKey.TextToggled: lambda: ZPalette.TextMutedMore,
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
            ZStyleDataKey.IconToggled: lambda: ZPalette.Primary,
        },
        'ZNavigationBar': {
            ZStyleDataKey.Indicator: lambda: ZPalette.Primary,
        },
        'ZNavBarButton': {
            ZStyleDataKey.Icon: lambda: ZPalette.IconMuted,
        },
        'ZNavBarToggleButton': {
            ZStyleDataKey.Icon: lambda: ZPalette.Icon,
            ZStyleDataKey.IconToggled: lambda: ZPalette.Primary,
        },
        'ZFramelessWindow': {
            ZStyleDataKey.Body: lambda: ZPalette.Background
        },
        'ZToolTip': {
            ZStyleDataKey.Body: lambda: ZPalette.Body,
            ZStyleDataKey.Border: lambda: ZPalette.BorderMuted,
            ZStyleDataKey.Text: lambda: ZPalette.TextMuted,
        }
    }
}

# region ZStyleData
@dataclass
class ZFramelessWindowStyleData:
    Body: QColor

@dataclass
class ZPanelStyleData:
    Body: QColor
    Border: QColor

@dataclass
class ZScrollPanelStyleData:
    Body: QColor
    Border: QColor
    Handle: QColor
    HandleBorder: QColor

@dataclass
class ZButtonStyleData:
    Body: QColor
    Border: QColor
    Text: QColor
    Icon: QColor

@dataclass
class ZToggleButtonStyleData:
    Body: QColor
    BodyToggled: QColor
    Border: QColor
    Text: QColor
    TextToggled: QColor
    Icon: QColor
    IconToggled: QColor

@dataclass
class ZFlatButtonStyleData:
    Border: QColor
    Text: QColor
    Icon: QColor

@dataclass
class ZFlatToggleButtonStyleData:
    Body: QColor
    BodyToggled: QColor
    Border: QColor
    Text: QColor
    Icon: QColor

@dataclass
class ZNavBarButtonStyleData:
    Icon: QColor

@dataclass
class ZNavBarToggleButtonStyleData:
    Icon: QColor
    IconToggled: QColor

@dataclass
class ZSliderStyleData:
    Track: QColor
    TrackBorder: QColor
    FillAreaStart: QColor
    FillAreaEnd: QColor
    FillAreaBorder: QColor
    HandleInner: QColor
    HandleOuter: QColor
    HandleBorder: QColor

@dataclass
class ZToolTipStyleData:
    Body: QColor
    Border: QColor
    Text: QColor

@dataclass
class ZHeadLineStyleData:
    Body: QColor
    Border: QColor
    Text: QColor
    TextBackSectcted: QColor
    Indicator: QColor

@dataclass
class ZLineEditStyleData:
    Body: QColor
    BodyFocused: QColor
    Border: QColor
    Text: QColor
    PlaceHolder: QColor
    TextBackSectcted: QColor
    Cursor: QColor
    Underline: QColor
    UnderlineFocused: QColor

@dataclass
class ZLoginEditStyleData:
    Body: QColor
    BodyFocused: QColor
    Border: QColor
    Text: QColor
    TextBackSectcted: QColor
    Cursor: QColor
    Underline: QColor
    UnderlineFocused: QColor

@dataclass
class ZNumberEditStyleData:
    Body: QColor
    BodyFocused: QColor
    Border: QColor
    Text: QColor
    TextBackSectcted: QColor
    Cursor: QColor
    Underline: QColor
    UnderlineFocused: QColor

@dataclass
class ZSwitchStyleData:
    Body: QColor
    Border: QColor
    Handle: QColor
    HandleToggled: QColor

@dataclass
class ZNavigationBarStyleData:
    Indicator: QColor

@dataclass
class ZComboBoxStyleData:
    Body: QColor
    Border: QColor
    Text: QColor
    Icon: QColor

@dataclass
class ZItemStyleData:
    Body: QColor
    Text: QColor
    Icon: QColor
    Indicator: QColor

@dataclass
class ZItemViewStyleData:
    Body: QColor
    Border: QColor

StyleDataUnion = Union[
    ZButtonStyleData,
    ZFramelessWindowStyleData,
    ZHeadLineStyleData,
    ZToolTipStyleData,
    ZToggleButtonStyleData,
    ZNavBarButtonStyleData,
    ZNavBarToggleButtonStyleData,
    ZScrollPanelStyleData,
    ZSliderStyleData,
    ZLineEditStyleData,
    ZLoginEditStyleData,
    ZNumberEditStyleData,
    ZPanelStyleData,
    ZSwitchStyleData,
    ZNavigationBarStyleData,
    ZComboBoxStyleData,
    ZItemStyleData,
    ZItemViewStyleData
    ]

StyleDataT = TypeVar('StyleDataT', bound='StyleDataUnion')

# region ZStyleDataFactory
class ZStyleDataFactory:
    dataclass_map = {
        'ZComboBox': ZComboBoxStyleData,
        'ZItem': ZItemStyleData,
        'ZItemView': ZItemViewStyleData,
        'ZNavigationBar': ZNavigationBarStyleData,
        'ZSwitch': ZSwitchStyleData,
        'ZLineEdit': ZLineEditStyleData,
        'ZHeadLine': ZHeadLineStyleData,
        'ZLoginEdit': ZLoginEditStyleData,
        'ZNumberEdit': ZNumberEditStyleData,
        'ZPanel': ZPanelStyleData,
        'ZScrollPanel': ZScrollPanelStyleData,
        'ZSlider': ZSliderStyleData,
        'ZButton': ZButtonStyleData,
        'ZFlatButton': ZFlatButtonStyleData,
        'ZToggleButton': ZToggleButtonStyleData,
        'ZFlatToggleButton': ZFlatToggleButtonStyleData,
        'ZNavBarButton': ZNavBarButtonStyleData,
        'ZNavBarToggleButton': ZNavBarToggleButtonStyleData,
        'ZFramelessWindow': ZFramelessWindowStyleData,
        'ZToolTip': ZToolTipStyleData,
    }

    @classmethod
    def create(cls, name: str, map: dict) -> StyleDataT:
        data_type = cls.dataclass_map.get(name)
        if data_type is None: raise ValueError(f"Unknown style data class for component: {name}")
        return cls.dictToDataclass(data_type, name, map)

    @staticmethod
    def dictToDataclass(data_type: StyleDataT, name: str, map: dict) -> StyleDataT:
        if not is_dataclass(data_type): raise TypeError(f"{data_type} is not a dataclass")
        # 获取组件对应的样式数据字典
        component_data = {}
        for key, value in map.items():
            if (isinstance(key, tuple) and name in key) or key == name:
                component_data = value
                break
        if not component_data:
            raise ValueError(f"No style data found for component: {name}")
        # 提取数据类所需的字段
        field_names = [f.name for f in fields(data_type)]
        filtered = {}
        for key, value in component_data.items():
            # 枚举键转换为字符串
            key_str = key.value if isinstance(key, Enum) else str(key)
            if key_str in field_names:
                # 确保值是QColor类型（处理可能的动态颜色值）
                if callable(value):
                    color_value = value()
                    filtered[key_str] = QColor(color_value)
                else:
                    color_value = value
                    filtered[key_str] = QColor(color_value)
        # 检查是否缺失必要字段
        missing = set(field_names) - set(filtered.keys())
        if missing:
            raise ValueError(f"Missing required fields for {data_type.__name__}: {missing}")
        return data_type(**filtered)

# region ZStyleDataManager
class ZStyleDataManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        super().__init__()
        self._cache: Dict[str, StyleDataT] = {}
        ZThemeManager().themeChanged.connect(self._theme_change_handler_)

    def _take_palette_snapshot(self) -> Dict[str, QColor]:
        """保存当前ZPalette的所有颜色状态"""
        return {
            field: getattr(ZPalette, field)
            for field in ZPalette.__annotations__
            if hasattr(ZPalette, field)
        }

    def _restore_palette_snapshot(self, snapshot: Dict[str, QColor]) -> None:
        """恢复ZPalette到指定的快照状态"""
        for field, color in snapshot.items():
            setattr(ZPalette, field, color)

    def getStyleData(self, name: str) -> StyleDataT:
        '''获取当前主题下的样式数据'''
        # 检查缓存
        if name in self._cache: return self._cache[name]
        # 缓存中没有，则创建并缓存
        style_data = ZStyleDataFactory.create(name, style_data_map[ZThemeManager().getThemeName()])
        self._cache[name] = style_data
        return style_data

    def getStyleDataByTheme(self, name: str, theme: str) -> StyleDataT:
        '''获取指定主题下的样式数据'''
        current_theme = ZThemeManager().getThemeName()
        if theme == current_theme:
            return self.getStyleData(name)

        # 保存当前调色板状态
        current_snapshot = self._take_palette_snapshot()
        try:
            # 临时切换到目标主题的调色板
            if theme == 'Light':
                ZPalette.loadLightPalette()
            elif theme == 'Dark':
                ZPalette.loadDarkPalette()
            # 创建目标主题的样式数据
            return ZStyleDataFactory.create(name, style_data_map[theme])
        finally:
            # 无论是否发生异常，都恢复原始调色板状态
            self._restore_palette_snapshot(current_snapshot)

    def _theme_change_handler_(self, theme: str) -> None:
        self.clearCache()
        if theme == 'Light':
            ZPalette.loadLightPalette()
        elif theme == 'Dark':
            ZPalette.loadDarkPalette()

    def clearCache(self) -> None:
        """清除所有缓存的样式数据实例，用于主题切换等场景"""
        self._cache.clear()


# region 测试
if __name__ == '__main__':
    # 加载默认调色板（浅色调）
    ZPalette.loadLightPalette()
    logging.info("已加载浅色调色板")

    # 获取所有组件名称列表
    component_names = list(ZStyleDataFactory.dataclass_map.keys())

    # 测试每个组件的样式数据
    logging.info("===== 测试浅色调色板样式 =====")
    for name in component_names:
        try:
            style_data = ZStyleDataManager().getStyleData(name)
            logging.info(f"---{name} 样式数据---")
            for field in fields(style_data):
                value = getattr(style_data, field.name)
                # 打印颜色的十六进制表示
                if isinstance(value, QColor):
                    logging.info(f"  |{field.name}: {value.name()}")
                else:
                    logging.info(f"  |{field.name}: {value}")
        except Exception as e:
            logging.info(f"{name} 样式数据获取失败: {str(e)}")

    # 切换到深色调色板
    ZPalette.loadDarkPalette()
    # 清除缓存以重新生成样式数据
    ZStyleDataManager().clearCache()
    logging.info("已加载深色调色板")

    # 测试深色调色板下的样式数据
    logging.info("===== 测试深色调色板样式 =====")
    for name in component_names:
        try:
            style_data = ZStyleDataManager().getStyleData(name)
            logging.info(f"---{name} 样式数据---")
            for field in fields(style_data):
                value = getattr(style_data, field.name)
                if isinstance(value, QColor):
                    logging.info(f"  |{field.name}: {value.name()}")
                else:
                    logging.info(f"  |{field.name}: {value}")
        except Exception as e:
            logging.info(f"{name} 样式数据获取失败: {str(e)}")

    logging.info("所有样式数据测试完成")

    print(ZPalette.Transparent())

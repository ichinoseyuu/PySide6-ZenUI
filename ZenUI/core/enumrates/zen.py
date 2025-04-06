from enum import Enum, auto

class Zen:
    """ ZenUI的各种枚举类型"""
    class Layout(Enum):
        """ 布局类型
        Attributes:
            Horizontal: 水平布局
            Vertical: 垂直布局
        """
        Horizontal = auto()
        Vertical = auto()
    class Theme(Enum):
        """ 主题类型
        Attributes:
            Light: 浅色主题
            Dark: 深色主题
        """
        Light = auto()
        Dark = auto()


    class WidgetFlag(Enum):
        """
        WidgetFlag
        Attributes:
            FlashOnHintUpdated: 在工具提示被重新设置时，使工具提示闪烁
            InstantMove: 是否立即移动而不运行动画
            InstantResize: 是否立即重设大小而不运行动画
            InstantSetOpacity: 是否立即重设透明度而不运行动画
            HasMoveLimits: 是否有移动限定区域
            AdjustSizeOnTextChanged: 是否在setText被调用时自动调整空间大小
            EnableAnimationSignals: 是否启用moved,resized,opacityChanged信号
            DeleteOnHidden: 下一次被隐藏时，运行 deleteLater()
            StyleSheetApplyToChildren: 是否将样式表应用到子控件
            BGHaveGradient: 背景是否使用渐变色
        """
        FlashOnHintUpdated = auto()         # 在工具提示被重新设置时，使工具提示闪烁
        InstantMove = auto()                # 是否立即移动而不运行动画
        InstantResize = auto()              # 是否立即重设大小而不运行动画
        InstantSetOpacity = auto()          # 是否立即重设透明度而不运行动画
        InstantSetColor = auto()            # 是否立即重设颜色而不运行动画
        HasMoveLimits = auto()              # 是否有移动限定区域
        AdjustSizeOnTextChanged = auto()    # 是否在setText被调用时自动调整空间大小
        EnableAnimationSignals = auto()     # 是否启用moved，resized，opacityChanged信号
        DeleteOnHidden = auto()             # 下一次被隐藏时，运行 deleteLater()
        StyleSheetApplyToChildren = auto()  # 是否将样式表应用到子控件
        GradientColor = auto()              # 背景是否使用渐变色


    class ColorRole(Enum):
        """ 颜色对象
        Attributes:
            Background_A: 背景颜色A
            Background_B: 背景颜色B
            Hover: 悬停颜色
            Pressed: 按下颜色
            Flash: 闪烁颜色
            Text: 文字颜色
            Border: 边框颜色
        """
        Background_A = auto()
        Background_B = auto()
        Hover = auto()
        Pressed = auto()
        Flash = auto()
        Text = auto()
        Border = auto()
        Disabled = auto()
        Icon = auto()


    class WidgetType(Enum):
        """ 控件类型
        Attributes:
            ZenPushButton: 按钮控件
            ZenContainer: 水平布局控件
            ZenText: 文本控件
        """
        PushButton = auto()
        TansButton = auto()
        Container = auto()
        TextLabel = auto()
        Titlebar = auto()


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import IntEnum,Enum,IntFlag,auto

class Zen:
    """ ZenUI的各种枚举类型"""
    class Theme(IntEnum):
        "主题类型"
        Light = auto()
        '浅色主题'
        Dark = auto()
        '深色主题'


    class WidgetFlag(IntEnum):
        '控件标志'
        FlashOnHintUpdated = auto()
        '在工具提示被重新设置时，使工具提示闪烁'
        InstantMove = auto()
        '立即移动而不运行动画'
        InstantResize = auto()
        '立即重设大小而不运行动画'
        InstantSetOpacity = auto()
        '立即重设透明度而不运行动画'
        InstantSetColor = auto() 
        '立即重设颜色而不运行动画'
        HasMoveLimits = auto()
        '有移动限定区域'
        AdjustSizeOnTextChanged = auto()
        '在`setText`被调用时自动调整空间大小'
        EnableAnimationSignals = auto()
        '启用`moved`,`resized`,`opacityChanged`信号'
        DeleteOnHidden = auto()
        '隐藏时删除控件'
        GradientColor = auto()
        '启用渐变'


    class ColorRole(IntEnum):
        '颜色对象'
        BackgroundA = auto()
        '背景颜色A'
        BackgroundB = auto()
        '背景颜色B'
        Hover= auto()
        '悬停时背景颜色'
        Pressed = auto()
        '按下时背景颜色'
        Flash = auto()
        '闪烁时背景颜色'
        SelectedA = auto()
        '选中时背景颜色A'
        SelectedB = auto()
        '选中时背景颜色B'
        Border = auto()
        '边框颜色'
        BorderHover = auto()
        '悬停时边框颜色'
        BorderPressed = auto()
        '按下时边框颜色'
        BorderSelected = auto()
        '选中时边框颜色'
        Text = auto()
        '文字颜色'
        TextHover = auto()
        '悬停时文字颜色'
        TextPressed = auto()
        '按下时文字颜色'
        TextSelected = auto()
        '选中时文字颜色'
        Icon = auto()
        '图标颜色'
        IconHover = auto()
        '悬停时图标颜色'
        IconPressed = auto()
        '按下时图标颜色'
        IconSelected = auto()
        '选中时图标颜色'
        IndicatorSelected = auto()
        '指示条选中时颜色'
        Track = auto()
        '轨道颜色'
        Fill = auto()
        '填充颜色'
        Handle = auto()
        '滑块颜色'
        HandleInner = auto()
        '滑块内部颜色'
        HandleOuter = auto()
        '滑块外部颜色'
        HandleBorder = auto()
        '滑块边框颜色'



    class WidgetType(IntEnum):
        '''控件类型'''
        Window = auto()
        '窗口控件'
        ToolTip = auto()
        '工具提示控件'
        Box = auto()
        '盒子控件'
        Drawer = auto()
        '抽屉控件'
        Page = auto()
        '页面控件'
        ScrollPage = auto()
        '滚动页面控件'
        PushButton = auto()
        '按钮控件'
        FillButton = auto()
        '填充按钮控件'
        GradientButton = auto()
        '渐变按钮控件'
        GhostButton = auto()
        '幽灵按钮控件'
        TransparentButton = auto()
        '透明按钮控件'
        NoBackgroundButton = auto()
        '无背景按钮控件'
        ToggleButton = auto()
        '开关按钮控件'
        TextLabel = auto()
        '文字标签控件'
        Slider = auto()
        '滑块控件'
        ScrollBar = auto()
        '滚动条控件'



    class Layout(IntEnum):
        '''布局类型'''
        Row = auto()
        '行布局'
        Column = auto()
        '列布局'
        Grid = auto()
        '网格布局'


    class Alignment(Enum):
        '''对齐方式'''
        Leading = Qt.AlignmentFlag.AlignLeading
        '靠左对齐'
        Left = Qt.AlignmentFlag.AlignLeft
        '靠左对齐'
        Right = Qt.AlignmentFlag.AlignRight
        '靠右对齐'
        Trailing = Qt.AlignmentFlag.AlignTrailing
        '靠右对齐'
        HCenter = Qt.AlignmentFlag.AlignHCenter
        '水平居中对齐'
        Justify = Qt.AlignmentFlag.AlignJustify
        '水平对齐'
        Absolute = Qt.AlignmentFlag.AlignAbsolute
        '绝对对齐'
        Horizontal_Mask = Qt.AlignmentFlag.AlignHorizontal_Mask
        '水平对齐掩码'
        Top = Qt.AlignmentFlag.AlignTop
        '靠上对齐'
        Bottom = Qt.AlignmentFlag.AlignBottom
        '靠下对齐'
        VCenter = Qt.AlignmentFlag.AlignVCenter
        '垂直居中对齐'
        Center = Qt.AlignmentFlag.AlignCenter
        '居中对齐'
        Baseline = Qt.AlignmentFlag.AlignBaseline
        '基线对齐'
        Vertical_Mask = Qt.AlignmentFlag.AlignVertical_Mask
        '垂直对齐掩码'


    class SizePolicy(Enum):
        '''控件大小策略'''
        Fixed = QSizePolicy.Policy.Fixed
        Minimum = QSizePolicy.Policy.Minimum
        MinimumExpanding = QSizePolicy.Policy.MinimumExpanding
        Maximum = QSizePolicy.Policy.Maximum
        Preferred = QSizePolicy.Policy.Preferred
        Expanding = QSizePolicy.Policy.Expanding
        Ignored = QSizePolicy.Policy.Ignored


    class Position(IntEnum):
        """位置类型"""
        Left = auto()
        Right = auto()
        Top = auto()
        Bottom = auto()


    class Direction(IntEnum):
        """方向类型"""
        LeftToRight = auto()
        RightToLeft = auto()
        TopToBottom = auto()
        BottomToTop = auto()
        Horizontal = auto()
        Vertical = auto()


    class State(IntEnum):
        """控件状态"""
        Normal = auto()
        Expand = auto()
        Collapsed = auto()
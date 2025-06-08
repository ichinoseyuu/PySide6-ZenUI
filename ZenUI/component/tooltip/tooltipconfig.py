from dataclasses import dataclass
@dataclass
class ToolTipConfig:
    """提示框配置"""
    MARGIN: int = 8  # 阴影间距
    '阴影间距'
    SHADOW_BLUR: int = 12  # 阴影模糊半径
    '阴影模糊半径'
    SHADOW_COLOR: tuple = (0, 0, 0, 100)  # 阴影颜色
    '阴影颜色'
    MIN_HEIGHT: int = 36  # 最小高度
    '最小高度'
    PADDING: int = 8  # 显示面板内边距
    '显示面板内边距'
    BORDER_RADIUS: int = 2  # 边框圆角
    '边框圆角'
    TRACKER_FPS: int = 60  # 位置更新帧率
    '位置更新帧率'
    SPACING: int = 6  # 控件间距
    '控件间距'
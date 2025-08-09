from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QRadialGradient, QConicalGradient
from ZenUI._legacy.core import Zen
class ZGradientLayer(QWidget):
    """渐变色绘制组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._start_color = QColor(255, 255, 255)  # 起始颜色
        self._end_color = QColor(0, 0, 0)          # 结束颜色
        self._gradient_type = Zen.GradientType.Linear  # 渐变类型
        self._direction = Zen.Direction.TopLeftToBottomRight  # 渐变方向
        self._reverse = False                        # 是否反向渐变
        self._custom_points:tuple = None            # 存储自定义渐变点
        self._radius = 100                         # 径向渐变半径
        self._angle = 0                            # 锥形渐变角度
        # 更新终点位置
        self.resizeEvent(None)

    def setStartColor(self, color: QColor):
        """设置起始颜色"""
        self._start_color = color
        self.update()

    def setEndColor(self, color: QColor):
        """设置结束颜色"""
        self._end_color = color
        self.update()

    def setColors(self, start_color: QColor, end_color: QColor):
        """设置起始和结束颜色"""
        self._start_color = start_color
        self._end_color = end_color
        self.update()

    def setGradientType(self, gradient_type: int):
        """设置渐变类型"""
        self._gradient_type = gradient_type
        self.update()

    def setGradientDirection(self, direction: Zen.Direction,reverse: bool=False):
        """设置渐变方向"""
        self._direction = direction
        self._reverse = reverse
        self.update()

    def setReverse(self, reverse: bool):
        """设置是否反向渐变"""
        self._reverse = reverse
        self.update()

    def setCustomGradientPoints(self, x1: float, y1: float, x2: float, y2: float):
        """设置自定义渐变点
        Args:
            x1: 起点x坐标 (0-1)
            y1: 起点y坐标 (0-1) 
            x2: 终点x坐标 (0-1)
            y2: 终点y坐标 (0-1)
        """
        # 确保坐标在0-1范围内
        x1 = max(0.0, min(1.0, x1))
        y1 = max(0.0, min(1.0, y1))
        x2 = max(0.0, min(1.0, x2))
        y2 = max(0.0, min(1.0, y2))
        self._custom_points = (x1, y1, x2, y2)
        self.update()

    def clearCustomGradientPoints(self):
        """清除自定义渐变点,恢复使用预设方向"""
        self._custom_points = None
        self.update()

    def _getGradientPoints(self) -> tuple[float, float, float, float]:
        """根据渐变方向获取归一化的起始和结束坐标"""
        # 优先使用自定义渐变点
        if self._custom_points is not None:
            return self._custom_points
        if self._direction == Zen.Direction.TopLeftToBottomRight:
            return (0, 0, 1, 1)
        elif self._direction == Zen.Direction.TopRightToBottomLeft:
            return (1, 0, 0, 1)
        elif self._direction == Zen.Direction.TopToBottom:
            return (0.5, 0, 0.5, 1)
        elif self._direction == Zen.Direction.LeftToRight:
            return (0, 0.5, 1, 0.5)
        elif self._direction == Zen.Direction.BottomLeftToTopRight:
            return (0, 1, 1, 0)
        elif self._direction == Zen.Direction.BottomRightToTopLeft:
            return (1, 1, 0, 0)
        elif self._direction == Zen.Direction.BottomToTop:
            return (0.5, 1, 0.5, 0)
        elif self._direction == Zen.Direction.RightToLeft:
            return (1, 0.5, 0, 0.5)

    def setRadius(self, radius: float):
        """设置径向渐变半径"""
        self._radius = radius
        self.update()

    def setAngle(self, angle: float):
        """设置锥形渐变角度"""
        self._angle = angle
        self.update()

    def resizeEvent(self, event):
        """处理大小改变事件"""
        self.update()

    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 根据渐变类型创建不同的渐变对象
        if self._gradient_type == Zen.GradientType.Linear:
            # 线性渐变
            # 获取归一化坐标
            x1, y1, x2, y2 = self._getGradientPoints()
            rect = self.rect()
            # 将归一化坐标映射到实际窗口尺寸
            gradient = QLinearGradient(
                rect.width() * x1,
                rect.height() * y1,
                rect.width() * x2,
                rect.height() * y2
            )

        elif self._gradient_type == Zen.GradientType.Radial:
            # 径向渐变
            center = QPoint(self.width()/2, self.height()/2)
            gradient = QRadialGradient(center, self._radius, center)

        elif self._gradient_type == Zen.GradientType.Conical:
            # 锥形渐变
            center = QPoint(self.width()/2, self.height()/2)
            gradient = QConicalGradient(center, self._angle)

        # 设置渐变颜色，根据反向标志决定颜色顺序
        if not self._reverse:
            gradient.setColorAt(0.0, self._start_color)
            gradient.setColorAt(1.0, self._end_color)
        else:
            gradient.setColorAt(0.0, self._end_color)
            gradient.setColorAt(1.0, self._start_color)

        # 绘制渐变
        painter.fillRect(self.rect(), gradient)

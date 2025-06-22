from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import Enum
import logging

class AnimatedColorProperty(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._color: QColor = '#dcdcdc'
        self._anim = QPropertyAnimation(self, b'color')
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    @property
    def animation(self) -> QPropertyAnimation:
        return self._anim

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    def getColor(self) -> QColor:
        return self._color

    def setColor(self, value: QColor):
        self._color = value
        self.parentWidget.update()

    color = Property(QColor, getColor, setColor)

    def setColorTo(self, value: QColor) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._color)
        self._anim.setEndValue(value)
        self._anim.start()

    def parent(self) -> QWidget:
        return super().parent()

class IconStyle(AnimatedColorProperty):
    pass

class TextStyle(AnimatedColorProperty):
    pass

class BackGroundStyle(AnimatedColorProperty):
    pass

class BorderStyle(AnimatedColorProperty):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._width: int = 1

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self.parentWidget.update()


class CornerStyle(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._radius: int = 5

    @property
    def parentWidget(self) -> QWidget:
        return self.parent()

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, value: int) -> None:
        self._radius = value
        self.parentWidget.update()

    def parent(self) -> QWidget:
        return super().parent()

class GradientBackGroundStyle(QObject):

    class Type(Enum):
        Linear = 0
        '线性'
        Radial = 1
        '径向'
        Conical = 2
        '锥形'

    class Direction(Enum):
        Horizontal = 0
        '水平'
        Vertical = 1
        '垂直'
        Diagonal = 2
        '对角线'
        DiagonalReverse = 3
        '反向对角线'
        Custom = 4
        '自定义'

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._color1: QColor = QColor('#202020')
        self._color2: QColor = QColor('#202020')
        self._type: GradientBackGroundStyle.Type = self.Type.Linear
        '渐变类型'
        self._direction: GradientBackGroundStyle.Direction = self.Direction.Diagonal
        '渐变方向'
        self._reverse: bool = False
        '是否反向渐变'
        self._linear_points: tuple[float, float, float, float] = (0, 0, 1, 1)
        '线性渐变起点和终点'
        self._radial_radius: int = 100
        '径向渐变半径'
        self._conical_angle: int = 0
        '锥形渐变角度'
        self._anim1 = QPropertyAnimation(self, b'colorStart')
        self._anim1.setDuration(150)
        self._anim1.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim2 = QPropertyAnimation(self, b'colorEnd')
        self._anim2.setDuration(150)
        self._anim2.setEasingCurve(QEasingCurve.Type.InOutQuad)

    @property
    def animationStart(self) -> QPropertyAnimation:
        return self._anim1


    @property
    def animationEnd(self) -> QPropertyAnimation:
        return self._anim2


    @property
    def parentWidget(self) -> QWidget:
        return self.parent()


    @property
    def type(self) -> Type:
        return self._type

    @type.setter
    def type(self, value: Type) -> None:
        self._type = value
        self.parentWidget.update()


    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction) -> None:
        if self._type is not self.Type.Linear:
            logging.warning('渐变类型不是线性，设置渐变方向无效')
            return
        self._direction = value
        if self._direction is self.Direction.Horizontal:
            self._linear_points = (0, 0, 1, 0)
        elif self._direction is self.Direction.Vertical:
            self._linear_points = (0, 0, 0, 1)
        elif self._direction is self.Direction.Diagonal:
            self._linear_points = (0, 0, 1, 1)
        elif self._direction is self.Direction.DiagonalReverse:
            self._linear_points = (1, 0, 0, 1)
        elif self._direction is self.Direction.Custom:
            logging.warning('自定义渐变方向请直接设置渐变起点和终点')
        self.parentWidget.update()


    @property
    def reverse(self) -> bool:
        return self._reverse

    @reverse.setter
    def reverse(self, value: bool) -> None:
        self._reverse = value
        self.parentWidget.update()


    @property
    def linearPoints(self) -> tuple[float, float, float, float]:
        return self._linear_points

    @linearPoints.setter
    def linearPoints(self, value: tuple[float, float, float, float]) -> None:
        if self._type is not self.Type.Linear:
            logging.warning('渐变类型不是线性，设置渐变方向无效')
            return
        self._linear_points = value
        self._direction = self.Direction.Custom
        self.parentWidget.update()


    @property
    def radialRadius(self) -> int:
        return self._radial_radius

    @radialRadius.setter
    def radialRadius(self, value: int) -> None:
        if self._type is not self.Type.Radial:
            logging.warning('渐变类型不是径向，设置径向半径无效')
            return
        self._radial_radius = value
        self.parentWidget.update()


    @property
    def conicalAngle(self) -> int:
        return self._conical_angle

    @conicalAngle.setter
    def conicalAngle(self, value: int) -> None:
        if self._type is not self.Type.Conical:
            logging.warning('渐变类型不是锥形，设置锥形角度无效')
            return
        self._conical_angle = value
        self.parentWidget.update()


    def getColorStart(self) -> QColor:
        return self._color1

    def setColorStart(self, value: QColor) -> None:
        self._color1 = value
        self.parentWidget.update()

    colorStart = Property(QColor, getColorStart, setColorStart)


    def getColorEnd(self) -> QColor:
        return self._color2

    def setColorEnd(self, value: QColor) -> None:
        self._color2 = value
        self.parentWidget.update()

    colorEnd = Property(QColor, getColorEnd, setColorEnd)

    def setColorStartTo(self, value: QColor) -> None:
        self._anim1.stop()
        self._anim1.setStartValue(self._color1)
        self._anim1.setEndValue(value)
        self._anim1.start()

    def setColorEndTo(self, value: QColor) -> None:
        self._anim2.stop()
        self._anim2.setStartValue(self._color2)
        self._anim2.setEndValue(value)
        self._anim2.start()

    def setColorTo(self, start: QColor, end: QColor) -> None:
        self._anim1.stop()
        self._anim1.setStartValue(self._color1)
        self._anim1.setEndValue(start)
        self._anim1.start()
        self._anim2.stop()
        self._anim2.setStartValue(self._color2)
        self._anim2.setEndValue(end)
        self._anim2.start()

    def parent(self) -> QWidget:
        return super().parent()

class Panel(QWidget):
    def __init__(self):
        super().__init__()
        self.background = GradientBackGroundStyle(self)
        self.border = BorderStyle(self)
        self.corner = CornerStyle(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|
                             QPainter.RenderHint.TextAntialiasing|
                             QPainter.RenderHint.SmoothPixmapTransform)
        rect = self.rect()
        # 绘制背景
        if self.background.type == self.background.Type.Linear:
            painter.fillRect(self.rect(), self.background.colorStart)
            x1, y1, x2, y2 = self.background.linearPoints
            # 将归一化坐标映射到实际窗口尺寸
            gradient = QLinearGradient(
                rect.width() * x1,
                rect.height() * y1,
                rect.width() * x2,
                rect.height() * y2
            )
        elif self.background.type == self.background.Type.Radial:
            center = QPoint(self.width()/2, self.height()/2)
            gradient = QRadialGradient(center, self.background.radialRadius, center)

        elif self.background.type == self.background.Type.Conical:
            # 锥形渐变
            center = QPoint(self.width()/2, self.height()/2)
            gradient = QConicalGradient(center, self.background.conicalAngle)
        # 设置渐变颜色，根据反向标志决定颜色顺序
        if not self.background.reverse:
            gradient.setColorAt(0.0, self.background.colorStart)
            gradient.setColorAt(1.0, self.background.colorEnd)
        else:
            gradient.setColorAt(0.0, self.background.colorEnd)
            gradient.setColorAt(1.0, self.background.colorStart)

        # 绘制渐变
        painter.fillRect(self.rect(), gradient)



def test():
    panel.background.setColorTo(QColor('#ff0000'), QColor('#00ff00'))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    panel = Panel()
    panel.resize(400, 300)
    btn = QPushButton('Change', panel)
    btn.setFont(QFont('Arial', 12))
    btn.setGeometry(10, 10, 100, 30)
    btn.clicked.connect(test)
    panel.show()
    app.exec()
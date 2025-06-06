from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ZQuickEffect:
    '''特效类，方便快速设置特效'''
    @staticmethod
    def applyDropShadowOn(widget: QWidget,
                          color: tuple[int, int, int, int]|None=None,
                          offset: tuple[int, int]|None=None,
                          blur_radius: int = 16):
        '设置阴影效果'
        if color is None:
            color = (0, 0, 0, 255)
        if offset is None:
            offset = (0, 0)

        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setColor(QColor(*color))
        shadow.setOffset(*offset)
        shadow.setBlurRadius(blur_radius)
        widget.setGraphicsEffect(shadow)

    @staticmethod
    def applyOpacityOn(widget: QWidget, opacity: float):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        widget.setGraphicsEffect(opacity_effect)


import math
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

__all__ = ['ZWidgetEffect']

class ZWidgetEffect:
    '''特效类，方便快速设置 ZWidget 特效'''
    @staticmethod
    def applyGraphicsShadow(widget: QWidget,
                            color: QColor = QColor(0, 0, 0, 40),
                            offset: QPoint = QPoint(0, 0),
                            blur: int = 16):
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setColor(color)
        shadow.setOffset(offset)
        shadow.setBlurRadius(blur)
        widget.setGraphicsEffect(shadow)


    @staticmethod
    def drawGraphicsShadow(painter: QPainter,
                        rect: QRect,
                        radius: float,
                        blur: int = 16,
                        offset: QPoint = QPoint(0, 0),
                        color: QColor = QColor(0, 0, 0, 40)):
        shadow_rect = QRectF(rect).translated(offset)
        # 控制初始透明度的比例
        max_alpha_ratio = 0.12
        for i in range(blur, 0, -1):
            # t 是归一化距离（0~1，i越大越靠近中心）
            t = i / blur
            # 指数衰减
            # 公式：alpha_ratio = max_alpha_ratio * e^(-k*(1-t))
            # 当 t=1（中心）时，alpha_ratio = max_alpha_ratio（初始值）
            # 当 t=0（边缘）时，alpha_ratio ≈ 0
            k = 3.0  # k越大，前期衰减越快（建议3~8之间调整）
            alpha_ratio = max_alpha_ratio * math.exp(-k * (1 - t))
            alpha = int(color.alpha() * alpha_ratio)
            if alpha <= 0: break
            c = QColor(color.red(), color.green(), color.blue(), alpha)
            expand = (blur - i) * 1.0
            r = QRectF(shadow_rect).adjusted(-expand, -expand, expand, expand)
            r_radius = max(0.0, radius + expand * 0.6)
            painter.save()
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(c)
            painter.drawRoundedRect(r, r_radius, r_radius)
            painter.restore()


    @staticmethod
    def applyOpacityOn(widget: QWidget, opacity: float):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        widget.setGraphicsEffect(opacity_effect)


    @staticmethod
    def applyBlurOn(widget: QWidget, radius: int):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(radius)
        widget.setGraphicsEffect(blur_effect)

    # region
    # @staticmethod
    # def drawGraphicsShadow(painter: QPainter,
    #                        rect: QRect,
    #                        radius: float,
    #                        blur: int = 16,
    #                        offset: QPoint = QPoint(0, 0),
    #                        color: QColor = QColor(0, 0, 0, 10)):
    #     shadow_rect = QRectF(rect).translated(offset)
    #     for i in range(blur, 0, -1):
    #         t = i / blur
    #         alpha = int(color.alpha() * (t **4))
    #         if alpha <= 0: break
    #         c = QColor(color.red(), color.green(), color.blue(), alpha)
    #         expand = (blur - i) * 1.0
    #         r = QRectF(shadow_rect).adjusted(-expand, -expand, expand, expand)
    #         r_radius = max(0.0, radius + expand * 0.6)
    #         painter.save()
    #         painter.setPen(Qt.PenStyle.NoPen)
    #         painter.setBrush(c)
    #         painter.drawRoundedRect(r, r_radius, r_radius)
    #         painter.restore()
    # endregion

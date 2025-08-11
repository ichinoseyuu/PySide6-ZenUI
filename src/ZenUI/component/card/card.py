from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRectF,Signal
from PySide6.QtGui import QPainter,QPen,QPainterPath
from ZenUI.component.base import ColorController,FloatController, LocationController,StyleData
from ZenUI.core import ZGlobal,ZCardStyleData

class ZCard(QWidget):
    resized = Signal()
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet('background-color:transparent;border: 1px solid red;')

        # style property
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._location_ctrl = LocationController(self)
        self._style_data = StyleData[ZCardStyleData](self, 'ZCard')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def locationCtrl(self): return self._location_ctrl

    @property
    def styleData(self): return self._style_data

    def _initStyle(self):
        data = self._style_data.data
        self._body_cc.color = data.Body
        self._border_cc.color = data.Border
        self._radius_ctrl.value = data.Radius
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._border_cc.setColorTo(data.Border)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._radius_ctrl.value
        if self._body_cc.color.alpha() > 0:
            # draw background
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self._border_cc.color.alpha() > 0:
        # draw border
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            # adjust border width
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
                radius,
                radius
            )
        painter.end()
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    #     rect = self.rect()
    #     # 获取四个角的半径
    #     r_tl = self._corner_style.radius.topLeft
    #     r_tr = self._corner_style.radius.topRight
    #     r_bl = self._corner_style.radius.bottomLeft
    #     r_br = self._corner_style.radius.bottomRight
    #     # 创建路径并添加圆角矩形
    #     path = QPainterPath()
    #     # 从左上角开始
    #     path.moveTo(rect.left(), rect.top() + r_tl)
    #     # 绘制左上角圆弧
    #     path.arcTo(rect.left(), rect.top(), 
    #             r_tl * 2, r_tl * 2, 
    #             180, -90)
    #     # 绘制上边线到右上角
    #     path.lineTo(rect.right() - r_tr, rect.top())
    #     # 绘制右上角圆弧
    #     path.arcTo(rect.right() - r_tr * 2, rect.top(), 
    #             r_tr * 2, r_tr * 2, 
    #             90, -90)
    #     # 绘制右边线到右下角
    #     path.lineTo(rect.right(), rect.bottom() - r_br)
    #     # 绘制右下角圆弧
    #     path.arcTo(rect.right() - r_br * 2, rect.bottom() - r_br * 2, 
    #             r_br * 2, r_br * 2, 
    #             0, -90)
    #     # 绘制下边线到左下角
    #     path.lineTo(rect.left() + r_bl, rect.bottom())
    #     # 绘制左下角圆弧
    #     path.arcTo(rect.left(), rect.bottom() - r_bl * 2, 
    #             r_bl * 2, r_bl * 2, 
    #             270, -90)
    #     # 闭合路径（回到起点）
    #     path.closeSubpath()
    #     # draw background
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(self._background_style.color)
    #     painter.drawPath(path)
    #     # draw border
    #     painter.setPen(QPen(self._border_style.color, self._border_style.width))
    #     painter.setBrush(Qt.NoBrush)
    #     painter.drawPath(path)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()
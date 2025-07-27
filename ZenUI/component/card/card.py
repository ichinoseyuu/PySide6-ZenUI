from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRectF,Signal
from PySide6.QtGui import QPainter,QPen,QPainterPath
from ZenUI.component.base import ColorManager,FloatManager, LocationManager
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
        self._body_color_mgr = ColorManager(self)
        self._border_color_mgr = ColorManager(self)
        self._radius_mgr = FloatManager(self)

        # animation property
        self._location_mgr = LocationManager(self)

        # style data
        self._style_data: ZCardStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__)

        ZGlobal.themeManager.themeChanged.connect(self.themeChangHandler)

    @property
    def bodyColorMgr(self): return self._body_color_mgr

    @property
    def borderColorMgr(self): return self._border_color_mgr

    @property
    def radiusMgr(self): return self._radius_mgr

    @property
    def locationMgr(self): return self._location_mgr

    @property
    def styleData(self): return self._style_data
    @styleData.setter
    def styleData(self, style_data: ZCardStyleData):
        self._style_data = style_data
        self._body_color_mgr.color = style_data.Body
        self._border_color_mgr.color = style_data.Border
        self._radius_mgr.value = style_data.Radius
        self.update()

    def themeChangHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData(self.__class__.__name__, theme.name)
        self._radius_mgr.value = data.Radius
        self._body_color_mgr.setColorTo(data.Body)
        self._border_color_mgr.setColorTo(data.Border)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._radius_mgr.value
        # draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_color_mgr.color)
        painter.drawRoundedRect(rect, radius, radius)
        # draw border
        painter.setPen(QPen(self._border_color_mgr.color, 1))
        painter.setBrush(Qt.NoBrush)
        # adjust border width
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            5,0)

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
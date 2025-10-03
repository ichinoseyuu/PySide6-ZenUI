from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint
from PySide6.QtWidgets import QWidget
from ZenUI.component.base import (
    ColorController,
    FloatController,
    OpacityController,
    SizeController,
    LocationController,
    StyleData,
    ABCButton,
    ZPosition)
from ZenUI.core import (
    ZButtonStyleData,
    ZDebug,
    ZGlobal
)

class ZComboBoxItem(ABCButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._font = QFont("Microsoft YaHei", 9)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._text_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._opacity_ctrl = OpacityController(self)



class ZComboBoxItemView(QWidget):
    def __init__(self, parent: QWidget, items: list[str]):
        super().__init__(parent)
        self._items = items
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._size_ctrl = SizeController(self)
        self._location_ctrl = LocationController(self)




class ZComboBox(ABCButton):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)

        self._items: list[str] = []
        self._list: ZComboBoxItemView = ZComboBoxItemView(self, self._items)
        self._text: str = ''
        self._drop_icon: QIcon = ZGlobal.getBuiltinIcon(u':/icons/arrow_down.svg')
        self._drop_icon_size = QSize(16, 16)
        self._font = QFont("Microsoft YaHei", 9)
        if text : self.text = text

        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._text_cc = ColorController(self)
        self._drop_icon_cc = ColorController(self)
        self._drop_icon_loc_ctrl = LocationController(self)
        self._radius_ctrl = FloatController(self)
        self._opacity_ctrl = OpacityController(self)
        self._style_data = StyleData[ZButtonStyleData](self, 'ZButton')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()
        self.resize(self.sizeHint())

    # region Property
    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def borderColorCtrl(self): return self._border_cc

    @property
    def textColorCtrl(self): return self._text_cc

    @property
    def radiusCtrl(self): return self._radius_ctrl

    @property
    def styleData(self): return self._style_data

    @property
    def text(self) -> str: return self._text
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()

    @property
    def font(self) -> QFont: return self._font
    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()

    # region public
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self._opacity_ctrl.fadeTo(1.0)
        else: self._opacity_ctrl.fadeTo(0.3)
        super().setEnabled(enable)

    def showList(self):
        pass

    def sizeHint(self):
        """重新实现sizeHint方法，更精确计算组合框合适尺寸"""
        # 基础内边距
        padding_left = 6
        padding_right = 6 + self._drop_icon_size.width() + 6  # 图标宽度+两侧边距
        padding_vertical = 4  # 上下内边距

        # 计算文本所需宽度
        text_width = self.fontMetrics().boundingRect(self._text).width() if self._text else 0
        # 计算总宽度：文本宽度 + 内边距
        total_width = text_width + padding_left + padding_right

        # 计算高度：字体高度 + 上下内边距，确保不小于图标高度
        font_height = self.fontMetrics().height()
        total_height = max(font_height + padding_vertical * 2, self._drop_icon_size.height() + 2)

        # 确保最小尺寸
        min_width = 60
        min_height = 30
        final_width = max(total_width, min_width)
        final_height = max(total_height, min_height)

        self.setMinimumSize(final_width, final_height)
        return QSize(final_width, final_height)


    # region private
    def _initStyle(self):
        data = self._style_data.data
        self._body_cc.color = data.Body
        self._text_cc.color = data.Text
        self._drop_icon_cc.color = data.Icon
        self._border_cc.color = data.Border
        self._radius_ctrl.value = data.Radius
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._border_cc.setColorTo(data.Border)
        self._text_cc.setColorTo(data.Text)
        self._drop_icon_cc.setColorTo(data.Icon)

    # region slot
    def hoverHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)

    def leaveHandler(self):
        self._body_cc.setColorTo(self._style_data.data.Body)


    def pressHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyPressed)

    def releaseHandler(self):
        self._body_cc.setColorTo(self._style_data.data.BodyHover)



    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self._opacity_ctrl.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self._radius_ctrl.value
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self._border_cc.color.alpha() > 0:
            # 绘制边框
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            # 调整矩形以避免边框模糊
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
                radius,
                radius
            )
        # 计算内容区域
        # 文本
        if self._text:
            painter.setFont(self._font)
            painter.setPen(self._text_cc.color)
            painter.drawText(
                rect.adjusted(6, 0, -24, 0),
                Qt.AlignLeft|Qt.AlignVCenter,
                self._text
                )
        # 图标
        if self._drop_icon:
            # 1. 获取原始 QPixmap
            pixmap = self._drop_icon.pixmap(self._drop_icon_size)
            # 2. 创建一个新的 QPixmap 用于着色
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
            colored_pixmap.fill(Qt.transparent)
            painter_pix = QPainter(colored_pixmap)
            painter_pix.drawPixmap(0, 0, pixmap)
            painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_pix.fillRect(colored_pixmap.rect(), self._drop_icon_cc.color)
            painter_pix.end()
            # 计算图标位置（右侧居中）
            icon_x = rect.right() - self._drop_icon_size.width() - 6  # 右侧距6px
            icon_y = (rect.height() - self._drop_icon_size.height()) // 2  # 垂直居中
            painter.drawPixmap(icon_x, icon_y, colored_pixmap)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


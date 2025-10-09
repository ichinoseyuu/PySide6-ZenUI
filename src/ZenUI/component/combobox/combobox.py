from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPointF,QPoint,Signal
from PySide6.QtWidgets import QWidget
from ZenUI.component.abstract import ABCButton
from ZenUI.component.window import ZFramelessWindow
from ZenUI.component.itemview import ZItemView
from ZenUI.component.base import (
    ColorController,
    FloatController,
    OpacityController,
    PointFController,
    StyleController,
    ZPadding
)
from ZenUI.core import (
    ZComboBoxStyleData,
    ZDebug,
    ZGlobal,
)

class ZComboBox(ABCButton):
    selected = Signal(str)
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    textColorCtrl: ColorController
    dropIconColorCtrl: ColorController
    dropIconPosCtrl: PointFController
    radiusCtrl: FloatController
    opacityCtrl: OpacityController
    styleDataCtrl: StyleController[ZComboBoxStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{
            'key': 'ZComboBox'
        },
    }
    def __init__(self,
                 options: list[str],
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._options: list[str] = options
        self._text: str = None
        self._drop_icon: QIcon = ZGlobal.getBuiltinIcon(u':/icons/arrow_down.svg')
        self._drop_icon_size = QSize(12, 12)
        self._padding = ZPadding(16, 8, 8, 8) # 内边距
        self._spacing: int = 16
        self._font = QFont("Microsoft YaHei", 9)
        if text : self.text = text

        self._item_view = ZItemView(self, self._options)
        self._item_view.selected.connect(self._select_handler_)

        self.dropIconPosCtrl.animation.setBias(0.1)
        self.dropIconPosCtrl.animation.setFactor(0.2)
        self._init_style_()
        self.resize(self.sizeHint())
        self.dropIconPosCtrl.setPos(self._get_drop_icon_pos())



    # region Property
    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()

    @property
    def opitions(self) -> list[str]: return self._options

    @property
    def font(self) -> QFont: return self._font

    @font.setter
    def font(self, f: QFont) -> None:
        self._font = f
        self.update()

    @property
    def spacing(self) -> int: return self._spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._spacing = spacing
        self.update()

    @property
    def padding(self) -> ZPadding: return self._padding

    @padding.setter
    def padding(self, padding: ZPadding) -> None:
        self._padding = padding
        self.update()

    # region public
    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(enable)

    def addItem(self, item: str) -> None:
        #self._options.append(item) # ZItemView 内部的i tems 与 _options 共用内存
        self._item_view.addItem(item)

    def removeItem(self, item: str) -> None:
        #self._options.remove(item)
        self._item_view.removeItem(item)

    def sizeHint(self):
        """重新实现sizeHint方法，更精确计算组合框合适尺寸"""
        text_width = self.fontMetrics().boundingRect(self._text).width() if self._text else 0
        total_width = text_width + self._drop_icon_size.width() + self._padding.horizontal + self._spacing
        font_height = self.fontMetrics().height()
        total_height = max(font_height + self._padding.vertical, self._drop_icon_size.height() + 2)
        min_width = 100
        min_height = 30
        final_width = max(total_width, min_width)
        final_height = max(total_height, min_height)
        self.setMinimumSize(final_width, final_height)
        return QSize(final_width, final_height)


    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.textColorCtrl.color = data.Text
        self.dropIconColorCtrl.color = data.Icon
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = data.Radius
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)
        self.textColorCtrl.setColorTo(data.Text)
        self.dropIconColorCtrl.setColorTo(data.Icon)

    # region slot
    def _hover_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)

    def _leave_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)


    def _press_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)
        self.dropIconPosCtrl.moveBy(0, 2)

    def _release_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)
        self.dropIconPosCtrl.moveTo(self._get_drop_icon_pos())

    def _click_handler_(self):
        self._item_view.show()

    def _select_handler_(self, item: str):
        self.text = item


    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)
        # 绘制背景
        rect = self.rect()
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self.borderColorCtrl.color.alpha() > 0:
            # 绘制边框
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
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
            painter.setPen(self.textColorCtrl.color)
            painter.drawText(
                rect.adjusted(self._padding.left, 0, 0, 0),
                Qt.AlignLeft|Qt.AlignVCenter,
                self._text
                )
        # 图标
        # 1. 获取原始 QPixmap
        pixmap = self._drop_icon.pixmap(self._drop_icon_size)
        # 2. 创建一个新的 QPixmap 用于着色
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self.dropIconColorCtrl.color)
        painter_pix.end()
        painter.drawPixmap(self.dropIconPosCtrl.pos, colored_pixmap)
        #print(self.dropIconPosCtrl.pos)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()


    def _get_drop_icon_pos(self):
        '''获取下拉图标位置'''
        rect = self.rect()
        icon_x = rect.right() - self._drop_icon_size.width() - self._padding.right  # 右侧距6px
        icon_y = (rect.height() - self._drop_icon_size.height()) // 2 + 1  # 垂直居中
        return QPointF(icon_x, icon_y)
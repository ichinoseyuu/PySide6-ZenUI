from PySide6.QtGui import QPainter,QFont,QPen,QIcon,QPixmap
from PySide6.QtCore import Qt,QSize,QRectF,QPointF,Signal
from PySide6.QtWidgets import QWidget
from typing import Any,Dict
from ZenWidgets.component.collections import ZItemView
from ZenWidgets.component.base import (
    QAnimatedColor,
    QAnimatedFloat,
    ZAnimatedPointF,
    StyleController,
    ZPadding,
    ABCButton
)
from ZenWidgets.core import (
    ZDebug,
    ZGlobal,
)
from ZenWidgets.gui import ZComboBoxStyleData

# region ZComboBox
class ZComboBox(ABCButton):
    optionChanged = Signal(str, object)

    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    textColorCtrl: QAnimatedColor
    dropIconColorCtrl: QAnimatedColor
    dropIconPosCtrl: ZAnimatedPointF
    radiusCtrl: QAnimatedFloat
    layerColorCtrl: QAnimatedColor
    styleDataCtrl: StyleController[ZComboBoxStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{'key': 'ZComboBox'},
        'radiusCtrl': {'value': 5.0},
    }
    def __init__(self,
                 parent: QWidget = None,
                 options: Dict[str, Any]= None,
                 text: str = None,
                 font: QFont = QFont("Microsoft YaHei", 9),
                 objectName: str | None = None
                 ):
        super().__init__(parent=parent,
                         objectName=objectName,
                         font=font,
                         focusPolicy=Qt.FocusPolicy.ClickFocus
                         )
        self._options: Dict[str, Any] = {}
        self._text: str = None
        self._drop_icon: QIcon = ZGlobal.getBuiltinIcon(u':/icons/arrow_down.svg')
        self._drop_icon_size = QSize(12, 12)
        self._padding = ZPadding(8, 8, 8, 8)
        self._spacing: int = 16
        if text :self._text = text
        if options: self._options = options
        self._options_view = ZItemView(self, self._options.keys())
        self._options_view.selected.connect(self._select_handler_)

        self.dropIconPosCtrl.animation.setBias(0.1)
        self.dropIconPosCtrl.animation.setFactor(0.2)
        self._init_style_()
        self.resize(self.sizeHint())
        self.dropIconPosCtrl.setPos(self._get_drop_icon_pos())


    # region public method
    def options(self) -> Dict[str, Any]:
        return self._options

    def currentValue(self) -> Any | None:
        if self._text in self._options:
            return self._options[self._text]
        return None

    def text(self) -> str: return self._text

    def setText(self, t: str) -> None:
        self._text = t
        self.update()

    def spacing(self) -> int: return self._spacing

    def setSpacing(self, s: int) -> None:
        self._spacing = s
        self.update()

    def padding(self) -> ZPadding: return self._padding

    def setPadding(self, p: ZPadding) -> None:
        self._padding = p
        self.update()

    def addOption(self, key: str, value: Any = None) -> None:
        #self._options.append(item) # ZItemView 内部的items 与 _options 共用内存
        self._options[key] = value
        self._options_view.addItem(key)
        # if key == self._text:
        #     self._options_view.selectItem(key)

    def removeOption(self, key: str) -> None:
        if key in self._options:
            del self._options[key]
            self._options_view.removeItem(key)
            if self._text == key:
                self._text = None
                self.update()

    def sizeHint(self):
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


    # region private method
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.dropIconColorCtrl.color = data.Icon
        self.textColorCtrl.color = data.Text
        self.layerColorCtrl.color = ZGlobal.palette.Transparent_reverse()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)
        self.dropIconColorCtrl.setColorTo(data.Icon)
        self.textColorCtrl.setColorTo(data.Text)
        self.layerColorCtrl.color = ZGlobal.palette.Transparent_reverse()

    # region slot
    def _hover_handler_(self):
        self.layerColorCtrl.setAlphaFTo(0.03)

    def _leave_handler_(self):
        self.layerColorCtrl.toTransparent()

    def _press_handler_(self):
        self.layerColorCtrl.setAlphaFTo(0.05)
        self.dropIconPosCtrl.moveBy(0, 2)

    def _release_handler_(self):
        self.layerColorCtrl.setAlphaFTo(0.03)
        self.dropIconPosCtrl.moveTo(self._get_drop_icon_pos())

    def _click_handler_(self):
        self._options_view.show()

    def _select_handler_(self, item: str):
        if item in self._options:
            self._text = item
            self.optionChanged.emit(item, self._options[item])
            self.update()

    # region event
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        rect = self.rect()
        radius = self.radiusCtrl.value

        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)

        if self.layerColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.layerColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        if self._text:
            painter.setFont(self.font())
            painter.setPen(self.textColorCtrl.color)
            painter.drawText(
                rect.adjusted(self._padding.left, 0, 0, 0),
                Qt.AlignLeft|Qt.AlignVCenter,
                self._text
                )

        pixmap = self._drop_icon.pixmap(self._drop_icon_size)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.setDevicePixelRatio(self.devicePixelRatioF())
        colored_pixmap.fill(Qt.transparent)
        painter_pix = QPainter(colored_pixmap)
        painter_pix.drawPixmap(0, 0, pixmap)
        painter_pix.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter_pix.fillRect(colored_pixmap.rect(), self.dropIconColorCtrl.color)
        painter_pix.end()
        painter.drawPixmap(self.dropIconPosCtrl.pos, colored_pixmap)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()
        event.accept()


    def _get_drop_icon_pos(self):
        '''获取下拉图标位置'''
        rect = self.rect()
        icon_x = rect.right() - self._drop_icon_size.width() - self._padding.right
        icon_y = (rect.height() - self._drop_icon_size.height()) // 2 + 1
        return QPointF(icon_x, icon_y)
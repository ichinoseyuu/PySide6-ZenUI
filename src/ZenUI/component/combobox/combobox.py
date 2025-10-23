from PySide6.QtGui import QPainter,QFont,QPen,QIcon,QPixmap
from PySide6.QtCore import Qt,QSize,QRectF,QPointF,Signal
from PySide6.QtWidgets import QWidget
from typing import Any,Dict
from ZenUI.component.abstract import ABCButton
from ZenUI.component.itemview import ZItemView
from ZenUI.component.base import (
    QAnimatedColor,
    QAnimatedFloat,
    ZAnimatedOpacity,
    ZAnimatedPointF,
    StyleController,
    ZPadding,
)
from ZenUI.core import (
    ZComboBoxStyleData,
    ZDebug,
    ZGlobal,
)

# region ZComboBox
class ZComboBox(ABCButton):
    optionChanged = Signal(str, object)

    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    textColorCtrl: QAnimatedColor
    dropIconColorCtrl: QAnimatedColor
    dropIconPosCtrl: ZAnimatedPointF
    radiusCtrl: QAnimatedFloat
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: StyleController[ZComboBoxStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZComboBox'}}

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 options: Dict[str, Any]= None,
                 text: str = None,
                 ):
        super().__init__(parent=parent, font=QFont("Microsoft YaHei", 9))
        if name: self.setObjectName(name)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
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
    @property
    def options(self) -> Dict[str, Any]:
        return self._options

    @property
    def currentValue(self) -> any:
        if self._text in self._options:
            return self._options[self._text]
        return None

    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, t: str) -> None:
        self._text = t
        self.update()

    def setText(self, t: str) -> None:
        self.text = t

    @property
    def spacing(self) -> int: return self._spacing

    @spacing.setter
    def spacing(self, s: int) -> None:
        self._spacing = s
        self.update()

    def setSpacing(self, s: int) -> None:
        self.spacing = s

    @property
    def padding(self) -> ZPadding: return self._padding

    @padding.setter
    def padding(self, p: ZPadding) -> None:
        self._padding = p
        self.update()

    def setPadding(self, p: ZPadding) -> None:
        self.padding = p

    def setEnabled(self, enable: bool) -> None:
        if enable == self.isEnabled(): return
        if enable: self.opacityCtrl.fadeTo(1.0)
        else: self.opacityCtrl.fadeTo(0.3)
        super().setEnabled(enable)

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
        self._options_view.show()

    def _select_handler_(self, item: str):
        if item in self._options:
            self._text = item
            self.optionChanged.emit(item, self._options[item])
            self.update()

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing|
            QPainter.RenderHint.TextAntialiasing|
            QPainter.RenderHint.SmoothPixmapTransform
            )
        painter.setOpacity(self.opacityCtrl.opacity)
        rect = self.rect()
        radius = self.radiusCtrl.value
        if self.bodyColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.bodyColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)
        if self.borderColorCtrl.color.alpha() > 0:
            painter.setPen(QPen(self.borderColorCtrl.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius, radius
                )
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


    def _get_drop_icon_pos(self):
        '''获取下拉图标位置'''
        rect = self.rect()
        icon_x = rect.right() - self._drop_icon_size.width() - self._padding.right
        icon_y = (rect.height() - self._drop_icon_size.height()) // 2 + 1
        return QPointF(icon_x, icon_y)
from PySide6.QtGui import QPainter,QFont,QPen,QIcon,QPixmap
from PySide6.QtCore import Qt,QRect,QSize,QRectF,Signal,QMargins,QPoint,QEvent
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.layout import ZVBoxLayout
from ZenWidgets.component.base import (
    QAnimatedColor,
    QAnimatedFloat,
    ZAnimatedOpacity,
    StyleController,
    ZWidget,
    ZButtonGroup,
    ZPadding,
    ZMargin,
    ABCToggleButton
)
from ZenWidgets.core import (
    ZDebug,
    ZQuickEffect,
)
from ZenWidgets.gui import ZItemStyleData, ZItemViewStyleData

# region ZItem
class ZItem(ABCToggleButton):
    indicatorWidth = 3
    layerColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    textColorCtrl: QAnimatedColor
    iconColorCtrl: QAnimatedColor
    indicatorColorCtrl: QAnimatedColor
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: StyleController[ZItemStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZItem'}}

    def __init__(self,
                 parent: QWidget = None,
                 text: str | None = None,
                 font=QFont("Microsoft YaHei", 9),
                 icon: QIcon | None = None,
                 checked: bool = False,
                 objectName: str | None = None,
                 ):
        super().__init__(parent=parent,
                         checked=checked,
                         is_group_member=True,
                         objectName=objectName,
                         font=font,
                         )
        self._text: str | None = text
        self._icon: QIcon | None = icon
        self._icon_size = QSize(16, 16)
        self._padding = ZPadding(4, 4, 16, 4)
        self._spacing = 4
        self._init_style_()
        self.resize(self.sizeHint())

    # region public method
    def text(self) -> str: return self._text

    def setText(self, t: str) -> None:
        self._text = t
        self.update()

    def icon(self) -> QIcon: return self._icon

    def setIcon(self, i: QIcon) -> None:
        self._icon = i
        self.update()

    def iconSize(self) -> QSize: return self._icon_size

    def setIconSize(self, s: QSize) -> None:
        self._icon_size = s
        self.update()

    def spacing(self) -> int: return self._spacing

    def setSpacing(self, s: int) -> None:
        self._spacing = s
        self.update()

    def padding(self) -> ZPadding: return self._padding

    def setPadding(self, p: ZPadding) -> None:
        self._padding = p
        self.update()

    def sizeHint(self):
        # 宽度由父控件决定，这里只计算高度
        content_height = 0
        if self._icon:
            content_height = max(content_height, self._icon_size.height())
        if self._text:
            text_height = self.fontMetrics().height()
            content_height = max(content_height, text_height)
        # 加上内边距
        total_height = content_height + self._padding.top + self._padding.bottom
        # 确保最小高度
        min_height = 26
        total_height = max(total_height, min_height)
        return QSize(self.width(), total_height)


    # region private method
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.layerColorCtrl.color = data.Layer
        self.textColorCtrl.color = data.Text
        self.iconColorCtrl.color = data.Icon
        self.indicatorColorCtrl.color = data.Indicator
        self.radiusCtrl.value = 5.0
        if self._checked:
            self.indicatorColorCtrl.opaque()
        else:
            self.indicatorColorCtrl.transparent()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.indicatorColorCtrl.color = data.Indicator
        self.layerColorCtrl.color = data.Layer
        self.textColorCtrl.setColorTo(data.Text)
        self.iconColorCtrl.setColorTo(data.Icon)
        if self._checked:
            self.indicatorColorCtrl.toOpaque()
        else:
            self.indicatorColorCtrl.toTransparent()

    # region slot
    def _hover_handler_(self):
        self.layerColorCtrl.setAlphaTo(16)

    def _leave_handler_(self):
        self.layerColorCtrl.setAlphaTo(0)

    def _press_handler_(self):
        self.layerColorCtrl.setAlphaTo(10)

    def _release_handler_(self):
        self.layerColorCtrl.setAlphaTo(16)

    def _toggle_handler_(self, checked):
        if checked:
            self.indicatorColorCtrl.toOpaque()
        else:
            self.indicatorColorCtrl.toTransparent()

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
        if self.layerColorCtrl.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.layerColorCtrl.color)
            painter.drawRoundedRect(rect, radius, radius)

        p = self._padding
        fm = self.fontMetrics()
        text_height = fm.height()
        indicator_w = self.indicatorWidth
        spacing = self._spacing
        content_rect = rect.adjusted(p.left, p.top, -p.right, -p.bottom)
        text_area_left = content_rect.left() + indicator_w + spacing

        if self._checked and self.indicatorColorCtrl.color.alpha() > 0:
            indicator_h = max(2.0, min(content_rect.height(), text_height - fm.descent()))
            indicator_y = content_rect.center().y() - indicator_h / 2
            indicator_x = content_rect.left()
            indicator_rect = QRectF(indicator_x, indicator_y, indicator_w, indicator_h)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.indicatorColorCtrl.color)
            painter.drawRoundedRect(indicator_rect, indicator_w / 2, indicator_w / 2)

        content_available_rect = QRect(
            text_area_left,
            content_rect.top(),
            content_rect.width() - (text_area_left - content_rect.left()),
            content_rect.height()
        )

        icon_draw = False
        icon_right = content_available_rect.left()
        if self._icon:
            icon_y = (content_available_rect.height() - self._icon_size.height()) // 2 + content_available_rect.top()
            pixmap = self._icon.pixmap(self._icon_size)
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.fill(Qt.transparent)
            with QPainter(colored_pixmap) as p:
                p.drawPixmap(0, 0, pixmap)
                p.setCompositionMode(QPainter.CompositionMode_SourceIn)
                p.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
            painter.drawPixmap(content_available_rect.left(), icon_y, colored_pixmap)
            icon_draw = True
            icon_right = content_available_rect.left() + self._icon_size.width() + spacing

        if self._text:
            text_rect = QRect(
                icon_right if icon_draw else content_available_rect.left(),
                content_available_rect.top(),
                content_available_rect.width() - (icon_right - content_available_rect.left()),
                content_available_rect.height()
            )
            painter.setFont(self.font())
            painter.setPen(self.textColorCtrl.color)
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self._text)

        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()
        event.accept()

# region ViewContent
class ViewContent(ZWidget):
    bodyColorCtrl: QAnimatedColor
    borderColorCtrl: QAnimatedColor
    radiusCtrl: QAnimatedFloat
    styleDataCtrl: StyleController[ZItemViewStyleData]
    __controllers_kwargs__ = {'styleDataCtrl':{'key': 'ZItemView'}}

    def __init__(self, parent: QWidget, items: list[str] = None):
        super().__init__(parent)
        self._items: list[str] = items
        self._layout = ZVBoxLayout(
            parent=self,
            margins=QMargins(4, 4, 4, 4),
            spacing=2)
        self._item_group = ZButtonGroup(self)
        self._item_group.clicked.connect(self._item_clicked_handler_)

        self._init_style_()
        self._init_items_()

    def items(self) -> list[ZItem]:
        return self._item_group.buttons()

    def addItem(self, text: str):
        self._items.append(text)
        item = ZItem(self, text=text)
        self._layout.addWidget(item)
        self._item_group.addButton(item)
        self.resize(self.sizeHint())

    def removeItem(self, text: str):
        for item in self._item_group.buttons():
            if isinstance(item, ZItem) and item.text() == text:
                self._items.remove(text)
                item.clicked.disconnect()
                item.deleteLater()
                self._item_group.removeButton(item)
                self._layout.removeWidget(item)
                break
        self.resize(self.sizeHint())

    def selectItem(self, text: str):
        for item in self._item_group.buttons():
            if isinstance(item, ZItem) and item.text() == text:
                self._item_group.checkedButton().setChecked(False)
                item.setChecked(True)

    def sizeHint(self):
        total_height = 0
        # 加上布局边距
        total_height += self._layout.contentsMargins().top() + self._layout.contentsMargins().bottom()

        # 加上所有item高度和间距
        item_count = self._layout.count()
        for i in range(item_count):
            item = self._layout.itemAt(i).widget()
            if isinstance(item, ZItem):
                total_height += item.sizeHint().height()

        # 加上间距
        if item_count > 0:
            total_height += self._layout.spacing() * (item_count - 1)

        return QSize(self.width(), total_height)

    def parent(self) -> 'ZItemView':
        return super().parent()


    # region private method
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = 5.0
        self.update()


    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)

    def _init_items_(self):
        if not self._items:
            self._items = []
            return
        for text in self._items:
            item = ZItem(self, text=text)
            self._layout.addWidget(item)
            self._item_group.addButton(item)
        self.resize(self.sizeHint())


    def _item_clicked_handler_(self):
        checked_item = self._item_group.checkedButton()
        if isinstance(checked_item, ZItem):
            self.parent().selected.emit(checked_item._text)
        self.parent().windowOpacityCtrl.fadeOut()

    # region event
    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
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
        painter.end()
        event.accept()

# region ZItemView
class ZItemView(ZWidget):
    selected = Signal(str)
    def __init__(self,target: QWidget = None,items: list[str] = None):
        super().__init__(f=Qt.WindowType.FramelessWindowHint|Qt.WindowType.Tool|Qt.WindowType.WindowStaysOnTopHint)
        self._target: QWidget = target
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._content = ViewContent(self, items)
        self._content.setFixedWidth(self._target.sizeHint().width()+self._content.layout().contentsMargins().left()+ZItem.indicatorWidth)
        self._margin = ZMargin(8, 8, 8, 8)
        self.windowOpacityCtrl.animation.setBias(0.02)
        self.windowOpacityCtrl.animation.setFactor(0.2)
        self.windowOpacityCtrl.completelyHide.connect(self._completely_hide_)
        self.resize(self.sizeHint())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)

    def content(self): return self._content

    def selectedItem(self): return self._content._item_group.checkedButton()

    def getSlectedItem(self): return self._content._item_group.checkedButton()

    def parent(self): return self._target

    def target(self): return self._target

    def sizeHint(self):
        return self._content.sizeHint() + QSize(self._margin.horizontal, self._margin.vertical)

    def show(self):
        super().show()
        self.move(self._get_ancher_position_())
        self.widgetSizeCtrl.resizeFromTo(QSize(self.width(),0),self.sizeHint())
        self.setFocus(Qt.FocusReason.PopupFocusReason)
        self.activateWindow()
        self.raise_()


    def addItem(self, text: str):
        self._content.addItem(text)
        self.resize(self.sizeHint())

    def removeItem(self, text: str):
        self._content.removeItem(text)
        self.resize(self.sizeHint())

    def selectItem(self, text: str):
        self._content.selectItem(text)


    # region event
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.move(self._margin.left, self._margin.top)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
        event.accept()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.windowOpacityCtrl.fadeIn()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.windowOpacityCtrl.fadeOut()

    def _get_ancher_position_(self) -> QPoint:
        """获取锚点位置"""
        target = self._target
        checked_item = self._content._item_group.checkedButton()
        offset = QPoint(
            self._margin.left + ZItem.indicatorWidth,
            self._margin.top - (target.height() - checked_item.height())//2
            )
        parent_pos = target.mapToGlobal(target.rect().topLeft())
        return parent_pos - checked_item.geometry().topLeft() - offset

    def _completely_hide_(self):
        self.hide()
        self.close()
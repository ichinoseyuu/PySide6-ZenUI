from typing import cast
from PySide6.QtGui import QPainter,QFont,QPen,QIcon,QPixmap
from PySide6.QtCore import Qt,QRect,QSize,QRectF,Signal,QMargins,QPoint,QEvent
from PySide6.QtWidgets import QWidget
from ZenWidgets.component.layout import ZVBoxLayout
from ZenWidgets.component.base import (
    ZOpacityEffect,
    ZAnimatedColor,
    QAnimatedFloat,
    ZAnimatedOpacity,
    ZStyleController,
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
    opacityEffectCtrl: ZOpacityEffect
    radiusCtrl: QAnimatedFloat
    textColorCtrl: ZAnimatedColor
    iconColorCtrl: ZAnimatedColor
    indicatorColorCtrl: ZAnimatedColor
    opacityCtrl: ZAnimatedOpacity
    styleDataCtrl: ZStyleController[ZItemStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{'key': 'ZItem'},
        'radiusCtrl': {'value': 4.0},
    }
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
        self.textColorCtrl.color = data.Text
        self.iconColorCtrl.color = data.Icon
        self.indicatorColorCtrl.color = data.Indicator
        if self._checked:
            self.indicatorColorCtrl.opaque()
        else:
            self.indicatorColorCtrl.transparent()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.indicatorColorCtrl.color = data.Indicator
        self.textColorCtrl.setColorTo(data.Text)
        self.iconColorCtrl.setColorTo(data.Icon)
        if self._checked:
            self.indicatorColorCtrl.toOpaque()
        else:
            self.indicatorColorCtrl.toTransparent()

    # region slot
    def _hover_handler_(self):
        self.opacityEffectCtrl.setAlphaFTo(0.11)

    def _leave_handler_(self):
        self.opacityEffectCtrl.toTransparent()

    def _press_handler_(self):
        self.opacityEffectCtrl.setAlphaFTo(0.16)

    def _release_handler_(self):
        self.opacityEffectCtrl.setAlphaFTo(0.11)

    def _toggle_handler_(self, checked):
        self.opacityEffectCtrl.toTransparent()
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
        self.opacityEffectCtrl.drawOpacityLayer(painter, rect, radius)

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
    bodyColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: QAnimatedFloat
    styleDataCtrl: ZStyleController[ZItemViewStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{'key': 'ZItemView'},
        'radiusCtrl': {'value': 5.0},
    }
    def __init__(self, parent: QWidget, items: list[str] = None):
        super().__init__(parent)
        self._items: list[str] = items or []
        self._layout = ZVBoxLayout(
            parent=self,
            margins=QMargins(4, 4, 4, 4),
            spacing=2)
        self._item_group = ZButtonGroup(self)
        self._item_group.toggled.connect(self._item_toggle_handler_)

        self._init_style_()
        self._init_items_()

    def addItem(self, text: str):
        item = ZItem(self, text=text)
        self._layout.addWidget(item)
        self._item_group.addButton(item, set_first_checked=False)
        self._items.append(text)  # 直接在这里添加
        self.resize(self.sizeHint())

    def addItems(self, texts: list[str]):
        for text in texts:
            item = ZItem(self, text=text)
            self._layout.addWidget(item)
            self._item_group.addButton(item, set_first_checked=False)
            self._items.append(text)
        self.resize(self.sizeHint())

    def removeItem(self, text: str):
        for item in self._item_group.buttons():
            item = cast(ZItem, item)
            if item.text() == text:
                self._items.remove(text)
                item.clicked.disconnect()
                item.deleteLater()
                self._item_group.removeButton(item)
                self._layout.removeWidget(item)
                break
        self.resize(self.sizeHint())

    def toggleTo(self, text: str):
        for item in self._item_group.buttons():
            item = cast(ZItem, item)
            if item.text() == text:
                try:self._item_group.checkedButton().setChecked(False)
                except:pass
                item.setChecked(True)
                break

    def sizeHint(self):
        total_height = self._layout.contentsMargins().top() + self._layout.contentsMargins().bottom()
        total_height += sum(cast(ZItem, self._layout.itemAt(i).widget()).sizeHint().height() for i in range(self._layout.count()))
        if self._layout.count() > 0:
            total_height += self._layout.spacing() * (self._layout.count() - 1)
        return QSize(self.width(), total_height)

    def parent(self) -> 'ZItemView':
        return super().parent()

    # region private method
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
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

    def _item_toggle_handler_(self):
        checked_item = cast(ZItem, self._item_group.checkedButton())
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
    def __init__(self, target: QWidget = None,items: list[str] = None):
        super().__init__(f=Qt.WindowType.FramelessWindowHint|Qt.WindowType.Tool|Qt.WindowType.WindowStaysOnTopHint)
        self._target: QWidget = target
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._content = ViewContent(self, items)
        self._margin = ZMargin(8, 8, 8, 8)
        self.windowOpacityCtrl.animation.setBias(0.02)
        self.windowOpacityCtrl.animation.setFactor(0.2)
        self.windowOpacityCtrl.completelyHide.connect(self._completely_hide_)
        self.resize(self.sizeHint())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)

    def addItem(self, text: str):
        self._content.addItem(text)
        self.resize(self.sizeHint())

    def addItems(self, texts: list[str]):
        self._content.addItems(texts)
        self.resize(self.sizeHint())

    def removeItem(self, text: str):
        self._content.removeItem(text)
        self.resize(self.sizeHint())

    def toggleTo(self, text: str):
        self._content.toggleTo(text)

    def parent(self): return self._target

    def sizeHint(self):
        return self._content.sizeHint() + QSize(self._margin.horizontal, self._margin.vertical)

    def show(self):
        self._content.setFixedWidth(self._target.sizeHint().width()+self._content.layout().contentsMargins().left()+ZItem.indicatorWidth)
        super().show()
        self.move(self._get_ancher_position_())
        self.widgetSizeCtrl.resizeFromTo(QSize(self.width(),0),self.sizeHint())
        self.setFocus(Qt.FocusReason.PopupFocusReason)
        self.activateWindow()
        self.raise_()

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
        offset = QPoint(self._margin.left + ZItem.indicatorWidth,self._margin.top - target.height())
        if not checked_item: return target.mapToGlobal(target.rect().topLeft()) - offset
        offset += QPoint(0, (target.height() + checked_item.height())//2)
        parent_pos = target.mapToGlobal(target.rect().topLeft())
        return parent_pos - checked_item.geometry().topLeft() - offset

    def _completely_hide_(self):
        self.hide()
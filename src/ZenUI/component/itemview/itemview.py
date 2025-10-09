import logging
from PySide6.QtGui import QPainter, QFont, QPen, QIcon, QPixmap, QCursor
from PySide6.QtCore import Qt, QRect, QSize, QRectF, QPoint,QMargins,Signal
from PySide6.QtWidgets import QWidget,QApplication
from ZenUI.component.abstract import ABCToggleButton
from ZenUI.component.layout import ZVBoxLayout
from ZenUI.component.base import (
    ColorController,
    FloatController,
    OpacityController,
    WindowOpacityController,
    WidgetSizeController,
    PositionController,
    StyleController,
    ZWidget,
    ButttonGroup,
    ZPadding,
    ZMargin
    )
from ZenUI.core import (
    ZItemStyleData,
    ZItemViewStyleData,
    ZDebug,
    CoordConverter,
    ZQuickEffect,
)

# region - ZItem
class ZItem(ABCToggleButton):
    bodyColorCtrl: ColorController
    textColorCtrl: ColorController
    iconColorCtrl: ColorController
    indicatorColorCtrl: ColorController
    radiusCtrl: FloatController
    opacityCtrl: OpacityController
    styleDataCtrl: StyleController[ZItemStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{
            'key': 'ZItem'
        },
    }
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None,
                 icon: QIcon = None,
                 checked: bool = False,
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self.isGroupMember = True

        self._text: str = None
        self._icon: QIcon = None
        self._icon_size = QSize(16, 16)
        self._font = QFont("Microsoft YaHei", 9)
        self._indicator_width = 3
        self._padding = ZPadding(4, 4, 16, 4)
        self._spacing = 6
        if text : self.text = text
        if icon : self.icon = icon
        if checked: self._checked = checked

        self._init_style_()
        self.resize(self.sizeHint())

    # region property
    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()

    @property
    def icon(self) -> QIcon: return self._icon

    @icon.setter
    def icon(self, icon: QIcon) -> None:
        self._icon = icon
        self.update()

    @property
    def iconSize(self) -> QSize: return self._icon_size

    @iconSize.setter
    def iconSize(self, size: QSize) -> None:
        self._icon_size = size
        self.update()

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
        min_height = 28
        total_height = max(total_height, min_height)

        return QSize(self.width(), total_height)


    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.textColorCtrl.color = data.Text
        self.iconColorCtrl.color = data.Icon
        self.indicatorColorCtrl.color = data.Indicator
        self.radiusCtrl.value = data.Radius
        if self.checked:
            self.indicatorColorCtrl.opaque()
        else:
            self.indicatorColorCtrl.transparent()
        self.update()

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.indicatorColorCtrl.color = data.Indicator
        self.bodyColorCtrl.setColorTo(data.Body)
        self.textColorCtrl.setColorTo(data.Text)
        self.iconColorCtrl.setColorTo(data.Icon)
        if self.checked:
            self.indicatorColorCtrl.toOpaque()
        else:
            self.indicatorColorCtrl.toTransparent()

    # region slot
    def _hover_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)

    def _leave_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.Body)

    def _press_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyPressed)

    def _release_handler_(self):
        self.bodyColorCtrl.setColorTo(self.styleDataCtrl.data.BodyHover)

    def _toggle_handler_(self, checked):
        if checked:
            self.indicatorColorCtrl.toOpaque()
        else:
            self.indicatorColorCtrl.toTransparent()

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

        # 绘制左侧指示器（仅当选中时）
        if self.checked and self.indicatorColorCtrl.color.alpha() > 0:
            indicator_width = self._indicator_width
            indicator_rect = QRect(
                self._padding.left,  # 左内边距作为起始位置
                self._padding.top,   # 上内边距
                indicator_width,  # 指示器宽度
                rect.height() - self._padding.vertical-2 # 指示器高度（减去上下内边距）
            )
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.indicatorColorCtrl.color)
            painter.drawRoundedRect(indicator_rect, indicator_width/2, indicator_width/2)


        # 计算内容区域
        content_left = self._padding.left + self._spacing + self._indicator_width
        content_top = self._padding.top
        content_right = rect.width() - self._padding.right + 1
        content_bottom = rect.height() - self._padding.bottom
        content_rect = QRect(content_left, content_top,
                            content_right - content_left,
                            content_bottom - content_top)

        # 绘制图标和文本（合并处理）
        icon_draw = False
        if self._icon:
            icon_y = (content_rect.height() - self._icon_size.height()) // 2 + content_rect.top()
            pixmap = self._icon.pixmap(self._icon_size)
            colored_pixmap = QPixmap(pixmap.size())
            colored_pixmap.fill(Qt.transparent)
            with QPainter(colored_pixmap) as p:
                p.drawPixmap(0, 0, pixmap)
                p.setCompositionMode(QPainter.CompositionMode_SourceIn)
                p.fillRect(colored_pixmap.rect(), self.iconColorCtrl.color)
            painter.drawPixmap(content_rect.left(), icon_y, colored_pixmap)
            icon_draw = True

        # 绘制文本
        if self._text:
            text_rect = content_rect
            if icon_draw:
                text_rect = text_rect.adjusted(
                    self._icon_size.width() + self._spacing,
                    0, 0, 0
                )
            painter.setFont(self._font)
            painter.setPen(self.textColorCtrl.color)
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self._text)

        if ZDebug.draw_rect: ZDebug.drawRect(painter, rect)
        painter.end()

# region - ItemViewContent
class ItemViewContent(ZWidget):
    bodyColorCtrl: ColorController
    borderColorCtrl: ColorController
    radiusCtrl: FloatController
    styleDataCtrl: StyleController[ZItemViewStyleData]
    __controllers_kwargs__ = {
        'styleDataCtrl':{
            'key': 'ZItemView'
        },
    }
    def __init__(self, parent: QWidget, items: list[str]):
        super().__init__(parent)
        self._items: list[str] = items
        self._layout = ZVBoxLayout(
            parent=self,
            margins=QMargins(4, 4, 4, 4),
            spacing=2)
        self._item_group = ButttonGroup(self)
        self._item_group.clicked.connect(self._item_clicked_handler_)

        self._init_style_()
        self._init_items_()


    def addItem(self, text: str):
        self._items.append(text)
        item = ZItem(self, text=text)
        self._layout.addWidget(item)
        self._item_group.addButton(item)
        self.resize(self.sizeHint())

    def removeItem(self, text: str):
        for item in self._item_group.buttons():
            if isinstance(item, ZItem) and item.text == text:
                self._items.remove(text)
                item.clicked.disconnect()
                item.deleteLater()
                self._item_group.removeButton(item)
                self._layout.removeWidget(item)
                break
        self.resize(self.sizeHint())

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


    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.borderColorCtrl.color = data.Border
        self.radiusCtrl.value = data.Radius
        self.update()


    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.radiusCtrl.value = data.Radius
        self.bodyColorCtrl.setColorTo(data.Body)
        self.borderColorCtrl.setColorTo(data.Border)

    def _init_items_(self):
        for text in self._items:
            item = ZItem(self, text=text)
            self._layout.addWidget(item)
            self._item_group.addButton(item)
        self.resize(self.sizeHint())


    def _item_clicked_handler_(self):
        checked_item = self._item_group.checkedButton()
        if isinstance(checked_item, ZItem):
            self.parent().selected.emit(checked_item.text)
        self.parent().opacityCtrl.fadeOut()

    # region event
    def paintEvent(self, event):
        painter = QPainter(self)
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
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
                radius,
                radius
            )
        painter.end()

# region - ItemView
class ZItemView(ZWidget):
    selected = Signal(str)
    sizeCtrl: WidgetSizeController
    positionCtrl: PositionController
    opacityCtrl: WindowOpacityController
    def __init__(self,
                 target: QWidget,
                 items: list[str]
                 ):
        super().__init__()
        self._target: QWidget = target
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint|
            Qt.WindowType.Tool|
            Qt.WindowType.WindowStaysOnTopHint
            )
        self._content = ItemViewContent(self, items)
        self._content.setFixedWidth(self._target.sizeHint().width())
        self._margin = ZMargin(8, 8, 8, 8)

        self.opacityCtrl.animation.setBias(0.02)
        self.opacityCtrl.animation.setFactor(0.2)
        self.opacityCtrl.animation.finished.connect(self._completely_hid_signal_handler)

        self.resize(self.sizeHint())
        ZQuickEffect.applyDropShadowOn(widget=self._content,color=(0, 0, 0, 40),blur_radius=12)

    @property
    def content(self): return self._content

    @property
    def selectedItem(self): return self._content._item_group.checkedButton()

    def parent(self): return self._target

    def target(self): return self._target

    def sizeHint(self):
        return self._content.sizeHint() + QSize(self._margin.horizontal, self._margin.vertical)

    def show(self):
        super().show()
        self.move(self._get_ancher_position_())
        self.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
        self.activateWindow()
        self.raise_()
        for item in self._content._item_group.buttons():
            rect = CoordConverter.rectToGlobal(item)
            if rect.contains(QCursor.pos()):
                item.entered.emit()
            else:
                item.leaved.emit()

    def addItem(self, text: str):
        self._content.addItem(text)
        self.resize(self.sizeHint())

    def removeItem(self, text: str):
        self._content.removeItem(text)
        self.resize(self.sizeHint())

    # region event
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.move(self._margin.left, self._margin.top)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.opacityCtrl.fadeIn()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.opacityCtrl.fadeOut()

    def _get_ancher_position_(self) -> QPoint:
        """获取锚点位置"""
        checked_item = self._content._item_group.checkedButton()
        item_global_pos = checked_item.geometry().topLeft()- QPoint(self._content._layout.contentsMargins().left(), 0)
        offset = QPoint(self._margin.left, self._margin.top)
        parent_pos = self.parent().mapToGlobal(self.parent().geometry().topLeft())
        return parent_pos - item_global_pos - offset

    def _completely_hid_signal_handler(self):
        if self.opacityCtrl.opacity == 0:
            self.hide()
            self.close()
            # self.selected.disconnect()
            # self.deleteLater()


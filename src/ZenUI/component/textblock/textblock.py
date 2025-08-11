from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize, QMargins,QRectF
from PySide6.QtGui import QPainter, QFont, QFontMetrics,QPen
from ZenUI.component.base import ColorController,FloatController
from ZenUI.core import ZGlobal,ZTextBlockStyleData
class ZTextBlock(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self.setMinimumHeight(24)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setStyleSheet('background:transparent;border:1px solid red;')

        self._text = text
        self._font = QFont("Microsoft YaHei", 10)
        self._margins = QMargins(0, 0, 0, 0)
        self._word_wrap = False
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter

        self._text_cc = ColorController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)

        self._style_data: ZTextBlockStyleData = None
        self._custom_style: ZTextBlockStyleData = None

        self.styleData = ZGlobal.styleDataManager.getStyleData('ZTextBlock')
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

    # region Property
    @property
    def textColorCtrl(self) -> ColorController: return self._text_cc

    @property
    def bodyColorCtrl(self) -> ColorController: return self._body_cc

    @property
    def borderColorCtrl(self) -> ColorController: return self._border_cc

    @property
    def radiusCtrl(self) -> FloatController: return self._radius_ctrl


    @property
    def text(self) -> str: return self._text
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    @property
    def font(self) -> QFont: return self._font
    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()

    @property
    def wordWrap(self) -> bool: return self._word_wrap
    @wordWrap.setter
    def wordWrap(self, enabled: bool) -> None:
        self._word_wrap = enabled
        self.update()

    @property
    def margins(self) -> QMargins: return self._margins
    @margins.setter
    def margins(self, margins: QMargins) -> None:
        self._margins = margins
        self.update()


    @property
    def alignment(self) -> Qt.AlignmentFlag: return self._alignment
    @alignment.setter
    def alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._alignment = alignment
        self.update()


    @property
    def styleData(self) -> ZTextBlockStyleData: return self._style_data
    @styleData.setter
    def styleData(self, style_data: ZTextBlockStyleData) -> None:
        self._style_data = style_data
        self._text_cc.color = style_data.Text
        self._body_cc.color = style_data.Body
        self._border_cc.color = style_data.Border
        self._radius_ctrl.value = style_data.Radius
        self.update()

    # region Slot
    def themeChangeHandler(self, theme):
        data = ZGlobal.styleDataManager.getStyleData('ZTextBlock', theme.name)
        self._style_data = data
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._border_cc.setColorTo(data.Border)
        self._text_cc.setColorTo(data.Text)

    # region Override
    def setFont(self, font: QFont) -> None:
        self._font = font
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
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
        painter.setFont(self._font)
        painter.setPen(self._text_cc.color)
        text_rect = rect.adjusted(
            self._margins.left(),
            self._margins.top(),
            -self._margins.right(),
            -self._margins.bottom()
        )
        alignment = self._alignment
        if self._word_wrap: alignment |= Qt.TextWordWrap
        painter.drawText(text_rect, alignment, self._text)
        painter.end()

    def sizeHint(self):
        fm = QFontMetrics(self._font)
        max_width = 500
        padding_w = self._margins.left() + self._margins.right()
        padding_h = self._margins.top() + self._margins.bottom()
        extra_w = 4  # 宽度补偿
        extra_h = 4  # 高度补偿
        if self._word_wrap:
            width = min(self.width() if self.width() > 0 else 200, max_width)
            rect = fm.boundingRect(0, 0, width, 1000, Qt.TextFlag.TextWordWrap, self._text)
            return rect.size() + QSize(padding_w + extra_w, padding_h + extra_h)
        else:
            rect = fm.boundingRect(self._text)
            return rect.size() + QSize(padding_w + extra_w, padding_h + extra_h)

    def adjustSize(self):
        size = self.sizeHint()
        self.resize(size)
        #self.setFixedSize(size)
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QSize, QRect, QMargins
from PySide6.QtGui import QPainter, QFont, QFontMetrics,QPen
from ZenUI.component.base import ColorController,FloatController

class ZToolTipContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(28)
        self.setMaximumWidth(300)

        self._text: str = None
        self._font = QFont("Microsoft YaHei", 9)
        self._word_wrap = Qt.TextFlag.TextWordWrap
        self._margins: QMargins = QMargins(10, 8, 10, 8)
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter

        self._text_cc = ColorController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)


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
    def wordWrap(self) -> Qt.TextFlag: return self._word_wrap

    @wordWrap.setter
    def wordWrap(self, mode: Qt.TextFlag) -> None:
        self._word_wrap = mode
        self.adjustSize()
        self.update()


    @property
    def margin(self) -> QMargins: return self._margins

    @margin.setter
    def margin(self, margin: QMargins) -> None:
        self._margins = margin
        self.adjustSize()
        self.update()

    @property
    def alignment(self) -> Qt.AlignmentFlag: return self._alignment

    @alignment.setter
    def alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._alignment = alignment
        self.adjustSize()
        self.update()


    # region Public
    def setText(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    def font(self): return self._font

    def setFont(self, font: QFont) -> None:
        self._font = font
        self.adjustSize()
        self.update()

    def setFontFamily(self, family: str) -> None:
        self._font.setFamily(family)
        self.adjustSize()
        self.update()

    def setFontSize(self, size: int) -> None:
        self._font.setPointSize(size)
        self.adjustSize()
        self.update()

    def setFontWeight(self, weight: QFont.Weight) -> None:
        self._font.setWeight(weight)
        self.adjustSize()
        self.update()


    def sizeHint(self):
        margins = self._margins
        margin_w = margins.left() + margins.right()
        margin_h = margins.top() + margins.bottom()

        if not self._text: return QSize(margin_w, self.minimumHeight())

        fm = QFontMetrics(self._font)
        width = fm.horizontalAdvance(self._text) + margin_w
        if width < self.maximumWidth():
            height = max(fm.height() + margin_h, self.minimumHeight())
            return QSize(width, height)

        if self._word_wrap == Qt.TextFlag.TextSingleLine:
            width = min(fm.horizontalAdvance(self._text) + margin_w, self.maximumWidth())
            height = max(fm.height() + margin_h, self.minimumHeight())
            return QSize(width, height)

        elif self._word_wrap in [Qt.TextFlag.TextWrapAnywhere,Qt.TextFlag.TextWordWrap]:
            rect = fm.boundingRect(margins.left(),
                                    margins.top(),
                                    self.maximumWidth()-margin_w,
                                    self.maximumHeight()-margin_h,
                                    self._word_wrap,
                                    self._text)
            height = max(rect.height() + margin_h, self.minimumHeight())
            return QSize(self.maximumWidth(), height)

    def adjustSize(self):
        size = self.sizeHint()
        self.setBaseSize(size)
        self.resize(size)

    # region Event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|QPainter.RenderHint.TextAntialiasing)
        # 绘制背景
        rect = self.rect()
        radius = self._radius_ctrl.value
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._body_cc.color)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._border_cc.color, 1))
        painter.setBrush(Qt.NoBrush)
        # 调整矩形以避免边框模糊
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
            radius,
            radius
        )
        painter.setFont(self._font)
        painter.setPen(self._text_cc.color)
        # 设置文本对齐方式
        text_flags = self._alignment | self._word_wrap
        # 计算文本绘制区域
        m = self._margins
        text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        # 绘制文本
        painter.drawText(text_rect, text_flags, self._text)
        painter.end()


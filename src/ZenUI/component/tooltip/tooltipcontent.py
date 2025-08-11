from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QSize, QRect, QMargins
from PySide6.QtGui import QPainter, QFont, QFontMetrics,QPen
from ZenUI.component.base import ColorController,FloatController

class ZToolTipContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(28)

        self._text: str = None
        self._font = QFont("Microsoft YaHei", 9)
        self._word_wrap = Qt.TextFlag.TextWrapAnywhere
        self._max_content_width = 300
        self._margins: QMargins = QMargins(8, 6, 8, 6)
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
    def font(self) -> QFont: return self._font
    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()

    @property
    def wordWrap(self) -> Qt.TextFlag:
        return self._word_wrap
    @wordWrap.setter
    def wordWrap(self, mode: Qt.TextFlag) -> None:
        self._word_wrap = mode
        self.update()

    @property
    def maxContentWidth(self) -> int: return self._max_content_width
    @maxContentWidth.setter
    def maxContentWidth(self, width: int) -> None:
        self._max_content_width = width
        self.update()

    @property
    def margin(self) -> QMargins: return self._margins
    @margin.setter
    def margin(self, margin: QMargins) -> None:
        self._margins = margin
        self.update()

    @property
    def alignment(self) -> Qt.AlignmentFlag: return self._alignment
    @alignment.setter
    def alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._alignment = alignment
        self.update()


    # region Override
    def setFont(self, font: QFont):
        self._font = font
        self.update()

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
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            radius,
            radius
        )
        painter.setFont(self._font)
        painter.setPen(self._text_cc.color)

        # 根据word_wrap设置不同的文本标志
        text_flags = self._alignment
        if self._word_wrap == Qt.TextFlag.TextWordWrap:
            text_flags |= Qt.TextFlag.TextWordWrap
        elif self._word_wrap == Qt.TextFlag.TextWrapAnywhere:
            text_flags |= Qt.TextFlag.TextWrapAnywhere
        text_rect = rect.adjusted(
            self._margins.left() + 1,
            self._margins.top(),
            -self._margins.right(),
            -self._margins.bottom()
        )
        painter.drawText(text_rect, text_flags, self._text)
        painter.end()

    def sizeHint(self):
        fm = QFontMetrics(self._font)
        margin = self._margins.left() + self._margins.right()  # 左右边距总和（和paintEvent一致）
        if not self._text: return super().sizeHint()
        # 计算文本实际宽度
        text_width = fm.horizontalAdvance(self._text) + 2
        width = min(text_width + margin, self._max_content_width)

        # 计算内容区域宽度（去除边距）
        content_width = width - margin
        # 计算高度，自动换行
        rect = fm.boundingRect(0, 0, content_width, 1000, self._word_wrap, self._text)
        height = rect.height() + self._margins.top() + self._margins.bottom() # 上下边距
        height = max(height, self.minimumHeight()) # 最小高度

        return QSize(width, height)

    def adjustSize(self):
        self.resize(self.sizeHint())

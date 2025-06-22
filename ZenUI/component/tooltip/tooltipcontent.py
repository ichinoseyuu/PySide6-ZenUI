from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QSize, QRect, QMargins
from PySide6.QtGui import QPainter, QFont, QFontMetrics,QPen
from ZenUI.core import TextStyle,BackGroundStyle,BorderStyle,CornerStyle
class ZToolTipContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(24)
        # 基本属性
        self._text: str = None
        self._font = QFont("Microsoft YaHei", 10)
        self._word_wrap = True
        self._max_content_width = 300
        self._margin: QMargins = QMargins(8, 6, 8, 6)
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        # 样式属性
        self._text_style = TextStyle(self)
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._corner_style = CornerStyle(self)


    # region Property
    @property
    def textStyle(self) -> TextStyle:
        return self._text_style

    @property
    def backgroundStyle(self) -> BackGroundStyle:
        return self._background_style

    @property
    def borderStyle(self) -> BorderStyle:
        return self._border_style

    @property
    def cornerStyle(self) -> CornerStyle:
        return self._corner_style


    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()


    @property
    def font(self) -> QFont:
        return self._font

    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()


    @property
    def wordWrap(self) -> bool:
        return self._word_wrap

    @wordWrap.setter
    def wordWrap(self, enabled: bool) -> None:
        self._word_wrap = enabled
        self.update()

    @property
    def maxContentWidth(self) -> int:
        return self._max_content_width

    @maxContentWidth.setter
    def maxContentWidth(self, width: int) -> None:
        self._max_content_width = width
        self.update()

    @property
    def margin(self) -> QMargins:
        return self._margin

    @margin.setter
    def margin(self, margin: QMargins) -> None:
        self._margin = margin
        self.update()

    @property
    def alignment(self) -> Qt.AlignmentFlag:
        return self._alignment

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
        radius = self._corner_style.radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._border_style.color, self._border_style.width))
        painter.setBrush(Qt.NoBrush)
        # 调整矩形以避免边框模糊
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            radius,
            radius
        )
        painter.setFont(self._font)
        painter.setPen(self._text_style.color)
        if self._word_wrap:
            self._alignment |= Qt.TextWordWrap
        painter.drawText(rect.adjusted(self._margin.left(), 0, -self._margin.right(), 0), self._alignment, self._text)
        painter.end()

    def sizeHint(self):
        fm = QFontMetrics(self._font)
        margin = self._margin.left() + self._margin.right()  # 左右边距总和（和paintEvent一致）
        if not self._text:
            return super().sizeHint()
        # 计算文本实际宽度
        text_width = fm.horizontalAdvance(self._text)
        width = min(text_width + margin, self._max_content_width)

        # 计算内容区域宽度（去除边距）
        content_width = width - margin
        # 计算高度，自动换行
        rect = fm.boundingRect(0, 0, content_width, 1000, Qt.TextWordWrap, self._text)
        height = rect.height() + self._margin.top() + self._margin.bottom() # 上下边距

        return QSize(width, height)

    def adjustSize(self):
        self.resize(self.sizeHint())
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect,Property,QPropertyAnimation,QEasingCurve,QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QTextOption, QFontMetrics,QPen
class ZTooltipContent(QWidget):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setMinimumHeight(24)
        self._text = text
        self._font = QFont("Microsoft YaHei", 10)
        self._color_text = QColor(30, 30, 30)
        self._color_bg = QColor(255, 255, 255)
        self._color_border = QColor(200, 200, 200)
        self._radius = 5
        self._word_wrap = True
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        self._anim_color = QPropertyAnimation(self, b"color")
        self._anim_color.setDuration(150)
        self._anim_color.setEasingCurve(QEasingCurve.Type.InOutQuad)

    # region Property
    @Property(QColor)
    def color(self):
        return self._color_text

    @color.setter
    def color(self, color):
        self._color_text = color
        self.update()

    # region Public Func
    def setText(self, text: str):
        self._text = text
        self.update()

    def text(self) -> str:
        return self._text

    def setFont(self, font: QFont):
        self._font = font
        self.update()

    def font(self) -> QFont:
        return self._font

    def setColorTo(self, color: QColor):
        self._anim_color.stop()
        self._anim_color.setStartValue(self._color)
        self._anim_color.setEndValue(color)
        self._anim_color.start()

    def setWordWrap(self, enabled: bool):
        self._word_wrap = enabled
        self.update()

    def wordWrap(self) -> bool:
        return self._word_wrap

    def setAlignment(self, alignment: Qt.AlignmentFlag):
        self._alignment = alignment
        self.update()

    def alignment(self) -> Qt.AlignmentFlag:
        return self._alignment

    # region Slot
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|QPainter.RenderHint.TextAntialiasing)
        # 绘制背景
        rect = self.rect()
        radius = self._radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color_bg)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._color_border, 1))
        painter.setBrush(Qt.NoBrush)
        # 调整矩形以避免边框模糊
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            radius,
            radius
        )
        painter.setFont(self._font)
        painter.setPen(self._color_text)
        if self._word_wrap:
            self._alignment |= Qt.TextWordWrap
        painter.drawText(rect.adjusted(10, 0, -10, 0), self._alignment, self._text)
        painter.end()

    def sizeHint(self):
        fm = QFontMetrics(self._font)
        if self._word_wrap:
            width = self.width() if self.width() > 0 else 200
            rect = fm.boundingRect(0, 0, width, 1000, Qt.TextWordWrap, self._text)
            return rect.size()
        else:
            rect = fm.boundingRect(self._text)
            return rect.size()



if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)

    tb1 = ZTooltipContent(text="这是一段可以自动换行的文本。This is a long text block. ")
    tb1.setWordWrap(True)
    tb1.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
    layout.addWidget(tb1)
    print(tb1.alignment().name)
    tb2 = ZTooltipContent(text="这是一段不会自动换行的文本。This is a long text block. ")
    tb2.setWordWrap(False)
    layout.addWidget(tb2)

    window.show()
    app.exec()
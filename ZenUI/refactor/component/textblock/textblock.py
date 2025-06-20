from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect,Property,QPropertyAnimation,QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont, QTextOption, QFontMetrics
from ZenUI.refactor.core import ZGlobal,ZTextBlockStyleData
class ZTextBlock(QWidget):
    def __init__(self, name: str, parent=None, text=None):
        super().__init__(parent)
        self.setObjectName(name)
        self.setMinimumHeight(24)
        self._text = text
        self._font = QFont("Microsoft YaHei", 10)
        self._color = QColor(30, 30, 30)
        self._word_wrap = True
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        self._style_data: ZTextBlockStyleData = None
        self.setStyleData(ZGlobal.styleDataManager.getStyleData('ZTextBlock'))
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)
        self._anim_color = QPropertyAnimation(self, b"color")
        self._anim_color.setDuration(150)
        self._anim_color.setEasingCurve(QEasingCurve.Type.InOutQuad)

    # region Property
    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.update()

    # region Public Func
    def setStyleData(self, style_data: ZTextBlockStyleData):
        self._style_data = style_data
        self._color = style_data.text
        self.update()

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
    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData('ZTextBlock', theme.name)
        self.setColorTo(self._style_data.text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setFont(self._font)
        painter.setPen(self._color)
        rect = self.rect()
        if self._word_wrap: self._alignment |= Qt.TextWordWrap
        painter.drawText(rect, self._alignment, self._text)
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

    tb1 = ZTextBlock("这是一段可以自动换行的文本。This is a long text block. ")
    tb1.setWordWrap(True)
    layout.addWidget(tb1)

    tb2 = ZTextBlock("这是一段不会自动换行的文本。This is a long text block. ")
    tb2.setWordWrap(False)
    layout.addWidget(tb2)

    window.show()
    app.exec()
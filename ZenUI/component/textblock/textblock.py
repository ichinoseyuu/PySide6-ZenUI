from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFont, QFontMetrics
from ZenUI.component.base import TextStyle
from ZenUI.core import ZGlobal,ZTextBlockStyleData
class ZTextBlock(QWidget):
    def __init__(self, name: str, parent=None, text=None):
        super().__init__(parent)
        self.setObjectName(name)
        self.setMinimumHeight(24)
        # 基本属性
        self._text = text
        self._font = QFont("Microsoft YaHei", 10)
        self._word_wrap = True
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        # 样式属性
        self._text_style = TextStyle(self)
        # 样式数据
        self._style_data: ZTextBlockStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData('ZTextBlock')
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

    # region Property
    @property
    def textStyle(self) -> TextStyle:
        return self._text_style


    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text


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
    def alignment(self) -> Qt.AlignmentFlag:
        return self._alignment

    @alignment.setter
    def alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._alignment = alignment
        self.update()


    @property
    def styleData(self) -> ZTextBlockStyleData:
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZTextBlockStyleData) -> None:
        self._style_data = style_data
        self._text_style.color = style_data.text
        self.update()

    # region Slot
    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData('ZTextBlock', theme.name)
        self._text_style.setColorTo(self._style_data.text)

    # region Override
    def setFont(self, font: QFont) -> None:
        self._font = font
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setFont(self._font)
        painter.setPen(self._text_style.color)
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
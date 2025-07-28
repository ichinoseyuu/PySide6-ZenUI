from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize, QMargins
from PySide6.QtGui import QPainter, QFont, QFontMetrics
from ZenUI.component.base import ColorController
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

        self._style_data: ZTextBlockStyleData = None
        self._custom_style: ZTextBlockStyleData = None

        self.styleData = ZGlobal.styleDataManager.getStyleData('ZTextBlock')
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)

    # region Property
    @property
    def textColorCtrl(self) -> ColorController: return self._text_cc

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
        self.update()

    # region Slot
    def themeChangeHandler(self, theme):
        self._style_data = ZGlobal.styleDataManager.getStyleData('ZTextBlock', theme.name)
        self._text_cc.setColorTo(self._style_data.Text)

    # region Override
    def setFont(self, font: QFont) -> None:
        self._font = font
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setFont(self._font)
        painter.setPen(self._text_cc.color)
        rect = self.rect().adjusted(
            self._margins.left(),
            self._margins.top(),
            -self._margins.right(),
            -self._margins.bottom()
        )
        alignment = self._alignment
        if self._word_wrap: alignment |= Qt.TextWordWrap
        painter.drawText(rect, alignment, self._text)
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
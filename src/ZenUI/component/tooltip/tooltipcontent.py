import logging
from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QSize, QRect, QMargins
from PySide6.QtGui import QPainter, QFont, QFontMetrics,QPen
from ZenUI.component.base import ColorController,FloatController

class ZToolTipContent(QWidget):
    class WrapMode(IntEnum):
        NoWrap = 0
        WordWrap = 1
        WrapAnywhere = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text: str = None
        self._font = QFont("Microsoft YaHei", 9)
        self._wrap_mode = self.WrapMode.WrapAnywhere
        self._margins: QMargins = QMargins(10, 8, 10, 8)
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter

        self._text_cc = ColorController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)

        self.setMinimumHeight(28)
        self.setMaximumWidth(300)

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
    def wrapMode(self) -> WrapMode: return self._wrap_mode

    @wrapMode.setter
    def wrapMode(self, mode: WrapMode) -> None:
        self._wrap_mode = mode
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

    def setFont(self, font: QFont | str) -> None:
        if isinstance(font, str):
            self._font.setFamily(font)
        else:
            self._font = font
        self.adjustSize()
        self.update()

    def sizeHint(self):
        m = self._margins
        mw = m.left() + m.right()
        mh = m.top() + m.bottom()
        # 如果没有文本，返回最小尺寸
        if not self._text: return QSize(mw, self.minimumHeight())
        # 文本实际宽度
        fm = QFontMetrics(self._font)
        text_width = fm.horizontalAdvance(self._text) + mw + 1

        if self._wrap_mode == self.WrapMode.NoWrap:
            height = max(fm.height() + mh, self.minimumHeight())
            return QSize(text_width, height)

        # 对于自动换行模式
        if text_width <= self.minimumWidth():
            width = self.minimumWidth()
        elif text_width <= self.maximumWidth():
            width = text_width
        else:
            width = self.maximumWidth()

        height = self.heightForWidth(width)
        return QSize(width, height)

    def adjustSize(self):
        self.resize(self.sizeHint())


    def hasHeightForWidth(self):
        if self._wrap_mode == self.WrapMode.NoWrap: return False
        return True

    def heightForWidth(self, width: int) -> int:
        m = self._margins
        fm = QFontMetrics(self._font)
        rect = fm.boundingRect(0, 0,
                                width,
                                0,
                                self._get_text_flag(),
                                self._text)
        height = max(rect.height() + m.top() + m.bottom(), self.minimumHeight())
        return height

    # region Private
    def _get_text_flag(self) -> Qt.TextFlag:
        """获取文本显示模式"""
        if self._wrap_mode == self.WrapMode.NoWrap:
            return Qt.TextFlag.TextSingleLine | self._alignment
        elif self._wrap_mode == self.WrapMode.WordWrap:
            return Qt.TextFlag.TextWordWrap | self._alignment
        else:
            return Qt.TextFlag.TextWrapAnywhere | self._alignment

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
        text_flags = self._get_text_flag()
        # 计算文本绘制区域
        m = self._margins
        text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        # 绘制文本
        painter.drawText(text_rect, text_flags, self._text)
        painter.end()


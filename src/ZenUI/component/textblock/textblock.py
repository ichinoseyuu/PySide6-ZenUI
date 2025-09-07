import logging
from enum import IntEnum
from PySide6.QtWidgets import QWidget,QSizePolicy
from PySide6.QtCore import Qt, QSize, QMargins,QRectF,Signal
from PySide6.QtGui import QPainter, QFont, QFontMetrics,QPen, QTextLayout, QTextOption
from ZenUI.component.base import ColorController,FloatController,StyleData
from ZenUI.core import ZTextBlockStyleData
class ZTextBlock(QWidget):
    class WrapMode(IntEnum):
        NoWrap = 0
        WordWrap = 1
        WrapAnywhere = 2

    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = "",
                 selectable: bool = False):
        super().__init__(parent=parent)
        if name: self.setObjectName(name)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet('background-color:transparent;border: 1px solid red;')
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self._text = text
        self._font = QFont("Microsoft YaHei", 10)
        self._selected_text = ""  # 选中的文字
        self._margins = QMargins(0, 0, 0, 0)
        self._wrap_mode = self.WrapMode.WordWrap
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        self._selectable = selectable  # 是否可选择文本
        self._selection_start = -1  # 选中开始位置
        self._selection_end = -1    # 选中结束位置
        self._is_selecting = False  # 是否正在选中
        self._drag_start_pos = None # 拖动开始位置

        self._text_back_cc = ColorController(self)
        self._text_cc = ColorController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._style_data = StyleData[ZTextBlockStyleData](self, 'ZTextBlock')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

        self.setMinimumSize(self._margins.left() + self._margins.right(), 24)


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
    def styleData(self): return self._style_data

    @property
    def selectedText(self) -> str: return self._selected_text

    @property
    def text(self) -> str: return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    @property
    def selectable(self) -> bool: return self._selectable

    @selectable.setter
    def selectable(self, selectable: bool) -> None:
        self._selectable = selectable
        if not selectable: self._clear_selection()
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
    def margins(self) -> QMargins: return self._margins

    @margins.setter
    def margins(self, margins: QMargins) -> None:
        self._margins = margins
        self.adjustSize()
        self.update()

    @property
    def alignment(self) -> Qt.AlignmentFlag: return self._alignment

    @alignment.setter
    def alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._alignment = alignment
        self.update()

    # region public
    def setText(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    def setSelectable(self, selectable: bool) -> None:
        self.selectable = selectable

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

    def resizeEvent(self, event):
        if self.hasHeightForWidth():
            new_height = self.heightForWidth(event.size().width())
            if new_height != event.size().height():
                self.resize(event.size().width(), new_height)
        super().resizeEvent(event)

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

    # region private
    def _initStyle(self):
        data = self._style_data.data
        self._text_cc.color = data.Text
        self._body_cc.color = data.Body
        self._border_cc.color = data.Border
        self._radius_ctrl.value = data.Radius
        self._text_back_cc.color = data.TextBackSectcted
        self.update()

    def _styleChangeHandler(self):
        data = self._style_data.data
        self._radius_ctrl.value = data.Radius
        self._body_cc.setColorTo(data.Body)
        self._border_cc.setColorTo(data.Border)
        self._text_cc.setColorTo(data.Text)
        self._text_back_cc.setColorTo(data.TextBackSectcted)


    def _is_selection(self) -> bool:
        """判断是否有选中"""
        return self._selection_start != -1 and self._selection_end != -1

    def _get_selection(self) -> tuple:
        """获取选中范围，返回(start, end)"""
        return min(self._selection_start, self._selection_end), max(self._selection_start, self._selection_end)

    def _get_text_flag(self) -> Qt.TextFlag:
        """获取文本显示模式"""
        if self._wrap_mode == self.WrapMode.NoWrap:
            return Qt.TextFlag.TextSingleLine | self._alignment
        elif self._wrap_mode == self.WrapMode.WordWrap:
            return Qt.TextFlag.TextWordWrap | self._alignment
        else:
            return Qt.TextFlag.TextWrapAnywhere | self._alignment

    def _update_selected_text(self):
        """更新选中的文字"""
        if self._is_selection():
            start, end = self._get_selection()
            if start < end and self._text:
                self._selected_text = self._text[start:end]
            else:
                self._selected_text = ""
        else:
            self._selected_text = ""

    def _clear_selection(self):
        """清除选中"""
        self._selection_start = -1
        self._selection_end = -1
        self._is_selecting = False
        self._selected_text = ""
        self.update()

    def _get_text_layout(self, text_rect: QRectF, fm: QFontMetrics):
        """获取文本的行布局信息，返回每行的文本内容、在原文本中的位置和精确的Y坐标"""
        if self._wrap_mode == self.WrapMode.NoWrap:
            # 单行文本也需要考虑垂直对齐
            line_height = fm.height()
            if self._alignment & Qt.AlignmentFlag.AlignVCenter:
                y_pos = text_rect.top() + (text_rect.height() - line_height) / 2
            elif self._alignment & Qt.AlignmentFlag.AlignBottom:
                y_pos = text_rect.bottom() - line_height
            else:  # AlignTop or default
                y_pos = text_rect.top()
            return [(self._text, 0, y_pos)]

        layout = QTextLayout(self._text, self._font)
        option = QTextOption()

        if self._wrap_mode == self.WrapMode.WordWrap:
            option.setWrapMode(QTextOption.WrapMode.WordWrap)
        elif self._wrap_mode == self.WrapMode.WrapAnywhere:
            option.setWrapMode(QTextOption.WrapMode.WrapAnywhere)

        # 设置水平对齐，但不设置垂直对齐，因为我们需要手动处理
        horizontal_alignment = self._alignment & (Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignHCenter)
        option.setAlignment(horizontal_alignment)
        layout.setTextOption(option)

        layout.beginLayout()
        lines_info = []

        # 首先收集所有行的信息
        temp_lines = []
        while True:
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(text_rect.width())
            temp_lines.append(line)

        layout.endLayout()

        # 计算总的文本高度
        total_height = sum(line.height() for line in temp_lines)

        # 根据垂直对齐计算起始Y位置
        if self._alignment & Qt.AlignmentFlag.AlignVCenter:
            start_y = text_rect.top() + (text_rect.height() - total_height) / 2
        elif self._alignment & Qt.AlignmentFlag.AlignBottom:
            start_y = text_rect.bottom() - total_height
        else:  # AlignTop or default
            start_y = text_rect.top()

        # 生成最终的行信息，包含精确的Y坐标
        current_y = start_y
        for line in temp_lines:
            line_text = self._text[line.textStart():line.textStart() + line.textLength()]
            lines_info.append((line_text, line.textStart(), current_y))
            current_y += line.height()

        return lines_info


    def _get_char_position_at_point(self, point):
        """根据坐标点获取字符位置"""
        if not self._text:
            return 0

        # 计算文本绘制区域
        m = self._margins
        text_rect = self.rect().adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        fm = QFontMetrics(self._font)

        # 使用统一的布局计算，获取精确的行位置
        lines_info = self._get_text_layout(text_rect, fm)
        click_y = point.y()

        # 根据Y坐标找到对应的行
        line_index = -1
        for i, (line_text, line_start_pos, line_y) in enumerate(lines_info):
            line_height = fm.height()
            if click_y >= line_y and click_y <= line_y + line_height:
                line_index = i
                break

        # 如果没有找到精确匹配的行，选择最接近的行
        if line_index == -1:
            if click_y < lines_info[0][2]:  # 在第一行之上
                line_index = 0
            else:  # 在最后一行之下
                line_index = len(lines_info) - 1

        # 在指定行中查找字符位置
        line_text, line_start_pos, _ = lines_info[line_index]
        click_x = point.x() - text_rect.left()

        char_pos_in_line = 0
        accumulated_width = 0
        for i, char in enumerate(line_text):
            char_width = fm.horizontalAdvance(char)
            if click_x <= accumulated_width + char_width / 2:
                char_pos_in_line = i
                break
            accumulated_width += char_width
            char_pos_in_line = i + 1

        return min(line_start_pos + char_pos_in_line, len(self._text))


    def _draw_selection_background(self, painter: QPainter, text_rect: QRectF, start: int, end: int, fm: QFontMetrics):
        """绘制选中区域背景（统一处理单行和多行）"""
        if start >= end:
            return

        # 使用统一的文本布局计算，获取精确的行位置
        lines_info = self._get_text_layout(text_rect, fm)
        line_height = fm.height() + 2 # 加上一些额外的空间

        # 为每行绘制选中区域
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._text_back_cc.color)

        for line_text, line_start_pos, line_y in lines_info:
            line_end_pos = line_start_pos + len(line_text)

            # 检查这一行是否有选中内容
            if start >= line_end_pos or end <= line_start_pos:
                continue

            # 计算在这一行中的选中范围
            line_sel_start = max(0, start - line_start_pos)
            line_sel_end = min(len(line_text), end - line_start_pos)

            if line_sel_start < line_sel_end:
                x1 = text_rect.left()
                if line_sel_start > 0:
                    x1 += fm.horizontalAdvance(line_text[:line_sel_start])

                x2 = x1 + fm.horizontalAdvance(line_text[line_sel_start:line_sel_end])

                # 使用从QTextLayout获取的精确Y坐标
                selection_rect = QRectF(x1, line_y + 1, x2 - x1, line_height - 2)
                painter.drawRoundedRect(selection_rect, 2, 2)


    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing|
                              QPainter.RenderHint.Antialiasing)
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
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius,
                radius
            )

        # 计算文本绘制区域
        m = self._margins
        text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())

        # 更新选中文字
        self._update_selected_text()

        # 绘制选中区域背景
        if self._selectable and self._is_selection() and self._text:
            start, end = self._get_selection()
            if start < end:
                fm = QFontMetrics(self._font)
                # 使用统一的选中区域绘制方法
                self._draw_selection_background(painter, text_rect, start, end, fm)

        # 绘制普通文本
        painter.setFont(self._font)
        painter.setPen(self._text_cc.color)
        # 根据word_wrap设置不同的文本标志
        text_flags = self._get_text_flag()
        painter.drawText(text_rect, text_flags, self._text)

        painter.end()


    # region keyPressEvent
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if not self._selectable:
            super().keyPressEvent(event)
            return

        # 处理复制操作 (Ctrl+C)
        if event.key() == Qt.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self._is_selection() and self._selected_text:
                from PySide6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(self._selected_text)
            return

        # Ctrl+A 全选
        elif event.key() == Qt.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self._text:
                self._selection_start = 0
                self._selection_end = len(self._text)
                self.update()
            return

        super().keyPressEvent(event)

    # region mouseEvent
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if not self._selectable or not self._text:
            super().mousePressEvent(event)
            return

        if event.button() == Qt.LeftButton:
            char_pos = self._get_char_position_at_point(event.pos())

            # 如果按住Shift键，则是扩展选择
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                if self._selection_start == -1:
                    self._selection_start = 0
                self._selection_end = char_pos
            else:
                # 开始新的选择
                self._selection_start = char_pos
                self._selection_end = char_pos
                self._is_selecting = True
                self._drag_start_pos = event.pos()

            self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if not self._selectable or not self._text:
            super().mouseMoveEvent(event)
            return

        if self._is_selecting:
            char_pos = self._get_char_position_at_point(event.pos())
            self._selection_end = char_pos
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._is_selecting = False
        super().mouseReleaseEvent(event)

    def focusOutEvent(self, event):
        if self._selectable:
            self._clear_selection()
        super().focusOutEvent(event)
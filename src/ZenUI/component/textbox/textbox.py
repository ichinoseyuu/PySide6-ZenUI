import logging
from enum import IntEnum
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorController, FloatController, StyleData, SizeController
from ZenUI.core import ZTextBoxStyleData
from .textcommand import TextCommand

class ZTextBox(QWidget):
    class WrapMode(IntEnum):
        NoWrap = 0
        WordWrap = 1
        WrapAnywhere = 2

    editingFinished = Signal()
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = "",
                 mask: str = "",
                 read_only: bool = False,
                 selectable: bool = True):
        super().__init__(parent=parent,
                         minimumSize=QSize(200, 30))
        if name: self.setObjectName(name)
        if read_only: self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        else: self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled)

        self._text = text # 用于存储文本内容
        self._mask_text = mask  # mask文本内容
        self._preedit_text = ""  # 用于存储预编辑文本（中文输入时的拼音）
        self._selected_text = ""    # 选中的文字
        self._cursor_pos = 0 # 光标位置,用于删除功能的定位
        self._font = QFont("Microsoft YaHei", 10)
        self._margins = QMargins(6, 6, 6, 6)
        self._wrap_mode = self.WrapMode.NoWrap
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop
        self._selectable = selectable  # 是否可选择文本
        self._selection_start = -1  # 选中开始位置
        self._selection_end = -1    # 选中结束位置
        self._is_selecting = False  # 是否正在选中
        self._drag_start_pos = None # 拖动开始位置
        self._read_only = read_only  # 是否只读
        self._text_offset = 0  # 文本水平偏移量
        self._undo_stack: list[TextCommand] = []  # 撤销栈
        self._redo_stack: list[TextCommand] = []  # 重做栈
        self._max_undo = 100   # 最大撤销次数
        self._undo_timer = QTimer()
        self._undo_timer.setSingleShot(True)
        self._undo_timer.timeout.connect(self._commit_undo)
        self._pending_undo: list[str, str, int, int] = None

        self._text_cc = ColorController(self)
        self._text_back_cc = ColorController(self)
        self._cursor_cc = ColorController(self)
        self._cursor_cc.animation.setDuration(500)
        self._cursor_cc.animation.finished.connect(self._toggle_cursor)
        self._mask_cc = ColorController(self)
        self._underline_cc = ColorController(self)
        self._underline_ctrl = FloatController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._size_ctrl = SizeController(self)
        self._style_data = StyleData[ZTextBoxStyleData](self, 'ZTextBox')
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

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
    def text(self) -> str: return self._text

    @text.setter
    def text(self, text: str) -> None:
        """text 属性设置器"""
        self._text = text
        if not self.isVisible():
            self.adjustSize()
        else:
            self._update_size()
        self.update()

    @property
    def selectedText(self) -> str: return self._selected_text


    @property
    def maskText(self) -> str: return self._mask_text

    @maskText.setter
    def maskText(self, text: str) -> None:
        self._mask_text = text
        if not self.isVisible():
            self.adjustSize()
        else:
            self._update_size()
        self.update()

    @property
    def wrapMode(self) -> WrapMode: return self._wrap_mode

    @wrapMode.setter
    def wrapMode(self, mode: WrapMode) -> None:
        self._wrap_mode = mode
        self.adjustSize()
        self.update()

    @property
    def readOnly(self) -> bool: return self._read_only

    @readOnly.setter
    def readOnly(self, read_only: bool) -> None:
        self._read_only = read_only
        self.update()

    @property
    def selectable(self) -> bool: return self._selectable

    @selectable.setter
    def selectable(self, selectable: bool) -> None:
        self._selectable = selectable
        if not selectable: self._clear_selection()
        self.adjustSize()
        self.update()

    # region public
    def setText(self, text: str) -> None:
        self._text = text
        if not self.isVisible():
            # 还未显示时使用 adjustSize
            self.adjustSize()
        else:
            # 已显示时使用 _update_size
            self._update_size()
        self.update()

    def setMaskText(self, text: str) -> None:
        """设置遮罩文本"""
        self._mask_text = text
        if not self.isVisible():
            self.adjustSize()
        else:
            self._update_size()
        self.update()

    def font(self): return self._font

    def setFont(self, font: QFont | str) -> None:
        if isinstance(font, str):
            self._font.setFamily(font)
        else:
            self._font = font
        self.adjustSize()
        self.update()

    def setReadOnly(self, read_only: bool) -> None:
        self._read_only = read_only
        self.update()

    def sizeHint(self) -> QSize:
        """返回推荐的尺寸"""
        fm = QFontMetrics(self._font)
        m = self._margins
        mw = m.left() + m.right()
        mh = m.top() + m.bottom()

        if not self._text and not self._mask_text and not self._preedit_text:
            return self.minimumSize()

        # 计算完整文本宽度（包括预编辑文本）
        display_text = self._text
        if self._preedit_text:
            display_text = (self._text[:self._cursor_pos] + 
                        self._preedit_text + 
                        self._text[self._cursor_pos:])

        text_width = fm.horizontalAdvance(display_text) + mw

        if self._wrap_mode == self.WrapMode.NoWrap:
            height = fm.height() + mh
            return QSize(max(text_width, self.minimumWidth()), 
                        max(height, self.minimumHeight()))

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

    def hasHeightForWidth(self) -> bool:
        if self._wrap_mode == self.WrapMode.NoWrap: return False
        return True

    def heightForWidth(self, width: int) -> int:
        """计算指定宽度下需要的高度"""
        m = self._margins
        mw = m.left() + m.right()
        mh = m.top() + m.bottom()
        fm = QFontMetrics(self._font)

        if not self._text and not self._mask_text and not self._preedit_text:
            return self.minimumHeight()

        # 包含预编辑文本
        display_text = self._text
        if self._preedit_text:
            display_text = (self._text[:self._cursor_pos] + 
                        self._preedit_text + 
                        self._text[self._cursor_pos:])

        available_width = width - mw

        if self._wrap_mode == self.WrapMode.NoWrap:
            return max(fm.height() + mh, self.minimumHeight())

        # 使用 QTextLayout 计算实际需要的高度
        layout = QTextLayout(display_text, self._font)
        option = QTextOption()
        if self._wrap_mode == self.WrapMode.WordWrap:
            option.setWrapMode(QTextOption.WrapMode.WordWrap)
        else:
            option.setWrapMode(QTextOption.WrapMode.WrapAnywhere)
        layout.setTextOption(option)

        layout.beginLayout()
        total_height = 0
        while True:
            line = layout.createLine()
            if not line.isValid():
                break
            line.setLineWidth(available_width)
            total_height += line.height()
        layout.endLayout()

        return max(total_height + mh, self.minimumHeight())

    # region private
    def _initStyle(self):
        data = self._style_data.data
        self._text_cc.color = data.Text
        self._text_back_cc.color = data.TextBackSectcted
        self._cursor_cc.color = data.Cursor
        self._mask_cc.color = data.Mask
        self._underline_cc.color = data.Underline
        self._body_cc.color = data.Body
        self._border_cc.color = data.Border
        self._radius_ctrl.value = data.Radius
        self._underline_ctrl.value = 1.3
        self.update()


    def _styleChangeHandler(self):
        data = self._style_data.data
        self._radius_ctrl.value = data.Radius
        self._mask_cc.setColorTo(data.Mask)
        self._cursor_cc.setColorTo(data.Cursor)
        self._border_cc.setColorTo(data.Border)
        self._text_cc.setColorTo(data.Text)
        self._text_back_cc.setColorTo(data.TextBackSectcted)

        if self.hasFocus():
            self._underline_cc.setColorTo(data.UnderlineFocused)
            self._body_cc.setColorTo(data.BodyFocused)
        else:
            self._underline_cc.setColorTo(data.Underline)
            self._body_cc.setColorTo(data.Body)


    def _update_size(self):
        """更新控件尺寸，确保不超过父控件范围"""
        size_hint = self.sizeHint()

        # 如果有父控件，限制大小不超过父控件
        if self.parentWidget():
            parent_rect = self.parentWidget().rect()
            # 考虑控件在父控件中的位置
            pos_in_parent = self.pos()
            # 计算可用空间
            available_width = parent_rect.width() - pos_in_parent.x() - 6
            available_height = parent_rect.height() - pos_in_parent.y() - 6
            # 限制尺寸不超过可用空间
            new_width = min(size_hint.width(), available_width)
            new_height = min(size_hint.height(), available_height)
            limited_size = QSize(new_width, new_height)
            self._size_ctrl.resizeTo(limited_size)
        else:
            # 没有父控件时使用原始的 sizeHint
            self._size_ctrl.resizeTo(size_hint)


    def _toggle_cursor(self):
        """切换光标可见性"""
        if self._cursor_cc.color.alpha() > 0:
            self._cursor_cc.toTransparent()
        else:
            self._cursor_cc.toOpaque()


    def _should_show_cursor(self) -> bool:
        """判断是否应该显示光标"""
        return (self.hasFocus() and
                not self._read_only and
                self._cursor_cc.color.alpha() > 0 and
                not self._selected_text)


    def _should_show_mask(self) -> bool:
        """判断是否应该显示掩码"""
        return not self._text and self._mask_text and not self.hasFocus()


    def _is_selection(self) -> bool:
        """判断是否有选中"""
        return self._selection_start != -1 and self._selection_end != -1 and self._selection_start != self._selection_end


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
            if start < end:
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

    def _cut(self):
        """剪切操作"""
        if self._is_selection() and self._selected_text:
            QApplication.clipboard().setText(self._selected_text)
            start, end = self._get_selection()
            old_text = self._text
            old_pos = self._cursor_pos
            self._text = self._text[:start] + self._text[end:]
            self._cursor_pos = start
            self._clear_selection()
            self._push_undo(old_text, self._text, old_pos, self._cursor_pos)
            self._update_size()

    def _copy(self):
        """复制操作"""
        if self._is_selection() and self._selected_text:
            QApplication.clipboard().setText(self._selected_text)
            logging.info("Copy done")

    def _paste(self, event: QKeyEvent):
        """粘贴操作"""
        clipboard_text = QApplication.clipboard().text()
        if clipboard_text:
            old_text = self._text
            old_pos = self._cursor_pos

            if self._is_selection():
                start, end = self._get_selection()
                self._text = self._text[:start] + clipboard_text + self._text[end:]
                self._cursor_pos = start + len(clipboard_text)
                self._clear_selection()
            else:
                self._text = self._text[:self._cursor_pos] + clipboard_text + self._text[self._cursor_pos:]
                self._cursor_pos += len(clipboard_text)
            if not event.isAutoRepeat():
                self._push_undo_delay(old_text, self._text, old_pos, self._cursor_pos)
            self._update_size()
            logging.info("Paste done")

    def _select_all(self):
        """全选操作"""
        self._selection_start = 0
        self._selection_end = len(self._text)
        self.update()
        logging.info("Select all: %d - %d", self._selection_start, self._selection_end)

    def _redo(self):
        """重做操作"""
        # 提交可能存在的未完成undo记录
        if self._undo_timer.isActive():
            self._undo_timer.stop()
            self._commit_undo()
        if not self._redo_stack:
            return
        # 获取下一次操作
        command = self._redo_stack.pop()
        # 保存当前状态到撤销栈
        undo_command = TextCommand(self._text, command.new_text, 
                                self._cursor_pos, command.new_pos)
        self._undo_stack.append(undo_command)
        # 执行重做
        self._text = command.new_text
        self._cursor_pos = command.new_pos
        self._clear_selection()
        self._update_size()
        logging.info("Redo done")


    def _undo(self):
        """撤销操作"""
        # 提交可能存在的未完成undo记录
        if self._undo_timer.isActive():
            self._undo_timer.stop()
            self._commit_undo()
        if not self._undo_stack:
            return
        # 获取上一次操作
        command = self._undo_stack.pop()
        # 保存当前状态用于重做
        redo_command = TextCommand(command.old_text, self._text, 
                                command.old_pos, self._cursor_pos)
        self._redo_stack.append(redo_command)
        # 恢复到上一次状态
        self._text = command.old_text
        self._cursor_pos = command.old_pos
        self._clear_selection()
        self._update_size()
        logging.info("Undo done")


    def _push_undo(self, old_text: str, new_text: str, old_pos: int, new_pos: int):
        """立即记录撤销操作，不使用计时器"""
        command = TextCommand(old_text, new_text, old_pos, new_pos)
        self._undo_stack.append(command)
        if len(self._undo_stack) > self._max_undo:
            self._undo_stack.pop(0)
        logging.info(f"Push undo{command.__dict__}")

    def _push_undo_delay(self, old_text: str, new_text: str, old_pos: int, new_pos: int):
        if self._undo_timer.isActive():
            self._pending_undo[1] = new_text
            self._pending_undo[3] = new_pos
        else:
            self._pending_undo = [old_text, new_text, old_pos, new_pos]
            self._redo_stack.clear()  # 只在开始新的撤销操作时清除重做栈
        logging.info(f"Push undo delay{self._pending_undo}")
        self._undo_timer.start(500)  # 500ms 内的连续操作会被合并


    def _commit_undo(self):
        """实际提交撤销操作"""
        if self._pending_undo:
            old_text, new_text, old_pos, new_pos = self._pending_undo
            command = TextCommand(old_text, new_text, old_pos, new_pos)
            self._undo_stack.append(command)
            if len(self._undo_stack) > self._max_undo:
                self._undo_stack.pop(0)
            logging.info(f"Commit undo{self._pending_undo}")
            self._pending_undo = None

    def _delete(self, event: QKeyEvent):
        """删除文本（选中区域或光标后字符）"""
        old_text = self._text
        old_pos = self._cursor_pos
        if self._is_selection():
            # 有选中区域时删除选中内容
            start, end = self._get_selection()
            self._text = self._text[:start] + self._text[end:]
            self._cursor_pos = start
            self._clear_selection()
        elif self._cursor_pos < len(self._text):
            # 无选中区域时删除光标后字符
            self._text = self._text[:self._cursor_pos] + self._text[self._cursor_pos + 1:]
        if not event.isAutoRepeat():
            self._push_undo_delay(old_text, self._text, old_pos, self._cursor_pos)
        self._update_size()

    def _insert_text(self, event: QKeyEvent):
        """插入文本"""
        old_text = self._text
        old_pos = self._cursor_pos
        if self._is_selection():
            start, end = self._get_selection()
            self._text = self._text[:start] + self._text[end:]
            self._cursor_pos = start
            self._clear_selection()
        self._text = self._text[:self._cursor_pos] + event.text() + self._text[self._cursor_pos:]
        self._cursor_pos += len(event.text())
        if not event.isAutoRepeat():
            self._push_undo_delay(old_text, self._text, old_pos, self._cursor_pos)
        self._update_size()

    def _backspace(self, event: QKeyEvent):
        """处理退格键"""
        old_text = self._text
        old_pos = self._cursor_pos
        if self._is_selection():
            start, end = self._get_selection()
            self._text = self._text[:start] + self._text[end:]
            self._cursor_pos = start
            self._clear_selection()
            #self._push_undo(old_text, self._text, old_pos, self._cursor_pos)
            if not event.isAutoRepeat():
                self._push_undo_delay(old_text, self._text, old_pos, self._cursor_pos)
            self._update_size()
            return
        if self._cursor_pos > 0:
            self._text = self._text[:self._cursor_pos - 1] + self._text[self._cursor_pos:]
            self._cursor_pos -= 1
            #self._push_undo(old_text, self._text, old_pos, self._cursor_pos)
            if not event.isAutoRepeat():
                self._push_undo_delay(old_text, self._text, old_pos, self._cursor_pos)
            self._update_size()
            return

    def _move_cursor_left(self):
        """向左移动光标"""
        if self._is_selection():
            self._clear_selection()
        if self._cursor_pos > 0:
            self._cursor_pos -= 1

    def _move_cursor_right(self):
        """向右移动光标"""
        if self._is_selection():
            self._clear_selection()
        if self._cursor_pos < len(self._text):
            self._cursor_pos += 1


    # region paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing|
                            QPainter.RenderHint.Antialiasing)
        # 创建圆角矩形路径作为裁剪区域
        rect = self.rect()
        radius = self._radius_ctrl.value
        clip_path = QPainterPath()
        clip_path.addRoundedRect(rect, radius, radius)
        # 设置裁剪区域
        painter.setClipPath(clip_path)
        # 绘制背景
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.fillRect(rect, self._body_cc.color)
        # 绘制边框
        if self._border_cc.color.alpha() > 0:
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius,
                radius)
        # 绘制下边缘线
        if self._underline_cc.color.alpha() > 0:
            # 使用矩形替代线条
            underline_height = self._underline_ctrl.value
            underline_rect = QRectF(
                0,
                rect.bottom() - underline_height + 1,
                rect.width(),
                underline_height
            )
            # painter.setBrush(self._underline_cc.color)
            # painter.drawRect(underline_rect)
            painter.fillRect(underline_rect, self._underline_cc.color)
        # 计算文本绘制区域
        m = self._margins
        text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        # 更新选中文字
        self._update_selected_text()

        painter.setFont(self._font)
        text_flags = self._get_text_flag()

        # 绘制文本
        if self._should_show_mask():
            # 显示mask文本
            painter.setPen(self._mask_cc.color)
            painter.drawText(text_rect, text_flags, self._mask_text)
        else:
            # 绘制选中区域
            if self._selectable and self._is_selection() and self._text:
                start, end = self._get_selection()
                if start < end:
                    fm = QFontMetrics(self._font)
                    # 使用统一的选中区域绘制方法
                    self._draw_selection_background(painter, text_rect, start, end, fm)

        # 创建要显示的文本
        display_text = self._text
        if self._preedit_text:
            # 将预编辑文本插入到当前光标位置
            display_text = self._text[:self._cursor_pos] + self._preedit_text + self._text[self._cursor_pos:]

        painter.setPen(self._text_cc.color)
        painter.drawText(text_rect, text_flags, display_text)

        # 光标绘制
        if self._should_show_cursor():
            fm = painter.fontMetrics()
            # 获取当前文本布局信息
            lines_info = self._get_text_layout(text_rect, fm)
            #cursor_text = display_text[:self._cursor_pos]

            # 找到光标所在行
            cursor_line = None
            for line_text, line_start, line_y in lines_info:
                line_end = line_start + len(line_text)
                if self._cursor_pos >= line_start and self._cursor_pos <= line_end:
                    cursor_line = (line_text, line_start, line_y)
                    break

            if cursor_line:
                line_text, line_start, line_y = cursor_line
                # 计算光标在当前行的水平位置
                cursor_x = text_rect.left() + fm.horizontalAdvance(line_text[:self._cursor_pos - line_start])
                # 使用行的精确 Y 坐标
                cursor_y = line_y
                cursor_height = fm.height()
                painter.setPen(self._cursor_cc.color)
                painter.drawLine(
                    QPointF(cursor_x, cursor_y),
                    QPointF(cursor_x, cursor_y + cursor_height)
                )

        painter.end()

    # region keyPressEvent
    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘事件"""
        # 重置光标显示
        self._cursor_cc.toOpaque()

        # 处理任何时候都可用的快捷键
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key_C and self._is_selection():  # 复制
                self._copy()
                return
            elif event.key() == Qt.Key_A:  # 全选
                self._select_all()
                return

        # 只读模式下忽略其他键盘事件
        if self._read_only: return

        # 处理编辑模式下的通用操作
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key_V:  # 粘贴
                self._paste(event)
                return
            elif event.key() == Qt.Key_Z:  # 撤销
                self._undo()
                return
            elif event.key() == Qt.Key_Y:  # 重做
                self._redo()
                return
            elif event.key() == Qt.Key_X:  # 剪切
                self._cut()
                return
            event.ignore()  # 其他 Ctrl 组合键不处理
            return

        # 处理基本编辑操作
        if event.key() == Qt.Key_Left:
            self._move_cursor_left()
            return
        elif event.key() == Qt.Key_Right:
            self._move_cursor_right()
            return
        elif event.key() == Qt.Key_Backspace:
            self._backspace(event)
            return
        elif event.key() == Qt.Key_Delete:
            self._delete(event)
            return
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.editingFinished.emit()
            return
        elif event.text():
            self._insert_text(event)
            return
        self.update()


    # region inputEvent
    def inputMethodEvent(self, event: QInputMethodEvent):
        """处理输入法事件"""
        # 只读模式下不处理输入法事件
        if self._read_only:
            return

        if event.commitString():
            # 提交文本（完成中文输入）
            old_text = self._text
            old_pos = self._cursor_pos
            commit_text = event.commitString()
            # 检查是否有选中的文本
            if self._is_selection():
                start, end = self._get_selection()
                self._text = self._text[:start] + commit_text + self._text[end:]
                self._cursor_pos = start + len(commit_text)
                self._clear_selection()
            else:
                self._text = self._text[:self._cursor_pos] + commit_text + self._text[self._cursor_pos:]
                self._cursor_pos += len(commit_text)

            self._push_undo(old_text, self._text, old_pos, self._cursor_pos)
            self._preedit_text = ""
        else:
            # 预编辑文本
            self._preedit_text = event.preeditString()

        self._update_size()


    def inputMethodQuery(self, query: Qt.InputMethodQuery):
        """处理输入法查询"""
        if query == Qt.ImCursorRectangle:
            # 返回光标位置
            font_metrics = self.fontMetrics()
            text_rect = self.style().subElementRect(QStyle.SE_LineEditContents, 
                                                  QStyleOptionFrame(), self)
            x = text_rect.left() + font_metrics.horizontalAdvance(self._text[:self._cursor_pos])
            y = text_rect.top()
            width = 1
            height = text_rect.height()
            return QRect(x, y, width, height)
        elif query == Qt.ImHints:
            return Qt.ImhNone
        return None

    # region mouseEvent
    def mousePressEvent(self, event: QMouseEvent):
        """处理鼠标点击事件"""
        if not self._selectable:
            super().mousePressEvent(event)
            return

        if event.button() == Qt.LeftButton:
            char_pos = self._get_char_position_at_point(event.pos())

            # 更新光标位置
            self._cursor_cc.toOpaque()
            self._cursor_pos = char_pos

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


    def mouseMoveEvent(self, event: QMouseEvent):
        """处理鼠标移动事件"""
        if self._is_selecting:
            new_cursor_pos = self._get_char_position_at_point(event.pos())
            self._selection_end = new_cursor_pos
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._is_selecting = False
        super().mouseReleaseEvent(event)

    def focusInEvent(self, event):
        if not self._read_only:
            self._cursor_cc.toOpaque()
        self._body_cc.setColorTo(self._style_data.data.BodyFocused)
        self._underline_cc.setColorTo(self._style_data.data.UnderlineFocused)
        self._underline_ctrl.setValueTo(2.0)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._cursor_cc.transparent()
        self._cursor_cc.stopAnimation()
        self._body_cc.setColorTo(self._style_data.data.Body)
        self._underline_cc.setColorTo(self._style_data.data.Underline)
        self._underline_ctrl.setValueTo(1.3)
        self._clear_selection()
        super().focusOutEvent(event)

    def enterEvent(self, event):
        if not self.hasFocus():
            self._body_cc.setColorTo(self._style_data.data.BodyHover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.hasFocus():
            self._body_cc.setColorTo(self._style_data.data.BodyFocused)
        else:
            self._body_cc.setColorTo(self._style_data.data.Body)
        super().leaveEvent(event)
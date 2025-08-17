from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.base import ColorController, FloatController, StyleData
from ZenUI.core import ZTextBoxStyleData

class ZTextBox(QWidget):
    editingFinished = Signal()
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 text: str = "",
                 mask: str = "",
                 read_only: bool = False):
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
        self._word_wrap = Qt.TextFlag.TextWordWrap
        self._alignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop
        self._selection_start = -1  # 选中开始位置
        self._selection_end = -1    # 选中结束位置
        self._is_selecting = False  # 是否正在选中
        self._drag_start_pos = None # 拖动开始位置
        self._read_only = read_only  # 是否只读


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
        self._text = text
        self.adjustSize()
        self.update()

    @property
    def selectedText(self) -> str: return self._selected_text


    @property
    def maskText(self) -> str: return self._mask_text

    @maskText.setter
    def maskText(self, text: str) -> None:
        self._mask_text = text
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
    def readOnly(self) -> bool: return self._read_only

    @readOnly.setter
    def readOnly(self, read_only: bool) -> None:
        self._read_only = read_only
        self.update()

    # region public
    def setText(self, text: str) -> None:
        self._text = text
        self.adjustSize()
        self.update()

    def setMaskText(self, text: str) -> None:
        self._mask_text = text
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

    def setReadOnly(self, read_only: bool) -> None:
        self._read_only = read_only
        self.update()


    def sizeHint(self):
        if not self._text and not self._mask_text:
            return self.minimumSize()
        fm = QFontMetrics(self._font)
        if self._text:
            return self._get_size_hint(self._text, fm)
        elif self._mask_text:
            return self._get_size_hint(self._mask_text, fm)


    def adjustSize(self):
        size = self.sizeHint()
        self.setBaseSize(size)
        self.resize(size)

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
        self._underline_ctrl.value = 0.5
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


    def _get_size_hint(self, text: str, fm: QFontMetrics) -> QSize:
        margins = self._margins
        margin_w = margins.left() + margins.right()
        margin_h = margins.top() + margins.bottom()
        width = fm.horizontalAdvance(text) + margin_w
        width = max(self.minimumWidth(), width)

        if width < self.maximumWidth():
                height = max(fm.height() + margin_h, self.minimumHeight())
                return QSize(width, height)

        if self._word_wrap == Qt.TextFlag.TextSingleLine:
            width = min(fm.horizontalAdvance(text) + margin_w, self.maximumWidth())
            height = max(fm.height() + margin_h, self.minimumHeight())
            return QSize(width, height)

        elif self._word_wrap in [Qt.TextFlag.TextWrapAnywhere,Qt.TextFlag.TextWordWrap]:
            rect = fm.boundingRect(margins.left(),
                                    margins.top(),
                                    self.maximumWidth()-margin_w,
                                    self.maximumHeight()-margin_h,
                                    self._word_wrap,
                                    text)
            height = max(rect.height() + margin_h, self.minimumHeight())
            return QSize(self.maximumWidth(), height)

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

    def _is_selection(self) -> bool:
        """判断是否有选中"""
        return self._selection_start != -1 and self._selection_end != -1

    def _get_selection(self) -> tuple:
        """获取选中范围，返回(start, end)"""
        return min(self._selection_start, self._selection_end), max(self._selection_start, self._selection_end)

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
            painter.setBrush(self._body_cc.color)
            painter.fillRect(rect, self._body_cc.color)
        # 绘制下边缘线
        if self._underline_cc.color.alpha() > 0:
            painter.setPen(QPen(self._underline_cc.color, self._underline_ctrl.value))
            painter.drawLine(
                QPointF(0, rect.bottom() - 1),
                QPointF(rect.right(), rect.bottom() - 1))
        # 绘制边框
        if self._border_cc.color.alpha() > 0:
            painter.setPen(QPen(self._border_cc.color, 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),
                radius,
                radius)
        # 计算文本绘制区域
        m = self._margins
        text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        # 设置字体
        painter.setFont(self._font)
        # 更新选中文字
        self._update_selected_text()
        # 设置文本对齐方式
        text_flags = self._alignment | self._word_wrap
        # 判断是否显示mask文本
        should_show_mask = (not self._text and self._mask_text and not self.hasFocus())
        if should_show_mask:
            # 显示mask文本
            painter.setPen(self._mask_cc.color)
            painter.drawText(text_rect, text_flags, self._mask_text)
        else:
            # 绘制选中区域
            if self._is_selection():
                start, end = self._get_selection()
                if start < end:
                    fm = painter.fontMetrics()
                    text = self._text
                    # 计算选中区域开始位置
                    x1 = text_rect.left() if start == 0 else text_rect.left() + fm.horizontalAdvance(text[:start])
                    # 计算选中区域结束位置
                    x2 = x1 + fm.horizontalAdvance(text[start:end])
                    # 创建选中区域的矩形
                    selection_rect = QRectF(x1, text_rect.top(), x2 - x1, fm.height())
                    # 创建选中区域的路径
                    selection_path = QPainterPath()
                    selection_path.addRoundedRect(selection_rect, 4, 4)
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(self._text_back_cc.color))
                    painter.drawPath(selection_path)

        # 创建要显示的文本
        display_text = self._text
        if self._preedit_text:
            # 将预编辑文本插入到当前光标位置
            display_text = self._text[:self._cursor_pos] + self._preedit_text + self._text[self._cursor_pos:]

        painter.setPen(self._text_cc.color)
        painter.drawText(text_rect, text_flags, display_text)

        # 修改光标显示条件：有焦点、光标可见、不在选中状态且选中文字为空
        if self._should_show_cursor():
            fm = painter.fontMetrics()
            cursor_x = text_rect.left() + fm.horizontalAdvance(self._text[:self._cursor_pos] + self._preedit_text)
            fm.height()
            painter.setPen(self._cursor_cc.color)
            painter.drawLine(cursor_x, text_rect.top(), cursor_x, fm.height() + text_rect.top())

        painter.end()

    # region keyPressEvent
    def keyPressEvent(self, event: QKeyEvent):
        self._cursor_cc.toOpaque() # 重置光标的显示
        # 只读模式下，只允许复制和选择操作
        if self._read_only:
            # 处理复制操作 (Ctrl+C)
            if event.key() == Qt.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                if self._is_selection() and self._selected_text:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(self._selected_text)
                return
            # Ctrl+A 全选
            elif event.key() == Qt.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._selection_start = 0
                self._selection_end = len(self._text)
                self.update()
                return
            # 其他按键在只读模式下被忽略
            return
        # 处理复制操作 (Ctrl+C)
        if event.key() == Qt.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self._is_selection() and self._selected_text:
                clipboard = QApplication.clipboard()
                clipboard.setText(self._selected_text)
            return
        # 处理剪切操作 (Ctrl+X)
        if event.key() == Qt.Key_X and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self._is_selection() and self._selected_text:
                # 复制到剪贴板
                clipboard = QApplication.clipboard()
                clipboard.setText(self._selected_text)
                # 删除选中的文本
                start, end = self._get_selection()
                if start < end:
                    self._text = self._text[:start] + self._text[end:]
                    self._cursor_pos = start
                    self._clear_selection()
                    self.update()
            return
        # 处理粘贴操作 (Ctrl+V)
        if event.key() == Qt.Key_V and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()
            if clipboard_text:
                if self._is_selection():
                    # 如果有选中文本，替换选中的文本
                    start, end = self._get_selection()
                    if start < end:
                        self._text = self._text[:start] + clipboard_text + self._text[end:]
                        self._cursor_pos = start + len(clipboard_text)
                        self._clear_selection()
                    else:
                        # 没有选中文本，在光标位置插入
                        self._text = self._text[:self._cursor_pos] + clipboard_text + self._text[self._cursor_pos:]
                        self._cursor_pos += len(clipboard_text)
                else:
                    # 没有选中文本，在光标位置插入
                    self._text = self._text[:self._cursor_pos] + clipboard_text + self._text[self._cursor_pos:]
                    self._cursor_pos += len(clipboard_text)
                self.update()
            return
        # 删除选中文本
        if self._is_selection():
            start, end = self._get_selection()
            if start < end:
                if event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
                    self._text = self._text[:start] + self._text[end:]
                    self._cursor_pos = start
                    self._clear_selection()
                    self.update()
                    return

        # 退格删除键
        if event.key() == Qt.Key_Backspace:
            if self._cursor_pos > 0:
                self._text = self._text[:self._cursor_pos - 1] + self._text[self._cursor_pos:]
                self._cursor_pos -= 1
        # 左移光标
        elif event.key() == Qt.Key_Left:
            if self._is_selection():
                self._clear_selection()
            if self._cursor_pos > 0:
                self._cursor_pos -= 1
        # 右移光标
        elif event.key() == Qt.Key_Right:
            if self._is_selection():
                self._clear_selection()
            if self._cursor_pos < len(self._text):
                self._cursor_pos += 1
        # 回车键
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.editingFinished.emit()
        # Ctrl+A 全选
        elif event.key() == Qt.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self._selection_start = 0
            self._selection_end = len(self._text)
            self.update()
        else:
            char = event.text()
            if len(char) == 1:
                if self._is_selection():
                    start, end = self._get_selection()
                    if start < end:
                        # 替换选中的文本
                        self._text = self._text[:start] + char + self._text[end:]
                        self._cursor_pos = start + 1
                        self._clear_selection()
                    else:
                        self._text = self._text[:self._cursor_pos] + char + self._text[self._cursor_pos:]
                        self._cursor_pos += 1
                else:
                    self._text = self._text[:self._cursor_pos] + char + self._text[self._cursor_pos:]
                    self._cursor_pos += 1
        self.update()


    def inputMethodEvent(self, event: QInputMethodEvent):
        """处理输入法事件"""
        # 只读模式下不处理输入法事件
        if self._read_only:
            return
        if event.commitString():
            # 提交文本（完成中文输入）
            commit_text = event.commitString()
            # 检查是否有选中的文本
            if self._is_selection():
                start, end = self._get_selection()
                if start < end:
                    # 替换选中的文本
                    self._text = self._text[:start] + commit_text + self._text[end:]
                    self._cursor_pos = start + len(commit_text)
                    self._clear_selection()
                else:
                    # 没有选中文本，正常插入
                    self._text = self._text[:self._cursor_pos] + commit_text + self._text[self._cursor_pos:]
                    self._cursor_pos += len(commit_text)
            else:
                # 没有选中文本，正常插入
                self._text = self._text[:self._cursor_pos] + commit_text + self._text[self._cursor_pos:]
                self._cursor_pos += len(commit_text)

            self._preedit_text = ""
            self.update()  # 添加更新显示
        else:
            # 更新预编辑文本（拼音输入）
            self._preedit_text = event.preeditString()
            # 更新显示
            self.update()

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
        if event.button() == Qt.LeftButton:
            # 获取文本区域
            rect = self.rect()
            m = self._margins
            text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
            # 获取字体度量信息
            font_metrics = self.fontMetrics()
            # 计算点击位置相对于文本区域的偏移
            click_x = event.pos().x() - text_rect.left()
            # 查找点击位置对应的光标位置
            new_cursor_pos = 0
            accumulated_width = 0
            # 遍历所有字符，找到点击位置对应的字符索引
            for i, char in enumerate(self._text):
                char_width = font_metrics.horizontalAdvance(char)
                # 如果点击位置在当前字符的范围内
                if click_x <= accumulated_width + char_width / 2:
                    new_cursor_pos = i
                    break
                accumulated_width += char_width
                new_cursor_pos = i + 1
            else:
                # 如果点击位置在所有字符之后
                new_cursor_pos = len(self._text)
            # 更新光标位置
            self._cursor_pos = new_cursor_pos
            # 重置光标可见性
            self._cursor_cc.toOpaque()
            # 如果按住Shift键，则是扩展选择
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self._selection_end = new_cursor_pos
            else:
                # 开始新的选择
                self._selection_start = new_cursor_pos
                self._selection_end = new_cursor_pos
                self._is_selecting = True
                self._drag_start_pos = event.pos()
            self.update()
        super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QMouseEvent):
        """处理鼠标移动事件"""
        if self._is_selecting:
            # 获取文本区域
            rect = self.rect()
            m = self._margins
            text_rect = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
            # 获取字体度量信息
            font_metrics = self.fontMetrics()
            # 计算鼠标位置相对于文本区域的偏移
            click_x = event.pos().x() - text_rect.left()
            # 查找鼠标位置对应的光标位置
            new_cursor_pos = 0
            accumulated_width = 0
            # 遍历所有字符，找到鼠标位置对应的字符索引
            for i, char in enumerate(self._text):
                char_width = font_metrics.horizontalAdvance(char)
                if click_x <= accumulated_width + char_width / 2:
                    new_cursor_pos = i
                    break
                accumulated_width += char_width
                new_cursor_pos = i + 1
            else:
                new_cursor_pos = len(self._text)
            # 更新选择结束位置
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
        self._underline_ctrl.setValueTo(2.5)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._cursor_cc.transparent()
        self._cursor_cc.stopAnimation()
        self._body_cc.setColorTo(self._style_data.data.Body)
        self._underline_cc.setColorTo(self._style_data.data.Underline)
        self._underline_ctrl.setValueTo(0.5)
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
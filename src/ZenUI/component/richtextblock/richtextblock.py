from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QSize, QMargins, QRectF
from PySide6.QtGui import (QPainter, QFont, QFontMetrics, QPen, QTextDocument, 
                          QAbstractTextDocumentLayout, QTextCursor)
from ZenUI.component.base import ColorController, FloatController, StyleData
from ZenUI.core import ZRichTextBlockStyleData

class ZRichTextBlock(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 html: str = None,
                 selectable: bool = False):
        super().__init__(parent)
        if name: 
            self.setObjectName(name)
        
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setMinimumHeight(24)

        # 富文本相关属性
        self._html = html or ""
        self._text_document = QTextDocument()
        self._text_cursor = None
        self._font = QFont("Microsoft YaHei", 10)
        self._margins = QMargins(0, 0, 0, 0)
        self._word_wrap = False  # 富文本默认启用自动换行
        self._alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        # 选择相关属性
        self._selectable = selectable
        self._is_selecting = False
        self._drag_start_pos = None

        # 样式控制器
        self._text_cc = ColorController(self)
        self._text_back_cc = ColorController(self)
        self._body_cc = ColorController(self)
        self._border_cc = ColorController(self)
        self._radius_ctrl = FloatController(self)
        self._style_data = StyleData[ZRichTextBlockStyleData](self, 'ZRichTextBlock')
        self._style_data.styleChanged.connect(self._styleChangeHandler)

        self._initStyle()
        self._setup_document()

    # region Properties
    @property
    def textColorCtrl(self) -> ColorController: 
        return self._text_cc

    @property
    def bodyColorCtrl(self) -> ColorController: 
        return self._body_cc

    @property
    def borderColorCtrl(self) -> ColorController: 
        return self._border_cc

    @property
    def radiusCtrl(self) -> FloatController: 
        return self._radius_ctrl

    @property
    def styleData(self): 
        return self._style_data

    @property
    def html(self) -> str: 
        return self._html

    @html.setter
    def html(self, html: str) -> None:
        self._html = html
        self._setup_document()
        self.adjustSize()
        self.update()

    @property
    def selectable(self) -> bool: 
        return self._selectable

    @selectable.setter
    def selectable(self, selectable: bool) -> None:
        self._selectable = selectable
        if selectable:
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        else:
            self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
            self._clear_selection()
        self.update()

    @property
    def selectedText(self) -> str:
        if self._text_cursor and self._text_cursor.hasSelection():
            return self._text_cursor.selectedText()
        return ""

    @property
    def font(self) -> QFont: 
        return self._font

    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self._setup_document()
        self.adjustSize()
        self.update()

    # region Public Methods
    def setHtml(self, html: str) -> None:
        self.html = html

    def setPlainText(self, text: str) -> None:
        self._html = text
        self._text_document.setPlainText(text)
        self.adjustSize()
        self.update()

    def setSelectable(self, selectable: bool) -> None:
        self.selectable = selectable

    def setFont(self, font: QFont) -> None:
        self.font = font

    def setFontFamily(self, family: str) -> None:
        self._font.setFamily(family)
        self._setup_document()
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

    def toPlainText(self) -> str:
        return self._text_document.toPlainText()

    def toHtml(self) -> str:
        return self._text_document.toHtml()

    def selectAll(self) -> None:
        if not self._text_cursor:
            self._text_cursor = QTextCursor(self._text_document)
        self._text_cursor.select(QTextCursor.SelectionType.Document)
        self.update()

    def copy(self) -> None:
        if self.selectedText:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.selectedText)

    def sizeHint(self):
        padding_w = self._margins.left() + self._margins.right()
        padding_h = self._margins.top() + self._margins.bottom()
        extra_w = 4  # 宽度补偿
        extra_h = 4  # 高度补偿

        # 确保文档设置正确
        self._setup_document()
        doc_size = self._text_document.size()

        return QSize(
            int(doc_size.width()) + padding_w + extra_w,
            int(doc_size.height()) + padding_h + extra_h
        )

    def adjustSize(self):
        size = self.sizeHint()
        self.resize(size)


    # region Private Methods
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

    def _setup_document(self):
        """设置富文本文档"""
        self._text_document.setDefaultFont(self._font)

        if self._html:
            self._text_document.setHtml(self._html)

        # 根据自动换行设置文档宽度
        if self._word_wrap:
            rect = self.rect()
            text_width = rect.width() - self._margins.left() - self._margins.right()
            if text_width > 0:
                self._text_document.setTextWidth(text_width)
        else:
            self._text_document.setTextWidth(-1)

    def _clear_selection(self):
        """清除选中"""
        if self._text_cursor:
            self._text_cursor.clearSelection()
        self._is_selecting = False
        self.update()

    def _get_position_at_point(self, point):
        """获取点击位置对应的文档位置"""
        # 计算文本绘制区域
        m = self._margins
        text_rect = self.rect().adjusted(m.left(), m.top(), -m.right(), -m.bottom())

        # 转换为相对于文档的坐标
        relative_point = point - text_rect.topLeft()

        # 使用文档布局来获取位置
        layout = self._text_document.documentLayout()
        return layout.hitTest(relative_point, Qt.HitTestAccuracy.ExactHit)

    def _draw_selection_background(self, painter: QPainter):
        """绘制圆角选中背景"""
        if not self._text_cursor.hasSelection():
            return

        layout = self._text_document.documentLayout()
        selection_start = self._text_cursor.selectionStart()
        selection_end = self._text_cursor.selectionEnd()

        # 获取选中区域的几何信息
        start_block = self._text_document.findBlock(selection_start)
        end_block = self._text_document.findBlock(selection_end)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._text_back_cc.color)

        # 处理单行选择
        if start_block.blockNumber() == end_block.blockNumber():
            # 获取选中部分在行内的位置
            block_layout = layout.blockBoundingRect(start_block)

            # 计算选中文本的水平范围
            block_text = start_block.text()
            start_pos = selection_start - start_block.position()
            end_pos = selection_end - start_block.position()

            font_metrics = QFontMetrics(self._font)
            x1 = font_metrics.horizontalAdvance(block_text[:start_pos])
            x2 = font_metrics.horizontalAdvance(block_text[:end_pos])

            # 绘制圆角选中矩形
            selection_rect = QRectF(
                block_layout.left() + x1,
                block_layout.top(),
                x2 - x1,
                block_layout.height() + 1
            )
            painter.drawRoundedRect(selection_rect, 4, 4)

        else:
            # 处理多行选择
            current_block = start_block
            while current_block.isValid() and current_block.blockNumber() <= end_block.blockNumber():
                block_layout = layout.blockBoundingRect(current_block)

                if current_block.blockNumber() == start_block.blockNumber():
                    # 第一行：从选择开始到行尾
                    block_text = current_block.text()
                    start_pos = selection_start - current_block.position()
                    font_metrics = QFontMetrics(self._font)
                    x1 = font_metrics.horizontalAdvance(block_text[:start_pos])

                    selection_rect = QRectF(
                        block_layout.left() + x1,
                        block_layout.top(),
                        block_layout.width() - x1,
                        block_layout.height() + 1
                    )
                    painter.drawRoundedRect(selection_rect, 4, 4)

                elif current_block.blockNumber() == end_block.blockNumber():
                    # 最后一行：从行首到选择结束
                    block_text = current_block.text()
                    end_pos = selection_end - current_block.position()
                    font_metrics = QFontMetrics(self._font)
                    x2 = font_metrics.horizontalAdvance(block_text[:end_pos])

                    selection_rect = QRectF(
                        block_layout.left(),
                        block_layout.top(),
                        x2,
                        block_layout.height() + 1
                    )
                    painter.drawRoundedRect(selection_rect, 4, 4)

                else:
                    # 中间行：整行选中
                    painter.drawRoundedRect(block_layout, 4, 4)

                current_block = current_block.next()


    # region Event
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing |
                              QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self._radius_ctrl.value

        # 绘制背景
        if self._body_cc.color.alpha() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)

        # 绘制边框
        if self._border_cc.color.alpha() > 0:
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

        # 绘制富文本
        painter.save()
        painter.translate(text_rect.topLeft())
        painter.setClipRect(QRectF(0, 0, text_rect.width(), text_rect.height()))

        # 更新文档宽度
        if self._word_wrap:
            self._text_document.setTextWidth(text_rect.width())

        # 先绘制选中区域背景（圆角）
        if self._selectable and self._text_cursor and self._text_cursor.hasSelection():
            self._draw_selection_background(painter)

        # 创建绘制上下文
        context = QAbstractTextDocumentLayout.PaintContext()
        context.palette.setColor(context.palette.ColorRole.Text, self._text_cc.color)

        # # 如果有选择，设置选择区域
        # if self._selectable and self._text_cursor and self._text_cursor.hasSelection():
        #     selection = QAbstractTextDocumentLayout.Selection()
        #     selection.cursor = self._text_cursor
        #     selection.format.setBackground(self._text_back_cc.color)
        #     context.selections = [selection]

        # 绘制文档
        self._text_document.documentLayout().draw(painter, context)
        painter.restore()
        painter.end()

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if not self._selectable:
            super().mousePressEvent(event)
            return

        if event.button() == Qt.LeftButton:
            position = self._get_position_at_point(event.pos())
            if position >= 0:
                if not self._text_cursor:
                    self._text_cursor = QTextCursor(self._text_document)

                # 如果按住Shift键，扩展选择
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    if self._text_cursor.hasSelection():
                        self._text_cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)
                    else:
                        current_pos = self._text_cursor.position()
                        self._text_cursor.setPosition(current_pos, QTextCursor.MoveMode.MoveAnchor)
                        self._text_cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)
                else:
                    # 开始新的选择
                    self._text_cursor.setPosition(position)
                    self._is_selecting = True
                    self._drag_start_pos = event.pos()

                self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if not self._selectable:
            super().mouseMoveEvent(event)
            return

        if self._is_selecting and self._text_cursor:
            position = self._get_position_at_point(event.pos())
            if position >= 0:
                self._text_cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)
                self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._is_selecting = False
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        """处理键盘事件"""
        if not self._selectable:
            super().keyPressEvent(event)
            return

        # 处理复制操作 (Ctrl+C)
        if event.key() == Qt.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self.selectedText:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.selectedText)
            return

        # Ctrl+A 全选
        elif event.key() == Qt.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if self._html or self._text_document.toPlainText():
                if not self._text_cursor:
                    self._text_cursor = QTextCursor(self._text_document)
                self._text_cursor.select(QTextCursor.SelectionType.Document)
                self.update()
            return

        # 处理 Esc 键清除选择
        elif event.key() == Qt.Key_Escape:
            self._clear_selection()
            return

        super().keyPressEvent(event)

    def focusOutEvent(self, event):
        if self._selectable:
            self._clear_selection()
        super().focusOutEvent(event)
from PySide6.QtCore import Qt, QSize, QMargins, QTimer, QEvent
from PySide6.QtWidgets import QWidget, QPushButton, QApplication

class ZVContainer(QWidget):
    """垂直方向对齐的容器控件，支持不同间距设置和子控件同宽功能"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets: list[QWidget] = []  # 存储所有子控件的列表
        self._alignment: Qt.AlignmentFlag = Qt.AlignLeft | Qt.AlignTop  # 默认为左上对齐
        self._spacings: list[int] = []  # 存储控件间的间距，n个控件有n-1个间距
        self._default_spacing = 16  # 默认间距
        self._batch_updating = False  # 批量更新锁
        self._layout_pending = False  # 布局更新 pending 标志
        self._width_expand = False  # 是否让所有控件与最宽控件同宽
        self._shrinking = False  # 是否启用收缩功能
        self._margins = QMargins(0, 0, 0, 0)  # 新增：边距（左、上、右、下）

        # # 初始化时自动开启批量更新
        # self.startBatchUpdate()
        # # 确保所有初始化代码执行完成后再结束批量更新
        # QTimer.singleShot(0, self.endBatchUpdate)
        self.adjustSize()

    # 新增：边距属性
    @property
    def margins(self):
        return self._margins

    @margins.setter
    def margins(self, margins: QMargins):
        if self._margins != margins:
            self._margins = margins
            self.arrangeWidgets()

    # 其余属性保持不变...
    @property
    def widgets(self):
        """返回所有子控件列表"""
        return self._widgets.copy()

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, align: Qt.AlignmentFlag):
        # 确保是支持的对齐方式
        valid_alignments = (Qt.AlignLeft | Qt.AlignRight | Qt.AlignHCenter | Qt.AlignJustify |
                           Qt.AlignTop | Qt.AlignBottom | Qt.AlignVCenter)
        self._alignment = align & valid_alignments
        self.arrangeWidgets()

    @property
    def defaultSpacing(self):
        """获取默认间距"""
        return self._default_spacing

    @defaultSpacing.setter
    def defaultSpacing(self, spacing: int):
        """设置默认间距，会影响后续添加的控件间距"""
        if spacing >= 0:
            self._default_spacing = spacing

    @property
    def widthExpand(self):
        """获取是否让所有控件与最宽控件同宽"""
        return self._width_expand

    @widthExpand.setter
    def widthExpand(self, value: bool):
        """设置是否让所有控件与最宽控件同宽"""
        if self._width_expand != value:
            self._width_expand = value
            self.arrangeWidgets()

    # 公共方法保持不变...
    def addWidget(self, widget: QWidget, index: int = -1, spacing: int = None):
        """
        添加控件到容器
        index为-1时添加到末尾
        spacing为None时使用默认间距，否则设置与前一个控件的间距
        """
        if widget in self._widgets:
            return
        w_index = 0
        length = len(self._widgets)
        if index == -1:
            w_index = length
        widget.setParent(self)
        self._widgets = self._widgets[:w_index] + [widget] + self._widgets[w_index:]

        # 处理间距，使用更新后的控件数量
        s_index = length - 1
        if s_index >= 0:
            new_spacing = spacing if spacing is not None else self._default_spacing
            self._spacings = self._spacings[:s_index] + [new_spacing] + self._spacings[s_index:]

    def removeWidget(self, widget: QWidget):
        """从容器移除控件"""
        if widget in self._widgets:
            index = self._widgets.index(widget)
            self._widgets.pop(index)
            # 同时移除对应的间距
            if index > 0 and index <= len(self._spacings):
                self._spacings.pop(index - 1)
            elif index < len(self._spacings):
                self._spacings.pop(index)
            return
        raise ValueError(f"Widget provided ({widget}) is not in this container.")

    def setSpacing(self, index: int, spacing: int):
        """设置指定位置的间距（index为控件间的索引，0到n-2）"""
        if 0 <= index < len(self._spacings) and spacing >= 0:
            self._spacings[index] = spacing
            self.arrangeWidgets()

    def getSpacing(self, index: int) -> int:
        """获取指定位置的间距"""
        if 0 <= index < len(self._spacings):
            return self._spacings[index]
        return 0

    def adjustSize(self):
        """调整容器大小以适应内容"""
        size = self.sizeHint()
        preferred_w, preferred_h = size.width(), size.height()

        if not self._shrinking:
            # 和原本自身的尺寸比较，取最大者
            preferred_w = max(preferred_w, self.width())
            preferred_h = max(preferred_h, self.height())

        self.resize(preferred_w, preferred_h)

    # 修改：sizeHint 计算时加入边距
    def sizeHint(self):
        height_used = self._margins.top() + self._margins.bottom()  # 上下边距
        for obj in self._widgets:
            height_used += obj.height()
        height_used += sum(self._spacings)
        
        # 左右边距 + 最宽控件宽度
        max_width = max([0] + [widget.width() for widget in self._widgets])
        max_width += self._margins.left() + self._margins.right()
        
        return QSize(max_width, height_used)

    # 修改：计算可用空间时加入边距
    def getUsedSpace(self):
        height_used = self._margins.top() + self._margins.bottom()
        for obj in self._widgets:
            height_used += obj.height()
        height_used += sum(self._spacings)
        return height_used

    def getSpareSpace(self):
        # 总高度减去边距和已使用高度
        total_available = self.height() - (self._margins.top() + self._margins.bottom())
        used = sum(w.height() for w in self._widgets) + sum(self._spacings)
        return max(0, total_available - used)

    def startBatchUpdate(self):
        """开始批量操作，暂停布局计算"""
        self._batch_updating = True
        self._layout_pending = False

    def endBatchUpdate(self):
        """结束批量操作，触发一次布局计算"""
        self._batch_updating = False
        if self._layout_pending:
            self.adjustSize()
            self.arrangeWidgets()
            self._layout_pending = False

    # 修改：布局排列时考虑边距
    def arrangeWidgets(self):
        """根据对齐方式、间距和边距排列控件"""
        if self._batch_updating:
            self._layout_pending = True
            return

        widget_count = len(self._widgets)
        if widget_count == 0:
            return

        spare_space = self.getSpareSpace()

        # 计算起始Y坐标（根据垂直对齐方式）+ 上边距
        if self._alignment & Qt.AlignTop:
            top_used = self._margins.top()
        elif self._alignment & Qt.AlignBottom:
            top_used = self._margins.top() + spare_space
        elif self._alignment & Qt.AlignVCenter:
            top_used = self._margins.top() + (spare_space // 2)
        else:  # 默认顶部对齐
            top_used = self._margins.top()

        # 可用宽度 = 容器宽度 - 左右边距
        available_width = self.width() - (self._margins.left() + self._margins.right())

        for i, obj in enumerate(self._widgets):
            # 适应最宽控件宽度（考虑边距后的可用宽度）
            if self._width_expand:
                obj.resize(available_width, obj.height())

            # 水平对齐计算（基于可用宽度）
            if self._alignment & Qt.AlignLeft:
                x = self._margins.left()
            elif self._alignment & Qt.AlignHCenter:
                x = self._margins.left() + (available_width - obj.width()) // 2
            elif self._alignment & Qt.AlignRight:
                x = self.width() - self._margins.right() - obj.width()
            else:
                x = self._margins.left()

            # 设置控件位置
            obj.move(x, top_used)

            # 累加高度和间距（最后一个控件不需要加间距）
            top_used += obj.height()
            if i < widget_count - 1:  # 只有前面的n-1个控件需要加间距
                top_used += self._spacings[i] if i < len(self._spacings) else self._default_spacing

    # 事件处理保持不变
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.arrangeWidgets()
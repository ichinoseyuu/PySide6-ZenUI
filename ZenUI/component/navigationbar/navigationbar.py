from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QSize
from PySide6.QtGui import QMouseEvent, QEnterEvent
from .buttonmanager import ZNavBtnManager
from .navbarbutton import ZNavBarButton
from .navbartogglebutton import ZNavBarToggleButton
class Panel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._content = QWidget(self)
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(6)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop|
                                          Qt.AlignmentFlag.AlignHCenter)
        self._content.setLayout(self._content_layout)
        self._offset = 0  # 垂直滚动偏移

    @property
    def zlayout(self):
        return self._content_layout

    def _updateContentGeometry(self):
        # 内容区宽度与Panel一致，高度由内容决定
        content_height = self._content_layout.sizeHint().height()
        self._content.resize(self.width(), content_height)
        self._content.move(0, -self._offset)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._updateContentGeometry()

    def wheelEvent(self, event):
        # 计算内容总高度和可视高度
        content_height = self._content_layout.sizeHint().height()
        visible_height = self.height()
        max_offset = max(0, content_height - visible_height)
        # 滚轮方向
        delta = event.angleDelta().y()
        step = 30  # 每次滚动的像素
        if delta < 0:
            self._offset = min(self._offset + step, max_offset)
        elif delta > 0:
            self._offset = max(self._offset - step, 0)
        self._updateContentGeometry()

    def sizeHint(self):
        return self._content_layout.sizeHint()

class FooterPanel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignBottom|
                                  Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self._layout)

    @property
    def zlayout(self):
        return self._layout

class ZNavigationBar(QWidget):
    def __init__(self, name: str = 'navigationBar', parent: QWidget = None):
        super().__init__(parent)
        self._panel = Panel(self)
        self._footer_panel = FooterPanel(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._panel)
        layout.addWidget(self._footer_panel)
        layout.setStretch(0, 1)  # 主体区占据剩余空间
        layout.setStretch(1, 0)  # 页脚自适应
        self.setLayout(layout)
        self._btn_manager = ZNavBtnManager()

    @property
    def panel(self):
        return self._panel

    @property
    def footerPanel(self):
        return self._footer_panel

    def addButton(self, panel:QWidget, btn: ZNavBarButton):
        if panel is self._panel:
            self._panel.zlayout.addWidget(btn)
        elif panel is self._footer_panel:
            self._footer_panel.zlayout.addWidget(btn)
        self.adjustSize()

    def addToggleButton(self, panel:QWidget, btn: ZNavBarToggleButton):
        if panel is self._panel:
            self._panel.zlayout.addWidget(btn)
        elif panel is self._footer_panel:
            self._footer_panel.zlayout.addWidget(btn)
        self._btn_manager.addButton(btn)
        self.adjustSize()

    def adjustSize(self):
        width = max(self._panel.zlayout.sizeHint().width(), self._footer_panel.zlayout.sizeHint().width())
        self.setFixedWidth(width)
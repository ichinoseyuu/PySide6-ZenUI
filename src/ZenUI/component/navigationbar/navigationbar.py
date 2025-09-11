from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, QMargins
from PySide6.QtGui import QMouseEvent, QPainter
from ZenUI.component.layout import ZVBoxLayout
from ZenUI.core import ZDebug
from .buttonmanager import ZNavBtnManager
from .navbarbutton import ZNavBarButton
from .navbartogglebutton import ZNavBarToggleButton
class Panel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._content = QWidget(self)
        self._content.setLayout(ZVBoxLayout(self._content,margins=QMargins(0, 0, 0, 0),spacing=6,alignment=Qt.AlignTop|Qt.AlignHCenter))
        self._offset = 0  # 垂直滚动偏移

    def _updateContentGeometry(self):
        # 内容区宽度与Panel一致，高度由内容决定
        content_height = self._content.layout().sizeHint().height()
        self._content.resize(self.width(), content_height)
        self._content.move(0, -self._offset)

    def layout(self):
        return self._content.layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._updateContentGeometry()

    def wheelEvent(self, event: QMouseEvent):
        # 计算内容总高度和可视高度
        content_height = self._content.layout().sizeHint().height()
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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

class FooterPanel(QWidget):
    def __init__(self,parent: QWidget = None):
        super().__init__(parent)
        self.setLayout(ZVBoxLayout(self,margins=QMargins(0, 0, 0, 0),spacing=6,alignment=Qt.AlignBottom|Qt.AlignHCenter))

    def layout(self) -> ZVBoxLayout:
        return super().layout()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

class ZNavigationBar(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._panel = Panel(self)
        self._footer_panel = FooterPanel(self)
        self.setLayout(ZVBoxLayout(self, margins=QMargins(0, 0, 0, 0), spacing=0))
        self.layout().addWidget(self._panel, stretch=1)
        self.layout().addWidget(self._footer_panel, stretch=0)
        self._btn_manager = ZNavBtnManager()


    @property
    def panel(self):
        return self._panel

    @property
    def footerPanel(self):
        return self._footer_panel

    def addButton(self, panel:QWidget, btn: ZNavBarButton):
        if panel is self._panel:
            self._panel.layout().addWidget(btn)
        elif panel is self._footer_panel:
            self._footer_panel.layout().addWidget(btn)

    def addToggleButton(self, panel:QWidget, btn: ZNavBarToggleButton):
        if panel is self._panel:
            self._panel.layout().addWidget(btn)
        elif panel is self._footer_panel:
            self._footer_panel.layout().addWidget(btn)
        self._btn_manager.addButton(btn)

    def toggleToNextButton(self):
        self._btn_manager.toggleToNextButton()

    def toggleToLastButton(self):
        self._btn_manager.toggleToLastButton()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
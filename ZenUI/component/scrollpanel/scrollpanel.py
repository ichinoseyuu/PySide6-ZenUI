from PySide6.QtWidgets import QScrollArea, QWidget
from PySide6.QtCore import Qt
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.layout import ZColumnLayout
from ZenUI.component.container import ZBox
from ZenUI.core import Zen, ZColorSheet, ZColorTool

class ZScrollPanel(ZWidget):
    """可滚动容器组件"""
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 scroll_policy: tuple[Zen.ScrollBarPolicy, Zen.ScrollBarPolicy] = None):
        super().__init__(parent, name)
        # 创建内容容器
        self._content = ZBox(parent=self,
                             style=ZBox.Style.Monochrome,
                             )

    def _init_style(self):
        """初始化样式"""
        super()._init_style()
        self._color_sheet = ZColorSheet(self, Zen.WidgetType.Container)
        # 设置滚动条样式
        self._scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(128, 128, 128, 80);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: transparent;
                height: 8px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(128, 128, 128, 80);
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

    def contentWidget(self) -> QWidget:
        """获取内容容器"""
        return self._content

    def scrollArea(self) -> QScrollArea:
        """获取滚动区域"""
        return self._scroll_area

    def setScrollBarPolicy(self, 
                          horizontal: Zen.ScrollBarPolicy, 
                          vertical: Zen.ScrollBarPolicy):
        """设置滚动条显示策略"""
        self._scroll_area.setHorizontalScrollBarPolicy(horizontal.value)
        self._scroll_area.setVerticalScrollBarPolicy(vertical.value)

    def ensureWidgetVisible(self, widget: QWidget):
        """确保指定控件在可视区域内"""
        self._scroll_area.ensureWidgetVisible(widget)

    def scrollToTop(self):
        """滚动到顶部"""
        self._scroll_area.verticalScrollBar().setValue(0)

    def scrollToBottom(self):
        """滚动到底部"""
        self._scroll_area.verticalScrollBar().setValue(
            self._scroll_area.verticalScrollBar().maximum()
        )
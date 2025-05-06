from PySide6.QtWidgets import QScrollArea, QWidget
from PySide6.QtCore import Qt
from ZenUI.component.widget.widget import ZWidget
from ZenUI.component.layout.column import ZColumnLayout
from ZenUI.component.container.container import ZContainer
from ZenUI.core import Zen, ZColorSheet, ZColorTool

class ZScrollWidget(ZWidget):
    """可滚动容器组件"""
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 scroll_policy: tuple[Zen.ScrollBarPolicy, Zen.ScrollBarPolicy] = None):
        super().__init__(parent, name)
        # 创建滚动区域
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QScrollArea.NoFrame)

        # 创建内容容器
        self._content = ZContainer(self._scroll_area)
        self._scroll_area.setWidget(self._content)
        
        # 设置滚动条策略
        if scroll_policy:
            h_policy, v_policy = scroll_policy
            self._scroll_area.setHorizontalScrollBarPolicy(h_policy)
            self._scroll_area.setVerticalScrollBarPolicy(v_policy)
        
        # 初始化布局
        super().setLayout(ZColumnLayout(self))
        self.layout().addWidget(self._scroll_area)

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
        self._scroll_area.setHorizontalScrollBarPolicy(horizontal)
        self._scroll_area.setVerticalScrollBarPolicy(vertical)
    
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
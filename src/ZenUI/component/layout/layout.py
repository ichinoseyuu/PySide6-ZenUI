from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout
from PySide6.QtCore import Qt, QMargins

class ZHBoxLayout(QHBoxLayout):
    def __init__(self,
                 parent: QWidget = None,
                 margins: QMargins = QMargins(6, 6, 6, 6),
                 spacing: int = 6,
                 alignment: Qt.AlignmentFlag = None
                 ):
        super().__init__(parent)
        self.setContentsMargins(margins)
        self.setSpacing(spacing)
        if alignment: self.setAlignment(alignment)

    def getAllWidgets(self) -> list[QWidget]:
        """获取布局中所有的QWidget及其子类控件"""
        widgets = []
        for i in range(self.count()):
            item = self.itemAt(i)
            if item.widget():
                widgets.append(item.widget())
        return widgets

class ZVBoxLayout(QVBoxLayout):
    def __init__(self,
                 parent: QWidget = None,
                 margins: QMargins = QMargins(6, 6, 6, 6),
                 spacing: int = 6,
                 alignment: Qt.AlignmentFlag = None
                 ):
        super().__init__(parent)
        self.setContentsMargins(margins)
        self.setSpacing(spacing)
        if alignment: self.setAlignment(alignment)

    def getAllWidgets(self) -> list[QWidget]:
        """获取布局中所有的QWidget及其子类控件"""
        widgets = []
        for i in range(self.count()):
            item = self.itemAt(i)
            if item.widget():
                widgets.append(item.widget())
        return widgets

class ZGridLayout(QGridLayout):
    def __init__(self,
                 parent: QWidget = None,
                 margins: QMargins = QMargins(6, 6, 6, 6),
                 spacing: int = 6,
                 alignment: Qt.AlignmentFlag = None
                 ):
        super().__init__(parent)
        self.setContentsMargins(margins)
        self.setSpacing(spacing)
        if alignment: self.setAlignment(alignment)

    def getAllWidgets(self) -> list[QWidget]:
        """获取布局中所有的QWidget及其子类控件"""
        widgets = []
        for i in range(self.count()):
            item = self.itemAt(i)
            if item.widget():
                widgets.append(item.widget())
        return widgets
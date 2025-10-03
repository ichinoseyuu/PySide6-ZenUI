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

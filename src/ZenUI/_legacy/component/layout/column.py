from PySide6.QtWidgets import QVBoxLayout
from ZenUI._legacy.component.basewidget import ZWidget
from ZenUI._legacy.core import ZMargins,Zen

class ZColumnLayout(QVBoxLayout):
    '''垂直布局'''
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 margins: ZMargins = ZMargins(0, 0, 0, 0),
                 spacing: int = 0,
                 alignment:Zen.Alignment = None
                 ):
        super().__init__(parent)
        if name:
            self.setObjectName(name)
        self.setContentsMargins(margins.toQmargins())
        self.setSpacing(spacing)
        if alignment:
            self.setAlignment(alignment.value)
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class ZToolTipContent(QWidget):
    pass

class ZToolTip(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|
                            Qt.WindowType.WindowStaysOnTopHint|
                            Qt.WindowType.Tool |
                            Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._is_shown = False
        '是否已经显示'
        self._completely_hide = False
        '是否已经完全隐藏'
        self._inside_of: QWidget = None
        '鼠标悬停的控件'
        self._margin = 8
        '给阴影预留的间隔空间'
        self._content = ZToolTipContent(self)


if __name__ == '__main__':
    app = QApplication([])
    tooltip = ZToolTip()
    tooltip.setText('This is a tooltip')
    tooltip.show()
    app.exec()
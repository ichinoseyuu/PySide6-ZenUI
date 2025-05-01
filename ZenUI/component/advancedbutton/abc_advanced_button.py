from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.widget.widget import ZWidget

class ABCAdvancedButton(QWidget):
    '''高级按钮抽象类'''
    hovered = Signal() # 悬停信号
    pressed = Signal() # 按下信号
    released = Signal() # 释放信号
    clicked = Signal() # 点击信号
    toggled = Signal(bool) # 切换信号
    leaved = Signal() # 离开信号
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 is_checkable: bool = False,
                 is_checked: bool = False):
        super().__init__(parent, name)
        self._is_checkable = is_checkable
        self._is_checked = is_checked
        self.hovered.connect(self._hovered_handler)
        self.pressed.connect(self._pressed_handler)
        self.released.connect(self._released_handler)
        self.clicked.connect(self._clicked_handler)
        self.toggled.connect(self._toggled_handler)
        self.leaved.connect(self._leaved_handler)
        self.setMouseTracking(True)


    # region Event
    def mouseMoveEvent(self, event):
        pass


    def enterEvent(self, event):
        super().enterEvent(event)
        self.hovered.emit()


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed.emit()


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.released.emit()
        self.clicked.emit()
        if self._is_checkable:
            self._is_checked = not self._is_checked
            self.toggled.emit()


    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.leaved.emit()

    # region Slot
    def _hovered_handler(self):
        '''悬停信号槽函数'''
        pass

    def _pressed_handler(self):
        '''按下信号槽函数'''
        pass

    def _released_handler(self):
        '''释放信号槽函数'''
        pass

    def _clicked_handler(self):
        '''点击信号槽函数'''
        pass

    def _toggled_handler(self, checked: bool):
        '''切换信号槽函数'''
        pass

    def _leaved_handler(self):
        '''离开信号槽函数'''
        pass
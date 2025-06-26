from PySide6.QtCore import QObject, Signal
from typing import Dict, List, Optional, Any
from .navbartogglebutton import ZNavBarToggleButton
class ZNavBtnManager(QObject):
    """按钮组管理器,用于管理一组按钮"""
    buttonToggled = Signal(str, bool)
    '切换信号(按钮名称, 是否选中)'
    buttonChanged = Signal(str, str)
    '选中信号（上一个按钮名称, 当前按钮名称）'
    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: Dict[str, ZNavBarToggleButton] = {}
        self._checked_button_last: Optional[str] = None
        self._checked_button: Optional[str] = None
        self._btn_count = 0
        self._enabled = True


    def addButton(self, button:ZNavBarToggleButton) -> None:
        """添加按钮到组中"""
        if not button.objectName():
            raise ValueError("Button must have a name")
        name = button.objectName()
        if name in self._buttons:
            raise ValueError(f"Button with name '{name}' already exists")
        self._buttons[name] = button
        # 使用clicked信号代替toggled信号
        button.clicked.connect(lambda: self._handle_button_clicked(name))
        if len(self._buttons) == 1: self.setCheckedButton(name)
        self._btn_count += 1



    def removeButton(self, button:ZNavBarToggleButton) -> None:
        """从组中移除按钮"""
        name = button.objectName()
        if name in self._buttons:
            del self._buttons[name]
            if name == self._checked_button:
                self._checked_button = None


    def setEnabled(self, enabled: bool) -> None:
        """设置按钮组是否启用"""
        self._enabled = enabled
        for button in self._buttons.values():
            button.setEnabled(enabled)


    def checkedButton(self):
        """获取当前选中的按钮"""
        return self._buttons.get(self._checked_button) if self._checked_button else None


    def setCheckedButton(self, name: str, clicked: bool = True):
        """设置选中的按钮"""
        if not self._enabled or name not in self._buttons: return
        button = self._buttons[name]
        # 取消之前选中的按钮
        if self._checked_button and self._checked_button != name:
            old_button = self._buttons[self._checked_button]
            old_button.checked = False
            old_button.leaved.emit()
        # 设置新的选中按钮
        if clicked: button.clicked.emit()
        button.checked = True
        # 发送信号
        if self._checked_button != name:
            self._checked_button_last = self._checked_button
            self._checked_button = name
            self.buttonChanged.emit(self._checked_button_last, name)
        self.buttonToggled.emit(name, True)



    def _handle_button_clicked(self, name: str):
        """处理按钮点击事件"""
        if not self._enabled: return
        if name == self._checked_button: return
        # 点击新按钮时
        self._checked_button_last = self._checked_button
        self._checked_button = name
        if self._checked_button_last:
            # 取消之前选中的按钮
            old_button = self._buttons[self._checked_button_last]
            old_button.checked = False
            old_button.leaved.emit()
        self.buttonChanged.emit(self._checked_button_last, name)
        self.buttonToggled.emit(name, True)


    def toggleToNextButton(self, clicked: bool = True):
        """切换到下一个按钮,仅互斥模式有效"""
        current = self.checkedButton()
        if not current:
            return
        buttons = list(self._buttons.values())
        current_index = buttons.index(current)
        next_index = (current_index + 1) % len(buttons)
        next_button = buttons[next_index]
        self.setCheckedButton(next_button.objectName(), clicked)


    def toggleToLastButton(self, clicked: bool = True):
        """切换到上一个按钮,仅互斥模式有效"""
        current = self.checkedButton()
        if not current:
            return
        buttons = list(self._buttons.values())
        current_index = buttons.index(current)
        prev_index = (current_index - 1) % len(buttons)
        prev_button = buttons[prev_index]
        self.setCheckedButton(prev_button.objectName(), clicked)

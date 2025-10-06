from PySide6.QtCore import QObject, Signal
from typing import Dict, List, Optional, Any
from ZenUI.component.abstract import ABCToggleButton

class ButttonGroup(QObject):
    """通用按钮组管理器,用于管理一组按钮"""
    toggled = Signal()
    '切换信号'

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: Dict[int, ABCToggleButton] = {}  # 使用int作为key
        self._checked_button_last: Optional[int] = None
        self._checked_button: Optional[int] = None
        self._btn_count = 0
        self._enabled = True
        self._next_available_key = 0  # 用于自动生成唯一key的计数器


    def checkedButton(self) -> Optional[ABCToggleButton]:
        """获取当前选中的按钮"""
        return self._buttons.get(self._checked_button)


    def getButton(self, key: int) -> Optional[ABCToggleButton]:
        """通过key获取按钮"""
        return self._buttons.get(key)


    def addButton(self, button: ABCToggleButton, key: Optional[int] = None) -> int:
        """
        添加按钮到组中

        Args:
            button: 要添加的按钮
            key: 可选的按钮key,不提供则自动生成

        Returns:
            按钮对应的key

        Raises:
            ValueError: 当提供的key已存在时
        """
        # 处理key生成逻辑
        if key is not None:
            if key in self._buttons:
                raise ValueError(f"Button with key '{key}' already exists")
            used_key = key
        else:
            # 自动生成不重复的key
            while self._next_available_key in self._buttons:
                self._next_available_key += 1
            used_key = self._next_available_key
            self._next_available_key += 1

        self._buttons[used_key] = button
        # 连接点击信号
        button.clicked.connect(lambda: self._handle_button_clicked(used_key))

        # 第一个按钮默认选中
        if self._btn_count == 0:
            self.setCheckedButton(used_key)

        self._btn_count += 1
        return used_key


    def removeButton(self, key: int) -> None:
        """通过key从组中移除按钮"""
        if key in self._buttons:
            del self._buttons[key]
            self._btn_count -= 1
            # 如果移除的是当前选中按钮，清除选中状态
            if key == self._checked_button:
                self._checked_button = None
                self._checked_button_last = None


    def setEnabled(self, enabled: bool) -> None:
        """设置按钮组是否启用"""
        self._enabled = enabled
        for button in self._buttons.values():
            button.setEnabled(enabled)


    def setCheckedButton(self, key: int, clicked: bool = True):
        """设置选中的按钮"""
        if not self._enabled or key not in self._buttons:
            return

        button = self._buttons[key]
        # 取消之前选中的按钮
        if self._checked_button is not None and self._checked_button != key:
            old_button = self._buttons[self._checked_button]
            # 假设按钮有checked属性，若使用QPushButton可改为setChecked(False)
            old_button.setChecked(False)
            # 如果按钮有leaved信号则发射（通用按钮可能没有，可根据实际需求调整）
            if hasattr(old_button, 'leaved') and callable(old_button.leaved):
                old_button.leaved.emit()

        # 发射点击信号（如果需要）
        if clicked:
            button.clicked.emit()

        # 设置新按钮为选中状态
        button.checked = True

        # 发送状态变化信号
        if self._checked_button != key:
            self._checked_button_last = self._checked_button
            self._checked_button = key
            #self.buttonChanged.emit(self._checked_button_last, key)

        #self.buttonToggled.emit(key, True)
        self.toggled.emit()


    def _handle_button_clicked(self, key: int):
        """处理按钮点击事件"""
        if not self._enabled:
            return

        # 如果点击的是已选中按钮则忽略
        if key == self._checked_button:
            return

        # 更新选中状态
        self._checked_button_last = self._checked_button
        self._checked_button = key

        # 取消之前选中按钮
        if self._checked_button_last is not None:
            old_button = self._buttons[self._checked_button_last]
            old_button.checked = False
            if hasattr(old_button, 'leaved') and callable(old_button.leaved):
                old_button.leaved.emit()

        # 发送状态变化信号
        #self.buttonChanged.emit(self._checked_button_last, key)
        #self.buttonToggled.emit(key, True)
        self.toggled.emit()


    def toggleToNextButton(self, clicked: bool = True):
        """切换到下一个按钮"""
        current = self.checkedButton()
        if not current:
            return

        # 获取有序按钮列表
        buttons = list(self._buttons.values())
        current_index = buttons.index(current)
        next_index = (current_index + 1) % len(buttons)
        next_button = buttons[next_index]

        # 查找下一个按钮的key
        next_key = next(k for k, v in self._buttons.items() if v == next_button)
        self.setCheckedButton(next_key, clicked)


    def toggleToLastButton(self, clicked: bool = True):
        """切换到上一个按钮"""
        current = self.checkedButton()
        if not current:
            return

        # 获取有序按钮列表
        buttons = list(self._buttons.values())
        current_index = buttons.index(current)
        prev_index = (current_index - 1) % len(buttons)
        prev_button = buttons[prev_index]

        # 查找上一个按钮的key
        prev_key = next(k for k, v in self._buttons.items() if v == prev_button)
        self.setCheckedButton(prev_key, clicked)
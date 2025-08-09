from PySide6.QtCore import QObject, Signal
from typing import Dict, List, Optional
from ZenUI._legacy.component.button.togglebutton import ZToggleButton

class ZButtonGroupManager(QObject):
    """按钮组管理器,用于管理一组按钮"""
    buttonToggled = Signal(str, bool)
    '切换信号(按钮名称, 是否选中)'
    buttonChanged = Signal(str, str)
    '选中信号（上一个按钮名称, 当前按钮名称）仅互斥模式有效'
    def __init__(self, exclusive: bool = True):
        """初始化按钮组
        Args:
            exclusive: 是否互斥,True表示同一时间只能有一个按钮被选中
        """
        super().__init__()
        self._buttons: Dict[str, ZToggleButton] = {}
        '按钮字典'
        self._checked_button_last: Optional[str] = None
        '上一个选中的按钮,仅互斥模式有效'
        self._checked_button: Optional[str] = None
        '当前选中的按钮,仅互斥模式有效'
        self._checked_buttons: List[str] = []
        '所有选中的按钮,仅非互斥模式有效'
        self._btn_count = 0
        '按钮数量'
        self._exclusive = exclusive
        '是否互斥'
        self._enabled = True
        '按钮组是否启用'


    def addButton(self, button: ZToggleButton) -> None:
        """添加按钮到组中"""
        if not button.objectName():
            raise ValueError("Button must have a name")
        name = button.objectName()
        if name in self._buttons:
            raise ValueError(f"Button with name '{name}' already exists")
        self._buttons[name] = button
        # 使用clicked信号代替toggled信号
        button.clicked.connect(lambda: self._handle_button_clicked(name))
        #如果是第一个按钮且是互斥模式，则设置为选中状态
        if len(self._buttons) == 1 and self._exclusive:
            self.setCheckedButton(name)
        self._btn_count += 1



    def removeButton(self, button: ZToggleButton) -> None:
        """从组中移除按钮"""
        name = button.objectName()
        if name in self._buttons:
            del self._buttons[name]
            if name == self._checked_button:
                self._checked_button = None


    def setExclusive(self, exclusive: bool) -> None:
        """设置是否互斥"""
        self._exclusive = exclusive


    def setEnabled(self, enabled: bool) -> None:
        """设置按钮组是否启用"""
        self._enabled = enabled
        for button in self._buttons.values():
            button.setEnabled(enabled)


    def checkedButton(self) -> Optional[ZToggleButton]:
        """获取当前选中的按钮"""
        return self._buttons.get(self._checked_button) if self._checked_button else None


    def setCheckedButton(self, name: str, clicked: bool = True):
        """设置选中的按钮"""
        if not self._enabled or name not in self._buttons:
            return
        button = self._buttons[name]
        if self._exclusive:
            # 取消之前选中的按钮
            if self._checked_button and self._checked_button != name:
                old_button = self._buttons[self._checked_button]
                old_button.setChecked(False)
                old_button.leaved.emit()
            # 设置新的选中按钮
            if clicked: button.clicked.emit()
            button.setChecked(True)
            # 发送信号
            if self._checked_button != name:
                self._checked_button_last = self._checked_button
                self._checked_button = name
                self.buttonChanged.emit(self._checked_button_last, name)
            self.buttonToggled.emit(name, True)
            return
        # 非互斥模式
        is_checked = not button.isChecked()
        button.setChecked(is_checked)
        if is_checked:
            self._checked_buttons.append(name)
        else:
            self._checked_buttons.remove(name)
        self.buttonToggled.emit(name, is_checked)



    def _handle_button_clicked(self, name: str):
        """处理按钮点击事件"""
        if not self._enabled:
            return
        button = self._buttons[name]
        if self._exclusive:
            # 如果点击当前选中按钮，保持选中状态
            if name == self._checked_button:
                # 由于click事件在toggled事件之前触发，先手动手动设置为非checked状态
                # 之后按钮的toggled事件会自动设置为checked状态
                button.setChecked(False)
                return
            # 点击新按钮时
            self._checked_button_last = self._checked_button
            self._checked_button = name
            # 按钮的toggled事件会自动设置为checked状态，无需手动设置
            if self._checked_button_last:
                # 取消之前选中的按钮
                old_button = self._buttons[self._checked_button_last]
                old_button.setChecked(False)
                old_button.leaved.emit()
            # 发送信号
            self.buttonChanged.emit(self._checked_button_last, name)
            self.buttonToggled.emit(name, True)
            return
        # 非互斥模式
        # 获取点击后的预期状态
        is_checked = not button.isChecked()
        if is_checked:
            self._checked_buttons.append(name)
        else:
            self._checked_buttons.remove(name)
        self.buttonToggled.emit(name, is_checked)


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

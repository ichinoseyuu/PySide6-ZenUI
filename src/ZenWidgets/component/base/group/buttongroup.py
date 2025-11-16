from PySide6.QtCore import QObject, Signal
from typing import Dict, List, Optional, Any, overload
from ZenWidgets.component.base.abstract import ABCToggleButton
from functools import partial
from itertools import count
class ZButtonGroup(QObject):
    """通用按钮组管理器,用于管理一组按钮"""
    toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: Dict[int, ABCToggleButton] = {}
        self._checked_button_last: Optional[int] = None
        self._checked_key: Optional[int] = None
        self._enabled = True
        self._key_counter = count(0)
        self._callbacks: Dict[int, Any] = {}

    def isEnabled(self) -> bool:
        return self._enabled

    def setEnabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)
        for button in self._buttons.values():
            button.setEnabled(self._enabled)

    def buttons(self) -> List[ABCToggleButton]:
        return list(self._buttons.values())

    def checkedButtonKey(self) -> Optional[int]:
        return self._checked_key

    def checkedButton(self) -> Optional[ABCToggleButton]:
        return self._buttons.get(self._checked_key)

    def lastCheckedButtonKey(self) -> Optional[int]:
        return self._checked_button_last

    def lastCheckedButton(self) -> Optional[ABCToggleButton]:
        return self._buttons.get(self._checked_button_last)

    def count(self) -> int:
        return len(self._buttons)

    def getButton(self, key: int) -> Optional[ABCToggleButton]:
        return self._buttons.get(key)

    def addButton(self,
                  button: ABCToggleButton,
                  key: Optional[int] = None,
                  is_checked: bool = False,
                  set_first_checked: bool = True) -> int:

        if key is None:
            while True:
                k = next(self._key_counter)
                if k not in self._buttons:
                    used_key = k
                    break
        else:
            if key in self._buttons:
                raise ValueError(f"Button with key '{key}' already exists")
            used_key = key

        self._buttons[used_key] = button
        button.setButtonGroup(self)

        # 创建并保存回调以便将来断开
        cb_toggled = partial(self._button_toggle_handler_, used_key)
        button.toggled.connect(cb_toggled)
        self._callbacks[used_key] = cb_toggled

        # 根据参数决定是否设置选中状态
        if is_checked or (len(self._buttons) == 1 and set_first_checked):
            self.toggleTo(used_key)

        return used_key

    @overload
    def removeButton(self, key: int) -> None: ...

    @overload
    def removeButton(self, button: ABCToggleButton) -> None: ...

    def removeButton(self, arg):
        key_to_remove: Optional[int] = None
        if isinstance(arg, int):
            key_to_remove = arg if arg in self._buttons else None
        else:
            for k, v in self._buttons.items():
                if v is arg:
                    key_to_remove = k
                    break
        if key_to_remove is None: return
        # 断开信号连接
        try:
            toggled_cb = self._callbacks.pop(key_to_remove, (None, None))
            btn = self._buttons[key_to_remove]
            if toggled_cb is not None:
                try:
                    btn.toggled.disconnect(toggled_cb)
                except Exception:
                    pass
        except Exception:
            pass
        # 从容器中移除
        del self._buttons[key_to_remove]

        # 如果移除的是当前选中项，清理状态
        if key_to_remove == self._checked_key:
            self._checked_key = None
            self._checked_button_last = None

    def toggleTo(self, key: int):
        '''外部调用，手动设置选中按钮'''
        if not self._enabled or key not in self._buttons: return
        if self._checked_key == key: return
        # 取消之前选中
        if self._checked_key is not None and self._checked_key in self._buttons:
            old_button = self._buttons[self._checked_key]
            old_button.setChecked(False)
            old_button._mouse_leave_()
            old_button.leaved.emit()
        # 设置新选中
        new_button = self._buttons[key]
        new_button.setChecked(True)
        self._checked_button_last = self._checked_key
        self._checked_key = key
        self.toggled.emit()

    def _button_toggle_handler_(self, key: int, checked: bool):
        """处理按钮自身的选中状态变化"""
        if not checked: return
        if not self._enabled or key not in self._buttons: return
        if self._checked_key == key:
            self.toggled.emit()
            return
        if self._checked_key is not None and self._checked_key in self._buttons:
            old_button = self._buttons[self._checked_key]
            old_button.setChecked(False)
            old_button._mouse_leave_()
            old_button.leaved.emit()
        self._checked_button_last = self._checked_key
        self._checked_key = key
        self.toggled.emit()

    def toggleToNextButton(self, clicked: bool = True):
        if not self._buttons or self._checked_key is None: return
        keys = list(self._buttons.keys())
        try:
            idx = keys.index(self._checked_key)
        except ValueError:
            return
        next_key = keys[(idx + 1) % len(keys)]
        self.toggleTo(next_key)
        if clicked: self._buttons[next_key].clicked.emit()

    def toggleToLastButton(self, clicked: bool = True):
        if not self._buttons or self._checked_key is None: return
        keys = list(self._buttons.keys())
        try:
            idx = keys.index(self._checked_key)
        except ValueError:
            return
        prev_key = keys[(idx - 1) % len(keys)]
        self.toggleTo(prev_key)
        if clicked: self._buttons[prev_key].clicked.emit()

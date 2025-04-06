from PySide6.QtWidgets import QWidget
from ZenUI.component.layer.layer import ZenLayer
class ButtonLayer(ZenLayer):
    """用于按钮的背景和高亮层"""
    def __init__(self, parent: QWidget | None= None):
        super().__init__(parent)
        self._schedule_update()

    def reloadStyleSheet(self):
        if self._fixed_stylesheet:
            return self._fixed_stylesheet+'\n'+f'background-color: {self._bg_color};'
        else:
            return f'background-color: {self._bg_color};'
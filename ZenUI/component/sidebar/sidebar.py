from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.container.container import ZenContainer
from ZenUI.core import Zen, ZenExpAnim
class ZenSidebar(ZenContainer):
    def __init__(self, parent: QWidget = None, name: str = None, dir = Zen.Direction.Left):
        super().__init__(parent, name)
        self._state = Zen.State.Collapsed
        self._collapse_dir = dir
        self._expand_width = 150
        self._collapse_width = 0

        self._anim_collapse = ZenExpAnim(self)
        self._anim_collapse.setBias(0.25)
        self._anim_collapse.setFactor(1)
        self._anim_collapse.connect(self._collapse_handler)

        self._anim_group.addMember(self._anim_collapse,'collapse')

        self.setMinimumWidth(self._collapse_width)
        self.setMaximumWidth(self._collapse_width)


    def _collapse_handler(self):
        pass
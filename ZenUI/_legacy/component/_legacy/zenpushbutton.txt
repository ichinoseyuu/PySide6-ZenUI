from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from .abcbutton import ABCButton
from .buttonlayer import BodyLayer,TextLayer
from ....core import Zen,ZenGlobal
class ZenPushButton(ABCButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 按钮表面
        self._body = BodyLayer(self)
        self._body.lower()
        self._text = TextLayer(self)
        #self.body.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setAttachmentShifting(0, 4)
        # 绑定到主体
        self.setAttachment(self._text)

    def setText(self, text):
        self._text.setText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self._hover_layer.resize(w, h - 3)
        self._flash_layer.resize(w, h - 3)
        self._body.resize(w, h - 3)

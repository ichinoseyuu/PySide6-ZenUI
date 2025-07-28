from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QFont, QIcon
from ZenUI import *


class DemoCard(ZCard):
    def __init__(self, parent=None):
        super().__init__(parent)
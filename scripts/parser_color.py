from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

print(QColor(0, 0, 0).name())
print(QColor(0, 0, 0).name(QColor.HexArgb))
print(QColor(100, 100, 255, 80).name(QColor.HexArgb))
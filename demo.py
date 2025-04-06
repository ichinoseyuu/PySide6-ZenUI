import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI import *


class ZenUIDemo(ZenMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(800, 600)
        self.setWindowTitle('ZenUI')

        self.Board = ZenContainer(self,'Board')
        #self.Board.setWidgetFlag(Zen.WidgetFlag.GradientColor)
        self.addWidget(self.Board)
        self.Board.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text = """<h1 style='color: blue;'>Hello, PySide6!</h1><p>This is a <b>bold</b> and <i>italic</i> text with <font color='green'>green</font> color.</p><p><a href="https://www.qt.io" style="color: red;">Click here to visit Qt</a></p>"""
        #text = 'Hello, PySide6!'
        self.text = ZenTextLabel(self.Board, 'text')
        self.text.setText(text)
        self.text.setAlignment(Qt.AlignCenter)
        self.Board.addWidget(self.text)

        self.btnTest = ZenPushButton(self, 'btnTest')
        self.btnTest.setText('btnTest')
        self.btnTest.setFixedSize(120, 40)
        self.Board.addWidget(self.btnTest)
        # import ZenUI
        # print(ZenUI.component.)


    def light(self):
        #self.setOpacityTo(0)
        #self.widget1.resizeTo(100, 100)
        #self.widget1.moveTo(100, 100)
        # self.widget1.setColorTo('#ffffff')
        # self.widget1.setBorderColorTo('#909999')
        ZenGlobal.ui.theme_manager.setTheme(Zen.Theme.Light)
        #print(self._color_group.reference)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    window = ZenUIDemo()
    window.show()
    app.exec()
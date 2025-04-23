import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI import *


class ZenUIDemo(ZenMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.btnConnect()

    def setupUi(self):
        self.resize(800, 600)
        self.setWindowTitle('ZenUI')

        self.containerlayout = QHBoxLayout()
        self.containerlayout.setContentsMargins(0, 0, 0, 0)
        self.addLayout(self.containerlayout)


        self.leftSideMenu = ZenLeftSideMenu(self,name='leftSideMenu')

        self.containerlayout.addWidget(self.leftSideMenu)

        self.Board = ZenContainer(self,'Board')
        #self.Board.setWidgetFlag(Zen.WidgetFlag.GradientColor)
        self.containerlayout.addWidget(self.Board)

        text = """<h1 style='color: blue;'>Hello, PySide6!</h1><p>This is a <b>bold</b> and <i>italic</i> text with <font color='green'>green</font> color.</p><p><a href="https://www.qt.io" style="color: red;">Click here to visit Qt</a></p>"""
        #text = 'Hello, PySide6!'
        self.text = ZenTextLabel(self.Board, 'text')
        self.text.setText(text)
        self.text.setAlignment(Qt.AlignCenter)
        self.Board.addWidget(self.text)

        self.btnTest2 = ZenPushButton(self.Board)
        #self.btnTest2.setWidgetFlag(Zen.WidgetFlag.StyleSheetApplyToChildren)
        self.btnTest2.setText('btnTest2')
        self.btnTest2.setToolTip("btnTest2.")
        self.btnTest2.setMinimumHeight(50)
        self.Board.addWidget(self.btnTest2)


    def btnConnect(self):
        #self.btnMenuTest.clicked.connect(lambda:self.leftSideMenu.setCollapseDir(Zen.Direction.Horizontal))
        #self.btnMenu.clicked.connect(self.leftSideMenu.toggleState)
        pass


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
    QApplication.setHighDpiScaleFactorRoundingPolicy( #  设置高DPI缩放因子的舍入策略为直接传递，不进行任何处理
         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv) #  创建一个QApplication对象，用于管理GUI应用程序的控制流和主要设置
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings) #  设置应用程序属性，禁止创建原生小部件的兄弟组件，以提高性能和避免潜在的问题
    window = ZenUIDemo()
    window.show()
    app.exec()
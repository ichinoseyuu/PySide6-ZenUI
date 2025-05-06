import sys
from PySide6.QtWidgets import QApplication
from ZenUI import *
from page_home import PageHome
from page_about import PageAbout
from page_box import PageBox
from navigation_bar import LeftNavigationBar
from functools import partial

class ZenUIGallary(ZMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.btnConnect()

    def setupUi(self):
        self.resize(800, 600)
        self.setWindowTitle('ZenUIGallary')

        self._layout = ZRowLayout()
        self.addLayout(self._layout)

        self.navigationBar = LeftNavigationBar(self,'navigationBar')
        self._layout.addWidget(self.navigationBar)

        self.board = ZContainer(parent=self, name='board', layout=Zen.Layout.Column)
        self._layout.addWidget(self.board)

        self.stackContainer= ZStackContainer(parent=self.board,
                                               name='stackContainer',
                                               hide_last_page=True,)
        self.board.layout().addWidget(self.stackContainer)

        self.pageHome = PageHome(self.stackContainer)
        self.stackContainer.addPage(self.pageHome, cover=False, anim=False)

        self.pageBox = PageBox(self.stackContainer)
        self.stackContainer.addPage(self.pageBox, cover=False, anim=False)

        self.pageAbout = PageAbout(self.stackContainer)
        self.stackContainer.addPage(self.pageAbout, cover=False, anim=False)




    def btnConnect(self):
        self.navigationBar.btnHome.clicked.connect(lambda: self.stackContainer.setCurrentPage('pageHome'))
        self.navigationBar.btnBox.clicked.connect(lambda: self.stackContainer.setCurrentPage('pageBox'))
        self.navigationBar.btnAbout.clicked.connect(lambda: self.stackContainer.setCurrentPage('pageAbout'))
        self.pageHome.btn_nextpage.clicked.connect(self.navigationBar.toggleToNextButton)





if __name__ == '__main__':
    # enable dpi scale
    #QApplication.setHighDpiScaleFactorRoundingPolicy( #  设置高DPI缩放因子的舍入策略为直接传递，不进行任何处理
    #     Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv) #  创建一个QApplication对象，用于管理GUI应用程序的控制流和主要设置
    #app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings) #  设置应用程序属性，禁止创建原生小部件的兄弟组件，以提高性能和避免潜在的问题
    window = ZenUIGallary()
    window.show()
    app.exec()
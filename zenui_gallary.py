import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI import *
from page_home import PageHome
from page_about import PageAbout
from page_box import PageBox
from navigation_bar import LeftNavigationBar

class ZenUIGallary(ZMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.btnConnect()

    def setupUi(self):
        screen_size = QGuiApplication.primaryScreen().size()
        self.resize(screen_size.width()*3/5-200,screen_size.height()*3/5)
        self.setWindowTitle('ZenUIGallary')
        self.setMinimumSize(800, 600)
        self.content = ZBox(parent=self,
                               name='content',
                               style= ZBox.Style.None_,
                               layout=Zen.Layout.Row)

        self.navigationBar = LeftNavigationBar(self,'navigationBar')
        self.content.layout().addWidget(self.navigationBar)

        self.stackPanel= ZStackPanel(parent=self.content,
                                               name='stackPanel',
                                               hide_last_page=True,)

        self.pageHome = PageHome(self.stackPanel)
        self.stackPanel.addPage(self.pageHome, cover=False, anim=False)

        self.pageBox = PageBox(self.stackPanel)
        self.stackPanel.addPage(self.pageBox, cover=False, anim=False)

        self.pageAbout = PageAbout(self.stackPanel)
        self.stackPanel.addPage(self.pageAbout, cover=False, anim=False)

        self.content.layout().addWidget(self.stackPanel)

        # self.scrollPage = ZScrollPage(self)
        # self.scrollPage.setScrollBarPolicy(Zen.ScrollBarPolicy.AlwaysOn, Zen.ScrollBarPolicy.AlwaysOn)
        # self.content.layout().addWidget(self.scrollPage)

        self.addWidget(self.content)




    def btnConnect(self):
        self.navigationBar.btnHome.clicked.connect(lambda: self.stackPanel.setCurrentPage('pageHome'))
        self.navigationBar.btnBox.clicked.connect(lambda: self.stackPanel.setCurrentPage('pageBox'))
        self.navigationBar.btnAbout.clicked.connect(lambda: self.stackPanel.setCurrentPage('pageAbout'))
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
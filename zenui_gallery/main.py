import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI import *
from navigation_bar import NavigationBar
from page_home import PageHome
from page_widget import PageWidget
from page_info import PageInfo
from page_about import PageAbout
from page_settings import PageSettings

class ZenUIGallery(ZFramelessWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        #self.setMinimumSize(400, 300)
        screen_size = QGuiApplication.primaryScreen().size()
        self.resize(screen_size.width()*0.5,screen_size.height()*0.6)
        self.moveCenter()
        self.setWindowTitle("ZenUI Gallery")
        self.setWindowIcon(QIcon(":/image/icon.svg"))
        self.contentLayout = QHBoxLayout(self.centerWidget)
        self.contentLayout.setContentsMargins(6, 6, 6, 6)
        self.contentLayout.setSpacing(6)
        self.navigationBar = NavigationBar(self.centerWidget)
        self.contentLayout.addWidget(self.navigationBar)

        self.stackPanel = ZStackPanel(self.centerWidget,name="StackPanel")
        self.contentLayout.addWidget(self.stackPanel)

        self.pageHome = PageHome(self.stackPanel)
        self.stackPanel.addPage(self.pageHome)

        self.pageWidget = PageWidget(self.stackPanel)
        self.stackPanel.addPage(self.pageWidget)

        self.pageInfo = PageInfo(self.stackPanel)
        self.stackPanel.addPage(self.pageInfo)

        self.pageAbout = PageAbout(self.stackPanel)
        self.stackPanel.addPage(self.pageAbout)

        self.pageSettings = PageSettings(self.stackPanel)
        self.stackPanel.addPage(self.pageSettings)

        self.navigationBar.btnHome.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageHome))
        self.navigationBar.btnWidget.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageWidget))
        self.navigationBar.btnInfo.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageInfo))
        self.navigationBar.btnAbout.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageAbout))
        self.navigationBar.btnSettings.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageSettings))





if __name__ == '__main__':
    # enable dpi scale
    # QApplication.setHighDpiScaleFactorRoundingPolicy( #  设置高DPI缩放因子的舍入策略为直接传递，不进行任何处理
    #      Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    #app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings) #  设置应用程序属性，禁止创建原生小部件的兄弟组件，以提高性能和避免潜在的问题
    app = QApplication(sys.argv)
    window = ZenUIGallery()
    window.show()
    app.exec()
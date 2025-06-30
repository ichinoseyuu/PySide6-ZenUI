import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os
# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ZenUI import *
from navigation_bar import NavigationBar
from page_widget import PageWidget
from page_about import PageAbout
from page_home import PageHome

class ZenUIGallery(ZFramelessWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        screen_size = QGuiApplication.primaryScreen().size()
        self.resize(screen_size.width()*0.5,screen_size.height()*0.6)
        self.moveCenter()
        self.contentLayout = QHBoxLayout(self.centerWidget)
        self.contentLayout.setContentsMargins(6, 6, 6, 6)
        self.contentLayout.setSpacing(6)
        self.navigationBar = NavigationBar(self.centerWidget)
        self.contentLayout.addWidget(self.navigationBar)

        self.stackPanel = ZStackPanel(self.centerWidget,name="stackPanel")
        self.contentLayout.addWidget(self.stackPanel)

        self.pageHome = PageHome(self.stackPanel)
        self.stackPanel.addPage(self.pageHome)

        self.pageWidget = PageWidget(self.stackPanel)
        self.stackPanel.addPage(self.pageWidget)

        self.pageAbout = PageAbout(self.stackPanel)
        self.stackPanel.addPage(self.pageAbout)

        self.navigationBar.btnHome.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageHome))
        self.navigationBar.btnWidget.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageWidget))
        self.navigationBar.btnAbout.clicked.connect(lambda: self.stackPanel.setCurrentPage(self.pageAbout))





if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy( #  设置高DPI缩放因子的舍入策略为直接传递，不进行任何处理
         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv) #  创建一个QApplication对象，用于管理GUI应用程序的控制流和主要设置
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings) #  设置应用程序属性，禁止创建原生小部件的兄弟组件，以提高性能和避免潜在的问题
    window = ZenUIGallery()
    window.show()
    app.exec()
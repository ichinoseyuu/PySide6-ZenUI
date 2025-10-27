import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenWidgets import *
from navigation_bar import NavigationBar
from panel_home import PanelHome
from panel_widget import PanelWidget
from panel_test import PanelTest
from panel_info import PanelInfo
from panel_about import PanelAbout
from panel_settings import PanelSettings

class ZenUIGallery(ZStandardFramelessWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        #self.setMinimumSize(400, 300)
        screen_size = QGuiApplication.primaryScreen().size()
        self.resize(screen_size.width()*0.5,screen_size.height()*0.6)
        self.moveCenter()
        self.setWindowTitle("ZenWidgets Gallery")
        self.setWindowIcon(QIcon(":/image/icon.svg"))
        self.contentLayout = ZHBoxLayout(self.centerWidget())

        self.navigationBar = NavigationBar(self.centerWidget())
        self.contentLayout.addWidget(self.navigationBar, stretch=0)

        self.stackContainer = ZStackContainer(self.centerWidget(),name="ZStackContainer")
        self.contentLayout.addWidget(self.stackContainer, stretch=1)

        self.panelHome = PanelHome(self.stackContainer)
        self.stackContainer.addPanel(self.panelHome)

        self.panelWidget = PanelWidget(self.stackContainer)
        self.stackContainer.addPanel(self.panelWidget)

        self.panelTest = PanelTest(self.stackContainer)
        self.stackContainer.addPanel(self.panelTest)

        self.panelInfo = PanelInfo(self.stackContainer)
        self.stackContainer.addPanel(self.panelInfo)

        self.panelAbout = PanelAbout(self.stackContainer)
        self.stackContainer.addPanel(self.panelAbout)

        self.pagelSettings = PanelSettings(self.stackContainer)
        self.stackContainer.addPanel(self.pagelSettings)

        self.navigationBar.getButton(0).clicked.connect(
            lambda: self.stackContainer.setCurrentPanel(self.panelHome)
            )
        self.navigationBar.getButton(1).clicked.connect(
            lambda: self.stackContainer.setCurrentPanel(self.panelWidget)
            )
        self.navigationBar.getButton(2).clicked.connect(
            lambda: self.stackContainer.setCurrentPanel(self.panelTest)
            )
        self.navigationBar.getButton(3).clicked.connect(
            lambda: self.stackContainer.setCurrentPanel(self.panelInfo)
            )
        self.navigationBar.getButton(4).clicked.connect(
            lambda: self.stackContainer.setCurrentPanel(self.panelAbout)
            )
        self.navigationBar.getButton(6).clicked.connect(
            lambda: self.stackContainer.setCurrentPanel(self.pagelSettings)
            )


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy( #  设置高DPI缩放因子的舍入策略为直接传递，不进行任何处理
         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings) #  设置应用程序属性，禁止创建原生小部件的兄弟组件，以提高性能和避免潜在的问题
    mainwindow = ZenUIGallery()
    mainwindow.show()
    app.exec()
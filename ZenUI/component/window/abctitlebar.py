from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from enum import Enum, auto
from ZenUI.component.widget.widget import ZenWidget
from ZenUI.component.button.transbutton import ZenTransButton
from ZenUI.component.label.textlabel import ZenTextLabel
from ZenUI.core import Zen,ZenGlobal,ColorSheet,ColorTool

class TitlebarButton(ZenTransButton):
    def __init__(self, parent=None, name=None, text=None, icon=None):
        super().__init__(parent, name, text, icon)
        self.setFixedStyleSheet("")
        self._schedule_update()

class ThemeButton(TitlebarButton):
    def _theme_changed_handler(self, theme):
        super()._theme_changed_handler(theme)
        self.hoverLayer().setColorTo(self._color_sheet.getColor(theme, Zen.ColorRole.Hover))


class ABCTitlebar(ZenWidget):
    '''标题栏基类'''
    class Obj(Enum):
        """ 标题栏内部控件
        Attributes:
            Icon (auto()): 图标
            Title (auto()): 标题
            BtnMin (auto()): 最小化按钮
            BtnMax (auto()): 最大化按钮
            BtnExit (auto()): 退出按钮
        """
        Icon = auto()
        Title = auto()
        BtnMin = auto()
        BtnMax = auto()
        BtnExit = auto()

    def __init__(self, parent):
        super().__init__(parent=parent,name="titleBar")
        self._color_sheet = ColorSheet(Zen.WidgetType.Titlebar)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._anim_bg_color_a.setCurrent(ColorTool.toArray(self._bg_color_a))
        self._anim_border_color.setCurrent(ColorTool.toArray(self._border_color))
        self._fixed_stylesheet = "border-bottom-width: 1px;\nborder-style: solid;"
        self._schedule_update()
        self._init_style()
        self._btnConnect()

    # region StyleSheet
    def reloadStyleSheet(self):
        sheet = f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'
        if not self.objectName(): raise ValueError("Widget must have a name when StyleSheetApplyToChildren is False")
        if self._fixed_stylesheet:
            return f"#{self.objectName()}"+"{\n"+  sheet +'\n'+self._fixed_stylesheet +"\n}"
        else:
            return f"#{self.objectName()}"+"{\n"+ sheet +"\n}"

    # region Slot
    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A))
        self.setBorderColorTo(self._color_sheet.getColor(theme,Zen.ColorRole.Border))


    def _init_style(self):
        """创建ui"""
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self.icon = ZenTextLabel(self)
        self.icon.setObjectName(u"icon")
        self._layout.addWidget(self.icon)

        self.title = ZenTextLabel(self,name="title") # 标题
        self._layout.addWidget(self.title)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._layout.addItem(self.spacer)

        self.btnTheme = ThemeButton(self, name="btnTheme")
        self.btnTheme.setCheckable(True)
        self._layout.addWidget(self.btnTheme)

        self.btnMin = TitlebarButton(self, name="btnMin")
        self._layout.addWidget(self.btnMin)

        self.btnMax = TitlebarButton(self, name="btnMax")
        #self.btnMax.setFixedStyleSheet("width: 30px;")
        self.btnMax.setCheckable(True)
        self._layout.addWidget(self.btnMax)

        self.btnExit = TitlebarButton(self, name="btnExit")
        self._layout.addWidget(self.btnExit)



    def _btnConnect(self):
        '''按钮连接'''
        self.btnTheme.clicked.connect(self.changeTheme)
        self.btnMin.clicked.connect(self.window().showMinimized)
        self.btnMax.clicked.connect(self._maxWindow)
        self.btnExit.clicked.connect(self.window().close)

    def changeTheme(self):
        if ZenGlobal.ui.theme_manager.theme() == Zen.Theme.Dark:
            ZenGlobal.ui.theme_manager.setTheme(Zen.Theme.Light)
        else:
            ZenGlobal.ui.theme_manager.setTheme(Zen.Theme.Dark)

    def _maxWindow(self):
        '''最大化窗口'''
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()


    def hideObj(self, *args: Obj):
        '''隐藏指定对象'''
        for obj in args:
            if obj == self.Obj.Icon:
                self.icon.hide()
            elif obj == self.Obj.Title:
                self.title.hide()
            elif obj == self.Obj.BtnMin:
                self.btnMin.hide()
            elif obj == self.Obj.BtnMax:
                self.btnMax.hide()
            elif obj == self.Obj.BtnExit:
                self.btnExit.hide()
            else:
                raise ValueError(f"Unknown TitleBarObj: {obj}")


    def setTitle(self, title: str):
        '''设置标题'''
        self.title.setText(title)


    def setTitleIcon(self, icon: QPixmap|str):
        '''设置标题栏图标'''
        if isinstance(icon, str):
            self.icon.setPixmap(QPixmap(icon))
        else:
            self.icon.setPixmap(QPixmap(u":/images/icon/icon.png"))


    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() != Qt.LeftButton:
            return
        self.btnMax.click()


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and not self.window().isMaximized():
            # 记录鼠标按下时的位置
            self.dragPosition = event.globalPosition().toPoint() - self.parent().frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and not self.window().isMaximized():
            # 窗口跟随鼠标移动
            self.parent().move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()


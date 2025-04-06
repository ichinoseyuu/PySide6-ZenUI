from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component import ZenWidget, ZenLayer, ZenTextLabel
from ZenUI.core import Zen,ColorTool,ColorSheet
class ToolTip(QWidget):
    '''ZenUI提示标签'''
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._setupUi()
        self._initAnim()
        self._adjustSize()

    def _setupUi(self):
        '''初始化UI'''
        self.setObjectName("tooltip")
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.board = Container(self)
        self.board.setObjectName(u"board")
        self.verticalLayout.addWidget(self.board)


        self.boardLayout = QVBoxLayout(self.board)
        self.boardLayout.setSpacing(0)
        self.boardLayout.setObjectName(u"boardLayout")
        self.boardLayout.setContentsMargins(9, 6, 9, 6)

        self.tipLabel = ZenTextLabel(self)
        self.tipLabel.setObjectName(u"tipLabel")
        #self.tipLabel.setWordWrap(True)
        self.tipLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.boardLayout.addWidget(self.tipLabel)

    def _initAnim(self):
        self.anim_fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.anim_fade_in.setDuration(200)

        self.anim_fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.anim_fade_out.setDuration(200)
        self.anim_fade_out.finished.connect(self._stopTimer)

        self.anim_resize = QPropertyAnimation(self, b"size")
        self.anim_resize.setDuration(100)

        self.tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self.tracker_timer.setInterval(int(1000/60))
        self.tracker_timer.timeout.connect(self._refreshPos)

    def _playFadeInAnim(self):
        if self.anim_fade_out.state() == QAbstractAnimation.State.Running:
            self.anim_fade_out.stop()
        self.anim_fade_in.setStartValue(self.windowOpacity())
        self.anim_fade_in.setEndValue(1.0)
        self.anim_fade_in.start()

    def _playFadeOutAnim(self):
        if self.anim_fade_in.state() == QAbstractAnimation.State.Running:
            self.anim_fade_in.stop()
        self.anim_fade_out.setStartValue(self.windowOpacity())
        self.anim_fade_out.setEndValue(0.0)
        self.anim_fade_out.start()

    def _stopTimer(self):
        self.tracker_timer.stop()
        self.close()

    def setTipText(self, tip: str):
        '''设置提示内容'''
        self.tipLabel.setText(tip)


    def showTip(self):
        '''显示提示'''
        QTimer.singleShot(100, self._adjustSize)
        self.tracker_timer.start()
        self._playFadeInAnim()
        self.show()


    def hideTip(self):
        '''隐藏提示'''
        self._playFadeOutAnim()




    def _adjustSize(self):
        """根据控件内容调整大小"""
        # 获取子控件的大小建议
        size = self.board.sizeHint()
        # 设置新尺寸，确保不小于最小尺寸
        new_width = max(size.width(), self.minimumWidth())
        new_height = max(size.height(), self.minimumHeight())
        # 调整大小
        self.anim_resize.setStartValue(QSize(self.width(), self.height()))
        self.anim_resize.setEndValue(QSize(new_width, new_height))
        self.anim_resize.start()



    def _refreshPos(self):
        '''根据鼠标位置刷新位置'''
        pos = QCursor.pos()
        left = pos.x() + TOOLTIP_OFFSET_X
        top = pos.y() - self.height() + TOOLTIP_OFFSET_Y
        screen_geometry = QApplication.primaryScreen().availableGeometry()  # 获取屏幕可用区域
        screen_left = screen_geometry.x()
        screen_top = screen_geometry.y()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        # 确保 tooltip 不会超出屏幕右边或底部
        new_left = max(left, screen_left)  # 确保 tooltip 不会在屏幕左边界外
        new_top = max(top, screen_top)    # 确保 tooltip 不会在屏幕上边界外
        # 如果 tooltip 超出了屏幕的右边界或下边界，调整它的位置
        if new_left + self.width() > screen_left + screen_width:
            new_left = screen_left + screen_width - self.width()
        if new_top + self.height() > screen_top + screen_height:
            new_top = screen_top + screen_height - self.height()
        # 移动 tooltip 到新的位置
        self.move(new_left, new_top)

    # region 已弃用的方法
    # def _refreshPos(self):
    #     '''根据鼠标位置刷新位置'''
    #     pos = QCursor.pos()
    #     x, y = pos.x(), pos.y()
    #     left = x + TOOLTIP_OFFSET_X
    #     top = y - self.geometry().height() + TOOLTIP_OFFSET_Y
    #     mainwindow = getReference('mainwindow')
    #     if mainwindow != None and mainwindow.isMaximized():
    #         new_left = max(left, mainwindow.geometry().left())
    #         new_top = max(top, mainwindow.geometry().top())
    #         if new_left + self.width() > mainwindow.geometry().right():
    #             new_left = min(left, mainwindow.geometry().right()-self.width())
    #         if new_top + self.height() > mainwindow.geometry().bottom():
    #             new_top = min(top, mainwindow.geometry().bottom()-self.height())
    #         self.move(new_left, new_top)
    #     else:
    #         self.move(left, top)
    # endregion
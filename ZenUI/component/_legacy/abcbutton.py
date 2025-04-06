import numpy
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ..widget.zenwidget import ZenWidget
from .buttonlayer import HoverLayer,BodyLayer
from ....core import ZenExpAnim, AnimGroup, ZenColor, ZenGlobal, Zen

class ABCButton(QPushButton):
    """
    抽象按钮控件\n
    提供点击、按下、松开的信号和色彩动画
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setStyleSheet("background-color: transparent")

        self._tooltip = ''
        self._color_group = ZenGlobal.ui.color_group
        self._flash_on_clicked = True # 是否在点击时闪烁
        self._enabled_repetitive_clicking = False # 是否允许重复点击

        self._attachment = ZenWidget()                       # 占位用的被绑定部件，显示在按钮正中央
        self._attachment_shifting = numpy.array([0, 0])      # 被绑定部件偏离中心的像素数

        # 提供悬停时的颜色变化动画
        self._hover_layer = HoverLayer(self)
        self._hover_layer.stackUnder(self)  # 置于按钮的底部
        self._hover_layer.setColor(ZenColor.trans(self.getColor(Zen.ColorRole.Button_Hover), 0.0))
        self._hover_layer.AnimGroup().fromToken("color_a").setBias(0.2)
        self._hover_layer.AnimGroup().fromToken("color_a").setFactor(1/8)

        # 提供点击时的颜色变化动画
        self._flash_layer = HoverLayer(self)
        self._flash_layer.stackUnder(self)  # 置于按钮的底部
        self._flash_layer.setColor(ZenColor.trans(self.getColor(Zen.ColorRole.Button_Flash), 0.0))
        self._flash_layer.AnimGroup().fromToken("color_a").setBias(0.2)
        self._flash_layer.AnimGroup().fromToken("color_a").setFactor(1/8)

        self.clicked.connect(self._on_self_clicked)

        self._repeat_click_timer = QTimer(self)
        self._repeat_click_timer.setInterval(50)
        self._repeat_click_timer.timeout.connect(self.clicked.emit)

        self._repeat_click_trigger = QTimer(self)
        self._repeat_click_trigger.setSingleShot(True)
        self._repeat_click_trigger.timeout.connect(self._repeat_click_timer.start)
        self._repeat_click_trigger.setInterval(500)

    def setAttachmentShifting(self, x, y):
        """设置被绑定部件偏离中心的像素数，偏移量将直接与其坐标相加作为最终位置"""
        self._attachment_shifting = numpy.array([x, y])


    def setAttachment(self, widget):
        """设置绑定部件。绑定部件会被设为按钮的子控件，并显示在按钮的正中央"""
        # 删除旧的绑定部件
        self._attachment.deleteLater()
        self._attachment = widget
        self._attachment.setParent(self)
        self.resize(self.size())  # 实现刷新位置


    def attachment(self):
        """返回被绑定的部件"""
        return self._attachment


    def getColor(self, token):
        return self._color_group.fromToken(token)


    def colorGroup(self):
        """Get the color group of this widget"""
        return self._color_group


    def setToolTip(self, text: str): 
        """设置工具提示"""
        # 劫持这个按钮的tooltip，只能设置outfit的tooltip
        self._tooltip = text


    def setRepetitiveClicking(self, state):
        self._enabled_repetitive_clicking = state


    def setFixedStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        设置按钮组件固定的样式表\n
        注意，这不会设置按钮本身的固定样式表，而且不能改变相应的颜色设置，本方法只应用于更改边框圆角半径等属性
        """
        self._hover_layer.setFixedStyleSheet(style_sheet)
        self._flash_layer.setFixedStyleSheet(style_sheet)


    def setStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        设置按钮组件样式表\n
        注意，这不会设置按钮本身的样式表，而且不能改变相应的颜色设置，本方法只应用于更改边框圆角半径等属性
        """
        self._hover_layer.setStyleSheet(style_sheet)
        self._flash_layer.setStyleSheet(style_sheet)


    def reloadStyleSheet(self):
        """
        重载样式表，建议将所有设置样式表的内容重写在此方法中\n
        此方法在窗口show方法被调用时、主题改变时被调用
        :return:
        """
        self.attachment().reloadStyleSheet()
        return


    def flashLabel(self):
        """ get the label that preform flashing animations """
        return self._flash_layer


    def hoverLabel(self):
        """ get the hover-highlight label """
        return self._hover_layer


    def setFlashOnClicked(self, state: bool):
        """设置是否启用点击动画"""
        self._flash_on_clicked = state


    def _on_self_clicked(self):
        if self._flash_on_clicked is True:
            self._run_clicked_ani()


    def _run_clicked_ani(self):
        self._flash_layer.setColor(self._color_group.fromToken(Zen.ColorRole.Button_Flash))
        self._flash_layer.setColorTo(ZenColor.trans(self._color_group.fromToken(Zen.ColorRole.Button_Flash), 0))


    def flash(self):
        """ play flash animation once but do nothing else """
        self._run_clicked_ani()


    def enterEvent(self, event):
        #super().enterEvent(event)
        self._hover_layer.setColorTo(self._color_group.fromToken(Zen.ColorRole.Button_Hover))

        # if self._tooltip != "" and "TOOL_TIP" in ZenGlobal.ui.windows:
        #     ZenGlobal.ui.windows["TOOL_TIP"].setNowInsideOf(self)
        #     ZenGlobal.ui.windows["TOOL_TIP"].show()
        #     ZenGlobal.ui.windows["TOOL_TIP"].setText(self._tooltip)

    def leaveEvent(self, event):
        #super().enterEvent(event)
        self._hover_layer.setColorTo(ZenColor.trans(self._color_group.fromToken(Zen.ColorRole.Button_Hover), 0))

        # if self._tooltip != "" and "TOOL_TIP" in ZenGlobal.ui.windows:
        #     ZenGlobal.ui.windows["TOOL_TIP"].setNowInsideOf(None)
        #     ZenGlobal.ui.windows["TOOL_TIP"].hide()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if self._enabled_repetitive_clicking:
            self._repeat_click_trigger.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._repeat_click_trigger.stop()
        self._repeat_click_timer.stop()

    def adjustSize(self):
        """
        根据被绑定控件的大小调整按钮的大小
        :return:
        """
        att_size = self.attachment().size()
        preferred_width = max(32, att_size.width() + 24)
        preferred_height = max(32, att_size.height() + 8)
        self.resize(preferred_width, preferred_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self._hover_layer.resize(size)
        self._flash_layer.resize(size)
        self._attachment.move((w - self._attachment.width()) // 2 + self._attachment_shifting[0],
                              (h - self._attachment.height()) // 2 + self._attachment_shifting[1])
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.core import ZenExpAnim, ColorTool
class ZenLayer(QWidget):
    """用于实现物件表面颜色变化的组件"""
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground) #启用样式表
        self._fixed_stylesheet = '' #固定样式表
        self._bg_color = 'transparent'
        self._can_update = True
        self._anim_bg_color = ZenExpAnim(self)
        self._anim_bg_color.ticked.connect(self._bg_color_handler)

    @property
    def colorController(self):
        "获取颜色控制器"
        return self._anim_bg_color

    # region StyleSheet
    def setStyleSheet(self, stylesheet: str):
        """设置样式表"""
        super().setStyleSheet(stylesheet)
        self._can_update = True

    def setFixedStyleSheet(self, stylesheet: str):
        """
        设置样式表固定内容，此后每次运行 setStyleSheet 方法时，都会在样式表前附加这段固定内容\n
        可以覆盖 reloadStyleSheet 方法里已经指定的样式表内容
        """
        self._fixed_stylesheet = stylesheet


    def reloadStyleSheet(self):
        """
        重载样式表，创建新组件类的时候使用，定义组件初始化的样式表，新组件类来实现
        """
        return

    def _schedule_update(self):
        """ 调度一次更新样式的方法，避免重复调用 """
        if self._can_update:
            self._can_update = False
            QTimer.singleShot(0, self.updateStyleSheet)

    def updateStyleSheet(self):
        """ 更新样式表 """
        self.setStyleSheet(self.reloadStyleSheet())


    # region Slot
    def _theme_changed_handler(self, arg_1):
        '''主题改变时调用，子类可以不实现该方法'''
        pass


    def _bg_color_handler(self, color_value):
        self._bg_color = ColorTool.toCode(color_value)
        self._schedule_update()


    # region Color
    def setColorTo(self, code):
        """
        设置背景颜色，同时启动动画
        Args:
            code_1: 颜色代码，格式为 `#AARRGGBB` 或 `#RRGGBB`
        """
        # 启动动画：根据是否是渐变色来处理
        color_value = ColorTool.toArray(code)
        self._anim_bg_color.setTarget(color_value)
        self._anim_bg_color.try_to_start()


    def setColor(self, code):
        """
        设置背景颜色
        Args:
            code_1: 颜色代码，格式为 `#AARRGGBB` 或 `#RRGGBB`
        """
        color_value = ColorTool.toArray(code)
        self._anim_bg_color.setCurrent(color_value)
        self._bg_color_handler(color_value)


    # region Event
    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)
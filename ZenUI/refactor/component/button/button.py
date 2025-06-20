
from PySide6.QtGui import QColor, QPainter, QFont, QPen, QIcon
from PySide6.QtCore import Qt, QRect, QSize, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.refactor.core import ZGlobal, ZButtonStyleData
from .abcbutton import ZABCButton

class ZButton(ZABCButton):
    def __init__(self,
                 name: str,
                 parent: QWidget = None,
                 text: str = None,
                 icon: QIcon = None):
        super().__init__(parent)
        self.setObjectName(name)
        # 基本属性
        self._text: str = None
        self._icon: QIcon = None
        self._icon_size = QSize(16, 16)
        if text : self.setText(text)
        if icon : self.setIcon(icon)
        self.setFont(QFont("Microsoft YaHei", 9))
        self._spacing = 4
        # 颜色属性
        self._color_bg = QColor(0, 0, 0)
        self._color_text = QColor(0, 0, 0)
        self._color_icon = QColor(0, 0, 0)
        self._color_border = QColor(0, 0, 0)
        self._radius = 4

        # 样式数据
        self._style_data: ZButtonStyleData = None
        self.setStyleData(ZGlobal.styleDataManager.getStyleData("ZButton"))
        # 属性动画
        self._anim_bg = QPropertyAnimation(self, b"backgroundColor")
        self._anim_bg.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim_bg.setDuration(150)
        self._anim_border = QPropertyAnimation(self, b"borderColor")
        self._anim_border.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim_border.setDuration(150)
        self._anim_icon = QPropertyAnimation(self, b"iconColor")
        self._anim_icon.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim_icon.setDuration(150)
        self._anim_text = QPropertyAnimation(self, b"textColor")
        self._anim_text.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim_text.setDuration(150)

        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @Property(QColor)
    def backgroundColor(self):
        """获取按钮背景颜色"""
        return self._color_bg

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        """设置按钮背景颜色"""
        self._color_bg = color
        self.update()

    @Property(QColor)
    def borderColor(self):
        """获取按钮背景颜色"""
        return self._color_border

    @borderColor.setter
    def borderColor(self, color: QColor):
        """设置按钮背景颜色"""
        self._color_border = color
        self.update()

    @Property(QColor)
    def iconColor(self):
        """获取图标颜色"""
        return self._color_icon

    @iconColor.setter
    def iconColor(self, color: QColor):
        """设置图标颜色"""
        self._color_icon = color
        self.update()

    @Property(QColor)
    def textColor(self):
        """获取文字颜色"""
        return self._color_text

    @textColor.setter
    def textColor(self, color: QColor):
        """设置文字颜色"""
        self._color_text = color
        self.update()

    @Property(int)
    def radius(self):
        """获取按钮圆角半径"""
        return self._radius

    @radius.setter
    def radius(self, radius: int):
        """设置按钮圆角半径"""
        self._radius = radius
        self.update()

    @Property(ZButtonStyleData)
    def styleData(self):
        """获取按钮样式数据"""
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZButtonStyleData):
        """设置按钮样式数据"""
        self._style_data = style_data
        self._color_bg = QColor(style_data.body)
        self._color_text = QColor(style_data.text)
        self._color_icon = QColor(style_data.icon)
        self._color_border = QColor(style_data.border)
        self._radius = style_data.radius
        self.update()

    # region Public Func
    def text(self):
        """获取按钮文本"""
        return self._text

    def setText(self, text: str):
        """设置按钮文本"""
        self._text = text
        self.update()

    def setIcon(self, icon: QIcon):
        """设置按钮图标"""
        self._icon = icon
        self.update()

    def setIconSize(self, size: QSize):
        """设置图标大小"""
        self._icon_size = size
        self.update()

    def setSpacing(self, spacing: int):
        """设置图标和文字之间的间距"""
        self._spacing = spacing
        self.update()

    def setFont(self, arg__1):
        super().setFont(arg__1)
        self.update()

    def setStyleData(self, style_data: ZButtonStyleData):
        """设置按钮样式数据"""
        self._style_data = style_data
        self._color_bg = QColor(style_data.body)
        self._color_text = QColor(style_data.text)
        self._color_icon = QColor(style_data.icon)
        self._color_border = QColor(style_data.border)
        self._radius = style_data.radius
        self.update()

    def setBackgroundColorTo(self, color: QColor):
        """设置按钮背景颜色"""
        self._anim_bg.stop()
        self._anim_bg.setStartValue(self._color_bg)
        self._anim_bg.setEndValue(color)
        self._anim_bg.start()

    def setBorderColorTo(self, color: QColor):
        """设置按钮背景颜色"""
        self._anim_border.stop()
        self._anim_border.setStartValue(self._color_border)
        self._anim_border.setEndValue(color)
        self._anim_border.start()

    def setIconColorTo(self, color: QColor):
        """设置图标颜色"""
        self._anim_icon.stop()
        self._anim_icon.setStartValue(self._color_icon)
        self._anim_icon.setEndValue(color)
        self._anim_icon.start()

    def setTextColorTo(self, color: QColor):
        """设置文字颜色"""
        self._anim_text.stop()
        self._anim_text.setStartValue(self._color_text)
        self._anim_text.setEndValue(color)
        self._anim_text.start()

    # region Slot
    def themeChangeHandler(self, theme):
        """主题改变事件处理"""
        data = ZGlobal.styleDataManager.getStyleData('ZButton',theme.name)
        self._style_data = data
        self.radius = data.radius
        self.setBackgroundColorTo(QColor(data.body))
        self.setBorderColorTo(QColor(data.border))
        self.setIconColorTo(QColor(data.icon))
        self.setTextColorTo(QColor(data.text))

    def hoverHandler(self, pos):
        """鼠标悬停事件处理"""
        self.setBackgroundColorTo(QColor(self._style_data.bodyhover))

    def leaveHandler(self):
        """鼠标离开事件处理"""
        self.setBackgroundColorTo(QColor(self._style_data.body))

    def pressHandler(self, pos):
        """鼠标按下事件处理"""
        self.setBackgroundColorTo(QColor(self._style_data.bodypressed))

    def releaseHandler(self, pos):
        """鼠标释放事件处理"""
        self.setBackgroundColorTo(QColor(self._style_data.bodyhover))

    # region Event
    def paintEvent(self, event):
        """绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|
                             QPainter.RenderHint.TextAntialiasing|
                             QPainter.RenderHint.SmoothPixmapTransform)
        # 绘制背景
        rect = self.rect()
        radius = self._radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color_bg)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._color_border, 1))
        painter.setBrush(Qt.NoBrush)
        # 调整矩形以避免边框模糊
        painter.drawRoundedRect(
            QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5),  # 使用 QRectF 实现亚像素渲染
            radius,
            radius
        )
        # 计算内容区域
        # 如果同时有图标和文本，绘制在一起
        if self._icon and self._text:
            # 计算总宽度
            total_width = self._icon_size.width() + self._spacing + \
                         self.fontMetrics().boundingRect(self._text).width()
            # 计算起始x坐标使内容居中
            start_x = (self.width() - total_width) // 2
            # 绘制图标
            icon_rect = QRect(
                start_x,
                (self.height() - self._icon_size.height()) // 2,
                self._icon_size.width(),
                self._icon_size.height()
            )
            self._icon.paint(painter, icon_rect)
            # 绘制文本
            painter.setFont(self.font())
            painter.setPen(self._color_text)
            text_rect = QRect(
                start_x + self._icon_size.width() + self._spacing,
                0,
                rect.width(),
                rect.height()
            )
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self._text)
        # 只有图标
        elif self._icon:
            self._icon.paint(
                painter,
                QRect(
                    (self.width() - self._icon_size.width()) // 2,
                    (self.height() - self._icon_size.height()) // 2,
                    self._icon_size.width(),
                    self._icon_size.height()
                )
            )
        # 只有文本
        elif self._text:
            painter.setFont(self.font())
            painter.setPen(self._color_text)
            painter.drawText(rect, Qt.AlignCenter, self._text)
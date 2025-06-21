
from PySide6.QtGui import QColor, QPainter, QFont, QPen, QIcon
from PySide6.QtCore import Qt, QRect, QSize, QRectF
from PySide6.QtWidgets import QWidget
from ZenUI.refactor.core import (ZGlobal, ZButtonStyleData,BackGroundStyle,BorderStyle,
                                 CornerStyle,TextStyle,IconStyle)
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
        self._font = QFont("Microsoft YaHei", 9)
        self._spacing = 4
        if text : self.text = text
        if icon : self.icon = icon
        # 样式属性
        self._background_style = BackGroundStyle(self)
        self._border_style = BorderStyle(self)
        self._text_style = TextStyle(self)
        self._icon_style = IconStyle(self)
        self._corner_style = CornerStyle(self)
        # 样式数据
        self._style_data: ZButtonStyleData = None
        self.styleData = ZGlobal.styleDataManager.getStyleData("ZButton")

        # 设置默认大小
        ZGlobal.themeManager.themeChanged.connect(self.themeChangeHandler)


    # region Property
    @property
    def backgroundStyle(self) -> BackGroundStyle:
        return self._background_style

    @property
    def borderStyle(self) -> BorderStyle:
        return self._border_style

    @property
    def textStyle(self) -> TextStyle:
        return self._text_style

    @property
    def iconStyle(self) -> IconStyle:
        return self._icon_style

    @property
    def cornerStyle(self) -> CornerStyle:
        return self._corner_style

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.update()

    @property
    def icon(self) -> QIcon:
        return self._icon

    @icon.setter
    def icon(self, icon: QIcon) -> None:
        self._icon = icon
        self.update()

    @property
    def iconSize(self) -> QSize:
        return self._icon_size

    @iconSize.setter
    def iconSize(self, size: QSize) -> None:
        self._icon_size = size
        self.update()

    @property
    def spacing(self) -> int:
        return self._spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._spacing = spacing
        self.update()

    @property
    def font(self) -> QFont:
        return self._font

    @font.setter
    def font(self, font: QFont) -> None:
        self._font = font
        self.update()

    @property
    def styleData(self) -> ZButtonStyleData:
        """获取按钮样式数据"""
        return self._style_data

    @styleData.setter
    def styleData(self, style_data: ZButtonStyleData) -> None:
        """设置按钮样式数据"""
        self._style_data = style_data
        self._background_style.color = QColor(style_data.body)
        self._text_style.color = QColor(style_data.text)
        self._icon_style.color = QColor(style_data.icon)
        self._border_style.color = QColor(style_data.border)
        self._corner_style.radius = style_data.radius
        self.update()


    # region Slot
    def themeChangeHandler(self, theme):
        """主题改变事件处理"""
        data = ZGlobal.styleDataManager.getStyleData('ZButton',theme.name)
        self._style_data = data
        self._corner_style.radius = data.radius
        self._background_style.setColorTo(QColor(data.body))
        self._border_style.setColorTo(QColor(data.border))
        self._icon_style.setColorTo(QColor(data.icon))
        self._text_style.setColorTo(QColor(data.text))

    def hoverHandler(self, pos):
        """鼠标悬停事件处理"""
        self._background_style.setColorTo(QColor(self.styleData.bodyhover))

    def leaveHandler(self):
        """鼠标离开事件处理"""
        self._background_style.setColorTo(QColor(self.styleData.body))

    def pressHandler(self, pos):
        """鼠标按下事件处理"""
        self._background_style.setColorTo(QColor(self.styleData.bodypressed))

    def releaseHandler(self, pos):
        """鼠标释放事件处理"""
        self._background_style.setColorTo(QColor(self.styleData.bodyhover))

    # region Override
    def paintEvent(self, event):
        """绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing|
                             QPainter.RenderHint.TextAntialiasing|
                             QPainter.RenderHint.SmoothPixmapTransform)
        # 绘制背景
        rect = self.rect()
        radius = self._corner_style.radius
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_style.color)
        painter.drawRoundedRect(rect, radius, radius)
        # 绘制边框
        painter.setPen(QPen(self._border_style.color, self._border_style.width))
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
            painter.setPen(self._text_style.color)
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
            painter.setFont(self.font)
            painter.setPen(self._text_style.color)
            painter.drawText(rect, Qt.AlignCenter, self._text)
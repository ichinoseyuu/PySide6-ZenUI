from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from enum import IntFlag
from textwrap import dedent
from ZenUI.component.basewidget import ZWidget
from ZenUI.component.layout import ZColumnLayout
from ZenUI.component.layout import ZRowLayout
from ZenUI.component.scrollpage.handle import ScrollPageHandle
from ZenUI.core import Zen,ZColorTool,ZMargins,drawBorder

class ZScrollPage(ZWidget):
    """可滚动页面组件"""
    class Style(IntFlag):
        '''背景样式'''
        None_ = 0
        Monochrome = 1 << 0
        '纯色'
        Gradient = 1 << 1
        '渐变'
        Border = 1 << 2
        '边框'
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 fixed_stylesheet: str = None,
                 style: Style = Style.Monochrome|Style.Border,
                 layout: Zen.Layout = Zen.Layout.Column,
                 margins: ZMargins = ZMargins(8, 8, 8, 8),
                 spacing: int = 0,
                 alignment: Qt.AlignmentFlag = None,
                 scrollbar_width: int = 8,):
        super().__init__(parent, name)
        self.setWidgetFlag(Zen.WidgetFlag.EnableAnimationSignals)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 创建内容容器
        self._content = ZWidget(self)
        self._content.setWidgetFlag(Zen.WidgetFlag.EnableAnimationSignals)
        # 创建滚动条手柄
        self._handle_v = ScrollPageHandle(
            parent=self,
            radius=4,
            direction=Zen.Direction.Vertical
        )
        self._handle_h = ScrollPageHandle(
            parent=self,
            radius=4,
            direction=Zen.Direction.Horizontal
        )
        self._handle_h.setFixedHeight(scrollbar_width)
        self._handle_v.setFixedWidth(scrollbar_width)
        self._style = style
        '背景样式'
        if fixed_stylesheet: self.setFixedStyleSheet(fixed_stylesheet)
        if layout == Zen.Layout.Row:
            self._layout = ZRowLayout(parent=self._content,
                                    margins=margins,
                                    spacing=spacing,
                                    alignment=alignment)
        if layout == Zen.Layout.Column:
            self._layout = ZColumnLayout(parent=self._content,
                                        margins=margins,
                                        spacing=spacing,
                                        alignment=alignment)
        self._content.setLayout(self._layout)
        # 连接信号
        self._content.resized.connect(self._update_handles)
        self.resized.connect(self._update_handles)
        self._anim_move.setBias(0.1)
        self._anim_move.setFactor(0.1)
        self._init_style()
        self.updateStyle()



    def _init_style(self):
        # 设置样式
        bg_style = self._style & (self.Style.Monochrome| self.Style.Gradient)
        if bin(bg_style).count('1') > 1:
            raise ValueError("Monochrome and Gradient are mutually exclusive")
        if self._style & self.Style.Gradient:
            self.setWidgetFlag(Zen.WidgetFlag.GradientColor)
        self._color_sheet.loadColorConfig(Zen.WidgetType.ScrollPage)
        self._colors.overwrite(self._color_sheet.getSheet())
        self._bg_color_a = self._colors.background_a
        self._bg_color_b = self._colors.background_b
        self._border_color = self._colors.border
        self._anim_bg_color_a.setCurrent(ZColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ZColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ZColorTool.toArray(self._border_color))
        self._handle_v.configColor(self._colors.handle, self._colors.handle_border)
        self._handle_h.configColor(self._colors.handle, self._colors.handle_border)
        self._handle_v.transparent()
        self._handle_h.transparent()


    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        if not self.objectName(): raise ValueError("Widget must have a name")

        sheet = [f"#{self.objectName()}{{"]

        if self._stylesheet_fixed: sheet.append(self._stylesheet_fixed)

        if self._style & self.Style.None_:
            sheet = dedent(f'''\
                background-color: transparent;
                border: none;}}''')
            self._stylesheet_cache = '\n'.join(sheet)
            self._stylesheet_dirty = False
            return self._stylesheet_cache

        if self._style & self.Style.Monochrome:
            sheet.append(f"background-color: {self._bg_color_a};")

        if self._style & self.Style.Gradient:
            x1, y1, x2, y2 = self._gradient_anchor
            sheet.append(dedent(f"""\
                background-color: qlineargradient(
                x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2},
                stop:0 {self._bg_color_a}, stop:1 {self._bg_color_b});"""))

        if self._style & self.Style.Border:
            sheet.append(f"border-color: {self._border_color};}}")
        else:
            sheet.append("border: none;}")

        self._stylesheet_cache = '\n'.join(sheet)
        self._stylesheet_dirty = False
        return self._stylesheet_cache


    def _theme_changed_handler(self, theme):
        super()._theme_changed_handler(theme)
        self._colors.overwrite(self._color_sheet.getSheet(theme))
        self._handle_v.configColor(self._colors.handle, self._colors.handle_border)
        self._handle_h.configColor(self._colors.handle, self._colors.handle_border)
        self._handle_v.transparent()
        self._handle_h.transparent()
        if self._style & self.Style.None_: return
        if self._style & self.Style.Monochrome:
            self.setColor(self._colors.background_a)
        if self._style & self.Style.Gradient:
            self.setColor(self._colors.background_a,self._colors.background_b)
        if self._style & self.Style.Border:
            self.setBorderColor(self._colors.border)


    def adjustSize(self):
        super().adjustSize()
        w, h = 0, 0
        if isinstance(self.layout(), ZRowLayout):
            for i in range(self._layout.count()):
                self._layout.itemAt(i).widget().adjustSize()
                w += self._layout.itemAt(i).widget().width()
                h = max(h, self._layout.itemAt(i).widget().height())
        else:
            for i in range(self._layout.count()):
                self._layout.itemAt(i).widget().adjustSize()
                w = max(w, self._layout.itemAt(i).widget().width())
                h += self._layout.itemAt(i).widget().height()
        return w, h


    def resizeEvent(self, event):
        """处理视口尺寸变化"""
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()
        # 更新垂直滚动条
        self._handle_v.setGeometry(
            self.width() - self._handle_v.width(),
            0,
            self._handle_v.width(),
            h
        )
        # 更新水平滚动条
        self._handle_h.setGeometry(
            0,
            self.height() - self._handle_h.height(),
            w,
            self._handle_h.height()
        )
        # 更新内容区域和滚动条状态
        #self._update_handles()


    def _update_handles(self):
        """更新滚动条状态"""
        viewport = self.size()
        content= self._content.size()
        # 更新滚动条
        self._update_vertical_handle(content.height(), viewport.height())
        self._update_horizontal_handle(content.width(), viewport.width())


    def _update_vertical_handle(self, content_height, viewport_height):
        """更新垂直滚动条"""
        if content_height <= viewport_height:
            self._handle_v.hide()
            # 重置位置
            self._content.move(self._content.x(), 0)
            return

        self._handle_v.show()
        # 计算滑块高度
        ratio = min(1.0, viewport_height / content_height)
        handle_height = max(30, viewport_height * ratio)
        self._handle_v.setFixedHeight(handle_height)
        # 计算内容的相对位置（百分比）
        current_scroll = -self._content.y()
        content_visible_ratio = current_scroll / content_height
        # 计算新的最大滚动范围
        max_scroll = content_height - viewport_height
        # 根据内容相对位置计算新的滚动位置
        new_scroll_pos = int(content_visible_ratio * content_height)
        # 限制在有效范围内
        new_scroll_pos = max(0, min(new_scroll_pos, max_scroll))
        # 更新内容位置
        self._content.move(self._content.x(), -new_scroll_pos)
        # 计算滑块位置
        handle_space = viewport_height - handle_height
        handle_pos = (new_scroll_pos / max_scroll) * handle_space if max_scroll > 0 else 0
        # 更新滑块位置
        self._handle_v.move(
            self.width() - self._handle_v.width(),
            handle_pos
        )


    def _update_horizontal_handle(self, content_width, viewport_width):
        """更新水平滚动条"""
        if content_width <= viewport_width:
            self._handle_h.hide()
            # 重置位置
            self._content.move(0, self._content.y())
            return
        self._handle_h.show()
        # 计算滑块宽度
        ratio = min(1.0, viewport_width / content_width)
        handle_width = max(30, viewport_width * ratio)
        self._handle_h.setFixedWidth(handle_width)
        # 计算内容的相对位置（百分比）
        current_scroll = -self._content.x()
        content_visible_ratio = current_scroll / content_width
        # 计算新的最大滚动范围
        max_scroll = content_width - viewport_width
        # 根据内容相对位置计算新的滚动位置
        new_scroll_pos = int(content_visible_ratio * content_width)
        # 限制在有效范围内
        new_scroll_pos = max(0, min(new_scroll_pos, max_scroll))
        # 更新内容位置
        self._content.move(-new_scroll_pos, self._content.y())
        # 计算滑块位置
        handle_space = viewport_width - handle_width
        handle_pos = (new_scroll_pos / max_scroll) * handle_space if max_scroll > 0 else 0
        # 更新滑块位置
        self._handle_h.move(
            handle_pos,
            self.height() - self._handle_h.height()
        )

    def scrollTo(self, x: int = None, y: int = None):
        """滚动到指定位置
        Args:
            x: 水平滚动位置,None表示不改变
            y: 垂直滚动位置,None表示不改变
        """
        current_x, current_y = self._content.pos().x(), self._content.pos().y()

        if y is not None:
            max_scroll_y = self._content.height() - (self.height() - self._handle_h.height())
            if max_scroll_y > 0:
                y = max(0, min(y, max_scroll_y))
                current_y = -y

        if x is not None:
            max_scroll_x = self._content.width() - (self.width() - self._handle_v.width())
            if max_scroll_x > 0:
                x = max(0, min(x, max_scroll_x))
                current_x = -x

        self._content.move(current_x, current_y)
        self._update_handles()

    def layout(self):
        return self._layout


    def enterEvent(self, event):
        super().enterEvent(event)
        #显示滚动条
        if self._handle_v.isVisible(): self._handle_v.toOpaque()
        if self._handle_h.isVisible(): self._handle_h.toOpaque()


    def leaveEvent(self, event):
        super().leaveEvent(event)
        #隐藏滚动条
        if self._handle_v.isVisible(): self._handle_v.toTransparent()
        if self._handle_h.isVisible(): self._handle_h.toTransparent()


    def wheelEvent(self, event: QWheelEvent):
        """处理滚轮事件"""
        # 判断是否按下 Shift 键
        if event.modifiers() & Qt.ShiftModifier:
            # 水平滚动
            delta = event.angleDelta().x() if event.angleDelta().x() != 0 else event.angleDelta().y()
            current_x = -self._content.x()
            # 计算滚动步长（可以调整这个值来改变滚动速度）
            step = delta / 120 * 50
            # 调用水平滚动
            self.scrollTo(x=current_x - step)
        else:
            # 垂直滚动
            delta = event.angleDelta().y()
            current_y = -self._content.y()
            # 计算滚动步长
            step = delta / 120 * 50
            # 调用垂直滚动
            self.scrollTo(y=current_y - step)
        # 接受事件，防止传递给父组件
        event.accept()
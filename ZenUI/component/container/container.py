from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ZenUI.component.widget.widget import ZenWidget
from ZenUI.core import Zen,ColorTool,ColorSheet

class ZenContainer(ZenWidget):
    'ZenUI基本容器类'
    def __init__(self, parent: QWidget = None, name: str = None, layout = Zen.Layout.Vertical):
        super().__init__(parent, name)
        self.setLayout(layout)


    # region Override
    def _init_style(self):
        super()._init_style()
        self._color_sheet = ColorSheet(Zen.WidgetType.Container)
        self._bg_color_a = self._color_sheet.getColor(Zen.ColorRole.Background_A)
        self._bg_color_b = self._color_sheet.getColor(Zen.ColorRole.Background_B)
        self._border_color = self._color_sheet.getColor(Zen.ColorRole.Border)
        self._anim_bg_color_a.setCurrent(ColorTool.toArray(self._bg_color_a))
        self._anim_bg_color_b.setCurrent(ColorTool.toArray(self._bg_color_b))
        self._anim_border_color.setCurrent(ColorTool.toArray(self._border_color))

    
    def reloadStyleSheet(self):
        if self.isWidgetFlagOn(Zen.WidgetFlag.GradientColor):
            x1, y1, x2, y2 = self._gradient_anchor
            sheet = f'background-color: qlineargradient(x1:{x1}, y1:{y1}, x2:{x2}, y2:{y2},stop:0 {self._bg_color_a},stop:1 {self._bg_color_b});'
        else:
            sheet = f'background-color: {self._bg_color_a};\nborder-color: {self._border_color};'
        is_apply_to_children = self.isWidgetFlagOn(Zen.WidgetFlag.StyleSheetApplyToChildren)
        if is_apply_to_children:
            if self._fixed_stylesheet:
                return self._fixed_stylesheet +'\n'+ sheet
            else:
                return sheet
        else:
            if not self.objectName(): raise ValueError("Widget must have a name when StyleSheetApplyToChildren is False")
            if self._fixed_stylesheet:
                return f"#{self.objectName()}"+"{\n"+  sheet +'\n'+self._fixed_stylesheet +"\n}"
            else:
                return f"#{self.objectName()}"+"{\n"+ sheet +"\n}"

    def _theme_changed_handler(self, theme):
        self.setColorTo(self._color_sheet.getColor(theme,Zen.ColorRole.Background_A),self._color_sheet.getColor(theme,Zen.ColorRole.Background_B))
        self.setBorderColorTo(self._color_sheet.getColor(theme,Zen.ColorRole.Border))


    # region New
    def setLayout(self,layout:Zen.Layout):
        if layout is Zen.Layout.Horizontal:
            self._layout = QHBoxLayout(self)
            self._layout.setContentsMargins(0, 0, 0, 0)
            self._layout.setSpacing(0)
        elif layout is Zen.Layout.Vertical:
            self._layout = QVBoxLayout(self)
            self._layout.setContentsMargins(0, 0, 0, 0)
            self._layout.setSpacing(0)
        super().setLayout(self._layout)

    def setContentsMargins(self, left, top, right, bottom):
        self._layout.setContentsMargins(left, top, right, bottom)

    def setSpacing(self, spacing):
        self._layout.setSpacing(spacing)

    def addWidget(self, widget):
        self._layout.addWidget(widget)

    def addLayout(self, layout):
        self._layout.addLayout(layout)

    def addItem(self, item):
        self._layout.addItem(item)

    def removeWidget(self, widget):
        self._layout.removeWidget(widget)

    def count(self):
        return self._layout.count()

    def insertWidget(self, index, widget):
        self._layout.insertWidget(index, widget)


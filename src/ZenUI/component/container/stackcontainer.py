from PySide6.QtGui import QPainter, QPen, QResizeEvent
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget
from typing import overload
from ZenUI.component.panel import ZPanel
from ZenUI.component.scrollpanel import ZScrollPanel
from ZenUI.core import ZDebug

class ZStackContainer(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 start_point: QPoint = QPoint(0, 40),
                 hide_last_panel: bool = True
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._panels = {}
        self._panel_count = 0
        self._current_panel = None
        self._last_panel = None
        self._start_point = start_point
        self._hide_last_panel = hide_last_panel


    # region public
    def addPanel(self, panel: ZPanel|ZScrollPanel, cover: bool = False, anim: bool = False):
        # 添加页面到页面字典并调整大小
        self._panels[self._panel_count] = panel
        panel.resize(self.width(), self.height())
        if cover:
            # 直接覆盖当前页面的情况
            self.setCurrentPanel(panel, anim)
        else:
            # 不覆盖当前页面的情况
            if self._current_panel is None:
                # 如果是第一个页面，设为当前页
                self._current_panel = panel
                self._current_panel.raise_()
            else:
                # 对于非第一个页面，先显示再根据条件隐藏
                #page.show()  # 强制完成渲染
                self._current_panel.raise_()
                if self._hide_last_panel:
                    panel.hide()
        # 增加页面计数
        self._panel_count += 1


    @overload
    def removePanel(self, index: int) -> None:
        ...
    @overload
    def removePanel(self, name: str) -> None:
        ...

    def removePanel(self, arg):
        if isinstance(arg, int):
            if arg in self._panels:
                del self._panels[arg]
        elif isinstance(arg, str):
            for k, v in self._panels.items():
                if v.objectName() == arg:
                    del self._panels[k]


    @overload
    def setCurrentPanel(self, name: str, anim: bool = True) -> None:
        ...

    @overload
    def setCurrentPanel(self, index: int, anim: bool = True) -> None:
        ...

    @overload
    def setCurrentPanel(self, panel: ZPanel|ZScrollPanel, anim: bool = True) -> None:
        ...

    def setCurrentPanel(self, arg, anim: bool = True):
        if isinstance(arg, (int, str)):
            page = self.panel(arg)
            if page is not None:
                self.setCurrentPanel(page, anim)
        elif isinstance(arg, ZPanel|ZScrollPanel):
            self._last_panel = self._current_panel
            self._current_panel = arg
            self._current_panel.resize(self.width(), self.height())
            if anim:
                self._current_panel.move(self._start_point)
                if self._hide_last_panel and self._last_panel is not None:
                    self._last_panel.hide()
                    self._current_panel.show()
                else:
                    self._current_panel.raise_()
                self._current_panel.positionCtrl.moveTo(0, 0)
            else:
                self._current_panel.move(0, 0)
                if self._hide_last_panel and self._last_panel is not None:
                    self._last_panel.hide()
                    self._current_panel.show()
                else:
                    self._current_panel.raise_()


    def currentPanel(self):
        return self._current_panel


    def currentPanelIndex(self) -> int|None:
        for key, val in self._panels.items():
            if val == self._current_panel:
                return key
        return None


    def lastPanel(self):
        return self._last_panel


    @overload
    def panel(self, index: int) -> ZPanel|ZScrollPanel|None:
        ...
    @overload
    def panel(self, name: str) -> ZPanel|ZScrollPanel|None:
        ...

    def panel(self, arg):
        if isinstance(arg, int):
            return self._panels.get(arg)
        elif isinstance(arg, str):
            for page in self._panels.values():
                if page.objectName() == arg:
                    return page
        return None


    def panels(self):
        pages = []
        for val in self._panels.values():
            pages.append(val)
        return pages

    def sizeHint(self):
        if self._current_panel is not None:
            return self._current_panel.sizeHint()
        return super().sizeHint()


    # region event
    def resizeEvent(self, event:QResizeEvent):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        if self._current_panel is not None:
            self._current_panel.resize(w, h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()
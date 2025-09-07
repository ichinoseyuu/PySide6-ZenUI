from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPoint
from PySide6.QtGui import QResizeEvent
from typing import overload
from ZenUI.component.page import ZPage
from ZenUI.component.scrollpage import ZScrollPage
class ZStackPanel(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 start_point: QPoint = QPoint(0, 40),
                 hide_last_page: bool = True
                 ):
        super().__init__(parent)
        if name: self.setObjectName(name)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setStyleSheet('background-color:transparent;border: 1px solid red;')
        self._pages = {}
        self._page_count = 0
        self._current_page = None
        self._last_page = None
        self._start_point = start_point
        self._hide_last_page = hide_last_page


    def addPage(self, page: ZPage|ZScrollPage, cover: bool = False, anim: bool = False):
        # 添加页面到页面字典并调整大小
        self._pages[self._page_count] = page
        page.resize(self.width(), self.height())
        if cover:
            # 直接覆盖当前页面的情况
            self.setCurrentPage(page, anim)
        else:
            # 不覆盖当前页面的情况
            if self._current_page is None:
                # 如果是第一个页面，设为当前页
                self._current_page = page
                self._current_page.raise_()
            else:
                # 对于非第一个页面，先显示再根据条件隐藏
                #page.show()  # 强制完成渲染
                self._current_page.raise_()
                if self._hide_last_page:
                    page.hide()
        # 增加页面计数
        self._page_count += 1


    @overload
    def removePage(self, index: int) -> None:
        ...
    @overload
    def removePage(self, name: str) -> None:
        ...

    def removePage(self, arg):
        if isinstance(arg, int):
            if arg in self._pages:
                del self._pages[arg]
        elif isinstance(arg, str):
            for k, v in self._pages.items():
                if v.objectName() == arg:
                    del self._pages[k]


    @overload
    def setCurrentPage(self, name: str, anim: bool = True) -> None:
        ...

    @overload
    def setCurrentPage(self, index: int, anim: bool = True) -> None:
        ...

    @overload
    def setCurrentPage(self, page: ZPage|ZScrollPage, anim: bool = True) -> None:
        ...

    def setCurrentPage(self, arg, anim: bool = True):
        if isinstance(arg, (int, str)):
            page = self.page(arg)
            if page is not None:
                self.setCurrentPage(page, anim)
        elif isinstance(arg, ZPage|ZScrollPage):
            self._last_page = self._current_page
            self._current_page = arg
            self._current_page.resize(self.width(), self.height())
            if anim:
                self._current_page.move(self._start_point)
                if self._hide_last_page and self._last_page is not None:
                    self._last_page.hide()
                    self._current_page.show()
                else:
                    self._current_page.raise_()
                self._current_page.locationCtrl.moveTo(0, 0)
            else:
                self._current_page.move(0, 0)
                if self._hide_last_page and self._last_page is not None:
                    self._last_page.hide()
                    self._current_page.show()
                else:
                    self._current_page.raise_()


    def currentPage(self):
        return self._current_page


    def currentPageIndex(self) -> int|None:
        for key, val in self._pages.items():
            if val == self._current_page:
                return key
        return None


    def lastPage(self):
        return self._last_page


    @overload
    def page(self, index: int) -> ZPage|ZScrollPage|None:
        ...
    @overload
    def page(self, name: str) -> ZPage|ZScrollPage|None:
        ...

    def page(self, arg):
        if isinstance(arg, int):
            return self._pages.get(arg)
        elif isinstance(arg, str):
            for page in self._pages.values():
                if page.objectName() == arg:
                    return page
        return None


    def pages(self):
        pages = []
        for val in self._pages.values():
            pages.append(val)
        return pages

    def sizeHint(self):
        if self._current_page is not None:
            return self._current_page.sizeHint()
        return super().sizeHint()

    def resizeEvent(self, event:QResizeEvent):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        if self._current_page is not None:
            self._current_page.resize(w, h)


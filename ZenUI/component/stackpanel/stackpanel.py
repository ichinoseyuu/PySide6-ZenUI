from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QPropertyAnimation,Property,QEasingCurve,QPoint
from PySide6.QtGui import QResizeEvent,QColor
from typing import overload
from ZenUI._legacy.component.page import ZPage
from ZenUI._legacy.component.scrollpage import ZScrollPage

class ZStackPanel(QWidget):
    '''堆叠面板'''
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None,
                 start_point: QPoint = QPoint(0, 40),
                 hide_last_page: bool = True
                 ):
        super().__init__(parent, name)
        self._pages = {}
        self._page_count = 0
        self._current_page = None
        self._last_page = None
        self._start_point = start_point
        self._hide_last_page = hide_last_page


    def addPage(self, page: ZPage|ZScrollPage, cover: bool = False, anim: bool = False):
        self._pages[self._page_count] = page
        page._anim_move.setFactor(self._page_factor)
        page._anim_move.setBias(self._page_bias)
        if not cover:
            self._handle_non_cover_page(page)
        else:
            self.setCurrentPage(page, anim)
        self._page_count += 1


    def _handle_non_cover_page(self, page: ZPage|ZScrollPage):
        if self._current_page is None:
            self._current_page = page
            self._current_page.resize(self.width(), self.height())
            self._current_page.raise_()
        else:
            self._current_page.raise_()
            if self._hide_last_page:
                page.hide()


    @overload
    def removePage(self, index: int) -> None:
        '''根据索引移除页面'''
        pass
    @overload
    def removePage(self, name: str) -> None:
        '''更具`objectName`移除页面'''
        pass

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
        '''将`objectName`为`name`的页面设置为当前页面'''
        pass
    @overload
    def setCurrentPage(self, index: int, anim: bool = True) -> None:
        '''将索引为`index`的页面设置为当前页面'''
        pass
    @overload
    def setCurrentPage(self, page: ZPage|ZScrollPage, anim: bool = True) -> None:
        '''将`page`设置为当前页面'''
        pass

    def setCurrentPage(self, arg, anim: bool = True):
        # 获取发送信号的对象
        if isinstance(arg, (int, str)):
            page = self.page(arg)
            if page is not None:
                self.setCurrentPage(page, anim)
        elif isinstance(arg, ZPage|ZScrollPage):
            self._last_page = self._current_page
            self._current_page = arg
            self._current_page.resize(self.width(), self.height())
            if anim:
                self._current_page.move(self._start_point.x, self._start_point.y)
                if self._hide_last_page and self._last_page is not None:
                    self._last_page.hide()
                    self._current_page.show()
                else:
                    self._current_page.raise_()
                self._current_page.moveTo(0, 0)
            else:
                self._current_page.move(0, 0)
                if self._hide_last_page and self._last_page is not None:
                    self._last_page.hide()
                    self._current_page.show()
                else:
                    self._current_page.raise_()


    def currentPage(self):
        '''获取当前页面'''
        return self._current_page


    def currentPageIndex(self) -> int|None:
        '''获取当前页面的索引'''
        for key, val in self._pages.items():
            if val == self._current_page:
                return key
        return None


    def lastPage(self):
        '''获取上一个页面'''
        return self._last_page


    @overload
    def page(self, index: int) -> ZPage|ZScrollPage|None:
        '''获取页面'''
        pass
    @overload
    def page(self, name: str) -> ZPage|ZScrollPage|None:
        '''获取页面'''
        pass

    def page(self, arg):
        if isinstance(arg, int):
            return self._pages.get(arg)
        elif isinstance(arg, str):
            for page in self._pages.values():
                if page.objectName() == arg:
                    return page
        return None


    def pages(self):
        '''获取所有页面'''
        pages = []
        for val in self._pages.values():
            pages.append(val)
        return pages


    def setPageAnim(self, factor: float, bias: float):
        '''设置页面移动动画'''
        self._page_factor = factor
        self._page_bias = bias
        for i in self.pages():
            i._anim_move.setFactor(factor)
            i._anim_move.setBias(bias)

    def sizeHint(self):
        return self._current_page.sizeHint()

    def resizeEvent(self, event:QResizeEvent):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        if self._current_page is not None:
            self._current_page.resize(w, h)


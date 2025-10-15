import logging
from typing import overload,Dict,Generic
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Signal
from ZenUI.core import StyleDataT, ZGlobal


class StyleController(QObject, Generic[StyleDataT]):
    '''样式管理器
    - 决定控件的当前样式
    - 存储自定义样式数据
    '''
    styleChanged = Signal()
    def __init__(self, parent: QWidget, key: str=''):
        super().__init__(parent)
        self._custom: bool = False
        self._key: str = key
        self._data: StyleDataT = None
        self._custom_data: Dict[str, StyleDataT] = {'Light': None, 'Dark': None}
        if key: self._data = ZGlobal.styleDataManager.getStyleData(key)
        ZGlobal.themeManager.themeChanged.connect(self.updateStyleData)

    @property
    def data(self,) -> StyleDataT: return self._data

    def updateStyleData(self, theme) -> None:
        if self._custom:
            self._data = self._custom_data[theme.name]
        else:
            self._data = ZGlobal.styleDataManager.getStyleData(self._key, theme.name)
        self.styleChanged.emit()

    def setKey(self, key: str, update: bool = False) -> None:
        self._key = key
        self._data = ZGlobal.styleDataManager.getStyleData(key)
        if update: self.styleChanged.emit()

    def updateDataFromManager(self):
        self._data = ZGlobal.styleDataManager.getStyleData(self._key)

    @overload
    def setData(self, theme: str, data: StyleDataT) -> None: ...

    @overload
    def setData(self, light_data: StyleDataT, dark_data: StyleDataT) -> None: ...

    def setData(self, *args) -> None:
        self._custom = True
        if len(args) == 2 and args[0] in ['Light', 'Dark']:
            # 设置指定主题的样式，同时保留另一个主题的现有样式或使用默认样式
            theme = args[0]
            self._custom_data[theme] = args[1]
            # 确保另一个主题也有值
            other_theme = 'Dark' if theme == 'Light' else 'Light'
            if self._custom_data[other_theme] is None:
                # 如果另一个主题没有自定义样式，使用默认样式
                self._custom_data[other_theme] = ZGlobal.styleDataManager.getStyleData(self._key, other_theme)
        elif len(args) == 2 and isinstance(args[0], StyleDataT):
            # 同时设置Light和Dark主题的样式
            self._custom_data['Light'] = args[0]
            self._custom_data['Dark'] = args[1]
        else:
            raise ValueError("Invalid arguments for setData")
        self.updateStyleData(ZGlobal.themeManager.theme)

    def clearCustomData(self) -> None:
        self._custom = False
        self.updateStyleData(ZGlobal.themeManager.theme.name)

    def parent(self) -> QWidget:
        return super().parent()

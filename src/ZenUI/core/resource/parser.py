import os

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QIcon
from PySide6.QtSvg import QSvgRenderer


class GlobalIconPack:
    current_module_path = os.path.dirname(os.path.abspath(__file__))
    package_folder_path = os.path.join(current_module_path, "packages")

    def __init__(self):
        self.default_color = '#a8a8a8'

        self.icons = {}
        self.icons_classified = {
            "__unclassified__": {}
        }

        # load internal icon packages
        self.reload_internals()

    def setDefaultColor(self, code) -> None:
        '''设置默认图标颜色'''
        self.default_color = code

    @property
    def defaultColor(self) -> str:
        return self.default_color

    def reload_internals(self) -> None:
        '''重新加载内置图标包'''
        for package_filename in os.listdir(self.package_folder_path):
            full_path = os.path.join(self.package_folder_path, package_filename)
            if os.path.isfile(full_path):
                self.load_from_file(full_path)

    def load_from_file(self, path) -> None:
        '''从文件加载图标包'''
        class_name = os.path.basename(path)
        self.append_class(class_name)
        with open(path, encoding="utf-8") as file:
            for line in file.readlines():
                if line[0:2] == "##":
                    continue
                if line.strip() == "":
                    continue

                line = line.strip()
                icon_name, icon_data = line.split("////")
                self.append(icon_name, icon_data, class_name)

    def append_class(self, class_name, force=False) -> None:
        '''添加图标包分类'''
        if class_name in self.icons_classified.keys() and (force is False):
            raise ValueError(f"Class name {class_name} is already exist.")
        self.icons_classified[class_name] = {}

    def append(self, name, data, class_name: str = "__unclassified__") -> None:
        '''添加图标'''
        self.icons[name] = data
        self.icons_classified[class_name][name] = data

    def get(self, name, color_code: str = None) -> bytes:
        '''获取图标数据'''
        color_code = self.default_color if color_code is None else color_code
        return self.icons[name].replace("<<<COLOR_CODE>>>", color_code).encode()

    def getFromData(self, data, color_code: str = None) -> bytes:
        '''从数据获取图标数据'''
        color_code = self.default_color if color_code is None else color_code
        return data.replace("<<<COLOR_CODE>>>", color_code).encode()

    def getByteArray(self, name, color_code: str = None) -> QByteArray:
        '''获取图标数据'''
        svg_bytes = self.get(name, color_code)
        return QByteArray(svg_bytes)

    def getDict(self, class_name=None) -> dict:
        """ 获取图标字典 """
        if class_name is None:
            return self.icons
        else:
            return self.icons_classified[class_name]

    def getClassNames(self) -> dict.keys:
        '''获取图标包分类名称列表'''
        return self.icons_classified.keys()

    def toPixmap(self, name: str, size: QSize = QSize(64, 64), color_code: str = None):
        '''
        将图标转换为Pixmap
        Args:
            name: 图标名称
            size: 图标大小
            color_code: 图标颜色
        Returns:
            QPixmap
        '''
        svg_bytes = self.get(name, color_code)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_bytes)
        svg_renderer.render(painter)
        painter.end()
        return pixmap

    def toIcon(self, name: str, size: QSize = QSize(64, 64), color_code: str = None) -> QIcon:
        '''
        将图标转换为QIcon
        Args:
            name: 图标名称
            size: 图标大小
            color_code: 图标颜色
        Returns:
            QIcon
        '''
        return QIcon(self.toPixmap(name, size, color_code))
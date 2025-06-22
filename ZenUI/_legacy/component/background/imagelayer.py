import os
from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt,QRect
from PySide6.QtGui import QPainter, QPixmap, QPainterPath
from ZenUI._legacy.core import Zen

class ZImageLayer(QWidget):
    """图片层,支持透明图片并保持比例"""
    def __init__(self,
                 parent=None,
                 image_path=None,
                 scale_type=Zen.ScaleType.Fit,
                 corner_radius=2,
                 opacity=1.0):
        super().__init__(parent)
        self._image = None          # 原始图片
        self._scaled_pixmap = None  # 缩放后的图片
        self._opacity = opacity      # 透明度
        self._scale_type =  scale_type # 缩放类型
        self._corner_radius = corner_radius     # 圆角半径
        self.setAttribute(Qt.WA_TranslucentBackground)  # 支持透明
        self.setMouseTracking(True)
        self.setImage(image_path)


    def setImage(self, image_path: str) -> bool:
        """设置图片
        Args:
            image_path: 图片路径或资源路径
        Returns:
            bool: 是否成功加载图片
        """
        if not image_path: return False
        # 判断是否是资源路径
        if image_path.startswith(':'):
            self._image = QPixmap(image_path)
        else:
            # 文件路径处理
            if not os.path.exists(image_path):
                print(f"图片文件不存在: {image_path}")
                return False
            self._image = QPixmap(image_path)
        if self._image.isNull():
            print(f"图片加载失败: {image_path}")
            return False
        self._updateScaledImage()
        self.update()
        return True

    def setOpacity(self, opacity: float):
        """设置透明度"""
        self._opacity = max(0.0, min(1.0, opacity))
        self.update()

    def setScaleType(self, scale_type: int):
        """设置缩放类型"""
        if self._scale_type != scale_type:
            self._scale_type = scale_type
            self._updateScaledImage()
            self.update()

    def setCornerRadius(self, radius: int):
        """设置圆角半径"""
        if radius != self._corner_radius:
            self._corner_radius = max(0, radius)
            self.update()

    def cornerRadius(self) -> int:
        """获取圆角半径"""
        return self._corner_radius

    def _updateScaledImage(self):
        """更新缩放后的图片"""
        if not self._image or self._image.isNull():
            return

        size = self.size()
        if size.isEmpty():
            return

        # 设置高质量缩放选项
        transform_mode = Qt.SmoothTransformation

        if self._scale_type == Zen.ScaleType.Stretch:
            # 拉伸填充
            self._scaled_pixmap = self._image.scaled(
                size,
                Qt.IgnoreAspectRatio,
                transform_mode
            )
        else:
            # 计算保持比例的尺寸
            image_size = self._image.size()

            if self._scale_type == Zen.ScaleType.Fit:
                # 适应窗口
                scaled_size = image_size.scaled(size, Qt.KeepAspectRatio)
            else:  # Fill
                # 填充窗口
                scaled_size = image_size.scaled(size, Qt.KeepAspectRatioByExpanding)

            self._scaled_pixmap = self._image.scaled(
                scaled_size,
                Qt.KeepAspectRatio,
                transform_mode
                )

    def resizeEvent(self, event):
        """处理大小改变事件"""
        super().resizeEvent(event)
        self._updateScaledImage()


    def paintEvent(self, event):
        """绘制事件"""
        if not self._scaled_pixmap or self._scaled_pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.setOpacity(self._opacity)

        # 计算居中绘制的位置
        x = (self.width() - self._scaled_pixmap.width()) // 2
        y = (self.height() - self._scaled_pixmap.height()) // 2
        if self._corner_radius > 0:
            # 创建圆角路径，使用整个组件的大小
            path = QPainterPath()
            path.addRoundedRect(
                0, 0, self.width(), self.height(),  # 使用组件的完整尺寸
                self._corner_radius, self._corner_radius
            )
            # 设置裁剪路径
            painter.setClipPath(path)
        # 直接绘制图片,不需要额外的圆角处理
        painter.drawPixmap(x, y, self._scaled_pixmap)

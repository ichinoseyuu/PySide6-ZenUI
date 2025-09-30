from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QMargins, Slot, QPoint
from PySide6.QtGui import QMouseEvent, QPainter
from ZenUI.component.base import (
    ColorController,
    LocationController,
    SizeController,
    StyleData,
    ButttonGroup
)
from ZenUI.component.layout import ZVBoxLayout
from ZenUI.core import ZDebug, ZNavigationBarStyleData
from .navbarbutton import ZNavBarButton
from .navbartogglebutton import ZNavBarToggleButton
class Panel(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._content = QWidget(self)
        self._content.setLayout(ZVBoxLayout(
            self._content,
            margins=QMargins(0, 0, 0, 0),
            spacing=6,
            alignment=Qt.AlignTop|Qt.AlignHCenter
            ))
        self._offset = 0  # 垂直滚动偏移

    def _updateContentGeometry(self):
        # 内容区宽度与Panel一致，高度由内容决定
        content_height = self._content.layout().sizeHint().height()
        self._content.resize(self.width(), content_height)
        self._content.move(0, -self._offset)

    def layout(self) -> ZVBoxLayout:
        return self._content.layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._updateContentGeometry()

    def wheelEvent(self, event: QMouseEvent):
        # 计算内容总高度和可视高度
        content_height = self._content.layout().sizeHint().height()
        visible_height = self.height()
        max_offset = max(0, content_height - visible_height)
        # 滚轮方向
        delta = event.angleDelta().y()
        step = 30  # 每次滚动的像素
        if delta < 0:
            self._offset = min(self._offset + step, max_offset)
        elif delta > 0:
            self._offset = max(self._offset - step, 0)
        self._updateContentGeometry()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

class FooterPanel(QWidget):
    def __init__(self,parent: QWidget = None):
        super().__init__(parent)
        self.setLayout(ZVBoxLayout(
            self,
            margins=QMargins(0, 0, 0, 0),
            spacing=6,
            alignment=Qt.AlignBottom|Qt.AlignHCenter
            ))

    def layout(self) -> ZVBoxLayout:
        return super().layout()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()


class Indicator(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._body_cc = ColorController(self)
        self._location_ctrl = LocationController(self)
        self._size_ctrl = SizeController(self)



    @property
    def bodyColorCtrl(self): return self._body_cc

    @property
    def locationCtrl(self): return self._location_ctrl

    @property
    def sizeCtrl(self): return self._size_ctrl

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        radius = self.width() / 2
        if self._body_cc.color.alpha() > 0:
            # draw background
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._body_cc.color)
            painter.drawRoundedRect(rect, radius, radius)
        painter.end()


class ZNavigationBar(QWidget):
    def __init__(self,
                 parent: QWidget = None,
                 name: str = None):
        super().__init__(parent)
        if name: self.setObjectName(name)
        self._panel = Panel(self)
        self._footer_panel = FooterPanel(self)
        self._indicator = Indicator(self)
        self._indicator.setFixedWidth(3)
        self.setLayout(ZVBoxLayout(self, margins=QMargins(0, 0, 0, 0), spacing=0))
        self.layout().addWidget(self._panel, stretch=1)
        self.layout().addWidget(self._footer_panel, stretch=0)
        self._btn_manager = ButttonGroup()
        self._style_data = StyleData[ZNavigationBarStyleData](self,"ZNavigationBar")
        self._btn_manager.toggled.connect(self.updateIndicator)
        self._style_data.styleChanged.connect(self._styleChangeHandler)
        self._initStyle()

    @Slot()
    def updateIndicator(self):
        btn = self._btn_manager.checkedButton()
        current_pos = self._indicator.pos()  # 获取指示器当前位置
        target_pos = self.getButtonPositionInNavBar(btn)
        # dx = abs(target_pos.x() - current_pos.x())
        # dy = abs(target_pos.y() - current_pos.y())
        # distance = (dx**2 + dy**2) **0.5
        # dy = abs(target_pos.y() - current_pos.y())
        distance = abs(target_pos.y() - current_pos.y())
        if distance == 0:
            self._indicator.resize(3, btn.height()-20)
            self._indicator.move(
            target_pos.x(),
            target_pos.y() + (btn.height()-self._indicator.height())/2
            )
            return
        factor = min(0.5, max(0.2, distance / self.height()))
        self._indicator.locationCtrl.animation.setFactor(factor)
        self._indicator.locationCtrl.moveTo(
            target_pos.x(),
            target_pos.y() + (btn.height()-self._indicator.height())/2
            )



    @property
    def panel(self):
        return self._panel

    @property
    def footerPanel(self):
        return self._footer_panel

    def addButton(self, panel:QWidget, btn: ZNavBarButton):
        if panel is self._panel:
            self._panel.layout().addWidget(btn)
        elif panel is self._footer_panel:
            self._footer_panel.layout().addWidget(btn)

    def insertButton(self, panel:QWidget, index:int, btn: ZNavBarButton):
        if panel is self._panel:
            self._panel.layout().insertWidget(index, btn)
        elif panel is self._footer_panel:
            self._footer_panel.layout().insertWidget(index, btn)

    def addToggleButton(self, panel:QWidget, btn: ZNavBarToggleButton):
        if panel is self._panel:
            self._panel.layout().addWidget(btn)
        elif panel is self._footer_panel:
            self._footer_panel.layout().addWidget(btn)
        self._btn_manager.addButton(btn)

    def insertToggleButton(self, panel:QWidget, index:int, btn: ZNavBarToggleButton):
        if panel is self._panel:
            self._panel.layout().insertWidget(index, btn)
        elif panel is self._footer_panel:
            self._footer_panel.layout().insertWidget(index, btn)
        self._btn_manager.addButton(btn)

    def toggleToNextButton(self):
        self._btn_manager.toggleToNextButton()

    def toggleToLastButton(self):
        self._btn_manager.toggleToLastButton()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        painter.end()

    # region private
    def _initStyle(self):
        self._indicator.bodyColorCtrl.color = self._style_data.data.Indicator
        self._indicator.update()

    def _styleChangeHandler(self):
        self._indicator.bodyColorCtrl.setColorTo(self._style_data.data.Indicator)

    def getButtonPositionInNavBar(self, btn: ZNavBarButton|ZNavBarToggleButton) -> QPoint:
        """获取按钮相对于ZNavigationBar的位置"""
        if not btn: return QPoint(0, 0)
        pos = btn.pos()
        parent_pos_in_nav = btn.parentWidget().pos()
        return QPoint(
            pos.x() + parent_pos_in_nav.x(),
            pos.y() + parent_pos_in_nav.y()
        )
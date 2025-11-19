from PySide6.QtWidgets import QWidget,QPushButton
from PySide6.QtCore import Qt,QRectF,QSize,QRect,QMargins,QPoint
from PySide6.QtGui import QPainter,QPen,QColor,QFont
from ZenWidgets.component.input import ZButton,ZLongPressButton
from ZenWidgets.component.layouts import ZVBoxLayout
from ZenWidgets.component.base import(
    ZWidget,
    ZAnimatedColor,
    ZAnimatedFloat,
    ZStyleController
)
from ZenWidgets.component.text import ZHeadLine
from ZenWidgets.core import ZMargin,ZDebug
from ZenWidgets.gui import ZWidgetEffect,ZDialogStyleData

class DialogContent(ZWidget):
    bodyColorCtrl: ZAnimatedColor
    footerColorCtrl: ZAnimatedColor
    borderColorCtrl: ZAnimatedColor
    radiusCtrl: ZAnimatedFloat
    styleDataCtrl: ZStyleController[ZDialogStyleData]
    __controllers_kwargs__ = {
        'radiusCtrl': {'value': 5.0},
        'styleDataCtrl': {'key': 'ZDialog'}
    }
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setLayout(ZVBoxLayout(self, spacing=0, margins=QMargins(1, 1, 1, 1)))
        # self._title = ZHeadLine(self, text='标题', font=QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        # self.layout().addWidget(self._title)
        # self._message = ZHeadLine(self, text='内容')
        # self.layout().addWidget(self._message)
        # self._footer = ZCard(self,display_border=False, display_shadow=False)
        # self.layout().addWidget(self._footer)
        # self._btn_ok = ZButton(self, text='确定')
        # self._footer.layout().addWidget(self._btn_ok)
        # self._btn_cancel = ZButton(self, text='取消')
        # self._footer.layout().addWidget(self._btn_cancel)
        # self._init_style_()
        # self._btn_ok.clicked.connect(self.window().close)
        # self._btn_cancel.clicked.connect(self.window().close)

        self.setLayout(ZVBoxLayout(self, spacing=0, margins=QMargins(0, 0, 0, 0)))

        self._region_content = QWidget(self)
        self._region_content.setLayout(ZVBoxLayout(self._region_content, spacing=6, margins=QMargins(6, 6, 6, 6)))
        self._title = ZHeadLine(self._region_content, text='标题', font=QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        self._region_content.layout().addWidget(self._title)
        self._message = ZHeadLine(self._region_content, text='内容')
        self._region_content.layout().addWidget(self._message)
        self.layout().addWidget(self._region_content, stretch=1)

        self._region_footer = QWidget(self)
        self._region_footer.setLayout(ZVBoxLayout(self._region_footer, spacing=6, margins=QMargins(6, 6, 6, 6)))
        self._btn_ok = ZButton(self._region_footer, text='确定')
        self._btn_ok.setFixedHeight(40)
        self._btn_ok.clicked.connect(self.window().close)
        self._region_footer.layout().addWidget(self._btn_ok)
        self._btn_cancel = ZButton(self._region_footer, text='取消')
        self._btn_cancel.setFixedHeight(40)
        self._btn_cancel.clicked.connect(self.window().close)
        self._region_footer.layout().addWidget(self._btn_cancel)
        self.layout().addWidget(self._region_footer, stretch=0)

        self._init_style_()

    # region private
    def _init_style_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.color = data.Body
        self.footerColorCtrl.color = data.RegionFooter
        self.borderColorCtrl.color = data.Border

    def _style_change_handler_(self):
        data = self.styleDataCtrl.data
        self.bodyColorCtrl.setColorTo(data.Body)
        self.footerColorCtrl.setColorTo(data.RegionFooter)
        self.borderColorCtrl.setColorTo(data.Border)

    def sizeHint(self):
        layout_size = self.layout().sizeHint()
        if self.screen():
            dpr = self.screen().devicePixelRatio()
        else:
            dpr = 1.0
        base_min_width = 200
        base_min_height = 150

        min_width = max(round(base_min_width * dpr), layout_size.width())
        min_height = max(round(base_min_height * dpr), layout_size.height())

        return QSize(min_width, min_height)

    def paintEvent(self, event):
        if self.opacityCtrl.opacity == 0: return
        painter = QPainter(self)
        painter.setOpacity(self.opacityCtrl.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        footer_rect = QRectF(self._region_footer.geometry())
        border_rect = QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = self.radiusCtrl.value

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.bodyColorCtrl.color)
        painter.drawRoundedRect(rect, radius, radius)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.footerColorCtrl.color)
        painter.drawRoundedRect(footer_rect, radius, radius)

        painter.setPen(QPen(self.borderColorCtrl.color, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(border_rect, radius, radius)
        event.accept()

class ZDialog(ZWidget):
    def __init__(self, target: ZWidget | QWidget | None = None):
        super().__init__(f=Qt.WindowType.FramelessWindowHint|Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowModal)
        self._target: ZWidget | QWidget | None = target
        self._content = DialogContent(self)
        self._margin = ZMargin(8, 8, 8, 8)
        self.windowOpacityCtrl.completelyHide.connect(self.hide)
        ZWidgetEffect.applyGraphicsShadow(self._content)

    def target(self): return self._target

    def sizeHint(self):
        return self._content.sizeHint() + QSize(self._margin.horizontal, self._margin.vertical)

    def show(self):
        self.raise_()
        super().show()
        size = self.sizeHint()
        window_center = self._target.window().geometry().center()
        print(window_center)
        x = window_center.x() - size.width()//2
        y = window_center.y() - size.height()//2
        self.widgetRectCtrl.scaleIn(QRect(x, y, size.width(), size.height()))
        self.windowOpacityCtrl.fadeIn()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._content.setGeometry(self._margin.left, self._margin.top, self.width() - self._margin.horizontal, self.height() - self._margin.vertical)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if ZDebug.draw_rect: ZDebug.drawRect(painter, self.rect())
        event.accept()

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ZDialog()
    w.show()
    sys.exit(app.exec())

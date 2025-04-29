from ZenUI import *

class PageSettings(ZenContainer):
    def __init__(self, parent = None, name = 'pageSettings', layout = Zen.Layout.Column):
        super().__init__(parent, name, layout)
        self._setup_ui()

    def _setup_ui(self):
        text = """设置"""
        self.text = ZenTextLabel(parent=self,
                                 name='text',
                                 text=text,
                                 alignment=Zen.Alignment.Left)
        self.text.setFixedStyleSheet('padding:5px;\nfont-size: 24px;\nfont-family: "幼圆";\nfont-weight: bold;')
        self.layout().addWidget(self.text)
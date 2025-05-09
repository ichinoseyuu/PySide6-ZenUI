from ZenUI import *

class PageAbout(ZBox):
    def __init__(self,parent = None,name ='pageAbout'):
        super().__init__(parent = parent,
                         name=name,
                         style= ZBox.Style.MonochromeWithBorder,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        text = """关于"""
        self.label_title = ZTextLabel(parent=self,
                                 name='text',
                                 text=text,
                                 alignment=Zen.Alignment.Left)
        self.label_title.setFixedStyleSheet('padding:5px;\nfont-size: 24px;\nfont-family: "幼圆";\nfont-weight: bold;')
        self.layout().addWidget(self.label_title)
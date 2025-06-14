from ZenUI import *

class PageAbout(ZPage):
    def __init__(self,parent = None,name ='pageAbout'):
        super().__init__(parent = parent,
                         name=name,
                         fixed_stylesheet="border-width: 1px;\nborder-style: solid;\nborder-radius:4px;",
                         style= ZPage.Style.Monochrome|ZPage.Style.Border,
                         layout=Zen.Layout.Column,
                         margins=ZMargins(6, 6, 6, 6),
                         spacing=12)
        self._setup_ui()

    def _setup_ui(self):
        self.label_title = ZTextLabel(parent=self,
                                 name='text',
                                 text='关于',
                                 alignment=Zen.Alignment.Left)
        self.label_title.setFixedStyleSheet('padding:5px;\nfont-size: 24px;\nfont-family: "微软雅黑";\nfont-weight: bold;')
        self.layout().addWidget(self.label_title)
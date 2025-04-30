from ZenUI import *

class PageHome(ZContainer):
    def __init__(self, parent = None, name = 'pageHome', layout = Zen.Layout.Column):
        super().__init__(parent, name, layout)
        self._setup_ui()

    def _setup_ui(self):
        text = """<h1 style='color: pink;'>Hello, ZenUI!"""
        self.text = ZTextLabel(parent=self,
                                 name='text',
                                 text=text)
        self.layout().addWidget(self.text)
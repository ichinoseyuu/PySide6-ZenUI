from ZenUI.component.label.abclabel import ABCLabel
from ZenUI.component.widget.widget import ZWidget
from ZenUI.core import Zen
from ZenUI.gui import ZPixmap,ZImage
class ZImageLabel(ABCLabel):
    """文本标签"""
    def __init__(self,
                 parent: ZWidget = None,
                 name: str = None,
                 image: ZPixmap|ZImage = None,
                 alignment: Zen.Alignment = Zen.Alignment.Center,
                 
                 ):
        super().__init__(parent = parent,
                         name=name,
                         image=image,
                         alignment=alignment)
        self._fixed_stylesheet = 'background-color: transparent;'
        self._schedule_update()

    # region Override
    def reloadStyleSheet(self):
        return self._fixed_stylesheet

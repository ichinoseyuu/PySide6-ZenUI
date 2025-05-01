from ZenUI.component.widget.widget import ZWidget

class ButtonLayer(ZWidget):
    """按钮层级，用于按钮的背景和高亮层"""
    def _init_style(self):
        super()._init_style()
        self._anim_bg_color_a.setBias(0.1)

    def reloadStyleSheet(self):
        if self._fixed_stylesheet:
            return self._fixed_stylesheet +'\n'+ f'background-color: {self._bg_color_a};'
        else:
            return f'background-color: {self._bg_color_a};'
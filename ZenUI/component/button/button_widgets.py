from textwrap import dedent
from ZenUI.component.widget.layer import ZColorLayer
class ButtonLayer(ZColorLayer):
    """按钮层级，用于按钮的背景和高亮层"""
    def __init__(self, parent = None):
        super().__init__(parent)
        self._style_vars = {
            'background_color': 'transparent',
            'border_color': 'transparent',
            'border_radius': 2}
        '默认样式'
        self._style_getters = {}
        '动态样式'
        self._init_style()
        self._schedule_update()

    def set_style_var(self, key: str, value):
        """设置静态样式变量"""
        self._style_vars[key] = value

    def set_style_getter(self, key: str, getter):
        """设置动态样式获取器"""
        self._style_getters[key] = getter

    def _init_style(self):
        self._anim_bg_color_a.setBias(0.1)


    def reloadStyleSheet(self):
        try:
            # 合并静态变量和动态获取的变量
            current_vars = self._style_vars.copy()
            for key, getter in self._style_getters.items():
                current_vars[key] = getter()
            return dedent('''\
            background-color: {background_color};
            border: 1px solid {border_color};
            border-radius: {border_radius}px;;
            ''').format(**current_vars)+self._fixed_stylesheet
        except KeyError as e:
            print(f"缺少样式变量: {e}")
            return ""


from textwrap import dedent
from ZenUI.component.basewidget import ZLayer
class ButtonLayer(ZLayer):
    '颜色层'
    def __init__(self, parent = None):
        super().__init__(parent)
        self._style_vars = {
            'background_color': 'transparent',
            'border_color': 'transparent'}
        '默认样式'
        self._style_getters = {}
        '动态样式'
        self._style_format = dedent('''\
            background-color: {background_color};
            border-color: {border_color};''')
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
            return self._style_format.format(**current_vars) +'\n'+ self._stylesheet_fixed
        except KeyError as e:
            print(f"缺少样式变量: {e}")
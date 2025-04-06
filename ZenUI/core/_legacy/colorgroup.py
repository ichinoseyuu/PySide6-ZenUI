
class ColorGroup:
    def __getitem__(self, token):
        return self.colors[token.name]

    def __init__(self, overwrite=None, reference=None):
        self.valid_state = True
        self.colors = {}
        if overwrite is not None:
            self.overwrite(overwrite)
            if reference is None:
                self.reference = overwrite.reference
            else:
                self.reference = reference
        else:
            self.reference = reference


    def assign(self, token, code: str):
        "分配指定物件颜色"
        self.colors[token.name] = code


    def remove(self, token):
        "移除指定物件颜色"
        if token.name in self.colors.keys():
            self.colors.pop(token.name)


    def fromToken(self, token):
        "获取颜色"
        if token.name in self.colors.keys() and self.valid_state:
            return self.colors[token.name]
        if self.reference is None:
            raise ValueError(
                f"Color under token {token.name} is not assigned yet either in this group or in its reference\n"
                f"Valid state: {self.valid_state}"
            )
        else:
            return self.reference.fromToken(token)


    def isAssigned(self, token):
        """检查颜色是否分配"""
        if self.reference is None:
            return token.name in self.colors.keys()
        else:
            return ((token.name in self.colors.keys()) and self.valid_state) or self.reference.isAssigned(token)


    def overwrite(self, color_group):
        "覆盖颜色组"
        self.colors.update(color_group.colors)


    def setReference(self, color_group):
        "设置颜色组参考"
        self.reference = color_group


    def setValid(self, state):
        "设置颜色组有效性"
        self.valid_state = state


    def isValid(self):
        "检查颜色组有效性"
        return self.valid_state